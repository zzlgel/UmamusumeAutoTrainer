from module.umamusume.context import UmamusumeContext
import bot.base.log as logger

log = logger.get_logger(__name__)

REGISTER_PARSE = {}

# 提供根据不同剧本注册方法的模式？TODO 谁注册，谁使用呢？
def register(ctx: UmamusumeContext, func: callable):
    scenario_type = UmamusumeContext.cultivate_detail.scenario
    if(REGISTER_PARSE.get(scenario_type)) == None:
        REGISTER_PARSE.setdefault(scenario_type, [])
    REGISTER_PARSE[scenario_type].append(func)