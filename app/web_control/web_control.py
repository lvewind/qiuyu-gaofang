from selenium import webdriver
from selenium.webdriver.common.by import By
import selenium.common
import time
import os
from app.kiki_signal.kiki_signal import signal_main_ui
from app.excel.excel_to_data import excel_to_list
from app.excel.data_to_excel import list_to_excel
# from threading import Thread
import re
import json
from copy import deepcopy
import random
from pyquery import PyQuery as pq


class KikiDriver:
    """
    KikiDriver
    """
    def __init__(self, bin_path="bin", driver_file="chromedriver.exe"):
        self.driver_path = os.path.join(os.path.abspath(os.getcwd()), bin_path, driver_file)
        self.stop = False
        self.pause = False
        self.is_pdd_login = False
        self.is_pdd_start_search = False
        self.is_am_login = False
        self.is_am_search_input = False

    def run_get(self, excel_input_path: str, platform: str, target_count: int):
        excel_name = time.strftime("%Y%m%d%H%M%S", time.localtime())
        products = excel_to_list(excel_input_path)

        if products:
            if platform == "tb":
                self.get_tb(products, target_count, excel_name)
            elif platform == "jd":
                self.get_jd(products, target_count, excel_name)
            elif platform == "pdd":
                self.get_pdd(products, target_count, excel_name)
            elif platform == "am":
                self.get_am(products, target_count, excel_name)
            elif platform == "wd":
                self.get_wd(products, target_count, excel_name)

    def get_tb(self, products: list, target_count, excel_name):
        """

        :param products:
        :param target_count:
        :param excel_name:
        :return:
        """
        driver = webdriver.Chrome(self.driver_path)
        signal_main_ui.refresh_text_browser.emit("打开淘宝登录页面")
        url = "https://login.taobao.com/"
        driver.get(url)
        signal_main_ui.refresh_text_browser.emit("选择扫码登录")
        qr_login = driver.find_element_by_xpath('//*[@id="login"]/div[1]/i')
        qr_login.click()
        while True:
            time.sleep(1)
            try:
                qr_code = driver.find_element_by_xpath('//*[@id="login"]/div[2]/div/div[1]/div[1]/undefined/canvas')
                if qr_code.is_displayed():
                    signal_main_ui.refresh_text_browser.emit("等待扫码登录")
            except selenium.common.exceptions.NoSuchElementException or selenium.common.exceptions.StaleElementReferenceException:
                try:
                    qr_code = driver.find_element_by_xpath('//*[@id="login"]/div[2]/div/div[1]/div[1]/div/button')
                    if qr_code.is_displayed():
                        signal_main_ui.refresh_text_browser.emit("二维码失效, 刷新二维码")
                        qr_code.click()
                except selenium.common.exceptions.NoSuchElementException or selenium.common.exceptions.StaleElementReferenceException:
                    try:
                        scan_success = driver.find_element_by_xpath('//*[@id="login"]/div[2]/div/div[1]/p')
                        if scan_success.is_displayed():
                            signal_main_ui.refresh_text_browser.emit("扫描成功, 等待确认")
                    except selenium.common.exceptions.NoSuchElementException or selenium.common.exceptions.StaleElementReferenceException:
                        try:
                            login_success = driver.find_element_by_xpath('//*[@id="J_MtMainNav"]/li[2]/a')
                            if login_success.is_displayed():
                                signal_main_ui.refresh_text_browser.emit("登录成功")
                                break
                        except selenium.common.exceptions.NoSuchElementException or selenium.common.exceptions.StaleElementReferenceException:
                            pass
                        try:
                            login_success = driver.find_element_by_xpath('//*[@id="J_SiteNavMytaobao"]/div[1]/a/span')
                            if login_success.is_displayed():
                                signal_main_ui.refresh_text_browser.emit("登录成功")
                                break
                        except selenium.common.exceptions.NoSuchElementException or selenium.common.exceptions.StaleElementReferenceException:
                            pass
        signal_main_ui.refresh_text_browser.emit("打开搜索页面")
        driver.get("https://s.taobao.com/")

        for product in products:
            while self.pause:
                if self.stop:
                    break
                time.sleep(1)
                signal_main_ui.refresh_text_browser.emit("暂停中")
            if self.stop:
                break
            else:

                brand = product[0] if product[0] else ""
                name = product[1] if product[1] else ""
                # size = product[2] if product[2] else ""
                if brand or name:
                    signal_main_ui.refresh_text_browser.emit("正在查询: " + str(brand) + str(name))
                    for t in range(10):
                        time.sleep(0.5)
                        try:
                            search_input = driver.find_element_by_xpath('//*[@id="q"]')
                            if search_input.is_displayed():
                                search_input.clear()
                                search_input.send_keys(str(brand) + str(name))
                                break
                        except selenium.common.exceptions.NoSuchElementException or selenium.common.exceptions.StaleElementReferenceException:
                            continue
                    else:
                        signal_main_ui.refresh_text_browser.emit("页面超时, 刷新页面")
                        driver.get("https://s.taobao.com/")

                    try:
                        search_button = driver.find_element_by_xpath('//*[@id="J_SearchForm"]/div/div[1]/button')
                        search_button.click()
                    except selenium.common.exceptions.NoSuchElementException or selenium.common.exceptions.StaleElementReferenceException:
                        try:
                            search_button = driver.find_element_by_xpath('//*[@id="J_SearchForm"]/button')
                            search_button.click()
                        except selenium.common.exceptions.NoSuchElementException or selenium.common.exceptions.StaleElementReferenceException:
                            pass
                    time.sleep(2)
                    result_count = 0
                    result = []  # 整理出我们关注的信息(ID,标题，链接，售价，销量和商家)
                    while True:
                        if result_count >= target_count:
                            break
                        html = driver.page_source
                        g_page_config = re.search(r'g_page_config = (.*?);\n', html)
                        page_config_json = json.loads(g_page_config.group(1))
                        try:
                            page_item = page_config_json['mods']['itemlist']['data']['auctions']
                        except ValueError:
                            break
                        except KeyError:
                            break
                        if page_item:
                            for each in page_item:
                                dict1 = dict.fromkeys(('id', 'title', 'link', 'price', 'sale', 'shoper'))
                                try:
                                    dict1['id'] = each['nid']
                                except ValueError:
                                    dict1['id'] = ""
                                except KeyError:
                                    dict1['id'] = ""

                                try:
                                    dict1['title'] = each['title'].replace("<span class=H>", "").replace("</span>", "")
                                except ValueError:
                                    dict1['id'] = ""
                                except KeyError:
                                    dict1['id'] = ""
                                try:
                                    dict1['link'] = each['detail_url']
                                except ValueError:
                                    dict1['link'] = ""
                                except KeyError:
                                    dict1['link'] = ""
                                try:
                                    dict1['price'] = each['view_price']
                                except ValueError:
                                    dict1['price'] = ""
                                except KeyError:
                                    dict1['price'] = ""
                                try:
                                    dict1['sale'] = each['view_sales']
                                except ValueError:
                                    dict1['sale'] = ""
                                except KeyError:
                                    dict1['sale'] = ""
                                try:
                                    dict1['shoper'] = each['nick']
                                except ValueError:
                                    dict1['shoper'] = ""
                                except KeyError:
                                    dict1['shoper'] = ""
                                result_count += 1
                                result.append(dict1)
                            else:
                                try:
                                    next_page = driver.find_element_by_xpath('//*[@id="mainsrp-pager"]/div/div/div/ul/li[8]')
                                    if next_page.is_displayed():
                                        next_page.click()
                                        time.sleep(3)
                                except selenium.common.exceptions.NoSuchElementException or selenium.common.exceptions.StaleElementReferenceException:
                                    break
                    if result:
                        list_to_excel(deepcopy(result), str(brand + name), "淘宝_" + excel_name)

                else:
                    pass
                time.sleep(1)
        signal_main_ui.refresh_text_browser.emit("查询已完成")

    def get_tm(self, products: list, target_count, excel_name):
        """

        :param products:
        :param target_count:
        :param excel_name:
        :return:
        """
        pass

    def get_jd(self, products: list, target_count, excel_name):
        """

        :param products:
        :param target_count:
        :param excel_name:
        :return:
        """
        driver = webdriver.Chrome(self.driver_path)
        signal_main_ui.refresh_text_browser.emit("打开京东登录页面")
        url = "https://passport.jd.com/uc/login"
        driver.get(url)
        signal_main_ui.refresh_text_browser.emit("选择扫码登录")
        qr_login = driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[1]/div/div[2]/a')
        qr_login.click()
        while True:
            time.sleep(1)
            try:
                qr_code = driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[1]/div/div[5]/div/div[2]/div[1]/img')
                if qr_code.is_displayed():
                    signal_main_ui.refresh_text_browser.emit("等待扫码登录")
            except selenium.common.exceptions.NoSuchElementException:
                pass
            except selenium.common.exceptions.StaleElementReferenceException:
                pass
            try:
                qr_code = driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[1]/div/div[5]/div/div[1]/a')
                if qr_code.is_displayed():
                    signal_main_ui.refresh_text_browser.emit("二维码失效, 刷新二维码")
                    qr_code.click()
            except selenium.common.exceptions.NoSuchElementException:
                pass
            except selenium.common.exceptions.StaleElementReferenceException:
                pass
            try:
                scan_success = driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[1]/div/div[5]/div/div[3]/div/div/h3')
                if scan_success.is_displayed():
                    signal_main_ui.refresh_text_browser.emit("扫描成功, 等待确认")
            except selenium.common.exceptions.NoSuchElementException:
                pass
            except selenium.common.exceptions.StaleElementReferenceException:
                pass
            try:
                login_success = driver.find_element_by_xpath('//*[@id="ttbar-login"]/div[1]/a')
                if login_success.is_displayed():
                    signal_main_ui.refresh_text_browser.emit("登录成功")
                    break
            except selenium.common.exceptions.NoSuchElementException:
                pass
            except selenium.common.exceptions.StaleElementReferenceException:
                pass

        signal_main_ui.refresh_text_browser.emit("打开搜索页面")
        driver.get("https://search.jd.com/Search?")

        for product in products:
            while self.pause:
                if self.stop:
                    break
                time.sleep(1)
                signal_main_ui.refresh_text_browser.emit("暂停中")
            if self.stop:
                break
            else:

                brand = product[0] if product[0] else ""
                name = product[1] if product[1] else ""
                # size = product[2] if product[2] else ""
                if brand or name:
                    signal_main_ui.refresh_text_browser.emit("正在查询: " + str(brand) + str(name))
                    for t in range(10):
                        time.sleep(0.5)
                        try:
                            search_input = driver.find_element_by_xpath('//*[@id="key"]')
                            if search_input.is_displayed():
                                search_input.clear()
                                search_input.send_keys(str(brand) + str(name))
                                break
                        except selenium.common.exceptions.NoSuchElementException or selenium.common.exceptions.StaleElementReferenceException:
                            continue
                    else:
                        signal_main_ui.refresh_text_browser.emit("页面超时, 刷新页面")
                        driver.get("https://search.jd.com/Search?")

                    try:
                        search_button = driver.find_element_by_xpath('//*[@id="search-2014"]/div/button')
                        search_button.click()
                    except selenium.common.exceptions.NoSuchElementException or selenium.common.exceptions.StaleElementReferenceException:
                        pass
                    time.sleep(2)
                    result_count = 0
                    result = []  # 整理出我们关注的信息(ID,标题，链接，售价，销量和商家)
                    while True:
                        if result_count >= target_count:
                            break
                        gl_items = driver.find_elements_by_class_name('gl-item')
                        if gl_items:
                            for gl_item in gl_items:
                                try:
                                    dict1 = dict.fromkeys(('id', 'title', 'link', 'price', 'sale', 'shoper'))
                                    dict1['id'] = gl_item.get_attribute('data-sku')
                                    dict1['title'] = gl_item.find_element_by_class_name('p-name').find_element_by_tag_name('em').text.replace('<font class="skcolor_ljg">', '').replace('</font>', '')
                                    dict1['link'] = gl_item.find_element_by_class_name('p-name').find_element_by_tag_name('em').get_attribute('href')
                                    dict1['price'] = gl_item.find_element_by_class_name('p-price').find_element_by_tag_name('i').text
                                    dict1['sale'] = gl_item.find_element_by_class_name('p-commit').find_element_by_tag_name('a').text
                                    dict1['shoper'] = gl_item.find_element_by_class_name('curr-shop').text
                                except selenium.common.exceptions.NoSuchElementException:
                                    continue
                                except selenium.common.exceptions.StaleElementReferenceException:
                                    continue
                                result_count += 1
                                result.append(dict1)
                            else:
                                try:
                                    next_page = driver.find_element_by_class_name('pn-next')
                                    if next_page.is_displayed():
                                        next_status = next_page.get_attribute('class')
                                        if "disabled" in next_status:
                                            break
                                        else:
                                            next_page.click()
                                            signal_main_ui.refresh_text_browser.emit("下一页")
                                        time.sleep(1)
                                    else:
                                        break
                                except selenium.common.exceptions.NoSuchElementException:
                                    break
                                except selenium.common.exceptions.StaleElementReferenceException:
                                    break
                    if result:
                        list_to_excel(deepcopy(result), str(brand + name), "京东_" + excel_name)

                else:
                    pass
                time.sleep(1)
        signal_main_ui.refresh_text_browser.emit("查询已完成")

    def get_pdd(self, products: list, target_count, excel_name):
        """

        :param products:
        :param target_count:
        :param excel_name:
        :return:
        """
        driver = webdriver.Chrome(self.driver_path)
        signal_main_ui.refresh_text_browser.emit("打开拼多多登录页面")
        url = "https://mobile.yangkeduo.com/login.html?"
        driver.get(url)
        self.is_pdd_login = False
        while not self.is_pdd_login:
            signal_main_ui.refresh_text_browser.emit("请手动登录PDD, 完成登录后点击上方确认按钮")
            time.sleep(1)

        while True:
            try:
                footer = driver.find_element_by_xpath('//*[@id="main"]/div/div[2]/div[4]/div')
                if footer.is_displayed():
                    first_search_input = driver.find_element_by_xpath('//*[@id="main"]/div/div[1]/div[1]/div[1]/div/div/div[1]')
                    if first_search_input.is_displayed():
                        first_search_input.click()
                        time.sleep(2)
            except selenium.common.exceptions.NoSuchElementException:
                pass
            except selenium.common.exceptions.StaleElementReferenceException:
                pass

            try:
                search_button = driver.find_element_by_xpath('//*[@id="main"]/div[2]/div[1]/div/div[2]')
                if search_button.is_displayed():
                    break
            except selenium.common.exceptions.NoSuchElementException:
                pass
            except selenium.common.exceptions.StaleElementReferenceException:
                pass
    
        for product in products:
            result = []  # 结果容器
            scroll_position = 1000
            scroll_times = 0
            self.is_pdd_start_search = True
            if self.stop:
                signal_main_ui.refresh_text_browser.emit("已停止")
                break
            while True:
                if self.pause:
                    if self.stop:
                        signal_main_ui.refresh_text_browser.emit("已停止")
                        break
                    time.sleep(1)
                    signal_main_ui.refresh_text_browser.emit("暂停中")
                else:
                    brand = product[0] if product[0] else ""
                    name = product[1] if product[1] else ""
                    # size = product[2] if product[2] else ""
                    if brand or name:
                        try:
                            if driver.find_element_by_xpath('//*[@id="captcha-dialog"]/div[1]').is_displayed():
                                signal_main_ui.refresh_text_browser.emit("请手动消除验证滑块")
                                time.sleep(1)
                        except selenium.common.exceptions.NoSuchElementException or selenium.common.exceptions.StaleElementReferenceException:
                            # 查出初始化
                            if self.is_pdd_start_search:
                                js = "var q=document.documentElement.scrollTop=" + str(scroll_position - 500)
                                signal_main_ui.refresh_text_browser.emit("正在查询: " + str(brand) + str(name))
                                try:
                                    driver.find_element_by_class_name('_1_lwtoht').click()
                                    time.sleep(1)
                                except selenium.common.exceptions.NoSuchElementException as e:
                                    print(e)
                                except selenium.common.exceptions.StaleElementReferenceException as e:
                                    print(e)
                                except selenium.common.exceptions.ElementClickInterceptedException as e:
                                    print(e)
                                try:
                                    # 输入 _1rjqjr6b
                                    search_input = driver.find_element_by_xpath('//*[@id="submit"]/input')
                                    if search_input.is_displayed():
                                        search_input.clear()
                                        search_input.send_keys(str(brand) + str(name))
                                        try:
                                            driver.find_element_by_xpath('//*[@id="main"]/div[2]/div[1]/div/div[2]').click()
                                            self.is_pdd_start_search = False
                                        except selenium.common.exceptions.NoSuchElementException as e:
                                            print(e)
                                        try:
                                            driver.find_element_by_class_name('_2wmqpCvm').click()
                                            self.is_pdd_start_search = False
                                        except selenium.common.exceptions.NoSuchElementException as e:
                                            print(e)

                                    else:
                                        driver.execute_script(js)
                                except selenium.common.exceptions.NoSuchElementException as e:
                                    print(e)
                                    driver.execute_script(js)
                                except selenium.common.exceptions.StaleElementReferenceException as e:
                                    print(e)
                                    driver.execute_script(js)
                            else:
                                # 获取查询数据
                                time.sleep(1)
                                try:
                                    no_goods = driver.find_element_by_xpath('//*[@id="main"]/div/div[2]/div/div/div[2]/div[1]/div/span')
                                    no_goods_tips = no_goods.text
                                    if "相关商品较少" in no_goods_tips:
                                        signal_main_ui.refresh_text_browser.emit("相关商品较少, 跳过查询")
                                        break
                                except selenium.common.exceptions.NoSuchElementException:
                                    pass
                                except selenium.common.exceptions.StaleElementReferenceException:
                                    pass
                                js = "var q=document.documentElement.scrollTop=" + str(scroll_position)
                                driver.execute_script(js)
                                signal_main_ui.refresh_text_browser.emit("正在翻页中...")
                                scroll_times += 1
                                scroll_position += random.randint(1000, 1200)
                                try:
                                    _2olq_Qet_items = driver.find_elements_by_class_name('_2olq_Qet')
                                except selenium.common.exceptions.NoSuchElementException or selenium.common.exceptions.StaleElementReferenceException:
                                    _2olq_Qet_items = []
                                if len(_2olq_Qet_items) >= target_count or scroll_times >= 20:
                                    for index, _2olq_Qet in enumerate(_2olq_Qet_items):
                                        dict1 = dict.fromkeys(('id', 'title', 'link', 'price', 'sale', 'shoper'))
                                        dict1['id'] = index + 1
                                        try:
                                            title = _2olq_Qet.find_element_by_class_name('RHpIDHFA').text.replace('"', '').replace('\n', '')
                                            dict1['title'] = title
                                        except selenium.common.exceptions.NoSuchElementException or selenium.common.exceptions.StaleElementReferenceException:
                                            dict1['title'] = "NO DATA"
                                        dict1['link'] = "NO DATA"
                                        try:
                                            price_el = _2olq_Qet.find_element_by_class_name('_2TktAWlc').find_elements_by_xpath('span')
                                            price_list = []
                                            if price_el:
                                                for el in price_el:
                                                    price_list.append(el.text)
                                                dict1['price'] = "".join(price_list) if price_list else "NO DATA"
                                        except selenium.common.exceptions.NoSuchElementException or selenium.common.exceptions.StaleElementReferenceException:
                                            dict1['price'] = "NO DATA"
                                        try:
                                            dict1['sale'] = _2olq_Qet.find_element_by_class_name('_5x_0r9h0').find_element_by_tag_name('span').text

                                        except selenium.common.exceptions.NoSuchElementException or selenium.common.exceptions.StaleElementReferenceException:
                                            dict1['sale'] = "NO DATA"
                                            dict1['shoper'] = "NO DATA"
                                        result.append(dict1)
                                    else:
                                        if result:
                                            print(result)
                                            list_to_excel(deepcopy(result), str(brand + name), "拼多多_" + excel_name)
                                        break

    def get_am(self, products: list, target_count, excel_name):
        """

        :param products:
        :param target_count:
        :param excel_name:
        :return:
        """
        driver = webdriver.Chrome(self.driver_path)
        signal_main_ui.refresh_text_browser.emit("打开亚马逊")
        url = "https://www.amazon.com/ref=nav_logo?language=en_US"
        driver.get(url)
        self.is_am_login = False

        for product in products:
            self.is_am_search_input = True
            index = 1
            if self.stop:
                signal_main_ui.refresh_text_browser.emit("已停止")
                break
            else:
                result_count = 0
                result_list = []  # 整理出我们关注的信息(ID,标题，链接，售价，销量和商家)
                brand = product[0] if product[0] else ""
                name = product[1] if product[1] else ""
                # size = product[2] if product[2] else ""
                if brand or name:
                    while True:
                        if self.is_am_search_input:
                            signal_main_ui.refresh_text_browser.emit("正在查询: " + str(brand) + " " + str(name))
                            try:
                                input_el = driver.find_element(By.ID, 'twotabsearchtextbox')
                                if input_el.is_displayed():
                                    input_el.clear()
                                    input_el.send_keys(brand + " " + name)
                                search_button = driver.find_element(By.ID, 'nav-search-submit-button')
                                if search_button.is_displayed():
                                    search_button.click()
                                    self.is_am_search_input = False
                            except selenium.common.exceptions.NoSuchElementException as e:
                                print(e)
                            except selenium.common.exceptions.StaleElementReferenceException as e:
                                print(e)
                            except selenium.common.exceptions.ElementClickInterceptedException as e:
                                print(e)
                        else:
                            time.sleep(2)
                            js = "var q=document.documentElement.scrollTop=9200"
                            driver.execute_script(js)
                            if self.pause:
                                if self.stop:
                                    signal_main_ui.refresh_text_browser.emit("已停止")
                                    break
                                time.sleep(1)
                                signal_main_ui.refresh_text_browser.emit("暂停中")
                            if result_count >= target_count:
                                break
                            # try:
                            #     result_items = driver.find_elements(By.CLASS_NAME, 's-result-item')
                            #     print(result_items)
                            # except selenium.common.exceptions.NoSuchElementException as e:
                            #     print(e)
                            #     result_items = []
                            # except selenium.common.exceptions.StaleElementReferenceException as e:
                            #     print(e)
                            #     result_items = []
                            html = pq(driver.page_source)

                            result_items = html("[data-asin]").items()
                            if result_items:
                                for item in result_items:
                                    dict1 = dict.fromkeys(('id', 'title', 'link', 'price', 'sale', 'shoper'))
                                    dict1['id'] = index
                                    index = index + 1
                                    try:
                                        dict1['title'] = item("h2.a-size-mini > a.a-link-normal > span.a-text-normal")[0].text
                                    except IndexError as e:
                                        print(e)
                                    dict1['link'] = "NO DATA"
                                    try:
                                        dict1['price'] = item("div.a-row > a > span > span > span.a-price-whole ")[0].text
                                    except IndexError as e:
                                        print(e)
                                    try:
                                        dict1['sale'] = item("div > span > a > span.a-size-base")[0].text
                                    except IndexError as e:
                                        print(e)
                                    dict1['shoper'] = "NO DATA"
                                    print(dict1)
                                    result_count += 1
                                    result_list.append(dict1)
                                else:
                                    try:
                                        next_page = driver.find_element(By.CSS_SELECTOR, 'li.a-last')
                                        if next_page.is_displayed():
                                            next_status = next_page.get_attribute('class')
                                            if "a-disabled" in next_status:
                                                break
                                            else:
                                                next_page.click()
                                                signal_main_ui.refresh_text_browser.emit("下一页")
                                            time.sleep(1)
                                        else:
                                            break
                                    except selenium.common.exceptions.NoSuchElementException:
                                        break
                                    except selenium.common.exceptions.StaleElementReferenceException:
                                        break
                            else:
                                break

                    if result_list:
                        list_to_excel(deepcopy(result_list), str(name)[0: 18], "亚马逊_" + excel_name)

    def get_wd(self, products: list, target_count, excel_name):
        """

        :param products:
        :param target_count:
        :param excel_name:
        :return:
        """
        pass
