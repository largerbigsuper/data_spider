# -*- encoding:utf-8 -*-
#coding:utf-8
import json
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import re
from selenium import webdriver

from parser import get_problem, Category

domain = 'http://www.tskspx.com/indexNew.do'
# userid = '18258477953'
userid = '18106518219'
password = '123456'

url_test = 'http://www.tskspx.com/user/100250/trainBegin.do?sss=1'

driver = webdriver.Chrome()

# step-1 登录
driver.get(domain)
input_name = driver.find_element_by_id('userid')
input_pwd = driver.find_element_by_id('password')
input_login = driver.find_element_by_class_name('btn_indexlog1')
input_name.send_keys(userid)
input_pwd.send_keys(password)
input_login.click()

# step-2 选择培训种类种类（先选则第一种）
# choise_1_id = 'lab_pn677173'
choise_1_id = 'lab_pn677111'
choise_2_id = 'lab_pn677181'
# choise_2_id = 'lab_pn677185'
groups = [choise_1_id, choise_2_id]
GROUP_ID = 0
CATEGORY_ID = 0
INDEX_URL = 'http://www.tskspx.com/toSelectProject.do'

for index, group_tag in enumerate(groups):
    GROUP_ID = index
    print '>>>>>>>>>>>GROUP：%s <<<<<<<<<<<<' % GROUP_ID

    driver.get(INDEX_URL)
    choice = driver.find_element_by_id('lab_pn677181')
    choice.click()
    btn_enter = driver.find_element_by_class_name('btn_orange2')
    btn_enter.click()

    # 进如题目库
    nav = driver.find_element_by_class_name('nav1')
    nav.click()
    nod = driver.find_element_by_class_name('nod1')
    nod.click()

    # 提取题目分类
    category_td = driver.find_elements_by_xpath("//td[@class='left']/a")

    for index, tag in enumerate(category_td):
        # print index, tag.text

        tag = driver.find_element_by_xpath("//td[@class='left']/a[%s]" % str(index + 1))
        CATEGORY_ID = index
        category = Category(group=GROUP_ID, num=index, name=tag.text)

        with open('category.txt', 'ab+') as f:
            line = json.dumps(dict(category.__dict__), ensure_ascii=False) + ",\n"
            f.write(line)

        tag.click()
        # 跳转第一题
        driver.find_element_by_link_text('第一题').click()

        # 题目总数
        total_page_num = driver.find_element_by_xpath("//td[@class='td2']").text
        total_page_num = int(re.findall(r'\d+', total_page_num)[0])

        for step in xrange(total_page_num - 1):
            # 当前题目id
            current_page_num = driver.find_element_by_id('currentPage').get_attribute('value')
            # print current_page_num
            # print type(current_page_num)

            driver.find_element_by_link_text('下一题').click()
            print '爬取:>>>Group:%s<<>>Category:%s<<>>ID:%s' % (GROUP_ID, CATEGORY_ID, step)
            get_problem(driver, group=GROUP_ID, category=CATEGORY_ID, num=current_page_num)
