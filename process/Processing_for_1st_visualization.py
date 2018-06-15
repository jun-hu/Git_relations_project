# coding: utf-8

# In[18]:


from pyspark.sql import SparkSession
from pyspark.sql.functions import split, explode
import pandas as pd
from pyspark.sql.functions import *

spark = SparkSession.builder.appName("Python Spark SQL basic example").config("spark.some.config.option",
                                                                              "some-value").getOrCreate()

# In[19]:


df = spark.read.json("/home/project/followinfo2.json", multiLine=True, mode="PERMISSIVE")
df = df.drop('trending')
# df.printSchema()

followers = df.select("reposWhatiSelect.meteor.commiters.followers").collect()
following = df.select("reposWhatiSelect.meteor.commiters.following").collect()
commiter = df.select("reposWhatiSelect.meteor.commiters.id").collect()

# In[20]:


followers_list = []

for i in range(0, len(followers[0][0])):
    # print(i,"------------------------------")
    f_list = []
    for j in followers[0][0][i]:

        for a in range(0, len(commiter[0][0])):
            # print(j.encode("utf-8"),"==",commiter[0][0][a].encode("utf-8"))
            if j.encode("utf-8") == commiter[0][0][a].encode("utf-8"):
                f_list.append(j)
    followers_list.append(f_list)
followers_list

# In[21]:


following_list = []

for i in range(0, len(following[0][0])):
    # print(i,"------------------------------")
    f_list = []
    for j in following[0][0][i]:

        for a in range(0, len(commiter[0][0])):
            # print(j.encode("utf-8"),"==",commiter[0][0][a].encode("utf-8"))
            if j.encode("utf-8") == commiter[0][0][a].encode("utf-8"):
                f_list.append(j)
    following_list.append(f_list)

for i in following_list:
    print(i)

# In[22]:


pdf = pd.DataFrame()
cml = pd.Series(commiter[0]['id'])
pdf['commiter'] = cml.values
frl = pd.Series(followers[0]['followers'])
pdf['follower'] = frl.values
fgl = pd.Series(following[0]['following'])
pdf['following'] = fgl.values

follower_r = pd.Series(followers_list)
pdf['follower_r'] = follower_r.values
following_r = pd.Series(following_list)
pdf['following_r'] = following_r.values

df = spark.createDataFrame(pdf)
from pyspark.sql.functions import col

from pyspark.sql.window import Window

w = Window().orderBy("commiter")
df = df.select(row_number().over(w).alias("ID"), col("*"))
df.show(40)

# In[23]:


##################################3


# In[ ]:


# In[24]:


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
        commiter1.append(commiter[0][0][i])
        follower_r1.append(follower_r[i][y])

        ########################
ab = 0

for i in range(0, len(following[0][0])):

    x = len(follower_r[i])

    for y in range(0, x):
        print(ab)
        ab = ab + 1

# In[25]:


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
        commiter2.append(commiter[0][0][i])
        following_r2.append(following_r[i][y])

        ########################

# In[26]:
