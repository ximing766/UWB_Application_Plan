# 闸机交易方案设计

## 0 时序图
TEST

## 1 入站

### 1.1 认证方案

#### 1.1.1 认证距离设计

认证距离与认证成功率正相关，需要对不同距离范围的认证成功率进行压力测试，以确定认证范围。

前置条件：anchor正向面对手机，距离为同一水平距离

| 距离 | 轮次 | 移动状态 | nLos | 成功率 | 备注 |
| :--- | :--- | :------- | :--- | :----- | :--- |
| 1.5m | 25   | 静态     | Los  |        |      |
| 2m   | 50   | 静态     | Los  |        |      |
| 2.5m | 50   | 静态     | Los  |        |      |
| 3m   | 50   | 静态     | Los  |        |      |
| 3m   | 75   | 动态     | Los  |        |      |
| 3m   | 100  | 动态     | nLos |        |      |



#### 1.1.2 认证周期设计

用户进入认证区后UWB启动认证流程，认证需在用户进入蓝区前完成。

- 成功 < 600ms
- 一次失败 < 1800ms
- 两次失败 < 3000ms

```c
#define  AUTHENCATIONTIMEOUT   100  
```

定时器的等待时间为500ms。500ms后没有回复则会触发定时器确认认证失败，开始等待600ms流程，给其他用户使用系统资源的机会。具体实现在1.1.3认证失败设计部分。

#### 1.1.3 认证失败设计

认证失败用户有600ms等待时间，等待时间到达后失败用户将重新参与认证流程。600ms的预留可以防止用户异常时独占系统时间，导致其它用户无法完成任何操作。此外，600ms的等待时间理论上刚好足够1个用户完成认证。

若认证失败次数 > 5，用户将会释放DTPML资源且优先级降低，需等待所有其它用户完成交易后才能重新获得DTPML资源。防止单个用户持续认证失败后，一直占用系统资源。

```c
static void apdu_quick_timer_callback(uint32_t timerid, timer_data_str *pContext)
{
    LOG_E("@@@ %s( ): Auth failed!!! restart Auth process.",__FUNCTION__);
    (void)phOsalUwb_Timer_Stop(timerid);
    EndUserDetected[pContext->index].uiSuccessiveError;         += 1;
    EndUserDetected[pContext->index].AuthenticationState  = notStarted;
    EndUserDetected[pContext->index].SendTimesTamp        = getTimestamp();
    gAuthenticateInterrupted                              = TRUE;
    vUpdateSystemStateMachine(SystemFree, 0x0000);
    LOG_I("@@@ %s( ): Auth failed times = %d.",__FUNCTION__, EndUserDetected[pContext->index].uiSuccessiveError;);
    printTimestamp("@@@ Time of Auth failed callback: ",EndUserDetected[pContext->index].uiDeviceMacAddress);
    (void)phOsalUwb_Timer_Delete(timerid);
}
```



```c
if((j != 0xFF) && (EndUserDetected[j].AuthFailFlag >= 1))
{
    if(EndUserDetected[j].AuthFailFlag >= 5 && CurrentSystemStatus.SystemStatus == SystemFree) 
    {
        vStopAuthentication(j,notStarted); 
        EndUserDetected[j].AuthFailFlag  = 1;
        EndUserDetected[j].priority      = 1;
        LOG_I("@@@ User %.2x Auth failed times more than 5, set priority = 1... contniue...", MacAddress);
        continue;
    }
    if((getTimestamp()-EndUserDetected[j].SendTimesTamp < 0.6 * 1000) || (CurrentSystemStatus.SystemStatus != SystemFree))
    {
        LOG_I("@@@ Auth failed and re-authentication not arrived, waitting for 600ms... continue...");
        continue;                                              
    }
}
```

> 可能需修改为：多次失败后本地清除用户，并告知手机重启。
>
> ```c
> uiInformStatusToPhone(j, phone_restart);
> RemoveUserInDTPML(MacAddress); 
> RemoveUser(j);
> ```
>
> 

### 1.2 预读方案

#### 1.2.1 预读距离设计

预读是用户在进入蓝区的流程，为减少红区交易时间。若用户跳过蓝区进入红区，将不再依赖预读，从头完成所有流程。

```
uint16_t BlueAreaHeight            = 250;
```

设计为全局变量，demo app可调。

#### 1.2.2 预读周期设计

认证完成的用户进入蓝区后会进行预读，并将结果存储，用于后续和读卡器交互。

- 成功 < 500ms
- 一次失败 < 1000ms
- 两次失败 < 1500ms

```c
#define  TRANSACTIONTIMEOUT    100
```

这里预读失败后的定时器等待时间是500ms，不考虑多用户影响的情况下，预读失败1次后完成预读的总时间将<800ms。

#### 1.2.3 预读失败设计

预读操作并未做延时设计，默认能够认证成功的用户通常不会出现连续多次的预读失败。

预读失败的用户将会在定时周期到达时重新开始**（TransactionState = Allewed）**

```c
static void retransfer_timer_callback(uint32_t timerid, void *pContext)
{
    LOG_E("@@@ Transfer failed! Restart transfer.");
    
    (void)phOsalUwb_Timer_Stop(timerid);
    if( EndUserDetected[(*(uint8_t *)pContext)].TransactionState == SubwayWirteCard_sent)
    {
        vUpdateTransactionStateMachine((*(uint8_t *)pContext),WriteCard_failed);  //only once
    }else{
        vUpdateTransactionStateMachine((*(uint8_t *)pContext),Allowed);
    }

    EndUserDetected[(*(uint8_t *)pContext)].uiSuccessiveError++;
    
    vUpdateSystemStateMachine(SystemFree, EndUserDetected[(*(uint8_t *)pContext)].uiDeviceMacAddress);
    printTimestamp("@@@ Time of re-transfer callback: ",EndUserDetected[(*(uint8_t *)pContext)].uiDeviceMacAddress);
    (void)phOsalUwb_Timer_Delete(timerid);
}
```



#### 1.2.4 预读完成处理

完成预读的用户不会释放DTPML资源，单通道目前最大支持5个用户同时占用DTPML，其它用户想要完成交易需要等待占据DTPML资源的用户完成交易后释放资源。

**预读过程发送的apdu指令可能会由于城市的不同发生改变，最佳方案是和读卡器进行一次apdu预读指令同步操作，需要得到读卡器支持(待优化)**

预读将会为最终交易时间减少 < 500ms的时间.

##### 1.2.4.1 APDU存储块

由于内存限制原因，无法为所有用户分配独立的空间存储其预读APDU，所有用户将共用内存块，数据结构如下：

```c
#define MAX_READ_CARD_NUM   (5)
typedef struct
{
    bool allocated;
    uint16_t block_size;
    uint8_t mrm_block[3 * 256];
}MrmBlock_t;
MrmBlock_t __attribute__((section(".bss.$SRAM1"))) MrmBlockArr[MAX_READ_CARD_NUM] = {};
```

所有用户共用5块APDU内存，当用户收到读卡APDU时查询是否有空闲的APDU内存块，成功则存储自己的读卡APDU，否则，回退至读卡前。

```c
uint8_t mrmIndex = searchUnallocatedMrm();
if(mrmIndex != -1){
    LOG_I("Found unallocated block at index: %d", mrmIndex);
    MrmBlockArr[mrmIndex].allocated = true;
    memcpy(MrmBlockArr[mrmIndex].mrm_block,pRcvDataPkt->data,pRcvDataPkt->data_size);
    EndUserDetected[uiUserIndex].apdu = &MrmBlockArr[mrmIndex].mrm_block;
    EndUserDetected[uiUserIndex].apdu_len = pRcvDataPkt->data_size;
    EndUserDetected[uiUserIndex].block_index = mrmIndex;           //记录用户分到的内存块
}else{
    printTimestamp("@@@ Time of RAM-Apdu block not enough: ",EndUserDetected[uiUserIndex].uiDeviceMacAddress);
    vUpdateSystemStateMachine(SystemFree, EndUserDetected[uiUserIndex].uiDeviceMacAddress);
    vUpdateTransactionStateMachine(uiUserIndex,Allowed);
    break;
}
```

用户读卡时会进行判断，若没有空间的APDU内存块，取消读卡。

```
uint8_t mrmIndex = searchUnallocatedMrm();
if (mrmIndex == -1) {
    LOG_W("No more MRMs available, quit and notify users");
    return;
}
```



### 1.3 交易方案

用户进入红区后，执行交易流程需要满足以下：

1. 多用户情形下，所有用户测距包OK（无法判断坏包用户是否处于红区）
2. 多用户情形下，所有用户未丢包（无法判断丢包用户是否处于红区）
3. systemFree且仅有一个用户处于红区
4. 读卡完成，若未读卡则启动读卡流程

#### 1.3.1 交易距离设计

红区被设计为半椭圆。

```c
if(is_point_in_ellipse(x,y,a/2,d/2))
{
    NXPLOG_APP_I("################################### into red area...##################################################");
    return WRITE_CARD_AREA;
}

if((y < m) && (y > 0))
{
    NXPLOG_APP_I("################################### into blue area...##################################################");
    return READ_CARD_AREA;
}
```

若用户存在遮挡，红、蓝区会动态增加nLos_bais大小。

```c
if (EndUserDetected[j].nLos == 1) {
    LOG_I("@@@ User nLos is 1 , the red area and blue area Radius will be expanded 25cm");
    d = d + nLos_bais;        
    m = m + nLos_bais;
}
```

nLos测量值经过KF_classify预测后得到nLos实际值，当前大致规律为：若之前nLos值为连续的0，期望nLos值被判定为1需要经过6-7次的连续测量值全1。

```c
uint8_t KF_classify(KalmanFilter *kf,uint8_t measurement) {
       const  float Q     = 0.003f;       // Process noise covariance
       const  float R     = 0.35f;        // Measurement noise covariance
       const  float F     = 1.0f;         // State transition matrix
       const  float H     = 1.0f;         // Observation matrix 

       kf->x     = F * kf->x;
       kf->E_est = F * kf->E_est * F + Q;
       float y = measurement - H * kf->x;
       float S = H * kf->E_est * H + R;
       float K = kf->E_est * H / S;             // Calculate Kalman gain
       kf->x     = kf->x + K * y;                // 新预测值 = 上一轮预测值（先验） + 权重 × 新息
       kf->E_est = (1 - K * H) * kf->E_est;      // Update error covariance
       uint8_t classification = kf->x >= 0.5f ? 1 : 0;
       return classification;
}
```



#### 1.3.2 交易周期设计

用户进入写卡区域后进行写卡：

- 1个测距轮成功：< 300ms
- 2个测距轮成功：< 600ms
- 一次失败：<  1 - 2s
- 二次失败： <  ???? ms

#### 1.3.3 交易失败设计

针对不同情形下的交易失败进行处理：

1. 向手机读卡失败：释放系统资源，400ms后可再次发起读卡
2. 向手机写卡失败：回退到读卡完成状态，400ms后可再次发起和Reader交互
3. Reader无返回：回退到读卡完成状态，400ms后可再次发起和Reader交互
4. 若1|2执行了5轮仍然失败，清除用户并通知手机重启

```c
static void retransfer_timer_callback(uint32_t timerid, void *pContext) {
    LOG_E("@@@ Transfer failed! Restart transfer.");
    printTimestamp("@@@ Time of re-transfer callback: ", EndUserDetected[(*(uint8_t *)pContext)].uiDeviceMacAddress);
    (void)phOsalUwb_Timer_Stop(timerid);
    if (EndUserDetected[(*(uint8_t *)pContext)].TransactionState == SubwayWirteCard_sent) {
        vUpdateTransactionStateMachine((*(uint8_t *)pContext), ReadCard_compelete);  
    } else {
        vUpdateTransactionStateMachine((*(uint8_t *)pContext), Allowed);
    }
    EndUserDetected[(*(uint8_t *)pContext)].uiSuccessiveError++;
    vUpdateSystemStateMachine(SystemFree, EndUserDetected[(*(uint8_t *)pContext)].uiDeviceMacAddress);
    (void)phOsalUwb_Timer_Delete(timerid);
}
```

> 注：失败+重试时间需小于信号量等待时间

#### 1.3.4 交易完成设计

用户接收来自Reader的HALT信号后开始进行交易完成处理流程：

1. 通知Phone交易完成
2. 更新交易完成表，防止连续对同一个用户进行交易
3. 删除本地存储的用户状态
4. 释放系统资源

```c
void transactionDoneRoutine(uint16_t uiAddressSource, uint8_t uiUserIndex) {
	vStopTransaction(uiUserIndex, EndUserDetected[uiUserIndex].TransactionState );
    printTimestamp("@@@ Time of Write Card End : ",sztapdudata.MACADDRESS);
	char doneMacKey[5] = {"init"};
	HexToAscii((uint8_t *)(&uiAddressSource), doneMacKey, 2); // 2 bytes
	updateTransactionAddressMap(uiAddressSource, doneMacKey);
    RemoveUser(uiUserIndex);
	vUpdateSystemStateMachine(SystemFree, 0x0000);    
}
```

###### 1.3.4.1 交易完成地址表策略

用户完成交易后，进行下一次交易限制条件：

1. 用户交易完成并断开连接30s后，允许再次交易
2. 用户未断开连接30s，强行等待64s后，允许再次交易
3. 用户未断开连接30s，未强行等待64s，期间有 > 10个用户完成交易，运行再次交易，循环覆盖

```
uint8_t transacIndex         = searchDoneUserIndex(MacAddress);
if (transacIndex != NUMBER_TRANCTION_HISTORY_DEVICES) {
    LOG_I("device detected with MAC Address %x already transaction done, ignored ",MacAddress);
    UserDoneTransaction[transacIndex].StayCurCount = UserDoneTransaction[transacIndex].StayCurCount + 1;
    UserDoneTransaction[transacIndex].StayPreCount = 120;
}
```









