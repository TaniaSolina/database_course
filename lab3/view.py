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
|   6: Exit the program        |
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
        }

    @staticmethod
    def input_choice(func, end):
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

    @staticmethod
    def table_parser(table_name, column_names, data):
        print("\n" + f" {table_name} ".center(75, "=") + "\n")
        for column in column_names:
            print(column.center(17, " "), end="")

        print()
        indents = [17 for _ in column_names]
        View.print_table_data(data, indents)

    @staticmethod
    def input_data(column_names):
        return [input(f"Enter {column}: ") for column in column_names]

    @staticmethod
    def delete():
        id_range = input("Select id range (x y) or just id (x): ").split()
        return [int(i) for i in id_range]

    @staticmethod
    def input_data_to_search(data_type):
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

    @staticmethod
    def search(column_names):
        for i, column in enumerate(column_names):
            print(str(i) + ": " + column)

        return int(input("\nEnter choice № "))
