from model import *
from view import View


class Controller:
    def __init__(self):
        self.view_obj = View()

    def menu(self):
        table_num = 0
        while True:
            operation_num = self.view_obj.operations_menu()
            if operation_num == 6:
                break
            if operation_num != 2:
                table_num = self.view_obj.tables_menu()

            if operation_num == 1:
                select_table(table_num)
            elif operation_num == 2:
                select_all_tables()
            elif operation_num == 3:
                insert_into_table(table_num)
            elif operation_num == 4:
                table = tables[table_num]
                column_names = get_column_names(table)
                data = self.view_obj.input_data(column_names)
                update_table(data, table_num)
            elif operation_num == 5:
                id_range = self.view_obj.delete()
                delete_data(table_num, id_range)
