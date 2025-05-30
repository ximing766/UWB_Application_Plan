# 🚀 快速开始

> 📖 **本指南将帮助您快速上手UWB闸机交易系统的开发，从环境搭建到基本功能实现。**

---

## 📋 前置要求

在开始之前，请确保您的开发环境满足以下要求：

### 硬件要求
- UWB开发板或模块
- 支持UWB的移动设备（如iPhone 11及以上）
- 开发用计算机（Windows/Linux/macOS）

### 软件要求
- Python 3.11+
- Git
- 串口调试工具
- UWB SDK

---

## 🛠️ 环境搭建

### 1. 克隆项目

```bash
git clone https://github.com/ximing766/UWB_Application_Plan.git
cd UWB_Application_Plan
```

### 2. 创建虚拟环境

```bash
# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境
# Windows
.venv\Scripts\activate

# Linux/macOS
source .venv/bin/activate
```

### 3. 安装依赖

```bash
# 安装项目依赖
pip install -e .

# 安装开发依赖（可选）
pip install -e ".[dev]"
```

---

## 🔧 基本配置

### UWB设备配置

1. **连接UWB设备**
   - 通过USB连接UWB开发板
   - 确认设备在设备管理器中正确识别
   - 记录串口号（如COM3、/dev/ttyUSB0等）

2. **配置通信参数**
   ```json
   {
     "port": "COM3",
     "baudrate": 115200,
     "timeout": 1.0
   }
   ```

### 认证距离设置

根据实际应用场景配置认证距离：

| 场景 | 推荐距离 | 说明 |
|------|----------|------|
| 地铁闸机 | 1.5-2m | 保证用户体验的同时避免误触发 |
| 办公楼门禁 | 1-1.5m | 提高安全性 |
| 停车场 | 2-3m | 便于车辆通行 |

---

## 🎯 第一个UWB应用

### 1. 基础连接测试

创建一个简单的连接测试程序：

```python
import serial
import time

def test_uwb_connection():
    """测试UWB设备连接"""
    try:
        # 打开串口连接
        ser = serial.Serial('COM3', 115200, timeout=1)
        print("✅ UWB设备连接成功")
        
        # 发送测试命令
        ser.write(b'AT\r\n')
        response = ser.readline().decode('utf-8').strip()
        
        if response == 'OK':
            print("✅ 设备响应正常")
        else:
            print(f"⚠️ 设备响应异常: {response}")
            
        ser.close()
        
    except Exception as e:
        print(f"❌ 连接失败: {e}")

if __name__ == "__main__":
    test_uwb_connection()
```

### 2. 距离测量示例

```python
import serial
import json
import time

class UWBRanging:
    def __init__(self, port='COM3', baudrate=115200):
        self.ser = serial.Serial(port, baudrate, timeout=1)
        
    def start_ranging(self, target_id):
        """开始距离测量"""
        command = f"RANGE:{target_id}\r\n"
        self.ser.write(command.encode())
        
    def get_distance(self):
        """获取距离数据"""
        try:
            data = self.ser.readline().decode('utf-8').strip()
            if data.startswith('DIST:'):
                distance = float(data.split(':')[1])
                return distance
        except:
            return None
        return None
    
    def close(self):
        """关闭连接"""
        self.ser.close()

# 使用示例
uwb = UWBRanging()
uwb.start_ranging('DEVICE_001')

for i in range(10):
    distance = uwb.get_distance()
    if distance:
        print(f"距离: {distance:.2f}m")
    time.sleep(0.1)

uwb.close()
```

---

## 🔐 认证流程实现

### 基本认证流程

```python
class UWBAuthentication:
    def __init__(self):
        self.auth_distance = 2.0  # 认证距离阈值
        self.auth_timeout = 0.6   # 认证超时时间（秒）
        
    def authenticate_user(self, user_id, distance):
        """用户认证"""
        if distance <= self.auth_distance:
            # 在认证范围内，开始认证流程
            return self._perform_authentication(user_id)
        else:
            return False, "用户不在认证范围内"
    
    def _perform_authentication(self, user_id):
        """执行认证"""
        start_time = time.time()
        
        # 模拟认证过程
        # 实际应用中这里会包含加密验证等步骤
        time.sleep(0.1)  # 模拟认证延迟
        
        elapsed_time = time.time() - start_time
        
        if elapsed_time < self.auth_timeout:
            return True, "认证成功"
        else:
            return False, "认证超时"
```

---

## 📊 数据监控

### 实时数据显示

```python
import matplotlib.pyplot as plt
import numpy as np
from collections import deque

class UWBMonitor:
    def __init__(self, max_points=100):
        self.distances = deque(maxlen=max_points)
        self.timestamps = deque(maxlen=max_points)
        
    def add_data(self, distance):
        """添加距离数据"""
        self.distances.append(distance)
        self.timestamps.append(time.time())
        
    def plot_realtime(self):
        """实时绘图"""
        plt.clf()
        plt.plot(list(self.timestamps), list(self.distances))
        plt.xlabel('时间')
        plt.ylabel('距离 (m)')
        plt.title('UWB距离实时监控')
        plt.grid(True)
        plt.pause(0.01)
```

---

## 🧪 测试验证

### 1. 距离精度测试

```bash
# 运行距离精度测试
python tests/test_ranging_accuracy.py
```

### 2. 认证性能测试

```bash
# 运行认证性能测试
python tests/test_auth_performance.py
```

### 3. 压力测试

```bash
# 运行多用户压力测试
python tests/test_multi_user.py
```

---

## 🚨 常见问题

### Q: 设备连接失败怎么办？

**A:** 检查以下几点：
1. 确认设备驱动已正确安装
2. 检查串口号是否正确
3. 确认波特率设置匹配
4. 检查设备是否被其他程序占用

### Q: 距离测量不准确？

**A:** 可能的原因：
1. 环境中存在金属障碍物
2. 多径效应影响
3. 设备校准问题
4. 天线方向不正确

### Q: 认证经常超时？

**A:** 优化建议：
1. 调整认证超时时间
2. 优化认证算法
3. 检查网络延迟
4. 增加重试机制

---

## 📚 下一步

完成快速开始后，建议继续学习：

1. [环境搭建详细指南](setup.md) - 深入了解开发环境配置
2. [API参考文档](../api/reference.md) - 完整的API接口说明
3. [协议规范](../protocol/uwb-protocol.md) - UWB通信协议详解
4. [高级应用示例](../examples/advanced.md) - 复杂场景的实现方案

---

## 💡 小贴士

- 🔧 **开发调试**: 使用串口调试工具监控数据传输
- 📊 **性能监控**: 定期检查认证成功率和响应时间
- 🛡️ **安全考虑**: 在生产环境中启用加密和身份验证
- 📝 **日志记录**: 保持详细的操作日志便于问题排查

---

*需要帮助？请查看 [常见问题](../guide/faq.md) 或在 [GitHub Issues](https://github.com/ximing766/UWB_Application_Plan/issues) 中提问。*