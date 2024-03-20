import copy
import datetime
import threading
import time

import croniter

from bot.base.task import TaskStatus as TaskStatus, TaskExecuteMode, Task
import bot.engine.executor as executor
import bot.base.log as logger

log = logger.get_logger(__name__)


class Scheduler:
    task_list: list[Task] = []
    running_task: Task = None

    active = False

    def add_task(self, task):
        log.info("已添加任务：" + task.task_id)
        self.task_list.append(task)

    def delete_task(self, task_id):
        remove_idx = -1
        # enumerate()会返回一个迭代器，这个迭代器在每次迭代时返回一个包含两个元素的元组。
        # 第一个元素是当前元素的索引（从0开始），第二个元素是当前元素的值。
        for i, v in enumerate(self.task_list):
            if v.task_id == task_id:
                remove_idx = i
        if remove_idx != -1:
            del self.task_list[remove_idx]
            return True
        else:
            return False

    def reset_task(self, task_id):
        reset_idx = -1
        for i, v in enumerate(self.task_list):
            if v.task_id == task_id:
                reset_idx = i
        if reset_idx != -1:
            self.task_list[reset_idx].task_status = TaskStatus.TASK_STATUS_PENDING
            self.task_list[reset_idx].end_task_reason = None
            return True
        else:
            return False

    def init(self):
        task_executor = executor.Executor()
        while True:
            if self.active:
                for task in self.task_list:
                    # 伪任务调度，永远保持只有一个任务执行。
                    # main.py调用Scheduler.init(),因为【不保存任务列表】，
                    # 所以【Scheduler.active赋值为false】。同时【task_executor.active赋值为false】。
                    # 当调用Scheduler.start()，Scheduler.active赋值为true。执行while循环，如果没有任务，active依然会被重新赋值false。
                    # 当通过接口添加task后，当前task在第一个分支进入，并开启任务执行器线程，调用task_executor.start，
                    # 将【task_executor.active赋值为true】，锁定该分支。
                    # 并且其他程序并不改变task_executor.active值，除非结束任务，所以此调度相当于入栈调度。
                    if task.task_execute_mode == TaskExecuteMode.TASK_EXECUTE_MODE_ONE_TIME:
                        if task.task_status == TaskStatus.TASK_STATUS_PENDING and not task_executor.active:
                            executor_thread = threading.Thread(target=task_executor.start, args=([task]))
                            executor_thread.start()
                    elif task.task_execute_mode == TaskExecuteMode.TASK_EXECUTE_MODE_CRON_JOB:
                        if task.task_status == TaskStatus.TASK_STATUS_SCHEDULED:
                            if task.cron_job_config is not None:
                                if task.cron_job_config.next_time is None:
                                    now = datetime.datetime.now()
                                    cron = croniter.croniter(task.cron_job_config.cron, now)
                                    task.cron_job_config.next_time = cron.get_next(datetime.datetime)
                                else:
                                    if task.cron_job_config.next_time < datetime.datetime.now():
                                        self.copy_task(task, TaskExecuteMode.TASK_EXECUTE_MODE_ONE_TIME)
                                        now = datetime.datetime.now()
                                        cron = croniter.croniter(task.cron_job_config.cron, now)
                                        task.cron_job_config.next_time = cron.get_next(datetime.datetime)
                    else:
                        log.warning("未知任务类型：" + str(task.task_execute_mode) + ", task_id: " + str(task.task_id))

            else:
                if task_executor.active:
                    task_executor.stop()
            time.sleep(1)

    # 复制任务
    def copy_task(self, task, to_task_execute_mode: TaskExecuteMode):
        new_task = copy.deepcopy(task)
        new_task.task_id = str(int(round(time.time() * 1000)))
        if (to_task_execute_mode == TaskExecuteMode.TASK_EXECUTE_MODE_ONE_TIME and task.task_execute_mode ==
                TaskExecuteMode.TASK_EXECUTE_MODE_CRON_JOB):
            new_task.task_id = "CRONJOB_" + new_task.task_id
            new_task.cron_job_config = None
        new_task.task_execute_mode = to_task_execute_mode
        if new_task.task_execute_mode == TaskExecuteMode.TASK_EXECUTE_MODE_ONE_TIME:
            new_task.task_status = TaskStatus.TASK_STATUS_PENDING
        self.task_list.append(new_task)

    def stop(self):
        self.active = False

    def start(self):
        self.active = True

    def get_task_list(self):
        return self.task_list


scheduler = Scheduler()




