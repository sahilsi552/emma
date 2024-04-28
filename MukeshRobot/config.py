
class Config(object):
    LOGGER = True
    # REQUIRED
    # Login to https://my.telegram.org and fill in these slots with the details given by it

    API_ID = "3595472" # integer value, dont use ""
    API_HASH = "1e1f25564047e2994d35ef7785ab6f04"
    TOKEN = "6891573695:AAHQG-Xj99KlzEZzO42Pfn4svUjZU-oOSgk"  # This var used to be API_KEY but it is now TOKEN, adjust accordingly.
    OWNER_ID = "6828102589" # If you dont know, run the bot and do /id in your private chat with it, also an integer
    
    SUPPORT_CHAT = "tyrosupport"  # Your own group for support, do not add the @
    START_IMG = "https://telegra.ph/file/000625ad0b270aaea4ec6.jpg"
    EVENT_LOGS = ()  # Prints information like gbans, sudo promotes, AI enabled disable states that may help in debugging and shit
    MONGO_DB_URI= "mongodb+srv://Mukesh01:mstboy@cluster0.8jwzl.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    # RECOMMENDED
    DATABASE_URL = "postgres://iadhvjopgtomul:4883b7456515dffbbea0b9e626bd06dbd33cdabfaaa6d1f5117d08c94ff777d6@ec2-18-206-103-49.compute-1.amazonaws.com:5432/dfh9hnujmva3kj"  # A sql database url from elephantsql.com
    CASH_API_KEY = (
        ""  # Get your API key from https://www.alphavantage.co/support/#api-key
    )
    TIME_API_KEY = ""
    
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
