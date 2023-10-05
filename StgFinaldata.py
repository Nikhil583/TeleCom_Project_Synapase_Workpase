#!/usr/bin/env python
# coding: utf-8

# ## StgFinaldata
# 
# 
# 

# ## call_records Dataset
# 

# In[7]:


call_records = spark.read.load('abfss://raw@adlscasestudystgacc.dfs.core.windows.net/call_records.csv', format='csv', header=True,inferSchema=True)
display(call_records.limit(10))

call_records.printSchema()

call_records.createOrReplaceTempView("CallRecords")

from pyspark.sql.functions import *
Filtered_Call_Records=spark.sql('select * from CallRecords where Duration >0')
display(Filtered_Call_Records)

Filtered_Call_Records.write.save('abfss://stg@adlscasestudystgacc.dfs.core.windows.net/CallRecords')


# ## complaints_data

# In[8]:


complaints_data=spark.read.csv("abfss://raw@adlscasestudystgacc.dfs.core.windows.net/complaints_data.csv",header=True,inferSchema=True)
display(complaints_data.limit(10))

complaints_data.printSchema()

complaints_data.columns

filtered_complaints_data=complaints_data.dropna(subset=['CustomerID', 'Date', 'ComplaintType', 'ResolutionTime', 'SatisfactionRating'])

display(filtered_complaints_data)

filtered_complaints_data.write.save('abfss://stg@adlscasestudystgacc.dfs.core.windows.net/ComplaintsData')


# ## __Networkmetric_Data

# In[9]:


Networkmetric_Data = spark.read.load('abfss://raw@adlscasestudystgacc.dfs.core.windows.net/network_metrics.csv', format='csv', header=True,inferSchema=True)
display(Networkmetric_Data.limit(10))

Networkmetric_Data.columns

Networkmetric_Data.createOrReplaceTempView("NetworkMetric")

Filtered_Network_Metrics=spark.sql("select * from NetworkMetric where SignalStrength <>'NA' and CallDropRate<>'NA' and DataTransferSpeed<>'NA'")

display(Filtered_Network_Metrics)

Filtered_Network_Metrics.write.save('abfss://stg@adlscasestudystgacc.dfs.core.windows.net/Network_Metrics_Data')


# ## customer_usage_data

# In[11]:


customer_usage_data = spark.read.load('abfss://raw@adlscasestudystgacc.dfs.core.windows.net/customer_usage_data.csv', format='csv',header=True,inferSchema=True)
customer_usage_data.printSchema()

customer_usage_data.write.save('abfss://stg@adlscasestudystgacc.dfs.core.windows.net/customer_usage_data')


# ## billing_history

# In[12]:


billing_history8 = spark.read.load('abfss://raw@adlscasestudystgacc.dfs.core.windows.net/billing_history8.csv', format='csv',header=True,inferSchema=True)
billing_history8.printSchema()

billing_history8.write.save('abfss://stg@adlscasestudystgacc.dfs.core.windows.net/billing_history8')


# In[ ]:




