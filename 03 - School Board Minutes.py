#!/usr/bin/env python
# coding: utf-8

# # School Board Minutes
# 
# Scrape all of the school board minutes from http://www.mineral.k12.nv.us/pages/School_Board_Minutes
# 
# Save a CSV called `minutes.csv` with the date and the URL to the file. The date should be formatted as YYYY-MM-DD.
# 
# **Bonus:** Download the PDF files
# 
# **Bonus 2:** Use [PDF OCR X](https://solutions.weblite.ca/pdfocrx/index.php) on one of the PDF files and see if it can be converted into text successfully.
# 
# * **Hint:** If you're just looking for links, there are a lot of other links on that page! Can you look at the link to know whether it links or minutes or not? You'll want to use an "if" statement.
# * **Hint:** You could also filter out bad links later on using pandas instead of when scraping
# * **Hint:** If you get a weird error that you can't really figure out, you can always tell Python to just ignore it using `try` and `except`, like below. Python will try to do the stuff inside of 'try', but if it hits an error it will skip right out.
# * **Hint:** Remember the codes at http://strftime.org
# * **Hint:** If you have a date that you've parsed, you can use `.dt.strftime` to turn it into a specially-formatted string. You use the same codes (like %B etc) that you use for converting strings into dates.
# 
# ```python
# try:
#   blah blah your code
#   your code
#   your code
# except:
#   pass
# ```
# 
# * **Hint:** You can use `.apply` to download each pdf, or you can use one of a thousand other ways. It'd be good `.apply` practice though!

# In[1]:


import requests
import pandas as pd
from selenium import webdriver
driver = webdriver.Chrome()
driver.get("http://www.mineral.k12.nv.us/pages/School_Board_Minutes")


# In[5]:


page = driver.find_element_by_id('livesite-page-content-left')


# In[39]:


minute_page2 = page.find_elements_by_tag_name('p')[4:-1]


# In[64]:


mins = []
for item in minute_page2:
    date = item.text.strip()
#     print(date)
    try:
        url = item.find_element_by_tag_name('a').get_attribute('href')
        mins.append({
            'date': date,
            'url': url
        })
    except:
        pass


# In[66]:


df = pd.DataFrame(mins)


# In[68]:


df.head()


# In[75]:


df['date'] = df['date'].astype('string')


# In[78]:


import datetime as dt


# In[85]:


df['the_date'] = pd.to_datetime(df.date, format='%B %d, %Y').dt.strftime("%Y-%m-%d")


# In[90]:


df.head()


# In[91]:


del df['date']


# In[92]:


df.head()


# In[107]:


df.to_csv('minutes.csv', index=False)


# ### Getting pdfs

# In[99]:


# row is not defined. we are creating it now
def scrape_pdf(df):
    print(df['url'])
    print('--')


# In[100]:


df.apply(scrape_pdf, axis=1)


# In[ ]:


# i'm not sure how to use selenium to download a pdf to display in the dataframe

