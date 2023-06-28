import os
import psycopg2
from dotenv import load_dotenv
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

FIXTURES = [
    (5724849259, "Купить продукты", "Овощи, фрукты, хлеб"),
    (5724849259, "Оплатить кварплату", "за Март"),
    (5724849259, "Купить билет", "в Дубаи на Апрель"),
    (5724849259, "Шашлыки", "Обзвонить друзей и собраться на шашлыки"),
    (5724849259, "ТО машины", "Пройти ТО до Ноября"),
]

load_dotenv()
PS_NAME = os.getenv('DB_NAME', default="postgres_db")
PS_USER = os.getenv('POSTGRES_USER', default="postgres")
PS_PASSWORD = os.getenv('POSTGRES_PASSWORD', default="lol123pop")
PS_HOST = os.getenv('DB_HOST', default="localhost")
PS_PORT = os.getenv('DB_PORT', default="5432")


def create_db():
    try:
        connection = psycopg2.connect(dbname=PS_NAME,
                                      user=PS_USER,
                                      password=PS_PASSWORD,
                                      host=PS_HOST,
                                      port=PS_PORT,
                                      )
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        cursor = connection.cursor()
        sql_create_database = 'create database postgres_db'
        cursor.execute(sql_create_database)

    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")


class Task:

    def __init__(self):
        # подключение к базе данных
        self.connection = psycopg2.connect(dbname=PS_NAME,
                                           user=PS_USER,
                                           password=PS_PASSWORD,
                                           host=PS_HOST,
                                           port=PS_PORT)
        self.cursor = self.connection.cursor()

    def __beautify_response(self, rows):
        statuses = []
        ids = []
        result = []
        for row in rows:
            ids.append(row[0])
            statuses.append(row[4])
            result.append(
                f"{' '*40}Задача №{row[0]}\n\n"
                f"Заголовок: {row[2]}\n"
                f"Описание: {row[3]}\n"
                f"Статус: {'💼 Не выполнена' if row[4] == 0 else '✅ Выполнена'}"
            )
        return ids, statuses, result

    # создание таблиц
    def create_table_tasks(self):
        with self.connection:
            query = "CREATE TABLE tasks ( "\
                    "id SERIAL PRIMARY KEY NOT NULL, "\
                    "user_id bigint NOT NULL, "\
                    "title TEXT NOT NULL, "\
                    "description TEXT NOT NULL, "\
                    "status INTEGER NOT NULL DEFAULT (0));"
            self.cursor.execute(query)
            self.connection.commit()

    # создание фикстур
    def fixtures_tasks(self):
        with self.connection:
            for data in FIXTURES:
                self.cursor.execute(
                    "INSERT INTO public.tasks(user_id, title, description) \
                                        VALUES(%s, %s, %s);",
                    (data[0], data[1], data[2]))
            self.connection.commit()

    def create_task(self, data):
        with self.connection:
            query = "INSERT INTO public.tasks("\
                    "user_id, title, description)"\
                    "VALUES (%s, %s, %s);"
            self.cursor.execute(query,
                                (data["user_id"], data["title"], data["desc"]))
            self.connection.commit()

    def get_tasks(self, user_id):
        with self.connection:
            query = "SELECT * FROM public.tasks WHERE user_id = %s ORDER BY id"
            self.cursor.execute(query, (user_id,))
            res = self.__beautify_response(self.cursor.fetchall())
            return res

    def get_task(self, user_id):
        with self.connection:
            query = "SELECT * \
                    FROM public.tasks \
                    WHERE user_id = %s \
                    ORDER BY id DESC \
                    LIMIT 1;"
            self.cursor.execute(query, (user_id,))
            res = self.__beautify_response(self.cursor.fetchall())
            return res

    def update_status(self, user_id, task_id):
        with self.connection:
            query = "UPDATE public.tasks "\
                    "SET status=1 "\
                    "WHERE user_id = %s and id = %s;"
            self.cursor.execute(query, (user_id, task_id))
            self.connection.commit()

    def delete_task(self, user_id, task_id):
        with self.connection:
            query = "DELETE FROM public.tasks \
                     WHERE user_id = %s and id = %s;"
            self.cursor.execute(query, (user_id, task_id))
            self.connection.commit()

if __name__ == '__main__':
    # create_db()
    obj = Task()
    obj.fixtures_tasks()
