# coding=utf-8
'''对数据做一些统计观察'''

import jieba
import sys
from collections import Counter

def top_words_per_class(class_name):
    '''统计每种类别出现的高频词'''
    sys.stderr.write("preprocessing data...\n\n")
    import mysql.connector
    conn = mysql.connector.connect(user='root', password='123456', database='fenghuang', use_unicode=True)
    cursor = conn.cursor()
    all_words = []
    try:
        cursor.execute("select final_cut from arts where !isNull(final_cut) and class='%s';"%class_name)
    except Exception as e:
        print e
    for rec in cursor.fetchall():
        words = rec[0].split(' ')
        all_words.extend(words)
    print '一共有%d个词'%len(all_words)
    counter = Counter(all_words)
    words = counter.most_common(20)
    for word in words:
        print word[0],' : ',word[1]
    cursor.close()
    conn.close()

if __name__ == '__main__':
    import main
    catedict = main.get_catedict()
    for class_name in catedict:
        print class_name
        top_words_per_class(class_name)