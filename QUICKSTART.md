# 快速开始指南 (Quick Start Guide)

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 三种使用方式

#### 方式一：命令行模式（最简单）

直接在命令行验证信息：

```bash
python verification_agent.py "你的待验证信息"
```

**示例：**
```bash
python verification_agent.py "立陶宛在2021年允许台湾设立代表处"
```

#### 方式二：Web界面模式（推荐）

启动Web服务器：

```bash
python verification_web_api.py
```

然后在浏览器访问：http://localhost:5000

**特点：**
- 🎨 友好的图形界面
- 📊 可视化的验证结果
- 🔗 可点击的来源链接
- 💾 结果可保存

#### 方式三：Python脚本调用

在你的Python代码中使用：

```python
from verification_agent import VerificationAgent

# 创建验证智能体
agent = VerificationAgent()

# 验证信息
result = agent.verify_information("你的待验证信息")

# 显示结果
agent.display_result(result)
```

### 3. 运行示例

查看更多使用示例：

```bash
python examples.py
```

该脚本包含5个不同类型的验证示例。

### 4. 运行测试

验证系统是否正常工作：

```bash
python test_verification_agent.py
```

## 📋 验证流程说明

1. **输入信息** - 提供需要验证的信息陈述
2. **分析信息** - 系统自动分析关键信息点
3. **联网搜索** - 搜索权威来源（目前为演示模式）
4. **收集资料** - 从多个来源收集相关信息
5. **交叉比对** - 对比不同来源的信息一致性
6. **生成结论** - 输出真伪判断和置信度

## 🔍 输出结果说明

### 真伪结论类型
- **真实** - 信息得到多个权威来源证实
- **部分真实** - 信息基本属实但有细节偏差
- **存疑** - 来源信息不一致或不充分
- **可能虚假** - 多数来源与信息相悖
- **无法充分验证** - 缺乏足够的公开信息

### 置信度
- **高** - 有充分的权威来源支持结论
- **中** - 有一定来源支持但需要更多验证
- **低** - 来源不足或质量不高

### 输出包含内容
1. 待验证信息
2. 验证结论（真/假）
3. 置信度（高/中/低）
4. 核查依据列表
5. 权威来源列表（含URL）
6. 验证详情说明
7. 验证时间戳

## ⚠️ 重要说明

### 当前状态
本版本使用**模拟搜索结果**进行演示。实际部署时需要集成真实的搜索API。

### 推荐集成的API
- **搜索API**：Google Search API, Bing Search API, DuckDuckGo API
- **事实核查API**：FactCheck.org, Snopes, PolitiFact, Full Fact

### 数据限制
- 仅能验证公开的、可通过网络搜索获取的信息
- 无法验证未公开的私密数据
- 验证准确性依赖于可获取信息的质量

## 🛠️ 故障排除

### 问题：无法安装依赖
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 问题：Web服务无法启动
检查端口5000是否被占用：
```bash
# Linux/Mac
lsof -i :5000

# Windows
netstat -ano | findstr :5000
```

### 问题：ImportError
确保在项目根目录运行命令：
```bash
cd /path/to/123456
python verification_agent.py
```

## 📚 更多帮助

- 查看完整文档：[README.md](README.md)
- 查看示例代码：[examples.py](examples.py)
- 运行单元测试：`python test_verification_agent.py`

## 🤝 反馈与支持

如有问题或建议，欢迎提交Issue或Pull Request。

---

**版本**: 1.0.0  
**最后更新**: 2026-02-13
