# -*- coding:utf-8 -*-
import re
import urllib2
import os.path


def image_downloader(url):
    """图片下载"""
    'http://www.tskspx.com/yhpicture/nj_cz_t2_tp88.jpg'

    data = urllib2.urlopen(url).read()
    prefix = 'http://www.tskspx.com/'
    suffix = re.sub(prefix, '', url)
    BASE_DIR = os.path.dirname(os.path.abspath('__file__'))
    path = os.path.join(BASE_DIR, 'images/' + suffix)
    dir_path = os.path.dirname(path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    with open(path, 'wb') as f:
        f.write(data)

    print '图片下载完成:%s' % str(url)


if __name__ == '__main__':
    image_downloader('http://www.tskspx.com/yhpicture/nj_cz_t2_tp88.jpg')
