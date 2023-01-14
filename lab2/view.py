class View:
    __operations_menu = """
+------------------------------+
| Select operation:            |
+------------------------------+
|   1: Show table              |
|   2: Show all tables         |
|   3: Add data                |
|   4: Update data             |
|   5: Delete data             |
|   6: Add random packed data  |
|   7: Search                  |
|   8: Exit the program        |
+------------------------------+
"""

    __tables_menu = """
+--------------------------+
| Select a table:          |
+--------------------------+
|	1: "film_genres"       |
|	2: "films"             |
|	3: "genres"            |
|	4: "halls"             |
|	5: "prices"            |
|	6: "session"           |
|	7: "sold_tickets"      |
|	8: "technologies"      |
+--------------------------+
"""

    def __init__(self):
        self.tables = {
            1: 'film_genres',
            2: 'films',
            3: 'genres',
            4: 'halls',
            5: 'prices',
            6: 'session',
            7: 'sold_tickets',
            8: 'technologies',
            # 9: 'Exit the program',
        }

    def input_choice(self, func, end):
        choice = int(input("Enter choice № "))
        if end < choice < 1:
            print(f"Enter the number from 1 to {end}")
            return func()
        return choice

    def operations_menu(self):
        print(self.__operations_menu)
        return self.input_choice(self.operations_menu, 7)

    def tables_menu(self):
        print(self.__tables_menu)
        return self.input_choice(self.operations_menu, 8)

    @staticmethod
    def print_table_data(data, indents):
        for i, item in enumerate(data, start=1):
            print(str(i).ljust(8, " "), end="")
            for j, indent in enumerate(indents):
                print(str(item[j]).ljust(indent, " "), end="")
            print()

    def film_genres_parser(self, data):
        print("\n" + " film_genres ".center(75, "=") + "\n")
        print("film_id".center(17, " ") + "genre_id".center(17, " ") + "\n")

        indents = (17, 0)
        self.print_table_data(data, indents)

    def films_parser(self, data):
        print("\n" + " films ".center(75, "=") + "\n")
        print("id".center(17, " ")
              + "title".center(17, " ")
              + "producer".center(17, " ")
              + "release_year".center(17, " ")
              + "duration".center(17, " ") + "\n")

        indents = (17, 17, 17, 17, 0)
        self.print_table_data(data, indents)

    def genres_parser(self, data):
        print("\n" + " genres ".center(75, "=") + "\n")
        print("id".center(17, " ") + "name".center(17, " ") + "\n")

        indents = (17,  0)
        self.print_table_data(data, indents)

    def halls_parser(self, data):
        print("\n" + " halls ".center(75, "=") + "\n")
        print("number".center(17, " ") + "technology_id".center(17, " ") + "\n")

        indents = (17, 0)
        self.print_table_data(data, indents)

    def prices_parser(self, data):
        print("\n" + " prices ".center(75, "=") + "\n")
        print("id".center(17, " ")
              + "technology_id".center(17, " ")
              + "price".center(17, " ") + "\n")

        indents = (17, 17, 0)
        self.print_table_data(data, indents)

    def session_parser(self, data):
        print("\n" + " session ".center(75, "=") + "\n")
        print("id".center(17, " ")
              + "hall_id".center(17, " ")
              + "film_id".center(17, " ")
              + "date_time".center(17, " ") + "\n")

        indents = (17, 17, 17, 0)
        self.print_table_data(data, indents)

    def sold_tickets_parser(self, data):
        print("\n" + " sold_tickets ".center(75, "=") + "\n")
        print("id".center(17, " ")
              + "session_id".center(17, " ")
              + "place".center(17, " ")
              + "row".center(17, " ") + "\n")

        indents = (17, 17, 17, 0)
        self.print_table_data(data, indents)

    def technologies_parser(self, data):
        print("\n" + " technologies ".center(75, "=") + "\n")
        print("id".center(17, " ")
              + "name".center(17, " ")
              + "description".center(17, " ") + "\n")

        indents = (17, 17, 0)
        self.print_table_data(data, indents)

    def input_data(self, column_names):
        return [input(f"Enter {column}: ") for column in column_names]

    def delete(self):
        id_range = input("Select id range (x y) or just id (x): ").split()
        return [int(i) for i in id_range]

    def input_data_to_search(self, data_type):
        if data_type == 'integer':
            min_value = input("Enter min value: ")
            max_value = input("Enter max value: ")
            return [min_value, max_value]
        elif data_type == 'character varying':
            return input("Enter data: ")
        elif data_type == 'timestamp without time zone':
            min_value = input("Enter YYYY-MM-DD HH:MM:SS min date: ")
            max_value = input("Enter YYYY-MM-DD HH:MM:SS max date: ")
            return [min_value, max_value]
        else:
            print(f"Cannot find data with '{data_type}' type")

    def search(self, column_names):
        for i, column in enumerate(column_names):
            print(str(i) + ": " + column)

        return int(input("\nEnter choice № "))
