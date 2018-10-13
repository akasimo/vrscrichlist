
# coding: utf-8

# In[1]:


import pandas as pd
import requests, time, pickle, os, time
from datetime import datetime
import numpy as np


# In[2]:


def seperate_tag(x):
    if " " in x:
        return x.split(" ")[0]
    else:
        return x


# In[3]:


filename = "richlist_vrsc.plk"


# In[4]:


link = "https://dexstats.info/richlist.php?asset=VRSC"
df = pd.read_html(link)[0]


# In[6]:

print(df.columns)
if "Detail " in df.columns:
    df.drop("Detail ", axis = 1, inplace = True)
elif "Detail" in df.columns:
    df.drop("Detail", axis = 1, inplace = True)

# In[7]:


columnnames= df.columns.tolist()
for i in range(len(columnnames)):
    if columnnames[i][-1]==" ":
        columnnames[i]  = columnnames[i][:-1]
df.columns = columnnames


# In[8]:


df["Address"] = df["Address"].apply(lambda x : seperate_tag(x))
df["Date"] = datetime.now()


# In[9]:


if filename not in os.listdir():
    print ("creating blank df main")
    df_main = pd.DataFrame(columns=df.columns.tolist())
else:
    print("loading historical")
    df_main = pd.read_pickle(filename)


# In[10]:


df_merged = pd.concat([df_main, df])


# In[11]:


checkdates = df_merged.Date.unique().tolist()
checkdates.sort()


# In[12]:


def coinsum(dataframe, epoch, rank=100):
    return dataframe[(dataframe.Date.apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))==datetime.utcfromtimestamp(int(epoch/1000000000)).strftime('%Y-%m-%d %H:%M:%S')) & (dataframe.Rank <= rank)].Balance.sum()


# In[14]:


# coinsum(df_merged, checkdates[-1], rank=100)/coinsum(df_merged, checkdates[-2], rank=100)


# In[15]:


df_merged.to_pickle(filename) 

