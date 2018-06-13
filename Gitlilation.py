
# coding: utf-8

# In[18]:


from pyspark.sql import SparkSession
from pyspark.sql.functions import split, explode
import pandas as pd
from pyspark.sql.functions import *

spark = SparkSession     .builder     .appName("Python Spark SQL basic example")     .config("spark.some.config.option", "some-value")     .getOrCreate() 


# In[19]:


df=spark.read.json("/home/project/followinfo2.json", multiLine=True,mode="PERMISSIVE")
df=df.drop('trending')
#df.printSchema()

followers=df.select("reposWhatiSelect.meteor.commiters.followers").collect()
following=df.select("reposWhatiSelect.meteor.commiters.following").collect()
commiter=df.select("reposWhatiSelect.meteor.commiters.id").collect()


# In[20]:


followers_list=[]

for i in range(0,len(followers[0][0])) :
    #print(i,"------------------------------")
    f_list=[]
    for j in followers[0][0][i] :
        
        for a in range(0,len(commiter[0][0])) :
            #print(j.encode("utf-8"),"==",commiter[0][0][a].encode("utf-8"))
            if j.encode("utf-8")==commiter[0][0][a].encode("utf-8") :
                f_list.append(j)
    followers_list.append(f_list)
followers_list    


# In[21]:


following_list=[]

for i in range(0,len(following[0][0])) :
    #print(i,"------------------------------")
    f_list=[]
    for j in following[0][0][i] :
        
        for a in range(0,len(commiter[0][0])) :
            #print(j.encode("utf-8"),"==",commiter[0][0][a].encode("utf-8"))
            if j.encode("utf-8")==commiter[0][0][a].encode("utf-8") :
                f_list.append(j)
    following_list.append(f_list)


for i in following_list :
    print(i)


# In[22]:


pdf=pd.DataFrame()
cml=pd.Series(commiter[0]['id'])
pdf['commiter'] = cml.values
frl=pd.Series(followers[0]['followers'])
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




leng = (0,len(following[0][0]))

ab = 0
commiter

commiter1 = []
follower_r1 = []

for i in range(0,len(following[0][0])) :
    
    x = len(follower_r[i])
    
        
    for y in range(0,x):
        print(ab)
        ab=ab+1
        commiter1.append(commiter[0][0][i])
        follower_r1.append(follower_r[i][y])    
            
  ########################          
ab=0
    
for i in range(0,len(following[0][0])) :
    
    x = len(follower_r[i])

        
    for y in range(0,x):
        print(ab)
        ab=ab+1
        
         
        
        

  


# In[25]:


leng = (0,len(following[0][0]))

ab = 0
commiter

commiter2 = []
following_r2 = []

for i in range(0,len(following[0][0])) :
    
    x = len(following_r[i])
    
        
    for y in range(0,x):
        print(ab)
        ab=ab+1
        commiter2.append(commiter[0][0][i])
        following_r2.append(following_r[i][y])    
            
  ########################          


# In[26]:




# libraries
get_ipython().magic(u'matplotlib inline')
# libraries
# libraries
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
plt.figure(figsize=(12,12))
# Build a dataframe with your connections
df = pd.DataFrame({ 'from':commiter1, 'to':follower_r1})
df
 
# Build your graph
G=nx.from_pandas_edgelist(df, 'from', 'to', create_using=nx.DiGraph())
 
# Fruchterman Reingold
nx.draw(G, with_labels=True,font_size=8, node_size=1000, node_color="skyblue", pos=nx.fruchterman_reingold_layout(G),arrows=True)
plt.title("fruchterman_reingold")
 

plt.title("commiters and follower")

plt.savefig("followers.png", dpi=1000)


# In[27]:


df1 = pd.DataFrame({ 'from':commiter2, 'to':following_r2})
df1
plt.figure(figsize=(12,12))
# Build your graph
G=nx.from_pandas_edgelist(df1, 'from', 'to' , create_using=nx.DiGraph())
 
# Fruchterman Reingold
nx.draw(G, with_labels=True,font_size=8, node_size=1000, node_color="skyblue", pos=nx.fruchterman_reingold_layout(G),arrows=True)
plt.title("fruchterman_reingold")
 

plt.title("commiters and following")

plt.savefig("following.png", dpi=1000)


# In[28]:


jsonData = spark.read.json("/home/project/outputjsons/*.json")

trendingRepos = jsonData.select(explode("trending").alias("trending"))
#trendingRepos.createOrReplaceTempView("trending")
trendingRepos.show()


# In[29]:


leng = len(commiter[0][0])
foll=0 # 총 팔로워의 숫자
for i in range(0,len(commiter[0][0])) :
    foll = foll+len(followers[0][0][i])



    
num = foll/leng
print(num)


# In[30]:


leng = len(commiter[0][0])
follw=0 # 총 팔로윙의 숫자
for i in range(0,len(commiter[0][0])) :
    follw = follw+len(following[0][0][i])



    
num1 = follw/leng
print(num1)


# In[31]:


from matplotlib import pyplot as plt
movies = ['followers','following']
num_of_oscars = [num,num1]
xs = [i + 0.1 for i, _ in enumerate(movies)]
plt.bar(xs,num_of_oscars)
plt.ylabel('figure')
plt.title('followers and following average value')
plt.xticks([i + 0.5 for i, _ in enumerate(movies)],movies)
plt.show()


# In[32]:


############## 여기서부터는 레포지토리 토픽, 랭귀지 갯수


# In[48]:


topic_ = []

df=spark.read.json("/home/project/outputjson.json", multiLine=True,mode="DROPMALFORMED")


df=df.drop('selectedRepo')

topic=df.select("trending.topic").collect()

for x in range(0,len(topic[0][0])):
    
    xx = len(topic[0][0][x])
    
    for y in range(0,xx):
        topic_.append(topic[0][0][x][y])

w_count = {}

for lst in topic_:

    try: 
        w_count[lst] += 1
        num_[lst]= num_[lst]+1

    except: w_count[lst]=1

print w_count    


# In[52]:


import json
import ast



lang_name = []
lang_per = []


num_ = [1,1,1,1]
comm = jsonData.select("trending").select("trending.language").toJSON().first()

lang_dict = ast.literal_eval(comm.encode("utf-8"))
for item in lang_dict['language']:
    lang_name.extend(item.keys())
    lang_per.extend(item.values())
    





# In[53]:


leng = len(commiter[0][0])
foll=0 # 총 팔로워의 숫자
for i in range(0,len(commiter[0][0])) :
    foll = foll+len(followers[0][0][i])



    
num = foll/leng
print(num)




leng = len(commiter[0][0])
follw=0 # 총 팔로윙의 숫자
for i in range(0,len(commiter[0][0])) :
    follw = follw+len(following[0][0][i])



    
num1 = follw/leng
print(num1)


# In[58]:


num = [1,1,1,1]

w_count_ = {}

for lst in lang_name:

    try:
        w_count_[lst] += 1
        num[lst]= num[lst]+1

    except: w_count_[lst]=1
        
        

from matplotlib import pyplot as plt
movies = ['Go','Makefile','TypeScript','JavaScript']
num_of_oscars = [num[0],num[1],num[2],num[3]]
xs = [i + 0.5 for i, _ in enumerate(movies)]
plt.bar(xs,num_of_oscars)
plt.ylabel('figure')
plt.title('language of chart ')
plt.xticks([i + 0.5 for i, _ in enumerate(movies)],movies)
plt.show()


# In[59]:




from matplotlib import pyplot as plt
movies = ['vuido','vue','libui','desktop']
num_of_oscars = [num_[0],num_[1],num_[2],num_[3]]
xs = [i + 0.5 for i, _ in enumerate(movies)]
plt.bar(xs,num_of_oscars)
plt.ylabel('figure')
plt.title('followers and following average value')
plt.xticks([i + 0.5 for i, _ in enumerate(movies)],movies)
plt.show()

