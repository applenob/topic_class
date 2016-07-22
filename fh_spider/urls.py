#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import utils
from lxml import html
import requests
import cPickle as Pickle

feng_url = 'http://i.ifeng.com/'
res = requests.get(feng_url)
html_s = res.text.encode('utf-8')
feng_tree = html.fromstring(html_s)
# 获取一级标题列表
sub_ones = feng_tree.xpath('//div[@id="ifgNavLis"]/a')
one_items = []
# 暂时不要的一级标题
drop_ones = ["视频","房产","读书","青年",
             "彩票","小说","FM","自媒体"]
for sub_one in sub_ones:
    name = sub_one.xpath('./text()')[0]
    if name not in drop_ones:
        item = {}
        item['name'] = name
        #除去连接后面的参数
        href = sub_one.xpath('./@href')[0]
        item['href'] = href[:href.find('?')]
        one_items.append(item)
for item in  one_items:
    # utils.show_dict(item)
    import list
    list.crawl_pages(item['href'], item['name'])