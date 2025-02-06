import aiosqlite

class Database:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    async def create(cls, db_path):
        instance = cls()
        instance.conn = await aiosqlite.connect(db_path)
        await instance._init_db()
        return instance

    async def _init_db(self):
        """Initialize database schema."""
        await self.conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                points INTEGER DEFAULT 0,
                submissions INTEGER DEFAULT 0,
                last_submission DATE
            )
        ''')
        await self.conn.execute('''
            CREATE TABLE IF NOT EXISTS submissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                points INTEGER,
                submission_date DATE
            )
        ''')
        await self.conn.execute('''
            CREATE TABLE IF NOT EXISTS archived_submissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                points INTEGER,
                submission_date DATE
            )
        ''')
        await self.conn.commit()

    async def execute(self, query, *args):
        cursor = await self.conn.execute(query, args)
        await self.conn.commit()
        return cursor

    async def fetchone(self, query, *args):
        cursor = await self.conn.execute(query, args)
        return await cursor.fetchone()

    async def fetchall(self, query, *args):
        cursor = await self.conn.execute(query, args)
        return await cursor.fetchall()
