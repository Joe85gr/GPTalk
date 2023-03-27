import json
from abc import ABC, abstractmethod
from logging import Logger
import sqlite3
from sqlite3 import Error as SqliteError
from pydantic import BaseModel
from constants import APP_NAME, CONFIG_PATH


class Chat(BaseModel):
    chat_id: int
    is_active: bool
    content: object


class IDatabase(ABC):
    @abstractmethod
    def add_new_chat(self) -> bool:
        pass

    @abstractmethod
    def get_chat(self, chat_id):
        pass

    @abstractmethod
    def delete_chat(self, chat_id):
        pass

    @abstractmethod
    def get_chats(self):
        pass

    @abstractmethod
    def update_chat(self, chat_id, content) -> bool:
        pass


class Sqlite(IDatabase):
    def __init__(self, logger: Logger, sqlite: sqlite3):
        self.logger = logger
        self.sqlite = sqlite
        self.__initialise()

    def __initialise(self) -> None:
        self.logger.debug("Initialising database..")
        try:
            with self.sqlite.connect(f"{CONFIG_PATH}/{APP_NAME}.db") as con:
                cur = con.cursor()

                cur.execute(""" CREATE TABLE IF NOT EXISTS chats (
                                    chat_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, 
                                    is_active TEXT,
                                    content BLOB);
                            """)
                con.commit()
                self.logger.debug("Database initialised successfully!")
        except SqliteError as e:
            self.logger.error(e)

    def add_new_chat(self) -> str:
        try:
            with self.sqlite.connect(f"{CONFIG_PATH}/{APP_NAME}.db") as con:
                cur = con.cursor()
                is_active = True
                data = (is_active, "",)
                cur.execute(f""" INSERT INTO chats (is_active,content)
                                    VALUES (?,?)
                            """, data)
                con.commit()

                return cur.lastrowid
        except SqliteError as e:
            con.rollback()
            self.logger.error(e)

            return "error"

    def get_chat(self, chat_id):
        try:
            with self.sqlite.connect(f"{CONFIG_PATH}/{APP_NAME}.db") as con:
                cur = con.cursor()
                data = (chat_id,)
                cur.execute(f""" SELECT content
                                 FROM chats
                                 WHERE chat_id = ?
                            """, data)
                content = cur.fetchone()

                if content is None:
                    return None
                return content[0]
        except SqliteError as e:
            con.rollback()
            self.logger.error(e)

            return "error"

    def delete_chat(self, chat_id):
        try:
            with self.sqlite.connect(f"{CONFIG_PATH}/{APP_NAME}.db") as con:
                cur = con.cursor()
                data = (chat_id,)
                a = cur.execute(f""" DELETE
                                 FROM chats
                                 WHERE chat_id = ?
                            """, data)
                con.commit()

                return cur.rowcount == 1
        except SqliteError as e:
            con.rollback()
            self.logger.error(e)

            return False

    def get_chats(self):
        try:
            with self.sqlite.connect(f"{CONFIG_PATH}/{APP_NAME}.db") as con:
                cur = con.cursor()
                cur.execute(f""" SELECT content
                                 FROM chats
                                 WHERE content != ''
                                 and content IS NOT NULL
                            """)
                content = cur.fetchall()

                if content is None:
                    return None
                data = [row[0] for row in content]
                return data
        except SqliteError as e:
            con.rollback()
            self.logger.error(e)

            return "error"

    def update_chat(self, chat_id, content) -> bool:
        try:
            with self.sqlite.connect(f"{CONFIG_PATH}/{APP_NAME}.db") as con:
                cur = con.cursor()
                data = (content, chat_id,)
                cur.execute(f""" UPDATE chats 
                                 SET content = ?
                                 WHERE chat_id = ?
                            """, data)

                con.commit()

                return True
        except SqliteError as e:
            con.rollback()
            self.logger.error(e)

            return False
