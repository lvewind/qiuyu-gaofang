import xlwings as xw
import time


def list_to_excel(data_list: list, product_name: str, excel_name: str):
    print(data_list)
    save_name = excel_name + ".xlsx"
    try:
        wb = xw.Book(save_name)
    except FileNotFoundError:
        wb = xw.Book()
    last_sht = wb.sheets[-1]
    if last_sht.name == "Sheet1":
        sht = wb.sheets["Sheet1"]
        sht.name = product_name
    else:
        wb.sheets.add(name=product_name, after=last_sht.name)
        sht = wb.sheets.active
    sht.range(1, 1).row_height = 24
    sht.range(1, 1).column_width = 20
    sht.range(1, 2).column_width = 64
    sht.range(1, 3).column_width = 40
    sht.range(1, 4).column_width = 15
    sht.range(1, 5).column_width = 15
    sht.range(1, 6).column_width = 40

    sht.range(1, 1).value = "ID"
    sht.range(1, 2).value = "标题"
    sht.range(1, 3).value = "链接"
    sht.range(1, 4).value = "价格"
    sht.range(1, 5).value = "销量"
    sht.range(1, 6).value = "店铺"

    for index, data_dict in enumerate(data_list):
        if data_dict:
            n = index + 2
            sht.range(n, 1).row_height = 20
            sht.range(n, 1).api.NumberFormat = "0"
            sht.range(n, 1).value = data_dict.get("id")
            sht.range(n, 2).value = data_dict.get("title")
            sht.range(n, 3).value = data_dict.get("link")
            sht.range(n, 4).value = data_dict.get("price")
            sht.range(n, 5).value = data_dict.get("sale")
            sht.range(n, 6).value = data_dict.get("shoper")

    active_window = wb.app.api.ActiveWindow
    active_window.FreezePanes = False
    active_window.SplitRow = 1
    active_window.FreezePanes = True
    wb.save(save_name)
