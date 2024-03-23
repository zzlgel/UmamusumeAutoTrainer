import csv
import os.path

from bot.base.resource import Template
from module.umamusume.asset import REF_SUITABLE_RACE

RACE_LIST: list[list] = []
UMAMUSUME_RACE_TEMPLATE_PATH = "/umamusume/race"
UMAMUSUME_RACE_DATA_PATH = "resource/umamusume/data/race.csv"


def load_race_data():
    # 以空间换便利
    for i in range(10000):
        RACE_LIST.append([])
    with open(UMAMUSUME_RACE_DATA_PATH, 'r', encoding="utf-8") as file:
        reader = csv.reader(file)
        for row in reader:
            race_id = row[1]
            path = "resource" + UMAMUSUME_RACE_TEMPLATE_PATH + "/" + str(race_id)+".png"
            if os.path.isfile(path):
                t = Template(str(race_id), UMAMUSUME_RACE_TEMPLATE_PATH)
                race_name = row[3]
                race_info = [race_id, race_name, t]
                RACE_LIST[int(race_id)] = race_info
    RACE_LIST[0] = [0, "suitable", REF_SUITABLE_RACE]


load_race_data()


