# 小六壬起课工具

一个面向中文用户的小六壬起课网页 MVP。  
项目使用 Python + Streamlit 构建，适合部署到 Streamlit Community Cloud，也适合本地运行学习。

本工具只使用本地规则模板，不调用外部大模型，不提供用户登录、数据库、付费系统或后端服务。

## 项目简介

小六壬是一种民间常见的时间起课方法，通常用农历月、农历日和时辰，沿“大安、留连、速喜、赤口、小吉、空亡”的顺序推算结果。

本项目把这个过程做成网页工具：

- 自动识别本机时间起课
- 支持手动输入阳历时间，并自动转换为农历
- 支持手动输入农历月、农历日和时辰
- 显示完整起课路径
- 根据不同问题场景给出本地规则解释

页面解释以“传统文化学习与娱乐参考”为定位，重在帮助用户整理问题、观察节奏、复盘结果，不承诺预测准确率。

## 功能列表

- 使用当前本机时间起课
- 自动识别浏览器本地时间和 IANA 时区
- 手动选择阳历日期和时间起课
- 阳历时间自动转换为农历月日
- 手动输入农历月、农历日、十二时辰起课
- 支持夜子时换日开关
- 支持闰月展示，算法默认按同名月份处理
- 支持多个占问场景：
  - 综合事项
  - 财运/求财
  - 工作/事业
  - 感情/关系
  - 寻物
  - 出行
  - 学业/考试
  - 消息等待
  - 合作/签约
  - 家宅/搬迁
  - 身心状态
  - 自定义问题
- 显示最终六神、结果总览、当前局势、场景含义、建议行动、避免事项、复盘提示
- 寻物场景额外显示寻找方向、搜索策略和提醒
- 使用表格展示起课路径
- 提供“学习与规则说明”折叠区域
- 不保存服务器数据库，也不保存用户起课记录

## 技术栈

- Python 3.11+
- Streamlit
- lunar_python
- streamlit-js-eval
- pytest

## 本地运行

### 1. 安装 Python

请先确认本机已经安装 Python 3.11 或更高版本：

```bash
python3 --version
```

如果你的系统使用 `python` 命令，也可以运行：

```bash
python --version
```

### 2. 创建虚拟环境

在项目根目录运行：

```bash
python3 -m venv .venv
```

### 3. 激活虚拟环境

macOS / Linux：

```bash
source .venv/bin/activate
```

Windows PowerShell：

```powershell
.venv\Scripts\Activate.ps1
```

Windows CMD：

```bat
.venv\Scripts\activate.bat
```

### 4. 安装依赖

```bash
python3 -m pip install -r requirements.txt
```

如果你的系统使用 `python` 命令：

```bash
python -m pip install -r requirements.txt
```

### 5. 启动网页

```bash
python3 -m streamlit run app.py
```

启动后，终端会显示访问地址，通常是：

```text
http://localhost:8501
```

打开浏览器访问这个地址即可使用。

## 测试

运行全部单元测试：

```bash
python3 -m pytest
```

如果你的系统使用 `python` 命令：

```bash
python -m pytest
```

可选：检查 Python 文件是否能正常编译：

```bash
python3 -m compileall .
```

## 项目结构

```text
xiaoliuren-web/
├── app.py                         # Streamlit 页面入口
├── requirements.txt               # 项目依赖
├── README.md                      # 中文说明文档
├── .gitignore                     # Git 忽略规则
├── .streamlit/
│   └── config.toml                # Streamlit 基础主题配置
├── assets/
│   └── xiaoliuren-six-signs.svg   # 小六壬六神示意图
├── xiaoliuren/
│   ├── __init__.py
│   ├── models.py                  # 枚举和数据结构
│   ├── exceptions.py              # 自定义异常
│   ├── constants.py               # 页面选项和常量
│   ├── engine.py                  # 小六壬核心算法和起课服务
│   ├── calendar_service.py        # 阳历转农历服务
│   ├── browser_time.py            # 浏览器本地时间识别
│   ├── form_service.py            # 表单输入到起课服务的编排
│   ├── interpretations.py         # 本地解释模板
│   ├── ui_helpers.py              # Streamlit 展示组件
│   └── utils.py                   # 通用工具函数
└── tests/
    ├── test_app_validation.py
    ├── test_browser_time.py
    ├── test_calendar_service.py
    ├── test_dependencies.py
    ├── test_engine.py
    └── test_interpretations.py
```

## 小六壬算法说明

当前只实现一个流派：

```text
标准月日时起课法
```

六神顺序固定为：

```text
大安 → 留连 → 速喜 → 赤口 → 小吉 → 空亡
```

本项目采用的公式：

```text
月位 = (农历月 - 1) % 6
日位 = (月位 + 农历日 - 1) % 6
时位 = (日位 + 时辰序号) % 6
最终结果 = 六神[时位]
```

十二时辰序号：

```text
子=0，丑=1，寅=2，卯=3，辰=4，巳=5，
午=6，未=7，申=8，酉=9，戌=10，亥=11
```

项目中已用单元测试固定以下示例：

```text
农历六月初五巳时 → 速喜
农历三月初五辰时 → 小吉
农历八月十七辰时 → 赤口
```

## 农历转换说明

当用户选择“使用当前时间”或“手动选择阳历时间”时，应用会使用 `lunar_python` 将阳历日期转换为农历日期。

转换逻辑集中在：

```text
xiaoliuren/calendar_service.py
```

页面入口 `app.py` 不直接调用农历库，避免把业务逻辑混在 UI 里。

## 闰月处理说明

当前默认规则：

```text
闰月按同名月份处理
```

例如闰二月仍按二月参与小六壬算法。  
页面会保留“是否闰月”的展示信息，但核心计算使用同名月份数字。

## 夜子时换日说明

默认不启用夜子时换日。

如果用户开启“夜子时换日”，并且本地时间是 23 点，则农历转换会先按次日处理，但时辰仍然是子时。

## 解释系统说明

解释内容全部来自本地规则模板，不调用 AI API。

每次起课结果会包含：

- 结果总览
- 当前局势
- 对这个问题的含义
- 建议行动
- 避免事项
- 复盘提示

每个六神解释会结合：

- 基础含义
- 五行取象
- 时间节奏
- 风险点
- 判断重点
- 场景化说明

解释风格尽量保持清楚、克制，不使用绝对化或收益承诺式表述。

## 部署到 Streamlit Community Cloud

### 1. 上传到 GitHub

先在 GitHub 新建仓库，然后把本项目提交并推送上去。

常见命令示例：

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/你的用户名/你的仓库名.git
git push -u origin main
```

### 2. 创建 Streamlit 应用

打开 Streamlit Community Cloud，选择新建应用。

### 3. 选择仓库

选择刚刚上传的 GitHub 仓库和分支。

### 4. 设置入口文件

Main file 填写：

```text
app.py
```

### 5. 确认依赖文件

确认仓库根目录有：

```text
requirements.txt
```

Streamlit Cloud 会根据这个文件安装依赖。

### 6. 部署

点击 Deploy。部署完成后，Streamlit 会提供公网访问链接。

## GitHub 发布前检查

建议提交前确认：

- 不要上传 `.venv/`
- 不要上传 `__pycache__/`
- 不要上传 `.pytest_cache/`
- 不要上传 `.streamlit/secrets.toml`
- 确认 `requirements.txt` 已包含所有依赖
- 确认 `python3 -m pytest` 可以通过
- 确认 `app.py` 是 Streamlit 入口文件

这些文件已经写入 `.gitignore`。

## 常见问题

### ModuleNotFoundError

通常是依赖没有安装，或虚拟环境没有激活。

解决：

```bash
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

Windows 用户请使用对应的虚拟环境激活命令。

### Streamlit Cloud 部署后缺包

请检查 `requirements.txt` 是否包含：

```text
streamlit
lunar_python
streamlit-js-eval
pytest
```

### Python 版本不一致

本项目按 Python 3.11+ 设计。  
如果本地或云端 Python 版本太低，可能出现语法或依赖问题。

### 浏览器时间识别不符合预期

“使用当前时间”模式会优先读取浏览器本地时间和浏览器 IANA 时区。  
如果浏览器时间识别暂未完成，系统会先按北京时间兜底处理。

如结果时间不符合预期，请检查：

- 电脑或手机系统时区是否正确
- 浏览器是否允许页面正常运行脚本
- 是否开启了夜子时换日

### lunar_python 转换失败

请检查：

- 依赖是否安装完整
- 输入阳历日期是否有效
- Python 环境是否能正常加载 `zoneinfo`

可重新安装依赖：

```bash
python3 -m pip install -r requirements.txt
```

## 免责声明

本项目仅作传统文化学习与娱乐参考。

页面中的起课结果和解释来自本地规则模板，不代表确定结论，不承诺准确率，也不应作为唯一决策依据。

本项目不提供：

- 医疗诊断
- 法律意见
- 投资建议
- 收益承诺
- 现实事件的确定性判断

涉及健康、医疗、法律、投资、财务、合同等重要事项时，请咨询相应领域的专业人士。

使用本工具即表示你理解：小六壬属于传统文化和民俗术数范畴，结果适合用于自我整理、娱乐体验和事后复盘，不适合替代专业判断。
