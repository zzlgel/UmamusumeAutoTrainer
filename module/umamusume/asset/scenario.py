import csv
import os.path

from bot.base.resource import Template


SCENARIO_LIST: list[list] = []
UMAMUSUME_SCENARIO_TEMPLATE_PATH = "/umamusume/scenario"


def load_scenario_data():
    for i in range(100):
        SCENARIO_LIST.append([])
    with open('resource/umamusume/data/scenario.csv', 'r', encoding="utf-8") as file:
        reader = csv.reader(file)
        for row in reader:
            scenario_id = row[0]
            path = "resource" + UMAMUSUME_SCENARIO_TEMPLATE_PATH + "/" + str(scenario_id)+".png"
            if os.path.isfile(path):
                t = Template(str(scenario_id), UMAMUSUME_SCENARIO_TEMPLATE_PATH)
                scenario_name = row[1]
                scenario_info = [scenario_id, scenario_name, t]
                SCENARIO_LIST[int(scenario_id)] = scenario_info


load_scenario_data()
