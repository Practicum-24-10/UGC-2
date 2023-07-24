import motor.motor_asyncio

mongo: motor.motor_asyncio.AsyncIOMotorClient | None = None


async def get_mongo():
    return mongo
