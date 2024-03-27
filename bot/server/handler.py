import os

from fastapi import FastAPI, Path
from fastapi.middleware.cors import CORSMiddleware

from bot.engine import ctrl as bot_ctrl
from bot.server.protocol.task import *
from starlette.responses import FileResponse

from module.umamusume import handler

server = FastAPI()

server.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 大应用多文件路由 https://fastapi.tiangolo.com/zh/tutorial/bigger-applications/
server.include_router(handler.router)


@server.get("/")
async def get_index():
    return FileResponse('public/index.html')


# 支持多任务添加
@server.post("/task")
def add_task(req: AddTaskRequest | list[AddTaskRequest]):
    if isinstance(req, AddTaskRequest):
        req = [req]
    for req in req:
        bot_ctrl.add_task(req.app_name, req.task_execute_mode, req.task_type, req.task_desc,
                          req.cron_job_config, req.attachment_data)

@server.delete("/task")
def delete_task(req: DeleteTaskRequest):
    bot_ctrl.delete_task(req.task_id)


@server.get("/task")
def get_task():
    return bot_ctrl.get_task_list()


@server.post("/action/bot/reset-task")
def reset_task(req: ResetTaskRequest):
    bot_ctrl.reset_task(req.task_id)


@server.post("/action/bot/start")
def start_bot():
    bot_ctrl.start()


@server.post("/action/bot/stop")
def stop_bot():
    bot_ctrl.stop()


@server.get("/{whatever:path}")
async def get_static_files_or_404(whatever):
    # try open file for path
    file_path = os.path.join("public", whatever)
    if os.path.isfile(file_path):
        if file_path.endswith((".js", ".mjs")):
            return FileResponse(file_path, media_type="application/javascript")
        else:
            return FileResponse(file_path)
    return FileResponse('public/index.html')
