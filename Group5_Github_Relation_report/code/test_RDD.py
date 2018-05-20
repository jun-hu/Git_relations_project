
# coding: utf-8

# In[25]:


from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext
conf = SparkConf().setAppName("miniProject").setMaster("local[*]")
sc = SparkContext.getOrCreate(conf)
sqlcontext = SQLContext(sc)


# In[26]:


orderHeader = sc.textFile("hdfs:///user/data/SalesLTSalesOrderHeader.txt")
customer = sc.textFile("hdfs:///user/data/SalesLTCustomer.txt")


# In[27]:


customer_header = customer.first()
customer_rdd = customer.filter(lambda line: line != customer_header)

orderHeader_header = orderHeader.first()
orderHeader_rdd = orderHeader.filter(lambda line: line != orderHeader_header)


# In[28]:


import time
start_time = time.time()


customer_rdd1 = customer_rdd.map(lambda line: (line.split("\t")[0], #CustomerID
                                               line.split("\t")[7]  #CompanyName
                                              ))
orderHeader_rdd1 = orderHeader_rdd.map(lambda line: (line.split("\t")[10], #CustomerID
                                                     (line.split("\t")[0], #SalesOrderID
                                                      float(line.split("\t")[-4]) # TotalDue
                                                     )))
invoice1 = customer_rdd1.join(orderHeader_rdd1)
invoice1.takeOrdered(10, lambda x: -x[1][1][1])


# In[29]:


import pandas as pd
top10 = invoice1.takeOrdered(10, lambda x: -x[1][1][1])
companies = [x[1][0] for x in top10]
total_due = [x[1][1][1] for x in top10]
top10_dict = {"companies": companies, "total_due":total_due}
top10_pd = pd.DataFrame(top10_dict)


# In[30]:


address = sc.textFile("hdfs:///user/data/SalesLTSalesOrderHeader.txt")
customer_address = sc.textFile("hdfs:///user/data/SalesLTSalesOrderHeader.txt")
customer_address.first()


# In[31]:


address.first()


# In[32]:


address_header = address.first()
address_rdd = address.filter(lambda line: line != address_header )
customer_address_header = customer_address.first()
customer_address_rdd = customer_address.filter(lambda line: line != customer_address_header)


# In[33]:


customer_address_rdd1 = customer_address_rdd.filter(lambda line: line.split("\t")[2] =="Main Office").map(lambda line: (line.split("\t")[0],     #CustomerID
                                                               line.split("\t")[1],    #AddressID
                                                               ))  

address_rdd1 = address_rdd.map(lambda line: (line.split("\t")[0], #AddressID
                                                               (line.split("\t")[1],  #AddressLine1
                                                                 line.split("\t")[3], #City
                                                                 line.split("\t")[4],  #StateProvince
                                                                  line.split("\t")[5] #CountryRegion
                                                               )))


# In[34]:


rdd = customer_rdd1.join(orderHeader_rdd1).join(customer_address_rdd1).map(lambda line: (line[1][1], # AddressID
                                                                                        (line[1][0][0], # Company
                                                                                        line[1][0][1][0],# SalesOrderID
                                                                                        line[1][0][1][1]# TotalDue
                                                                                        )))
final_rdd = rdd.join(address_rdd1)


# In[35]:


final_rdd2 = final_rdd.map(lambda line: (line[1][0][0],                    # company
                                        float(line[1][0][2]),              # TotalDue
                                        line[1][1][0],                     # Address 1
                                        line[1][1][1],                     # City
                                        line[1][1][2],                     # StateProvince
                                        line[1][1][3]                      # CountryRegion
                                            ))


# In[36]:


final_rdd2.takeOrdered(10, lambda x: -x[1])


# In[37]:


customer_header = customer.first()
customer_rdd = customer.filter(lambda line: line != customer_header)

orderHeader_header = orderHeader.first()
orderHeader_rdd = orderHeader.filter(lambda line: line != orderHeader_header)


# In[38]:


customer_rdd1 = customer_rdd.map(lambda line: (line.split("\t")[0], #CustomerID
                                              (line.split("\t")[3], #FirstName
                                               line.split("\t")[5] #LastName
                                              )))

orderHeader_rdd1 = orderHeader_rdd.map(lambda line: (line.split("\t")[10], # CustomerID
                                                    (line.split("\t")[0],  # SalesOrderID
                                                     line.split("\t")[-4]   # TotalDue
                                                    )))


# In[39]:


joined = customer_rdd1.leftOuterJoin(orderHeader_rdd1)
NonNulls = joined.filter(lambda line: line[1][1]!=None)
Nulls = joined.filter(lambda line: line[1][1]==None)


# In[40]:


NonNulls.take(5)


# In[41]:


NonNulls2 = NonNulls.map(lambda line: (line[0], line[1][0][0],line[1][0][1], line[1][1][0], float(line[1][1][1])))
NonNulls2.first()


# In[42]:


Nulls.take(5)


# In[43]:


Nulls2 = Nulls.map(lambda line: (line[0], line[1][0][0],line[1][0][1], "NULL", "NULL"))


# In[44]:


union_rdd = NonNulls2.union(Nulls2)


# In[45]:


customer_header = customer.first()
customer_rdd = customer.filter(lambda line: line != customer_header)

customer_address_header = customer_address.first()
customer_address_rdd = customer_address.filter(lambda line: line != customer_address_header)
customer_rdd1 = customer_rdd.map(lambda line: (line.split("\t")[0],  #CustomerID
                                              (line.split("\t")[3],  #FirstName
                                              line.split("\t")[5],  #LastName
                                              line.split("\t")[7],  #CompanyName
                                              line.split("\t")[9],  #EmailAddress
                                              line.split("\t")[10] #Phone
                                              )))

customer_address_rdd1 = customer_address_rdd.map(lambda line: (line.split("\t")[0],line.split("\t")[1]))


# In[46]:


joined = customer_rdd1.leftOuterJoin(customer_address_rdd1)


# In[47]:


print("start_time", start_time) #출력해보면, 시간형식이 사람이 읽기 힘든 일련번호형식입니다.
print("--- %s seconds ---" %(time.time() - start_time))

