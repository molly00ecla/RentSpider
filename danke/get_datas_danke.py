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
            EC.presence_of_element_located((By.CLASS_NAME, "roomlist"))
        )


        # 获取房源信息
        for house_detail in element.find_elements_by_class_name('r_lbx'):
            print('-'*10)
            print(house_detail.text.encode('utf-8'))
            print('-' * 10)

            detail = house_detail.text.encode('utf-8')
            detail_l = detail.split('\n')
            if len(detail_l) < 2:
                continue   #广告
            house_name = detail.split('\n')[1]
            area_pattern = r'(\d+)'
            house_area = re.findall(area_pattern, detail_l[2].split('|')[0])[0]
            house_price = re.findall(area_pattern, detail.split('\n')[-2])[0]
            house_name_list.append(house_name)
            house_area_list.append(house_area)
            house_price_list.append(house_price)

            print house_area, house_name

    finally:
        driver.quit()
        return house_name_list, house_area_list, house_price_list


fw = codecs.open('沙河-蛋壳-20180825.csv', 'w')
for p in range(1):
    house_name_list, house_area_list, house_price_list = get_house_detail('https://www.dankegongyu.com/room/bj/d%E6%98%8C%E5%B9%B3%E5%8C%BA-b%E6%B2%99%E6%B2%B3%EF%BC%88%E5%8C%97%E4%BA%AC%EF%BC%89.html' )
    # house_name_list, house_area_list, house_price_list = get_house_detail('https://www.dankegongyu.com/room/bj/d%E6%9C%9D%E9%98%B3%E5%8C%BA-b%E5%8C%97%E8%8B%91.html?page='+str(p+1))
    for i in range(len(house_name_list)):
        fw.write('"%s",%s,%s\n'%(house_name_list[i], house_area_list[i], house_price_list[i]))