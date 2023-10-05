#!/usr/bin/env python
# coding: utf-8

# ## Business Required Data
# 
# 
# 

# In[66]:


df = spark.read.load('abfss://stg@adlscasestudystgacc.dfs.core.windows.net/CallRecords/part-00000-509aea1d-0609-4837-8490-8491c1614cbc-c000.snappy.parquet', format='parquet')
display(df.limit(5))


# In[109]:


from pyspark.sql.functions import *
df.columns


# In[68]:


df.createOrReplaceTempView("CallRecords")


# In[89]:


Total_Duration_DF=spark.sql("select  CustomerID ,sum(Duration) as TotalDuration from CallRecords group by CustomerID order by CustomerID ")
Total_Duration_DF.show(5)


# In[79]:


Total_Duration_DF.printSchema()


# In[80]:


Total_Duration_DF.createOrReplaceTempView("TotalDurationview")


# In[135]:


df1 = spark.read.load('abfss://stg@adlscasestudystgacc.dfs.core.windows.net/customer_usage_data/part-00000-7f4b7d51-e26c-47a1-8205-9e302f780bcf-c000.snappy.parquet', format='parquet')
#df1.printSchema()
df1.show(5)


# In[136]:


df1.createOrReplaceTempView("customer_usage_data")


# In[118]:


Customer_Total_usage_data=spark.sql("select c.CustomerID , c.Date, c.DataUsage, c.VoiceMinutes, c.TextMessages, t.TotalDuration, (c.VoiceMinutes+t.TotalDuration) TotalVoiceMinutes from customer_usage_data c join TotalDurationview t on c.CustomerID=t.CustomerID")


# In[119]:


Customer_Total_usage_data.write.save('abfss://processed@adlscasestudystgacc.dfs.core.windows.net/customer_usage_data')


# In[120]:


display(Customer_Total_usage_data)


# In[122]:


billing = spark.read.load('abfss://stg@adlscasestudystgacc.dfs.core.windows.net/billing_history8/part-00000-6059233d-3d8f-421f-9e35-956ee75e66d1-c000.snappy.parquet', format='parquet')
display(billing)


# In[123]:


billing.createOrReplaceTempView("Billing")


# In[124]:


MergeDF=billing.join(Customer_Total_usage_data,on='CustomerID',how='inner')


# In[128]:


MergeDF.columns


# In[139]:


MergeDF.createOrReplaceTempView("merge")


# In[150]:


Billing_history=spark.sql("select CustomerID,BillingAmount,PaymentDate, OutstandingBalance,(DataUsage*0.1 + VoiceMinutes*0.01 +TextMessages*0.1) as Payment_Amount from merge ")


# In[151]:


Billing_history.show()


# In[153]:


Billing_history.createOrReplaceTempView("Final_merge")


# In[162]:


payment_calculation=spark.sql("select CustomerID,BillingAmount,PaymentDate, OutstandingBalance,Payment_Amount, round(((OutstandingBalance)+Payment_Amount),2) as Total_Payable from Final_merge ")
payment_calculation.columns


# In[165]:


Billing_history9=payment_calculation.select('CustomerID', 'PaymentDate', 'OutstandingBalance', 'Total_Payable')
Billing_history9.printSchema()


# In[168]:


Billing_history9=Billing_history9.withColumn("OutstandingBalance",lit(0))


# In[169]:


Billing_history9.show()


# In[176]:


Billing_history9=Billing_history9.withColumn("PaymentDate",lit("2023-09-29"))


# In[177]:


Billing_history9.show()


# In[184]:


Billing_history9.write.save('abfss://processed@adlscasestudystgacc.dfs.core.windows.net/Billing_history9')


# In[ ]:




