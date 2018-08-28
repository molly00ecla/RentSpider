# coding:gbk

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import time
import codecs

import recong_digit


def get_house_detail(house_url):
    driver = webdriver.Chrome()
    print house_url
    driver.get(house_url)    # 打开某个页面
    house_name_list = []
    house_area_list = []
    house_price_list = []
    try:
        # 加载，等待房源列表加载出来
        element = WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.ID, "houseList"))
        )

        # 得到背景图位置-数码的对应关系
        price_img_pattern = r'ROOM_PRICE = {"image":"(.+?)"'
        img_url = re.findall(price_img_pattern, driver.page_source)
        img_url = 'http:' + img_url[0]
        # print img_url
        img_digits = recong_digit.get_digit(img_url)        # 识别图片中的数字
        # print img_digits


        # 获取房源信息
        for house_detail in element.find_elements_by_class_name('clearfix'):
            class_name = house_detail.get_attribute('class')
            if not class_name == 'clearfix':
                continue

            # 房源名称
            detail = house_detail.text.encode('utf-8')
            house_name = detail.split('\n')[0]
            area_pattern = r'([\d\.]+) '
            house_area = re.findall(area_pattern, detail)[0]
            price_element = house_detail.find_elements_by_class_name('num')
            house_price = 0
            for p in price_element[1:]:
                # 对应图片位置到价格数字
                bp_pattern = r'background-position: (.+)px center;'
                background_position = re.findall(bp_pattern, p.get_attribute('style'))[0]
                pos_index = abs(int(background_position)/30)
                real_digit = int(img_digits[pos_index])
                house_price = house_price*10 + real_digit
            house_name_list.append(house_name)
            house_area_list.append(house_area)
            house_price_list.append(house_price)

            print house_area, house_name


    finally:
        driver.quit()
        return house_name_list, house_area_list, house_price_list


fw = codecs.open('天通苑20180821.csv', 'w')
for p in range(19):
    house_name_list, house_area_list, house_price_list = get_house_detail(r'http://www.ziroom.com/z/nl/z2-d23008611-b18335747.html?p='+str(p))
    for i in range(len(house_name_list)):
        fw.write('%s,%s,%s\n'%(house_name_list[i], house_area_list[i], house_price_list[i]))

fw.close()