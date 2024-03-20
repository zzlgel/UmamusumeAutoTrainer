import yaml
import bot.base.log as logger

log = logger.get_logger(__name__)


# Config 配置
class Config(dict):
    # __getattr__ 通过属性访问配置
    def __getattr__(self, key):
        # 通过属性访问配置
        value = self.get(key, None)
        # 如果value是字典类型，递归调用Config
        if isinstance(value, dict):
            value = Config(value)
        return value


# load 加载配置
def load() -> Config:
    # 读取配置文件
    config_file = open("config.yaml", 'r', encoding='utf-8')
    config = config_file.read()
    return Config(yaml.load(config, yaml.FullLoader))


CONFIG = load()
