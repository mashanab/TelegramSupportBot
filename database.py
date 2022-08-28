import sqlite3

from config import DB


class RequestsDb:
    def __init__(self):
        self.connection = sqlite3.connect(DB)
        self.cursor = self.connection.cursor()

    def create_database(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS communication (id_message_stuff INTEGER, "
                            "name_client TEXT, id_client INTEGER)")
        self.connection.commit()

    def add_request(self, id_message_stuff, name_client, id_client):
        self.cursor.execute("INSERT INTO communication VALUES (?, ?, ?)", (id_message_stuff,
                                                                           name_client, id_client))
        self.connection.commit()

    def find_name_client_for_request(self, id_message_stuff) -> tuple:
        rows = self.cursor.execute("SELECT id_message_stuff, name_client, id_client FROM communication "
                                   "WHERE id_message_stuff = ?",
                                   (id_message_stuff,)).fetchall()
        self.connection.commit()
        name_client, id_client = rows[0][1], rows[0][2]
        return name_client, id_client

    def existence_request(self, id_message_stuff) -> bool:
        rows = self.cursor.execute("SELECT id_message_stuff, name_client, id_client FROM communication "
                                   "WHERE id_message_stuff = ?",
                                   (id_message_stuff,)).fetchall()
        self.connection.commit()
        if len(rows) != 0:
            return True
        return False

    def remove_request(self, id_message_stuff):
        self.cursor.execute("DELETE FROM communication WHERE id_message_stuff = ?", (id_message_stuff,))
        self.connection.commit()

    def close_connection(self):
        self.cursor.close()
        self.connection.close()

    def delete_table(self):
        self.cursor.execute("DROP TABLE IF EXISTS communication")
        self.connection.commit()
