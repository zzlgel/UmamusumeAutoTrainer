from fastapi import APIRouter

from module.umamusume.protocol.preset import AddPresetRequest
from module.umamusume.user_data import read_presets, write_preset

router = APIRouter(prefix="/umamusume", tags=["umamusume"])


# 从这里开始，是一个简单的接口，用于读取和写入预设
@router.post("/get-presets")
def get_presets():
    return read_presets()


@router.post("/add-presets")
def add_preset(req: AddPresetRequest):
    write_preset(req.preset)
    return
