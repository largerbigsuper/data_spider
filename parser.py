#coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import json

import re

from tools import image_downloader

INDEX = 1


def get_problem(driver, group=1, category=1, num=1):
    # 提取题目
    # 标题
    title = driver.find_element_by_class_name('headtop').text
    # print title

    # 是否为单选
    # print type('单选题')
    # print type(title)

    if unicode('单选题', 'utf-8') in title:
        radio = 0
    elif unicode('判断题', 'utf-8') in title:
        radio = 1
    elif unicode('多选题', 'utf-8') in title:
        radio = 2
    else:
        radio = 3
    print radio

    # 图片地址
    images = ''
    images_list = driver.find_elements_by_xpath("//td[@class='headtop'][1]/img")
    if images_list:
        images = images_list[0].get_attribute('src')
    # images = re.sub(images, '', 'http://www.tskspx.com/')
    images_url = images
    images = images.replace('http://www.tskspx.com/', '')
    print images

    # 选项
    choice_labels = driver.find_elements_by_xpath("//table[@class='ks_st']//label")
    choices = '**'
    for label in choice_labels:
        choices += label.text + "**"
    # print choices

    # 答案
    driver.find_element_by_class_name('pbtn08').click()
    answers = driver.find_element_by_xpath("//table[@class='plxanswer2'][1]//span").text
    # print answers

    item = Item(group=group, category=category, num=num, title=title,
                choices=choices, answers=answers, images=images,
                radio=radio
                )
    print item
    # 保存记录
    # import ipdb
    # ipdb.sset_trace()
    with open('problems.txt', 'ab+') as f:
        # line = str(item) + ',\n'
        # # line = line.decode('unicode-escape')
        line = json.dumps(dict(item.__dict__), ensure_ascii=False) + ",\n"
        f.write(line)

    # 下载图片文件
    if images_url:
        image_downloader(images_url)
    global INDEX
    print '>>>>>>>>>>>>>完成第%s个记录爬取<<<<<<<<<<<<<' % INDEX
    INDEX += 1


# 构造类
class Item(object):
    """题目"""

    def __init__(self, group, category, num, title, choices, answers, images=None, radio=1):
        self.group = group
        self.categoty = category
        self.num = num
        self.title = title
        self.choices = choices
        self.answers = answers
        self.images = images
        self.radio = radio

    def __repr__(self):
        return json.dumps(self.__dict__)


class Category(object):
    """小分类"""

    def __init__(self, group, num, name):
        self.group = group
        self.num = num
        self.name = name

    def __repr__(self):
        return json.dumps(self.__dict__)
