import os

env = os.getenv("ENV", "PROD")

if env == "DEV":
    MONGO_URL = "mongodb://127.0.0.1:27017"
else:
    MONGO_URL = "mongodb://<username>:<password>@portal-ssl723-0.intrepid-mongodb-51.794609107.composedb.com:16817,portal-ssl831-1.intrepid-mongodb-51.794609107.composedb.com:16817/compose?authSource=admin&ssl=true"