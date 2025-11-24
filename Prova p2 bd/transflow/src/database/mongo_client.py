import os
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = os.getenv('MONGO_URL', 'mongodb://mongo:27017')

class MongoDB:
    client = None
    db = None

    @classmethod
    def init(cls):
        if cls.client is None:
            cls.client = AsyncIOMotorClient(MONGO_URL)
            cls.db = cls.client['transflow_db']
        return cls.db

db = MongoDB.init()
corridas_collection = db.get_collection('corridas')
