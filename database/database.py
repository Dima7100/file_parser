import aiosqlite

async def init_db():
    async with aiosqlite.connect("../data/users.db") as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                user_id INTEGER UNIQUE,
                first_name TEXT,
                last_name TEXT,
                username TEXT,
                status TEXT DEFAULT 'pending'
            )
        """)
        await db.commit()

async def add_user(user_id: str, first_name: str, last_name: str, username: str):
    async with aiosqlite.connect("../data/users.db") as db:
        await db.execute("""
            INSERT OR IGNORE INTO users (user_id, first_name, last_name, username)
            VALUES (?, ?, ?, ?)
        """, (user_id, first_name, last_name, username))
        await db.commit()

async def update_user_status(user_id: str, status: str):
    async with aiosqlite.connect("../data/users.db") as db:
        await db.execute("""
            UPDATE users SET status = ? WHERE user_id = ?
        """, (status, user_id))
        await db.commit()

async def get_user(user_id: str):
    async with aiosqlite.connect("../data/users.db") as db:
        async with db.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)) as cursor:
            return await cursor.fetchone()

# надо ещё проверить возвращает ли всех
async def get_users_id():
    async with aiosqlite.connect("../data/users.db") as db:
        async with db.execute("SELECT user_id FROM users WHERE status='approved'") as cursor:
            users = await cursor.fetchall()
            return [user[0] for user in users]