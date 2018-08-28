# coding:gbk

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import time
import codecs


def get_house_detail(house_url):
    house_name_list = []
    house_area_list = []
    house_price_list = []
    print(house_url)
    driver = webdriver.Chrome()
    driver.get(house_url)
    try:
        # 加载，等待房源列表加载出来
        element = WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.CLASS_NAME, "houseList"))
        )


        # 获取房源信息
        for house_detail in element.find_elements_by_class_name('hiddenMap'):
            print('-'*10)
            print(house_detail.text.encode('utf-8'))
            print('-' * 10)

            detail = house_detail.text.encode('utf-8')
            detail_l = detail.split('\n')
            if len(detail_l) < 2:
                continue   #广告
            house_name = detail.split('\n')[1]
            area_pattern = r'(\d+)'
            house_area = re.findall(area_pattern, detail_l[2].split('|')[2])[0]
            house_price = re.findall(area_pattern, detail.split('\n')[-1])[0]
            house_name_list.append(house_name)
            house_area_list.append(house_area)
            house_price_list.append(house_price)

            print house_area, house_name

    finally:
        driver.quit()
        return house_name_list, house_area_list, house_price_list


fw = codecs.open('龙泽苑东区-房天下-20180821.csv', 'w')
for p in range(2):
    # house_name_list, house_area_list, house_price_list = get_house_detail('http://zu.fang.com/house/s31-kw%c1%fa%bd%f5%d4%b7%cb%c4%c7%f8/' )
    house_name_list, house_area_list, house_price_list = get_house_detail('http://zu.fang.com/house/i3'+str(p+1)+'-s31-kw%c1%fa%d4%f3%d4%b7%b6%ab%c7%f8/' )
    for i in range(len(house_name_list)):
        fw.write('"%s",%s,%s\n'%(house_name_list[i], house_area_list[i], house_price_list[i]))