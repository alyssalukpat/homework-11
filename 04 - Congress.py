#!/usr/bin/env python
# coding: utf-8

# # Scraping one page per row
# 
# Let's say we're interested in our members of Congress, because who isn't? Read in `congress.csv`.

# In[1]:


import pandas as pd
df = pd.read_csv("congress.csv")


# In[4]:


df.head()


# # Let's scrape one
# 
# The `slug` is the part of the URL that's particular to that member of Congress. So `/james-abdnor/A000009` really means `https://www.congress.gov/member/james-abdnor/A000009`.
# 
# Scrape his name, birthday, party, whether he's currently in congress, and his bill count (don't worry if the bill count is dirty, you can clean it up later).

# In[5]:


import requests
from bs4 import BeautifulSoup


# In[6]:


response = requests.get('https://www.congress.gov/member/james-abdnor/A000009')
doc = BeautifulSoup(response.text)


# In[39]:


import re


# In[42]:


name_text


# In[46]:


name_html = doc.find(class_='legDetail')
name_text = name_html.text.strip()
name_finder = r"^(.*) \("
name = re.findall(name_finder,name_text)
name


# In[38]:


birthday = doc.find(class_='birthdate')
birthday.text.strip()


# In[24]:


congress_term = doc.find(class_='legDetail').find_all('span')[1]
congress_term.text.strip()


# In[52]:


bills = doc.find(class_="results-number").text.strip()
bill_num = r"of (.*)$"
total_bills = re.findall(bill_num,bills)
total_bills


# # Build a function
# 
# Write a function called `scrape_page` that makes a URL out of the the `slug`, like we're going to use `.apply`.

# In[55]:


def scrape_page(df):
    slug = df['slug']
    print(f'https://www.congress.gov/member/{slug}')


# In[56]:


df.apply(scrape_page, axis=1)


# # Do the scraping
# 
# Rewrite `scrape_page` to actually scrape the URL. You can use your scraping code from up above. Start by testing with just one row (I put a sample call below) and then expand to your whole dataframe.
# 
# Save the results as `scraped_df`.
# 
# * **Hint:** Be sure to use `return`!
# * **Hint:** Make sure you return a `pd.Series`

# In[88]:


def scrape_page(df):
    slug = df['slug']
    url = f'https://www.congress.gov/member/{slug}'
    response = requests.get(url)
    doc = BeautifulSoup(response.text)

    name_html = doc.find(class_='legDetail')
    name_text = name_html.text.strip()
    name_finder = r"^(.*) \("
    name = re.findall(name_finder,name_text)
    for item in name:
        official_name = item
    
    birthday = doc.find(class_='birthdate')
    official_birthday = birthday.text.strip()

    congress_term = doc.find(class_='legDetail').find_all('span')[1]
    official_congress_term = congress_term.text.strip()
    
    bills = doc.find(class_="results-number").text.strip()
    bill_num = r"of (.*)$"
    total_bills = re.findall(bill_num,bills)
    for item in total_bills:
        official_total_bills = item

    data = {}
    data['url'] = url
    data['name'] = official_name
    data['birthday'] = official_birthday
    data['congress_term'] = official_congress_term
    data['total_bills'] = official_total_bills
    
    
    # sends it to df.apply(scrape_lyrics, axis=1)
    # adding pd.Series turns it into a dataframe
    return pd.Series(data)


# In[89]:


# Test with this
scrape_page({'slug': 'neil-abercrombie/A000014'})


# In[90]:


congress = df.apply(scrape_page, axis=1)


# In[102]:


# remove comma from total_bills column
congress['total_bills'].replace( { r"," : '' }, inplace= True, regex = True)


# In[103]:


congress.head()


# In[105]:


congress.total_bills.astype(int)


# ## Join with your original dataframe
# 
# Join your new data with your original data, adding the `_scraped` suffix on the new columns. You can use either `.join` or `.merge`, but be sure to read the docs to know the difference!

# In[ ]:


# Sorry Soma but the function took FOREVER to run and I didn't realize we'd be merging with the original df
# so I had the function find the name again
# so everything is in the new df already :)


# ## Save it
# 
# Save your combined results to `congress-plus-scraped.csv`.

# In[106]:


congress.to_csv('congress-plus-scraped.csv', index=False)


# In[ ]:




