# coding: utf-8

# In[44]:


from pyspark.sql import SparkSession
from pyspark.sql.functions import split, explode
import pandas as pd
from pyspark.sql.functions import *

spark = SparkSession.builder.appName("Python Spark SQL basic example").config("spark.some.config.option",
                                                                              "some-value").getOrCreate()

# In[45]:


jsonData = spark.read.json("/home/project/outputjsons/*.json")

trendingRepos = jsonData.select(explode("trending").alias("trending"))
# trendingRepos.createOrReplaceTempView("trending")
trendingRepos.show()

# In[ ]:


# In[46]:


followers2 = trendingRepos.select(explode("trending.commiters").alias("commiters")).select(
    explode("commiters.followers").alias("followers")).select("followers.followers").alias("followers").collect()
# ollowers2

following = trendingRepos.select(explode("trending.commiters").alias("commiters")).select(
    explode("commiters.followers").alias("following")).select("following.following").alias("following").collect()
# following

commiter = trendingRepos.select(explode("trending.commiters.id")).collect()
# #commiter

# following


# In[47]:


followers_list = []

for i in range(0, len(followers2)):
    # print(i,"------------------------------")
    f_list = []
    for j in range(0, len(followers2[i])):

        for a in range(0, len(followers2[i][j])):
            # for y in range(0,len(followers2[i][j][a])):

            f_list.append(followers2[i][j][a])
    followers_list.append(f_list)
followers_list

# In[ ]:


# In[49]:


##################################3


# In[50]:


following_list = []

for i in range(0, len(following)):
    # print(i,"------------------------------")
    f_list = []
    for j in range(0, len(following[i])):

        for a in range(0, len(following[i][j])):
            # for y in range(0,len(followers2[i][j][a])):

            f_list.append(following[i][j][a])
    following_list.append(f_list)
following_list

####


# In[51]:


pdf = pd.DataFrame()

follower_r = pd.Series(followers_list)
following_r = pd.Series(following_list)

from pyspark.sql.functions import col

from pyspark.sql.window import Window

# In[27]:


leng = (0, len(following[0][0]))

ab = 0
commiter

commiter1 = []
follower_r1 = []

for i in range(0, len(following[0][0])):

    x = len(follower_r[i])

    for y in range(0, x):
        print(ab)
        ab = ab + 1
        commiter1.append(commiter[i][0])
        follower_r1.append(follower_r[i][y])

        ########################
ab = 0

for i in range(0, len(following[0][0])):

    x = len(follower_r[i])

    for y in range(0, x):
        print(ab)
        ab = ab + 1

# In[28]:


leng = (0, len(following[0][0]))

ab = 0
commiter

commiter2 = []
following_r2 = []

for i in range(0, len(following[0][0])):

    x = len(following_r[i])

    for y in range(0, x):
        print(ab)
        ab = ab + 1
        commiter2.append(commiter[i][0])
        following_r2.append(following_r[i][y])

        ########################

# In[29]:


# In[30]:


topic_ = []

df = spark.read.json("/home/project/outputjson.json", multiLine=True, mode="DROPMALFORMED")

df = df.drop('selectedRepo')

topic = df.select("trending.topic").collect()

for x in range(0, len(topic[0][0])):

    xx = len(topic[0][0][x])

    for y in range(0, xx):
        topic_.append(topic[0][0][x][y])

w_count = {}

for lst in topic_:

    try:
        w_count[lst] += 1

    except:
        w_count[lst] = 1

print w_count

# In[43]:


import json
import ast

lang_name = []
lang_per = []

comm = jsonData.select("trending").select("trending.language").toJSON().first()

lang_dict = ast.literal_eval(comm.encode("utf-8"))
for item in lang_dict['language']:
    lang_name.extend(item.keys())
    lang_per.extend(item.values())

w_count_ = {}

for lst in lang_name:

    try:
        w_count_[lst] += 1

    except:
        w_count_[lst] = 1

print w_count_




