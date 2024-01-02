from databases import Database

DATABASE_URL = "sqlite:///./test.db"

database = Database(DATABASE_URL)

create_table_query = """
CREATE TABLE IF NOT EXISTS chat_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER,
    message TEXT,
    bot_reply TEXT
);
"""

async def connect_db():
    await database.connect()
    await database.execute(create_table_query)

async def disconnect_db():
    await database.disconnect()

def get_database():
    return database