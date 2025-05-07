import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
import asyncio
from beanie import init_beanie, Document
import database.models as models_module
import inspect

# Load environment variables
load_dotenv()

DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_CLUSTER = os.getenv("DB_CLUSTER")
DB_NAME = os.getenv("DB_NAME")
APP_NAME = os.getenv("APP_NAME")

# MongoDB URI
MONGO_URI = (
    f"mongodb+srv://{DB_USERNAME}:{DB_PASSWORD}@{DB_CLUSTER}/"
    f"{DB_NAME}?retryWrites=true&w=majority&appName={APP_NAME}"
)

# MongoDB Client
client = AsyncIOMotorClient(
    MONGO_URI
)

def get_connection():
    if not DB_NAME:
        raise EnvironmentError("Environment variable DB_NAME is missing or empty")
    return client[DB_NAME]

async def get_session():
    return await client.start_session()

# Connection Test Function
async def run():
    try:
        await client.admin.command("ping")
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as error:
        print(f"MongoDB connection failed: {error}")
        raise
    finally:
        client.close()

# Connect to MongoDB using Beanie
async def connect_db():
    try:
        await client.admin.command("ping")
        print("MongoDB connected successfully!")
        document_models = [
            member for _, member in inspect.getmembers(models_module)
            if inspect.isclass(member) and issubclass(member, Document) and member is not Document
        ]
        await init_beanie(
            database=client[DB_NAME],
            document_models=document_models  # List all your models here
        )
    except Exception as error:
        print(f"MongoDB connection failed: {error}")
        raise

# Disconnect from MongoDB
async def disconnect_db():
    try:
        client.close()
        print("Disconnected from MongoDB successfully.")
    except Exception as error:
        print(f"Error disconnecting from MongoDB: {error}")
        raise

# Run the ping test on startup
if __name__ == "__main__":
    asyncio.run(run())
    asyncio.run(connect_db())
    asyncio.run(disconnect_db())
