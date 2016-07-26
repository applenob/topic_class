#coding=utf-8
from sklearn.base import TransformerMixin
from nltk import word_tokenize
from sklearn.feature_extraction import DictVectorizer
import sklearn.naive_bayes as nb
from sklearn.cross_validation import cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.multiclass import OneVsRestClassifier
import numpy as np

class NLTKBOW(TransformerMixin):
    def fit(self,X,y=None):
        return self
    def transform(self,X):
        return [{word:True for word in word_tokenize(document)}
                    for document in X]

def do_pipeline(X,y):
    pipeline = Pipeline([('bag_of_words',NLTKBOW()),
                         ('vectorizer',DictVectorizer()),
                         ('naive-bayes',nb.MultinomialNB(alpha=0.02))
                         ])
    scores = cross_val_score(pipeline,X=X,y=y,cv=5,scoring='f1_weighted')
    print scores
    print("Score(f1): {:.3f}".format(np.mean(scores)))
    return pipeline

def pipeline_debug(pipeline,X,y):
    model = pipeline.fit(X,y)
    mnb = model.named_steps['naive-bayes'] #通过named_steps返回pipeline的部件
    feature_probabilities = mnb.feature_log_prob_
    top_features = np.argsort(-feature_probabilities[1])[:100]
    dv = model.named_steps['vectorizer']
    for i, feature_index in enumerate(top_features):
        print i, dv.feature_names_[feature_index],\
            np.exp(feature_probabilities[1][feature_index])



if __name__ == '__main__':
    arts = []
    art1 = '今天 今天 天气 不错 我们 愉快 玩耍'
    art2 = '今天 锻炼 舒服 天气 一般'
    art3 = '天气 糟糕'
    arts.append(art1)
    arts.append(art2)
    arts.append(art3)
    y = [1,1,0]
    nlt = NLTKBOW()
    print word_tokenize(art1)
    bw = nlt.transform(arts)
    dv = DictVectorizer()
    dv_x = dv.fit_transform(bw,y)
    print dv_x.toarray()
    print
