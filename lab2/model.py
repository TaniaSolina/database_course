from view import View

from datetime import datetime

import psycopg2
import psycopg2.extras
from psycopg2.extras import DictCursor


class Model:
    def __init__(self):
        self.view_obj = View()

    def connect(self):
        return psycopg2.connect(dbname='cinema', user='postgres', password='Sqlpr0v0d0k', host='localhost')

    def select_table(self, table_num):
        with self.connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT * FROM \"{self.view_obj.tables[table_num]}\"")
                self.tables_parser_controller(table_num, cursor.fetchall())

    def select_all_tables(self):
        for table_num in range(1, 9):
            self.select_table(table_num)

    def tables_parser_controller(self, table_num, data):
        if table_num == 1:
            self.view_obj.film_genres_parser(data)
        elif table_num == 2:
            self.view_obj.films_parser(data)
        elif table_num == 3:
            self.view_obj.genres_parser(data)
        elif table_num == 4:
            self.view_obj.halls_parser(data)
        elif table_num == 5:
            self.view_obj.prices_parser(data)
        elif table_num == 6:
            self.view_obj.session_parser(data)
        elif table_num == 7:
            self.view_obj.sold_tickets_parser(data)
        elif table_num == 8:
            self.view_obj.technologies_parser(data)

    def get_column_names(self, table_name):
        with self.connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT * FROM \"{table_name}\"")
                return [item[0] for item in cursor.description]

    def get_column_types(self, cursor, table_name):
        cursor.execute(f"""SELECT data_type FROM information_schema.columns
        WHERE table_schema = 'public' AND table_name = '{table_name}'""")
        return [i[0] for i in cursor.fetchall()]

    def data_converter(self, data, column_types):
        return [value
                if _type == 'integer' else "'" + str(value) + "'"
                for value, _type in zip(data, column_types)]

    def insert_into_table(self, table_name, data=()):
        with self.connect() as connection:
            with connection.cursor() as cursor:
                column_names = self.get_column_names(table_name)
                column_names_str = ", ".join(column_names)
                column_types = self.get_column_types(cursor, table_name)
                if not data:
                    data = self.view_obj.input_data(column_names)
                converted_data = self.data_converter(data, column_types)
                new_data_str = ", ".join(converted_data)

                cursor.execute(f"""INSERT INTO \"{table_name}\" ({column_names_str}) VALUES({new_data_str});""")

    def get_last_entry_from_column(self, table_name, column_name, cursor):
        cursor.execute(f"""SELECT {column_name} FROM \"{table_name}\"
        ORDER BY {column_name} DESC LIMIT 1""")
        return cursor.fetchone()[0]

    def generate_random_data(self, cursor, length):
        uppercase_letter = "chr(ascii('A') + (random() * 25)::int)"
        lowercase_letter = "chr(ascii('a') + (random() * 25)::int)"
        cursor.execute(f"""SELECT ({uppercase_letter}{(" || " + lowercase_letter) * (length - 1)})""")
        return cursor.fetchone()[0]

    def insert_random_data_packet(self):
        with self.connect() as connection:
            with connection.cursor() as cursor:
                film_id = self.get_last_entry_from_column('films', 'id', cursor) + 1
                title = self.generate_random_data(cursor, 10)
                producer = self.generate_random_data(cursor, 7)
                self.insert_into_table('films', (str(film_id),
                                                 title,
                                                 producer,
                                                 '2022',
                                                 '25'))

                genre_id = self.get_last_entry_from_column('genres', 'id', cursor) + 1
                genre_name = self.generate_random_data(cursor, 10)
                self.insert_into_table('genres', (str(genre_id),
                                                  genre_name))

                self.insert_into_table('film_genres', (str(film_id),
                                                       str(genre_id)))

                technology_id = self.get_last_entry_from_column('technologies', 'id', cursor) + 1
                technology_name = self.generate_random_data(cursor, 5)
                description = self.generate_random_data(cursor, 15)
                self.insert_into_table('technologies', (str(technology_id),
                                                        technology_name,
                                                        description))

                hall_number = self.get_last_entry_from_column('halls', 'number', cursor) + 1
                self.insert_into_table('halls', (str(hall_number),
                                                 str(technology_id)))

                price_id = self.get_last_entry_from_column('prices', 'id', cursor) + 1
                self.insert_into_table('prices', (str(price_id),
                                                  str(technology_id),
                                                  '100'))

                session_id = self.get_last_entry_from_column('session', 'id', cursor) + 1
                date_time = datetime.now().strftime("%y-%m-%d %H:%M:%S")
                self.insert_into_table('session', (str(session_id),
                                                   str(hall_number),
                                                   str(film_id),
                                                   date_time))

                ticket_id = self.get_last_entry_from_column('sold_tickets', 'id', cursor) + 1
                self.insert_into_table('sold_tickets', (str(ticket_id),
                                                        str(session_id),
                                                        str(ticket_id),
                                                        str(ticket_id)))

    def update_table(self, table_num, data):
        with self.connect() as connection:
            with connection.cursor() as cursor:
                table_name = self.view_obj.tables[table_num]
                column_names = self.get_column_names(table_name)
                id_name = column_names[0]

                for i, column in enumerate(column_names[1:], start=1):
                    cursor.execute(f"""UPDATE \"{table_name}\"
                    SET {column} = '{data[i]}' WHERE {id_name} = {data[0]}""")

    def delete_data(self, table_num, id_to_delete):
        with self.connect() as connection:
            with connection.cursor() as cursor:
                table_name = self.view_obj.tables[table_num]
                cursor.execute(f"SELECT * FROM \"{table_name}\"")
                id_column_name = cursor.description[0][0]

                # begin == first value, end == second value (if it exists)
                # if there is no second value end == begin
                begin, end = id_to_delete[0], id_to_delete[-(len(id_to_delete) - 1)] + 1

                for i in range(begin, end):
                    cursor.execute(f"DELETE FROM \"{table_name}\" WHERE {id_column_name} = {i};")

    def get_column_names_to_view(self, table_num):
        with self.connect() as connection:
            with connection.cursor() as cursor:
                table_name = self.view_obj.tables[table_num]
                return self.get_column_names(table_name)


    def string_search(self, cursor, table_names_list, column_name, data):
        for table in table_names_list:
            cursor.execute(f"""SELECT * FROM \"{table}\" WHERE {column_name} LIKE '{data}'""")
            print("---------------------------------------------------------")
            for i in cursor:
                print(table + ": " + str(i))

    def integer_search(self, cursor, table_names_list, column_name, min_value, max_value):
        for table in table_names_list:
            cursor.execute(f"""SELECT * FROM \"{table}\"
            WHERE {min_value} <= {column_name} AND {column_name} <= {max_value};""")
            print("---------------------------------------------------------")
            for i in cursor:
                print(table + ": " + str(i))

    def date_search(self, cursor, table_names_list, column_name, min_value, max_value):
        for table in table_names_list:
            cursor.execute(f"""SELECT * FROM \"{table}\"
            WHERE {column_name} BETWEEN '{min_value}' AND '{max_value}'""")
            print("---------------------------------------------------------")
            for i in cursor:
                print(table + ": " + str(i))

    def search_controller(self, cursor, table_names_list, column_name, data_type, data):
        print("\n#########################################################")
        print(f"#########\tSearch by '{column_name}' column with {data}")
        if data_type == 'integer':
            self.integer_search(cursor, table_names_list, column_name, *data)
        elif data_type == 'character varying':
            self.string_search(cursor, table_names_list, column_name, data)
        elif data_type == 'timestamp without time zone':
            self.date_search(cursor, table_names_list, column_name, *data)
        print("#########################################################\n\n")


    def search_into_table(self, table_num, search_param):
        with self.connect() as connection:
            with connection.cursor(cursor_factory=DictCursor) as cursor:
                table_name = self.view_obj.tables[table_num]
                column_names = self.get_column_names(table_name)
                column = column_names[search_param]

                cursor.execute(f"""SELECT TABLE_NAME FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE COLUMN_NAME = '{column}'""")
                table_names_list = [item[0] for item in cursor.fetchall()]

                cursor.execute(f"""SELECT * FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_NAME = '{table_name}' AND COLUMN_NAME  = '{column}'""")
                data_type = cursor.fetchone()['data_type']

                data_to_search = self.view_obj.input_data_to_search(data_type)
                self.search_controller(cursor, table_names_list, column, data_type, data_to_search)
