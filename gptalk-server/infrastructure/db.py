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
    def add_new_chat(self, content) -> bool:
        pass

    @abstractmethod
    def get_chat(self, chat_id):
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

    def add_new_chat(self, content) -> str:
        try:
            with self.sqlite.connect(f"{CONFIG_PATH}/{APP_NAME}.db") as con:
                cur = con.cursor()
                is_active = True
                data = (is_active, content,)
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
                content = cur.fetchone()[0]
                return json.loads(content)
        except SqliteError as e:
            con.rollback()
            self.logger.error(e)

            return "error"

    # def get_all_chat_ids(self) -> list:
    #     try:
    #         with self.sqlite.connect(f"{CONFIG_PATH}/{APP_NAME}.db") as con:
    #             cur = con.cursor()
    #             cur.execute("""SELECT chat_id FROM chats""")
    #             results = cur.fetchall()
    #
    #             return results
    #
    #     except SqliteError as e:
    #         self.logger.error(e)
    #         return []

    # def get_chat_ids(self, is_active: bool) -> list:
    #     try:
    #         with self.sqlite.connect(f"{CONFIG_PATH}/{APP_NAME}.db") as con:
    #             cur = con.cursor()
    #             data = (is_active,)
    #             cur.execute("""SELECT chat_id
    #                             FROM chats
    #                             WHERE is_active = ?
    #                         """, data)
    #             results = cur.fetchall()
    #
    #             return results
    #
    #     except SqliteError as e:
    #         self.logger.error(e)
    #         return []

    # def add_new_chat(self, content) -> bool:
    #     try:
    #         with self.sqlite.connect(f"{CONFIG_PATH}/{APP_NAME}.db") as con:
    #             cur = con.cursor()
    #             is_active = True
    #             data = (is_active, content,)
    #             cur.execute(f""" INSERT INTO chats (is_active,content)
    #                                 VALUES (?,?)
    #                         """, data)
    #             con.commit()
    #
    #             return True
    #     except SqliteError as e:
    #         con.rollback()
    #         self.logger.error(e)
    #
    #         return False

    # def get_chat(self, chat_id) -> Chat | None:
    #     try:
    #         with self.sqlite.connect(f"{CONFIG_PATH}/{APP_NAME}.db") as con:
    #             cur = con.cursor()
    #             data = (chat_id,)
    #             cur.execute("""SELECT chat_id, is_active, content
    #                             FROM chats
    #                             WHERE chat_id = ?
    #                         """, data)
    #             result = cur.fetchall()[0]
    #             chat = Chat(chat_id=result[0], is_active=result[1], content=result[2])
    #
    #             return chat
    #
    #     except SqliteError as e:
    #         self.logger.error(e)
    #         return None

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
