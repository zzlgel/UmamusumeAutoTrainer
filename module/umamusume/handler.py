from bot.server.handler import server
from module.umamusume.protocol.preset import AddPresetRequest
from module.umamusume.user_data import read_presets, write_preset


# 从这里开始，是一个简单的接口，用于读取和写入预设
@server.post("/umamusume/get-presets")
def get_presets():
    return read_presets()


@server.post("/umamusume/add-presets")
def add_preset(req: AddPresetRequest):
    write_preset(req.preset)
    return
