import subprocess
from subprocess import Popen
from typing import Any
from plyer import notification
import bot.base.log as logger

log = logger.get_logger(__name__)


# run_cmd 执行命令行
def run_cmd(cmd_string) -> Popen[bytes] | Popen[Any]:
    log.debug('run cmdline: {}'.format(cmd_string))
    # 创建一个子进程。
    # shell命令，可以是字符串或者序列类型（如：list，元组）
    # shell：如果该参数为 True，将通过操作系统的 shell 执行指定的命令。
    # 子进程的标准输入、输出和错误。subprocess.PIPE 表示为子进程创建新的管道。subprocess.DEVNULL 表示使用 os.devnull。默认使用的是 None，表示什么都不做
    return subprocess.Popen(cmd_string, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


# 桌面通知应用程序
def push_system_notification(title, message, timeout):
    notification.notify(
        title=title,
        message=message,
        timeout=timeout
    )
