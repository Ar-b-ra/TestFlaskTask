import sqlite3
from pathlib import Path
from src.config import DATABASE_DIR


class DatabaseWorker:

    @staticmethod
    def get_db_by_name(db_name: str | int) -> Path:
        return (Path(DATABASE_DIR) / f"database_{db_name}").with_suffix('.db')

    @classmethod
    def execute_query(cls, db_number: str | int, query: str) -> any:
        db = cls.get_db_by_name(db_number)
        try:
            with sqlite3.connect(db) as conn:
                cursor = conn.cursor()
                cursor.execute(query)
                # Если запрос изменяет данные, фиксируем изменения
                if query.strip().lower().startswith(("insert", "update", "delete", "create", "alter")):
                    conn.commit()
                    result = {"message": "Query executed successfully"}
                else:
                    # Если запрос возвращает данные, получаем их
                    result = cursor.fetchall()
            
        except sqlite3.Error as e:
            result = {"error": str(e)}
        
        finally:
            conn.close()
        
        return result
        