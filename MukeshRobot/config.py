
class Config(object):
    LOGGER = True

    API_ID = "3595472" 
    API_HASH = "1e1f25564047e2994d35ef7785ab6f04"
    TOKEN = "7178343344:AAE-gvFvekF-8l1gRTQaD6KxyKgf289vqlw"  
    OWNER_ID = 6828102589 
    
    SUPPORT_CHAT = "tyrosupport"  
    START_IMG = "https://telegra.ph/file/000625ad0b270aaea4ec6.jpg"
    EVENT_LOGS = (-1002050675293)  
    MONGO_DB_URI = "mongodb+srv://Mukesh01:mstboy@cluster0.8jwzl.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
   
    DATABASE_URL = "postgres://iadhvjopgtomul:4883b7456515dffbbea0b9e626bd06dbd33cdabfaaa6d1f5117d08c94ff777d6@ec2-18-206-103-49.compute-1.amazonaws.com:5432/dfh9hnujmva3kj"  
    CASH_API_KEY = (TCOVLTKUMVPOCWXO)
    TIME_API_KEY = "MSATXGNOJ0GQ"
    
    # Get your API key from https://timezonedb.com/api


    # Optional fields
    BL_CHATS = []  # List of groups that you want blacklisted.
    DRAGONS = []  # User id of sudo users
    DEV_USERS = []  # User id of dev users
    DEMONS = []  # User id of support users
    TIGERS = []  # User id of tiger users
    WOLVES = []  # User id of whitelist users

    ALLOW_CHATS = True
    ALLOW_EXCL = True
    DEL_CMDS = True
    INFOPIC = True
    LOAD = []
    NO_LOAD = []
    STRICT_GBAN = True
    TEMP_DOWNLOAD_DIRECTORY = "./"
    WORKERS = 8
    

class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True
