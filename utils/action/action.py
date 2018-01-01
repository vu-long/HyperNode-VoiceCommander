import sys
import os.path
import logging
import json
import time

TOP_DIR = os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir), os.pardir)
UTILS_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)

try:
    import amqp_client as amqp
except ImportError:
    print("File: " + __file__ + " - Import AMQP failed")
    exit()

try:
    sys.path.insert(0, os.path.join(UTILS_DIR, "logger"))
    import logger as log
except ImportError:
    print("File: " + __file__ + " - Import log failed")
    exit()

try:
    sys.path.insert(0, os.path.join(TOP_DIR, "utils/JSON"))
    import json_utils
except ImportError:
    print("File: " + __file__ + " - Import JSON failed")
    exit()


actionStatusList = []
actionTimerList = ["alarm", "time"]
actionLightList = ["smarthome.lights", "lights"]
actionMusicList = ["music", "music_player_control", "video", "video_player_control"]
actionHumidifierList = ["smarthome.humidifier", "smarthome.devices", "humidifier"]
actionList = [actionStatusList, actionTimerList, actionLightList, actionMusicList, actionHumidifierList]
processName = ["status", "timer", "light", "music", "humidifier"]

def ActionManagerProcess(log_q, action_q, cmd_q):
    try:
        logger = log.loggerInit(log_q)
    except Exception as e:
        print("Create logger failed")
        exit()

    logger.log(logging.INFO, "Action Manager Process is started")
    while True:
        # Debug
        # cmdStr = '{"parameters": {"device": "humidifier", "on_off": "on"}, "des": "humidifier", "action": "smarthome.humidifier.hotmist.set"}'
        # cmd_q.put_nowait(cmdStr)
        # time.sleep(10)

        # Release
        try:
            action = action_q.get()
            # action = "{\"action\":\"smarthome.lights.switch.on\"}"
            if action is None:
                # continue
                pass
            else:
                actionStr = json_utils.jsonSimpleParser(action, "action")
                if actionStr is None:
                    logger.log(logging.DEBUG, "actionStr: " + action)
                    continue
                gotIt = False
                for index, item in enumerate(actionList):
                    for i in item:
                        if (str.find(str(actionStr),i) >= 0):
                            gotIt = True
                            break
                    if gotIt is True:
                        break
                if gotIt is True:
                    processTarget = processName[index]
                    logger.log(logging.DEBUG, "Process Target: " + processTarget)
                    logger.log(logging.DEBUG, "Action: " + action)
                    cmdStr = json_utils.jsonDoubleGenerate(json_utils.jsonSimpleGenerate("des",processTarget), action)
                    logger.log(logging.DEBUG, "Cmd Str: " + cmdStr)
                    cmd_q.put_nowait(str(cmdStr))
                else:
                    print("Not found")
        except Exception as e:
            logger.log(logging.ERROR, "Action Manager: Failed to run: exception={})".format(e))
            raise e
