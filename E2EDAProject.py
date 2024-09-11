#!/usr/bin/env python
# coding: utf-8

# # End To End Data Analytics Project

# #### Introduction

# The purpose of this project is to implement ETL in Python using Jupyter Notebook and then perform arithmetic operations in SQL. We begin with loading the data from Kaggle into our python script (Extract), after which we clean/"Transform" our data. Once we're satisfied with our clean data, we "Load" it into our SQL Database where we answer some important questions. 
# 
# The goal here is to understand how, in the practical world, businesses can use such a skillset to their advantage. 
# 
# It was a great learning curve for me especially, where I learnt from my mistakes and the problems that I encountered during the whole exercise. I would highly encourage anyone going through this project to critically analyze it and let me know what can be done better.
# 
# Lastly, I would like to thank Ankit for uploading such a valuable tutorial on his Youtube channel: **Ankit Bansal**. You can find many informative videos on his channel in English Language. While most of the code you'll find here is quite similar, I ran into specific problems while trying to load the data into SQL, so I had to apply a different code for it than the tutorial. My SQL version is different than the one being used in the video by Ankit, so it's possible to face some issues during this step. Nevertheless, it was a great learning curve for me while trying to figure out a solution for it, so I wouldn't be discouraged incase you face such a scenario. 

# ## -- Extract --

# In[16]:


# Import libraries

import pandas as pd
import numpy as np
import kaggle

get_ipython().system('kaggle datasets download ankitbansal06/retail-orders -f orders.csv --force')


# In[18]:


# Extract File From zip File

import zipfile
zip_ref = zipfile.ZipFile('orders.csv.zip')
zip_ref.extractall() #Extract File To dir
zip_ref.close() #Close File


# ## -- Transform --

# In[19]:


# Read Data From The File And Handle Null Values

df = pd.read_csv('orders.csv.zip')
# df.head(20) # In the ship mode column, we can see some values like Not Available, unknown etc. which we want to change to null values
df['Ship Mode'].unique() # Checking how many unique values are there in the Ship Mode column


# In[20]:


df = pd.read_csv('orders.csv.zip', na_values=['Not Available', 'unknown']) # Specifying Null Values inside the Ship Mode column
df['Ship Mode'].unique() # Checking the unique values again to see if the above line of code worked


# In[21]:


# View column names before renaming them

df.columns


# In[ ]:


# Renaming Column Names One By One (Not a good practise!)

# df.rename(columns={'Order Id': 'order_id', 'Order Date': 'order_date', 'Ship Mode': 'ship_mode', 'Segment': 'segment', 'Country': 'country', 'City': 'city', 'State': 'state', 'Postal Code': 'postal_code', 'Region': 'region', 'Category': 'category', 'Sub Category': 'sub_category', 'Product Id': 'product_id', 'cost price': 'cost_price', 'List Price': 'list_price', 'Quantity': 'quantity', 'Discount Percent': 'discount_percent'})


# In[22]:


# Renaming columns the correct way

df.columns = df.columns.str.lower() # First make them all lower case
df.columns


# In[23]:


# Replacing the space with underscore

df.columns = df.columns.str.replace(' ', '_')


# In[24]:


df.columns


# In[25]:


# Create new columns: discount, sales price and profit

df['discount'] = df['list_price']*df['discount_percent']/100
df.head()


# In[26]:


# Creating Sales Price

df['sales_price'] = df['list_price'] - df['discount']
df.head(5)


# In[27]:


# Finding the Profit

df['profit'] = df['sales_price'] - df['cost_price']
df.head(5)


# In[28]:


# Check data types

df.dtypes # We can see that the order_date column has the wrong data type


# In[29]:


# Changing Data Type of order_date column

df['order_date'] = pd.to_datetime(df['order_date'], format="%Y-%m-%d")
df.dtypes


# In[30]:


# Dropping columns cost price, list price and discount percent

df.drop(columns=['list_price', 'cost_price', 'discount_percent'], inplace=True) # The inplace=True is used to make sure that the columns are dropped from the DF permanently


# In[31]:


df.head(5)


# ## -- Load --

# In[32]:


# Loading the data into a sql server
get_ipython().system('pip install sqlalchemy')
get_ipython().system('pip install pyodbc')
get_ipython().system('pip install mysql-connector-python')
get_ipython().system('pip install pymysql')

import sqlalchemy as sal
import pymysql as pmsal
from sqlalchemy import create_engine

# Connect to Master database

#engine = sal.create_engine('mssql+pyodbc://@localhost/master?driver=SQL+Server&trusted_connection=yes')
#conn = engine.connect()

# Replace 'dialect+driver://username:password@host:port/database' with your actual connection details
username = '********'
password = '********'
host = 'localhost'  # or your specific host
port = '3306'  # default port for MySQL, change if needed
database = 'E2EDAProject'

# Creating the connection string
connection_string = f'mysql+pymysql://{username}:{password}@{host}:{port}/{database}'

# Creating the engine
engine = create_engine(connection_string)

# Test the connection
try:
    connection = engine.connect()
    print("Connection successful!")
    connection.close()
except Exception as e:
    print(f"Connection failed: {e}")


# In[ ]:


# %pip install --upgrade pandas sqlalchemy pymysql


# In[34]:


# Load the data in sql server using append option

df.to_sql("df_orders", con=engine, index=False, if_exists = "append")

