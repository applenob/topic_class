#coding=utf-8
import requests
import utils
import time
from datetime import datetime

def crawl_one_page(url,base_url):
    res = requests.get(url=url)
    str = res.text.encode('utf-8')
    if str=='getListDatacallback([]);':
        # 已经爬不到东西了
        return None
    str_n = str[str.find('(') + 1:-2]
    str_n = str_n.replace('null', 'None')
    # print str_n
    dics = eval(str_n)
    items = []
    # print len(dics)
    for one in dics:
        item = {}
        item['title'] = utils.part_ustr_to_str(one['title'])
        page_url = one['pageUrl']
        item['url'] = base_url+page_url
        item['collect_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        item['id'] = page_url[page_url.find('/')+1:page_url.find('/n')]
        items.append(item)
    return items

def save_items_to_mysql(items,class_name):
    import mysql.connector
    conn = mysql.connector.connect(user='root', password='123456', database='fenghuang', use_unicode=True)
    cursor = conn.cursor()
    for item in items:
        try:
            cursor.execute("insert into arts ( collect_time, id, title, class, url) values('%s','%s','%s','%s','%s');"
                           % (item['collect_time'], item['id'], item['title'],class_name,item['url']
                              ))
        except Exception as e:
            print e
            print item
    conn.commit()
    cursor.close()
    conn.close()

def crawl_pages(base_url,class_name,num):
    urls = [base_url + '/%d_%d/data.shtml' % (num,i) for i in range(20)]
    for url in urls:
        items = crawl_one_page(url,base_url)
        if not items :
            break
        save_items_to_mysql(items, class_name)
        # time.sleep(2)


if __name__ == '__main__':
    # base_url = 'http://inews.ifeng.com'
    # crawl_pages(base_url,'新闻')
    one_dic = [{'href' : 'http://inews.ifeng.com',
                    'name' : '新闻',
                    'num' : 32},
                {'href': 'http://ifinance.ifeng.com',
                    'name': '财经',
                    'num': 20},
                {'href' : 'http://ient.ifeng.com',
                    'name' : '娱乐',
                    'num' : 14},
                {'href' : 'http://isports.ifeng.com',
                    'name' : '体育',
                    'num' : 33},
                {'href' : 'http://imil.ifeng.com',
                    'name' : '军事',
                    'num' : 20},
                # {'href':  'http://i.ifeng.com/auto/autoi/',
                #     'name':'汽车'},
                {'href' : 'http://ifashion.ifeng.com',
                    'name' : '时尚',
                    'num': 11},
                {'href' : 'http://itech.ifeng.com',
                    'name' : '科技',
                    'num': 7},
                {'href' : 'http://ihistory.ifeng.com',
                    'name' : '历史',
                    'num' : 21},

                # {'href':  'http://g.ifeng.com/',
                #                 'name':  '游戏'}
    ]
    for item in one_dic:
        crawl_pages(item['href'], item['name'], item['num'])

