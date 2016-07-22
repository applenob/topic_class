#coding=utf-8
import requests
from lxml import html
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def get_detail(url):
    content = ''
    try:
        res = requests.get(url)
        res_tree = html.fromstring(res.text)
        # title = res_tree.xpath('//h1/text()')[0]
        ps = res_tree.xpath('//div[@class="acTxt wrap"]/p')
        for p in ps:
            texts = ''.join(p.xpath('.//text()'))
            # print texts.encode(errors='ignore')
            content += texts

        if content == '': #如果这样爬取的页面没有内容，推测是图片类网页
            lis = res_tree.xpath('//*[@id="picTxt"]/ul/li')
            for li in lis:
                try:
                    content+=li.xpath('./p/text()')[0]
                except Exception as ex:
                    print ex
    except Exception as e:
        print e
        print url
    return content.replace("'",r"\'")  #解决文本本身含有 ' 的情况

def update_content():
    import mysql.connector
    conn = mysql.connector.connect(user='root', password='123456', database='fenghuang', use_unicode=True)
    cursor = conn.cursor()
    try:
        cursor.execute("select url from arts where isNull(content);")
    except Exception as e:
        print e
    all_rec = cursor.fetchall()
    # 对所有没有内容的记录
    for rec in all_rec:
        url = rec[0]
        content = get_detail(url)
        # print "url:",url
        # print "content:",content
        if content != '':
            try:
                cursor.execute("UPDATE arts SET content = '%s' WHERE url = '%s'; "
                               % (content, url))
                conn.commit()
            except Exception as e:
                print e
                print "UPDATE arts SET content = '%s' WHERE url = '%s'; "% (content, url)
        else:
            print "content is null ..."
            print url
    cursor.close()
    conn.close()

def save_content_to_mysql(url,content):
    import mysql.connector
    conn = mysql.connector.connect(user='root', password='123456', database='fenghuang', use_unicode=True)
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE arts SET content = '%s' WHERE url = '%s'; "
                       % (content,url))
    except Exception as e:
        print e
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == '__main__':
    # url = 'http://ihistory.ifeng.com/49403253/news.shtml'
    # content = get_detail(url)
    update_content()