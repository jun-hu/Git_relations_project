


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
nx.draw(G, with_labels=True,font_size=3, node_size=500, node_color="skyblue", pos=nx.fruchterman_reingold_layout(G),arrows=True)
plt.title("fruchterman_reingold")
 

plt.title("commiters and follower")

plt.savefig("followers.png", dpi=1000)


# In[31]:


pdf=pd.DataFrame()


follower_r = pd.Series(followers_list)
following_r = pd.Series(following_list)

from pyspark.sql.functions import col

from pyspark.sql.window import Window



followers_list_=[]
following_list_=[]

for i in range(0,len(following)) :
    #print(i,"------------------------------")
    f_list=[]
    for j in range(0,len(following[i])) :
        
        for a in range(0,len(following[i][j])) :
            #for y in range(0,len(followers2[i][j][a])):
                
            f_list.append(following[i][j][a])
    followers_list_.append(f_list)
followers_list_ 



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
        commiter2.append(commiter[i][0])
        following_r2.append(following_r[i][y])  


# In[32]:


df1 = pd.DataFrame({ 'from':commiter2, 'to':following_r2})
df1
plt.figure(figsize=(9,9))
# Build your graph
G=nx.from_pandas_edgelist(df1, 'from', 'to' , create_using=nx.DiGraph())
 
# Fruchterman Reingold
nx.draw(G, with_labels=True,font_size=8, node_size=1000, node_color="skyblue", pos=nx.fruchterman_reingold_layout(G),arrows=True)
plt.title("fruchterman_reingold")
 

plt.title("commiters and following")
plt.savefig("following.png", dpi=1000)


# In[33]:


leng = len(commiter[0][0])
foll=0 # 총 팔로워의 숫자
for i in range(0,len(commiter[0][0])) :
    foll = foll+len(followers2[0][0][i])



    
num = foll/leng
print(num)


# In[34]:


leng = len(commiter[0][0])
follw=0 # 총 팔로윙의 숫자
for i in range(0,len(commiter[0][0])) :
    follw = follw+len(following[0][0][i])



    
num1 = follw/leng
print(num1)


# In[ ]:


from matplotlib import pyplot as plt
movies = ['followers','following']
num_of_oscars = [num,num1]
xs = [i + 0.1 for i, _ in enumerate(movies)]
plt.bar(xs,num_of_oscars)
plt.ylabel('figure')
plt.title('followers and following average value')
plt.xticks([i + 0.5 for i, _ in enumerate(movies)],movies)
plt.show()


