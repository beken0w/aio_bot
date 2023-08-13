import os
import psycopg2
import logging

from dotenv import load_dotenv

load_dotenv()
PS_NAME = os.getenv('DB_NAME', default="postgres_db")
PS_USER = os.getenv('POSTGRES_USER', default="postgres")
PS_PASSWORD = os.getenv('POSTGRES_PASSWORD', default="lol123pop")
PS_HOST = os.getenv('DB_HOST', default="localhost")
PS_PORT = os.getenv('DB_PORT', default="5432")

logger = logging.getLogger(__name__)


class Category:

    def __init__(self):
        # подключение к базе данных
        self.connection = psycopg2.connect(dbname=PS_NAME,
                                           user=PS_USER,
                                           password=PS_PASSWORD,
                                           host=PS_HOST,
                                           port=PS_PORT)
        self.cursor = self.connection.cursor()

    def create_table_category(self):
        with self.connection:
            query = "CREATE TABLE category ( "\
                    "id SERIAL PRIMARY KEY NOT NULL, "\
                    "user_id bigint NOT NULL, "\
                    "title TEXT NOT NULL)"
            self.cursor.execute(query)
            self.connection.commit()

    def create_category(self, data):
        with self.connection:
            query = "INSERT INTO public.category("\
                    "user_id, title)"\
                    "VALUES (%s, %s);"
            self.cursor.execute(query,
                                (data["user_id"],
                                 data["new_title"]))
            self.connection.commit()

    def get_category(self, data):
        # [(1, 12321312123, 'New Category')]
        with self.connection:
            query = "SELECT * FROM public.category "\
                    "WHERE user_id = %s and title = %s"
            self.cursor.execute(query, (data["user_id"],
                                        data["new_title"]))
            res = self.cursor.fetchall()
            return res

    def is_exist(self, user_id, ctgr_id):
        with self.connection:
            query = 'SELECT title from public.category '\
                    'where user_id = %s and id = %s;'
            self.cursor.execute(query, (user_id, ctgr_id))
            res = self.cursor.fetchone()
            return res

    def get_all_categories(self, user_id):
        # [(1, 12321312123, 'New Category'), (2, 12321312123, 'ANother')]
        with self.connection:
            query = "SELECT * FROM public.category "\
                    "WHERE user_id = %s ORDER BY id"
            self.cursor.execute(query, (user_id,))
            res = self.cursor.fetchall()
            logger.info("Получаем все категории")
            return res

    def update_title(self, data):
        with self.connection:
            query = "UPDATE public.category "\
                    "SET title=%s "\
                    "WHERE user_id = %s and title = %s;"
            self.cursor.execute(query,
                                (data["new_title"],
                                 data["user_id"],
                                 data["old_title"]))
            self.connection.commit()

    def delete_category(self, user_id, ctgr_id):
        with self.connection:
            query = "DELETE FROM public.category \
                     WHERE user_id = %s and id = %s;"
            try:
                self.cursor.execute(query,
                                    (user_id, ctgr_id))
                self.connection.commit()
                logging.error("TEST:")
            except Exception as e:
                logging.error(f"Ошибка: {e}")


if __name__ == '__main__':
    print(Category().get_all_categories('12321312123'))
    # Category().create_category({'user_id': '12321312123', 'title': 'ANother'})
    print(Category().get_category({'user_id': '12321312123', 'title': 'New Category'}))
