from bot.base.resource import UI
from typing import Dict

# AppManifest 是一个应用的配置文件，用于描述一个应用的基本信息和构建过程
class AppManifest:

    # app_name: 应用名称
    app_name: str = None
    # app_activity_name: 应用的启动 Activity 名称
    app_activity_name: str = None
    # app_package_name: 应用的包名
    app_package_name: str = None
    # build_context: 构建上下文
    build_context: callable = None
    # build_task: 构建任务
    build_task: callable = None
    # ui_list: UI 列表
    ui_list: list[UI] = None
    # script: 脚本
    script: callable = None
    # before_hook: 前置钩子
    before_hook: callable = None
    # after_hook: 后置钩子
    after_hook: callable = None

    def __init__(self, app_name: str, app_activity_name: str, app_package_name: str,
                 build_context: callable, build_task: callable, ui_list: list[UI],
                 script: callable, before_hook: callable, after_hook: callable):
        self.app_name = app_name
        self.app_activity_name = app_activity_name
        self.app_package_name = app_package_name
        self.build_context = build_context
        self.build_task = build_task
        self.ui_list = ui_list
        self.before_hook = before_hook
        self.after_hook = after_hook
        self.script = script


# APP_MANIFEST_LIST 是一个应用配置文件的列表，用于存储所有的应用配置文件
APP_MANIFEST_LIST: Dict[str, AppManifest] = {}


# register_app 用于注册一个应用配置文件
def register_app(app_manifest: AppManifest):
    APP_MANIFEST_LIST[app_manifest.app_name] = app_manifest
