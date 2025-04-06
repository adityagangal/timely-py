from .config import get_connection
from contextlib import asynccontextmanager

@asynccontextmanager
async def transaction():
    client = get_connection().client
    session = await client.start_session()
    session.start_transaction()
    try:
        yield session
        await session.commit_transaction()
    except Exception as e:
        await session.abort_transaction()
        raise e
    finally:
        session.end_session()

