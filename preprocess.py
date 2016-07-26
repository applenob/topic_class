# coding=utf-8
'''
中文文本预处理
'''
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction import FeatureHasher
import jieba
import re
import numpy as np
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class Preprocessor(object):
    """中文文本数据预处理"""

    def __init__(self):
        super(Preprocessor, self).__init__()

    def preprocess(self, text):
        """数据预处理的方法,中文分词去停用词，
        返回保存词的list"""

        # 结巴加载用户字典
        jieba.load_userdict("dict.txt")
        # 用户自定义停用词词组
        user_stopwords = ['\n', '\r\n', ' ', '\t', '时间', '年', '月', '日', '号',
                          '图', '图片', '中', '?','说', '称','时']
        # 常用的停用词加载
        with open("stopwords.txt") as file:
            stopwords = file.readlines()
            stopwords = [word.replace('\n', '') for word in stopwords]
        # 分词
        line_words = jieba.cut(text)
        # 筛除停用词,数字也去掉
        words = [word for word in line_words if word not in stopwords and word not in user_stopwords
                 and not re.match('\d+', word)]
        return ' '.join(words)

    def calc_tfidf(self, texts):
        '''计算中文文本的tf-idf矩阵
        texts的格式类似为：
        texts=[
            u'我 来到 北京 清华大学',#第一类文本切词后的结果，词之间以空格隔开
            u'他 来到 了 网易 杭研 大厦',#第二类文本的切词结果
            u'小明 硕士 毕业 与 中国 科学院',#第三类文本的切词结果
            u'我 爱 北京 天安门'
           ]
        '''
        vectorizer = CountVectorizer()  # 该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
        count_texts = vectorizer.fit_transform(texts)
        #只使用tf
        tf_transformer = TfidfTransformer(use_idf=False).fit(count_texts)
        ti_texts = tf_transformer.transform(count_texts)
        return ti_texts

    def calc_count_vectorize(self, texts):
        '''计算词频矩阵，texts格式同calc_tfidf'''
        vectorizer = CountVectorizer()  # 该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
        count_texts = vectorizer.fit_transform(texts)
        return count_texts

    def calc_hash_trick(self,texts,n_fs):
        fh = FeatureHasher(n_features=n_fs, non_negative=True, input_type='string')
        hash_text = fh.fit_transform(texts)
        return hash_text

    def test(self):
        texts = []
        import mysql.connector
        conn = mysql.connector.connect(user='root', password='123456', database='fenghuang', use_unicode=True)
        cursor = conn.cursor()
        try:
            cursor.execute("select content from arts limit 1,5;")
        except Exception as e:
            print e
        for rec in cursor.fetchall():
            texts.append(rec[0])
        conn.commit()
        cursor.close()
        conn.close()

        prepro = Preprocessor()
        words_list = []
        for text in texts:
            words = prepro.preprocess(text)
            words_list.append(words)
        print prepro.calc_count_vectorize(words_list)
        print type(prepro.calc_tfidf(words_list))

    def clean_and_cut(self):
        sys.stderr.write("preprocessing data...\n\n")
        prepro = Preprocessor()
        import mysql.connector
        conn = mysql.connector.connect(user='root', password='123456', database='fenghuang', use_unicode=True)
        cursor = conn.cursor()
        try:
            # cursor.execute("select content,class from arts where !isNull(content) and class!='新闻';")
            cursor.execute("select content,id from "
                           "arts where !isNull(content) and isNull(final_cut);")  # 只处理还没处理的数据
            # cursor.execute("select content,id from arts where !isNull(content);")  # 处理全部有content，在数据清洗的方式改变的情况下使用
        except Exception as e:
            print e
        for rec in cursor.fetchall():
            words = prepro.preprocess(rec[0])
            try:
                cursor.execute("UPDATE arts SET final_cut = '%s' WHERE id = '%s';" % (words, rec[1]))
                conn.commit()
            except Exception as e:
                print e
        cursor.close()
        conn.close()

    def get_tag(self):
        from snownlp import SnowNLP
        prepro = Preprocessor()
        import mysql.connector
        conn = mysql.connector.connect(user='root', password='123456', database='fenghuang', use_unicode=True)
        cursor = conn.cursor()
        try:
            cursor.execute("select final_cut,id from arts where !isNull(final_cut) and isNull(tags);")  # 只处理还没处理的数据
        except Exception as e:
            print e
        for rec in cursor.fetchall():
            s = SnowNLP(rec[0])
            key_words = ' '.join(s.keywords(5))
            try:
                cursor.execute("UPDATE arts SET tags = '%s' WHERE id = '%s';" % (key_words, rec[1]))
                conn.commit()
            except Exception as e:
                print e
        cursor.close()
        conn.close()


if __name__ == '__main__':
    prepro = Preprocessor()
    prepro.clean_and_cut()
    # prepro.get_tag()
