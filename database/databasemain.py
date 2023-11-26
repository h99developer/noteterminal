import aiosqlite

async def connectdb() -> aiosqlite.connect:
    """Функция возвращает соединение с базой данных и курсор"""

    db = await aiosqlite.connect('database/base.db')
    sql = await db.cursor()

    return db, sql


async def createtables():
    """Функция создания таблиц"""

    db, sql = await connectdb()

    await sql.execute("""CREATE TABLE IF NOT EXISTS notes (
        note_id INTEGER PRIMARY KEY AUTOINCREMENT,
        note_title TEXT,
        note_description TEXT
    )""")

    await db.commit()
    await db.close()