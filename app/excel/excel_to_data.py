import xlwings as xw
from app.kiki_signal.kiki_signal import signal_main_ui


def excel_to_list(excel_input_path: str):
    signal_main_ui.refresh_text_browser.emit("开始解析数据源Excel")
    source_list = []
    try:
        wb = xw.Book(excel_input_path)
        sht_count = len(wb.sheets)
        for sht_n in range(sht_count):
            empty_lines = 0
            sht = wb.sheets[sht_n]
            for row in range(2, 999):
                if empty_lines >= 10:
                    break
                brand = sht.range("A" + str(row)).value
                name = sht.range("B" + str(row)).value
                size = sht.range("C" + str(row)).value
                if not brand and not name and not size:
                    empty_lines += 1
                else:
                    empty_lines = 0
                    # signal_main_ui.refresh_text_browser.emit(str(brand) + str(name) + str(size))
                    source_list.append([brand, name, size])
        signal_main_ui.refresh_text_browser.emit("Excel数据源解析完成")
        return source_list
    except ValueError as e:
        signal_main_ui.refresh_text_browser.emit("Excel解析失败,请关闭同名Excel文件" + str(e))
        return
