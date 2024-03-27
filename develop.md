# 赛马娘识别训练器
## 说明
因为赛马娘的游戏机制比较简单，所以可以通过图像识别的方式来实现自动化。这个项目是一个赛马娘的图像识别训练器，可以通过图像识别来实现自动化。
另外，这个项目是一个练手项目，用来练习图像识别和自动化。
赛马娘游戏每日任务比较多，而且每日任务比较重复，所以可以通过图像识别来实现自动化。
尤其是活动任务需要大量时间刷养成，为了能够更好的体验游戏，不想略过活动奖励，所以需要一个自动化的工具。

# 制作步骤

## 1. 准备工作

由于赛马娘是一个安卓游戏，所以需要安装安卓模拟器。安卓模拟器有很多，比如雷电模拟器、夜神模拟器、MuMu模拟器等等。这里使用MuMu模拟器。
赛马娘是一款养成类肉鸽游戏，具有很大的随机性，需要对大量的角色，支援卡，随机事件，赛事等等进行处理，所以需要一个图像识别的工具。

### 1.1 技术准备
    从requirements.txt文件中，我们可以看到项目使用了以下的Python库：  
    adbutils: 用于Android设备的操作和管理
    aiofiles, aiohttp, aiosignal, anyio: 用于异步I/O操作和HTTP请求
    apkutils2: 用于分析Android APK文件
    astor: 用于Python抽象语法树的操作
    Babel: 用于国际化和本地化
    bce-python-sdk: 百度云的Python SDK
    beautifulsoup4: 用于解析HTML和XML文档
    cachetools: 提供缓存数据的工具
    certifi: 提供Mozilla的CA Bundle
    click, colorama, colorlog: 用于命令行界面的创建和日志的记录
    croniter: 用于处理cron表达式
    cssselect, cssutils: 用于处理CSS选择器和CSS样式
    Cython: 用于编写C扩展的Python库
    decorator, Deprecated: 用于创建和管理Python装饰器
    dill: 用于Python对象序列化
    fastapi: 用于创建API的web框架
    flake8: Python的代码风格检查工具
    Flask, Flask-Babel: 用于创建web应用的框架和Flask的国际化扩展
    fonttools: 用于操作和修改字体文件
    future: 用于在Python 2和3之间提供兼容性
    h11: 用于HTTP/1.1协议的处理
    imageio, imgaug: 用于图像的读取和增强
    importlib-metadata: 用于读取Python包的元数据
    jarowinkler: 用于字符串相似度的计算
    Jinja2: 用于创建和管理模板的库
    lmdb: 用于LMDB数据库的操作
    lxml: 用于处理XML和HTML文档
    matplotlib: 用于数据可视化
    multidict: 提供多值字典的数据结构
    networkx: 用于创建和操作复杂网络的库
    numpy: 用于数值计算
    openai: OpenAI的Python SDK
    opencv-contrib-python, opencv-python: 用于图像处理和计算机视觉的库
    openpyxl: 用于读写Excel 2010 xlsx/xlsm/xltx/xltm文件
    paddleocr, paddlepaddle: 百度的深度学习框架和OCR工具
    pandas: 用于数据分析和操作
    pdf2docx: 用于将PDF转换为docx格式
    Pillow: 用于图像处理
    pre-commit: 用于管理git pre-commit钩子的工具
    protobuf: Google的数据交换格式
    psutil: 用于获取系统和进程信息
    pydantic: 用于数据验证和设置管理
    PyMuPDF: 用于PDF和其他格式文件的处理
    pyparsing: 用于创建解析器的库
    python-dateutil: 提供强大的日期和时间工具
    rapidfuzz: 用于字符串模糊匹配和相似度计算
    requests: 用于HTTP请求
    scikit-image: 用于图像处理的库
    scipy: 用于科学计算
    Shapely: 用于操作和分析平面几何对象
    tornado: 用于创建web应用的框架
    tqdm: 用于创建进度条的库
    uiautomator2: 用于Android UI测试的库
    urllib3: 用于HTTP请求
    uvicorn: 用于运行ASGI应用的服务器
    visualdl: 百度的深度学习可视化工具
    websockets: 用于创建WebSocket服务器和客户端的库
    Werkzeug: 用于创建WSGI应用的库
    wrapt: 用于创建装饰器、包装器和代理的库
    xmltodict: 用于将XML转换为Python字典的库
    yarl: 用于URL处理的库

### 1.2 环境准备
    1. 安装Python
    2. 安装MuMu模拟器
    3. 安装ADB
    4. 安装Python库

### 1.3 ocr训练准备
    1. 准备训练数据
    2. 训练模型

## 2. 确认步骤
    
赛马娘需要哪几种操作：

    1. 点击，包括点击按钮、点击坐标、点击图片。
    2. 滑动，包括滑动坐标、滑动图片。
    3. 输入，包括输入文字。
    4. 识别，包括识别文字、识别图片。

赛马娘有哪些玩法：
    
    1. 养成：剧本养成（当前ura）。
    2. 社团：社团捐赠、捐赠请求。
    3. 商店：限时商店。
    4. 奖励：任务领取，礼物箱领取。
    5. 活动：活动任务奖励，轮盘德比。
    6. 强化编成（不介入）。
    7. 剧情（不介入）。
    8. 赛事：团队竞技场，日常赛事，赛事活动-群英联赛，赛事活动-传奇赛事。
    9. 扭蛋（不介入）。
    10. 菜单（不介入）。

赛马娘养成有哪些要素：
    
    1. 剧本选择
    2. 剧本事件
    3. 赛马娘选择、出借赛马娘选择、出借赛马娘次数限制
    4. 赛马娘事件
    5. 协助卡选择（卡组选择）、好友协助卡选择（突破等级）
    6. 协助卡事件
    7. 速耐力毅智技六种属性数值养成
    8. 速耐力毅智五种训练设施等级
    9. 技能学习（指定日期学习、指定技能点数学习、指定最后学习技能，指定优先学习技能，指定禁止学习技能）
    10. 比赛，三年跑法，指定赛事适应性满足，指定具体赛事，预设赛程，粉丝数未达标时主动比赛
    11. 养成结束，因子展示
    12. 养成过程中属性养成分阶段目标，养成总目标
    13. 养成过程中训练失败率
    14. 外出，友人卡外出

游戏界面

    1. 游戏主界面
    2. 养成选择剧本界面
    3. 选择养成赛马娘界面
    4. 选择种马界面
    5. 协助卡编成界面
    6. 选择好友协助卡界面
    7. 养成主界面
    8. 训练界面
    9. 技能学习界面
    10. 外出选择界面（友人时出现）
    11. 赛事选择界面
    12. 赛事界面
    13. 事件选项界面
    14. 编成信息页面
    
    15. 社团界面

    16. 商店界面
    17. 限时特卖界面

    18. 赛事界面
    19. 团队竞技场界面
    20. 团队赛事界面
    21. 日常赛事界面
    22. 赛事活动界面-...

    23. 礼物领取界面
    24. 任务奖励领取界面

    25. 剧情活动界面
    26. 活动任务奖励界面
    27. 轮盘德比


## 3. 制作步骤

## 4. 制作步骤

## 5. 类

### 5.1 类的定义

```
UmamusumeAutoTrainer
├─bot   # 这个模块包含了机器人的所有功能，包括基础功能、连接、引擎、识别和服务。
│  ├─base   # 这个模块包含了机器人的基础功能，如通用类、常量、上下文、日志、配置、坐标、资源、任务和用户数据。
│  │  ├─common.py   # 通用类
│  │  ├─const.py    # 常量
│  │  ├─context.py  # 上下文
│  │  ├─log.py    # 日志
│  │  ├─manifest.py # 配置
│  │  ├─point.py    # 坐标
│  │  ├─resource.py # 资源
│  │  ├─task.py   # 任务
│  │  └─user_data.py    # 用户数据
│  ├─conn   # 这个模块包含了机器人的连接功能，如控制、截图、操作系统和uiautomator2。
│  │  ├─ctrl.py # 控制
│  │  ├─minicap.py # 截图
│  │  ├─os.py # 操作系统
│  │  └─u2_ctrl.py # uiautomator2
│  ├─engine # 这个模块包含了机器人的引擎功能，如控制、执行器和调度器
│  │  ├─ctrl.py # 控制
│  │  ├─executer.py # 执行器
│  │  └─scheduler.py # 调度器
│  ├─recog # 这个模块包含了机器人的识别功能，如图像匹配和文字识别。
│  │  ├─image_matcher.py # 图像匹配
│  │  └─ocr.py # 文字识别
│  ├─server # 这个模块包含了机器人的服务功能，如协议和处理。
│  │  ├─protocol # 协议
│  │  │  ├─common.py # 通用
│  │  │  └─task.py # 任务
│  └─ └─handler.py # 处理
├─deps # 这个模块包含了项目的依赖，如adb。
│  └─adb # adb
├─docs # 文档
├─error # 错误
├─logs # 日志
├─module # 这个模块包含了项目的模块，如赛马娘模块。
│  ├─umamusume # 这个模块包含了赛马娘的所有功能，如资产、协议、脚本、检查、上下文、定义、处理、钩子、配置、任务和用户数据。
│  │  ├─asset # 这个模块包含了赛马娘的资产功能，如坐标、赛事数据、模板和界面。
│  │  │  ├─point.py # 坐标
│  │  │  ├─race_data.py # 赛事数据
│  │  │  ├─template.py # 模板
│  │  │  └─ui.py # 界面
│  │  ├─protocol # 这个模块包含了赛马娘的协议功能，如预设。
│  │  │  └─preset.py # 预设
│  │  ├─script # 这个模块包含了赛马娘的脚本功能，如培养、AI、常量、培养、信息、解析和支援卡。
│  │  │  ├─cultivate_task # 培养
│  │  │  │  ├─event # 事件
│  │  │  │  │  ├─manifest.py # 配置
│  │  │  │  │  └─scenario_event.py # 场景事件
│  │  │  │  ├─ai.py # AI
│  │  │  │  ├─const.py # 常量
│  │  │  │  ├─cultivate.py # 培养
│  │  │  │  ├─info.py # 信息
│  │  │  │  ├─parse.py # 解析
│  │  │  │  └─support_card.py # 支援卡
│  │  │  └─default.py # 默认
│  │  ├─check.py # 检查
│  │  ├─context.py # 上下文
│  │  ├─define.py # 定义
│  │  ├─handler.py # 处理
│  │  ├─hook.py # 钩子
│  │  ├─manifest.py # 配置
│  │  ├─task.py # 任务
│  └─ └─user_data.py # 用户数据
├─public # 这个模块包含了项目的公共资源，如资产。
│  └─assets # 资产
├─resource # 这个模块包含了项目的公共资源，如资产。
│  └─umamusume # 赛马娘
│      ├─btn # 按钮
│      ├─data # 数据
│      ├─race # 赛事
│      ├─ref # 参考
│      ├─ui # 界面
│      └─uma_icon # 赛马娘图标
├─userdata # 这个模块包含了项目的用户数据，如赛马娘的预设。
│  └─umamusume # 赛马娘
│      └─presets # 预设
├─web # 这个模块包含了项目的网页功能，如源码、资产、组件、路由、工具和视图。
│  └─src # 源码
│      ├─assets # 资产
│      ├─components # 组件
│      │  ├─base # 基础
│      │  └─umamusume # 赛马娘
│      ├─router # 路由
│      ├─util # 工具
│    └─views # 视图
├─config.py # 配置
├─config.yaml # 配置
├─develop.md # 开发
├─install.ps1 # 安装
├─main.py # 主程序
├─README.md # 说明
├─requirements.txt # 依赖
└─run.ps1 # 运行
```
