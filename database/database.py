import aiosqlite
import functools
from pathlib import Path
PROJECT_ROOT = Path(__file__).parent.parent
DB_PATH = PROJECT_ROOT / 'data' / 'bot.db'
print(DB_PATH)
DB_DIR = PROJECT_ROOT / 'data'
DB_DIR.mkdir(parents=True, exist_ok=True)

async def init_db():
    """
    База данных состоит из трех таблиц. Отношение многие ко многие.
    Users из типичных полей имеет поле status, которое определяет доступ к подпискам
    При запросе на подключение ему ставится статус pending,
    потом админ одобрит или отклонит и статус меняется соответствующе.
    Таблица subscribes описывает сами подписки с их id
    И таблица subscribes_users объединяет id подписки с user_id из users (не id записи в таблице users!)
    :return:
    """
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("PRAGMA foreign_keys = ON;")
        await db.commit()
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
        await db.execute("""
            CREATE TABLE IF NOT EXISTS subscribes_users (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                subscribe_id INTEGER,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
                FOREIGN KEY (subscribe_id) REFERENCES subscribes(id) ON DELETE CASCADE      
            )
            """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS subscribes (
                id INTEGER PRIMARY KEY,
                name TEXT
            )
            """)
        await db.commit()


async def add_user(user_id: int, first_name: str, last_name: str, username: str, status = 'pending'):
    """
    Берет из updates информацию по юзеру и добавляет его в таблицу.
    :param status:
    :param user_id:
    :param first_name:
    :param last_name:
    :param username:
    :return:
    """
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT OR IGNORE INTO users (user_id, first_name, last_name, username, status)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, first_name, last_name, username, status))
        await db.commit()

async def update_user_status(user_id: int, status: str):
    """
    Меняет статус после проверки админом
    :param user_id:
    :param status:
    :return:
    """
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            UPDATE users SET status = ? WHERE user_id = ?
        """, (status, user_id))
        await db.commit()

async def get_user(user_id: int):
    """
    Берет запись по определенному юзеру
    :param user_id:
    :return:
    """
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)) as cursor:
            return await cursor.fetchone()

async def get_users_id(subscribe):
    """
    Берет только user_id всех пользователей БД (для рассылки)
    :return:
    """
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("""
        SELECT users.user_id
        FROM users INNER JOIN subscribes_users ON users.user_id = subscribes_users.user_id
        INNER JOIN subscribes ON subscribes_users.subscribe_id = subscribes.id
        WHERE subscribes.name = (?)""", (subscribe,)) as cursor:
            users = await cursor.fetchall()
            return [user[0] for user in users]

async def get_users() -> tuple:
    """
    Берет всю информацию по всем юзерам из БД (для админа)
    :return:
    """
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT user_id, first_name, last_name, username, status FROM users") as cursor:
            users = await cursor.fetchall()
            return users

async def add_subscribe(name: str):
    """
    Добавляет подписку. Доступно только админку
    :param name:
    :return:
    """
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT OR IGNORE INTO subscribes (name) VALUES (?) 
            """, (name,))
        await db.commit()

async def get_subscribes() -> list:
    """
    Берет список подписок. (для инлайн клавиатуры пользователю)
    :return:
    """
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT name FROM subscribes") as cursor:
            subscribes = await cursor.fetchall()
            return [subscribe[0] for subscribe in subscribes]

async def get_user_subscribes(user_id) -> list:
    """
    Берет подписки, на которые пользователь уже подписался
    :param user_id:
    :return:
    """
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("""
        SELECT subscribes.name 
        FROM subscribes INNER JOIN subscribes_users ON subscribes.id = subscribes_users.subscribe_id
        INNER JOIN users ON users.user_id = subscribes_users.user_id 
        WHERE users.user_id = (?)""", (user_id,)) as cursor:
            user_subscribes = await cursor.fetchall()
            return [user_subscribe[0] for user_subscribe in user_subscribes]


async def add_user_subscribe(user_id: int, subscribe: str):
    """
    Добавляет подписку пользователем
    :param user_id:
    :param subscribe:
    :return:
    """
    async with aiosqlite.connect(DB_PATH) as db:
        subscribe_id = await db.execute("""
        SELECT id FROM subscribes WHERE name = ?""", (subscribe,))
        print(f'subscribe_id in db: {subscribe_id}')
        sub_id = await subscribe_id.fetchone()
        await db.execute("""
        INSERT INTO subscribes_users (user_id, subscribe_id)
        VALUES (?, ?)""", (user_id, sub_id[0]))
        await db.commit()


async def delete_user_subscribe(user_id: int, subscribe: str):
    """
    Удаляет подписку пользователем
    :param user_id:
    :param subscribe:
    :return:
    """
    async with aiosqlite.connect(DB_PATH) as db:
        subscribe_id = await db.execute("""
                     SELECT id FROM subscribes WHERE name = ?""", (subscribe,))
        sub_id = await subscribe_id.fetchone()
        await db.execute("""
        DELETE FROM subscribes_users WHERE user_id = ? AND subscribe_id = ?""", (user_id, sub_id[0]))

        await db.commit()

async def check_user_status(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT status FROM users WHERE user_id = ?", (user_id,)) as cursor:
            status = await cursor.fetchone()
            return status[0]

async def delete_user(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("PRAGMA foreign_keys = ON;")
        await db.commit()
        await db.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        await db.commit()
        print(f'{user_id} удалён с подписками')


