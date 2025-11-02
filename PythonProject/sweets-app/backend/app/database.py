from motor.motor_asyncio import AsyncIOMotorClient
from .config import settings

client: AsyncIOMotorClient | None = None
db = None

async def connect_to_mongo():
    global client, db
    client = AsyncIOMotorClient(settings.MONGO_URL)
    await client.admin.command('ping')
    db = client[settings.MONGO_DB_NAME]

async def close_mongo_connection():
    global client
    client.close()

