
# coding: utf-8

# In[1]:


from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext
conf = SparkConf().setAppName("miniProject").setMaster("local[*]")
sc = SparkContext.getOrCreate(conf)
sqlcontext = SQLContext(sc)


# In[2]:


orderHeader = sc.textFile("hdfs:///user/data/SalesLTSalesOrderHeader.txt")
customer = sc.textFile("hdfs:///user/data/SalesLTCustomer.txt")

customer_header = customer.first()
customer_rdd = customer.filter(lambda line: line != customer_header)

orderHeader_header = orderHeader.first()
orderHeader_rdd = orderHeader.filter(lambda line: line != orderHeader_header)


# In[3]:


import time
start_time = time.time() 

customer_df = sqlcontext.createDataFrame(customer_rdd.map(lambda line: line.split("\t")),
                                        schema = customer.first().split("\t"))

orderHeader_df = sqlcontext.createDataFrame(orderHeader_rdd.map(lambda line: line.split("\t")),
                                        schema = orderHeader.first().split("\t"))


# In[4]:


joined = customer_df.join(orderHeader_df, 'CustomerID', how = "inner")
joined.select(["CustomerID", 'CompanyName','SalesOrderID','TotalDue']).orderBy("TotalDue", ascending = False).show(10, truncate = False)


# In[5]:


joined.printSchema()


# In[6]:


from pyspark.sql.functions import col, udf
from pyspark.sql.types import DoubleType
convert = udf(lambda x: float(x), DoubleType())


# In[7]:


joined2 = joined.withColumn('Total_Due',convert(col("TotalDue"))).drop("TotalDue")
joined2.dtypes[-1]  # we have created a new column with double type


# In[8]:


joined2.select(["CustomerID", 'CompanyName','SalesOrderID','Total_Due']).orderBy("Total_Due", ascending = False).show(10, truncate = False)


# In[9]:


address = sc.textFile("hdfs:///user/data/SalesLTSalesOrderHeader.txt")
customer_address = sc.textFile("hdfs:///user/data/SalesLTSalesOrderHeader.txt")
customer_address.first()

address_header = address.first()
address_rdd = address.filter(lambda line: line != address_header )
customer_address_header = customer_address.first()
customer_address_rdd = customer_address.filter(lambda line: line != customer_address_header)


# In[10]:


address_df = sqlcontext.createDataFrame(address_rdd.map(lambda line: line.split("\t")),
                                        schema = address_header.split("\t") )

customer_address_df = sqlcontext.createDataFrame(customer_address_rdd .map(lambda line: line.split("\t")),
                                        schema = customer_address_header.split("\t") )


# In[11]:


address_df.printSchema()


# In[12]:


customer_address_df.printSchema()


# In[13]:


customer_df = sqlcontext.createDataFrame(customer_rdd.map(lambda line: line.split("\t")),
                                        schema = customer.first().split("\t"))

orderHeader_df = sqlcontext.createDataFrame(orderHeader_rdd.map(lambda line: line.split("\t")),
                                        schema = orderHeader.first().split("\t"))


# In[14]:


customer_df.printSchema()


# In[15]:


orderHeader_df.printSchema()


# In[16]:


joined = customer_df.join(orderHeader_df, 'CustomerID', how = "left")
joined.select(["CustomerID", 'FirstName','LastName','SalesOrderNumber','TotalDue']).orderBy("TotalDue", ascending = False).show(10, truncate = False)


# In[17]:


joined.select(["CustomerID", 'FirstName','LastName','SalesOrderNumber','TotalDue']).orderBy("TotalDue", ascending = True).show(10, truncate = False)


# In[ ]:





# In[18]:


orderHeader_df.createOrReplaceTempView("orderHeader_table")
customer_df.createOrReplaceTempView("customer_table")

sqlcontext.sql("SELECT c.CustomerID, c.CompanyName,oh.SalesOrderID,cast(oh.TotalDue AS DECIMAL(10,4))                FROM customer_table AS c INNER JOIN orderHeader_table AS OH ON c.CustomerID=oh.CustomerID                ORDER BY TotalDue DESC LIMIT 10").show(10, truncate = False)


# In[19]:


orderHeader_df.createOrReplaceTempView("orderHeader_table")
customer_df.createOrReplaceTempView("customer_table")

sqlcontext.sql("SELECT c.CustomerID, c.FirstName,c.LastName, oh.SalesOrderID,cast(oh.TotalDue AS DECIMAL(10,4))                FROM customer_table AS c LEFT JOIN orderHeader_table AS oh ON c.CustomerID = oh.CustomerID                ORDER BY TotalDue DESC LIMIT 10").show(truncate = False)


# In[20]:





# In[21]:


print("start_time", start_time) #출력해보면, 시간형식이 사람이 읽기 힘든 일련번호형식입니다.
print("--- %s seconds ---" %(time.time() - start_time))

