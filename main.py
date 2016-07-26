#coding=utf-8
import jieba
import utils
from preprocess import Preprocessor
from sklearn.multiclass import OneVsRestClassifier
from sklearn.multiclass import OneVsOneClassifier
from sklearn.cross_validation import train_test_split
from sklearn.svm import SVC
from sklearn import cross_validation
import sklearn.feature_extraction
from sklearn import metrics
import sklearn.naive_bayes as nb
import sklearn.externals.joblib as jl
import time
import sys
import numpy as np
import nltk_pipeline

def get_catedict():
    '''返回分类标签和数字对应的dict'''
    import mysql.connector
    conn = mysql.connector.connect(user='root', password='123456', database='fenghuang', use_unicode=True)
    cursor = conn.cursor()
    try:
        # cursor.execute("select class from arts where class!='新闻' group by class;")
        cursor.execute("select class from arts group by class;")
    except Exception as e:
        print e
    rec_all = cursor.fetchall()
    catelist = []
    for i,rec in enumerate(rec_all):
        catelist.append([rec[0],i+1])
    catedict = dict(catelist)
    conn.commit()
    cursor.close()
    conn.close()
    return catedict

def load_data_from_mysql():
    sys.stderr.write("loading data...\n")
    texts = []
    classes = []
    catedict = get_catedict()
    import mysql.connector
    conn = mysql.connector.connect(user='root', password='123456', database='fenghuang', use_unicode=True)
    cursor = conn.cursor()
    try:
        # cursor.execute("select content,class from arts where !isNull(content) and class!='新闻';")
        cursor.execute("select final_cut,class from arts where !isNull(content) and !isNull(final_cut);")
    except Exception as e:
        print e
    for rec in cursor.fetchall():
        texts.append(rec[0])
        classes.append(int(catedict[rec[1]]))
    conn.commit()
    cursor.close()
    conn.close()
    return texts,classes

def train_and_evaluate(clf,X,Y):
    # 分离训练集和数据集
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2,random_state=0)
    sys.stderr.write("model training...\n")
    clf.fit(X_train, Y_train)
    sys.stderr.write("model training finished.\n")
    # jl.dump(clf, 'mnb.pkl')

    print "Accuracy on training set:"
    print clf.score(X_train, Y_train)
    print "Acuracy on testing set:"
    print clf.score(X_test, Y_test)
    Y_pred = clf.predict(X_test)
    print "Classification Report:"
    from sklearn import metrics
    print metrics.classification_report(Y_test, Y_pred)
    print "Confusion Matrix:"
    print metrics.confusion_matrix(Y_test, Y_pred)

def cross_vali(clf,X,Y,K=5):
    '''使用交叉验证评估模型,创建一个k-fold交叉验证，K默认为5'''
    from scipy.stats import sem
    cv = cross_validation.KFold(len(Y), n_folds=K, shuffle=True, random_state=0)
    score = cross_validation.cross_val_score(clf, X,Y,cv=cv)
    print score
    print("Mean score: {0:.3f} (+/-{1:.3f})").format(np.mean(score), sem(score))

def run_steps():
    t_s = time.time()
    clf = OneVsRestClassifier(nb.MultinomialNB(alpha=0.02))
    # clf = OneVsRestClassifier(nb.BernoulliNB(alpha=0.01))
    # clf = OneVsRestClassifier(SVC(kernel='linear', C=1))

    X_text, Y = load_data_from_mysql()

    prepro = Preprocessor()
    sys.stderr.write("preprocessing data...\n")
    # X = prepro.calc_hash_trick(texts,15000)
    X = prepro.calc_tfidf(X_text)
    # for i in range(50):
    #     print catedict.keys()[catedict.values().index(Y[-50:][i])],' ', X_text[-50:][i]
    print X.get_shape()
    train_and_evaluate(clf, X, Y)
    # cross_vali(clf, X, Y)
    t_e = time.time()
    sys.stderr.write("all using %.2f seconds.\n" % (t_e - t_s))

def run_pipeline():
    t_s = time.time()
    X, Y = load_data_from_mysql()

    pipeline = nltk_pipeline.do_pipeline(X, Y)
    nltk_pipeline.pipeline_debug(pipeline,X, Y)

    t_e = time.time()
    sys.stderr.write("all using %.2f seconds.\n" % (t_e - t_s))

if __name__ == '__main__':
    # run_steps()
    run_pipeline()