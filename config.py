from decouple import config

try:
    APP_ID = 29426486
    API_HASH = config("API_HASH", default="d71ad4ec048ab41677a1a439b21ff0c9")
    BOT_TOKEN = "7355006985:AAEY8ijg4CP-8GgcliRGJja87Tby78QT7To"
    OWNER = 5976437467
    CHAT = 5976437467
except Exception as e:
    LOGS.info("Environment vars Missing")
    LOGS.info("something went wrong")
    LOGS.info(str(e))
    exit()
