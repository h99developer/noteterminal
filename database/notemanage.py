from database.databasemain import connectdb
import aiosqlite


async def getnotes() -> list or None:
    """
    Функция возвращает все заметки, которые есть в базе данных
    """
    notes = []

    db, sql = await connectdb()

    await sql.execute("SELECT * FROM notes")
    result = await sql.fetchall()

    await db.close()

    if result is not None:
    
        for note in result:
            notes.append(
                {
                    "note_id": note[0],
                    "note_title": note[1],
                    "note_description": note[2]
                }
            )

        return notes
    else:
        return None

async def searchnote(keyword: str) -> list or None:
    """
    Функция для поиска заметок с помощью ключевого слова
    """
    db, sql = await connectdb()

    await sql.execute("SELECT note_id, note_title FROM notes WHERE note_title LIKE ? OR note_description LIKE ?", (f"%{keyword}%", f"%{keyword}%"))
    result = await sql.fetchall()
    
    await db.close()
    notes_id = []
    if result is not None:
        for note in result:
            notes_id.append({"note_id": note[0], "note_title": note[1]})

        return notes_id
    
    else:
        return None

class Note:

    """
    Класс, отвечающий за управлением заметками
    """

    def __init__(self, note_id: int = None):
        self.note_id = note_id

    async def create(self, note_title: str, note_description: str) -> int:

        """
        Функция создания заметки
        """

        db, sql = await connectdb()

        await sql.execute("INSERT INTO notes VALUES (NULL, ?, ?)", (str(note_title), str(note_description),))

        self.note_id = sql.lastrowid

        await db.commit()
        await db.close()

    async def delete(self) -> bool:

        """
        Функция удаления заметки
        """

        if self.note_id is not None:
            db, sql = await connectdb()

            await sql.execute("DELETE FROM notes WHERE note_id = ?", (self.note_id,))

            await db.commit()
            await db.close()

            return True
        else:
            return False
        
    async def get(self) -> dict:

        """
        Функция для получения информации о заметки (ид заметки, заголовок заметки, содержание заметки)
        """

        if self.note_id is not None:
            db, sql = await connectdb()

            await sql.execute("SELECT * FROM notes WHERE note_id = ?", (self.note_id,))
            note = await sql.fetchone()
            await db.close()

            if note is not None:
                data = {
                    "note_id": note[0],
                    "note_title": note[1],
                    "note_description": note[2]
                }

                return dict(data)
            
            else:
                return None
        else:
            return None
        

    

                