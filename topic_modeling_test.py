# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 14:42:03 2019

@author: Weilong
"""

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from tqdm import tqdm

data_raw = pd.read_csv(r'\Users\Weilong\Onedrive\Purdue\CS 573\Project\youtube_data_new.csv')

data = data_raw.dropna(subset=['description'])
data = data.reset_index()
    
cateid = np.unique(data_raw.categoryId)

topic_all = np.zeros((10,len(cateid)))
columns_names = [str(e) for e in cateid]
topic_all = pd.DataFrame(topic_all, columns=columns_names)
for i in range(len(cateid)):
    c_topic = []
    des_sub = data[data.categoryId == cateid[i]].description
    vectorizer = CountVectorizer(stop_words='english')
    X = vectorizer.fit_transform(des_sub)
    terms = vectorizer.get_feature_names()

    lda = LatentDirichletAllocation(n_topics=10).fit(X)
    for topic_idx, topic in enumerate(lda.components_):
        current_topic = " ".join([terms[j] for j in topic.argsort()[:-4-1:-1]])
        c_topic.append(current_topic)
    topic_all[str(cateid[i])] = c_topic

cate_pre = []
for j in tqdm(range(len(data))):
    score_com = []
    for k1 in range(len(cateid)):
        sim_score = 0
        for k2 in range(topic_all.shape[0]):
            c = [data.description[j], topic_all[str(cateid[k1])][k2]]
            vectorizer = CountVectorizer()
            vectorizer.fit(c)
            v_c = vectorizer.transform(c).toarray()
            sim_score += cosine_similarity([v_c[0,:]],[v_c[1,:]])
        score_com.append(sim_score)
    cate_loc = score_com.index(max(score_com))
    cate_pre.append(cateid[cate_loc])

accuracy = sum(cate_pre == data.categoryId)/len(data)