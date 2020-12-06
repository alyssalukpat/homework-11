#!/usr/bin/env python
# coding: utf-8

# # North Korean News
# 
# Scrape the North Korean news agency http://kcna.kp
# 
# Save a CSV called `nk-news.csv`. This file should include:
# 
# * The **article headline**
# * The value of **`onclick`** (they don't have normal links)
# * The **article ID** (for example, the article ID for `fn_showArticle("AR0125885", "", "NT00", "L")` is `AR0125885`
# 
# The last part is easiest using pandas. Be sure you don't save the index!
# 
# * _**Tip:** If you're using requests+BeautifulSoup, you can always look at response.text to see if the page looks like what you think it looks like_
# * _**Tip:** Check your URL to make sure it is what you think it should be!_
# * _**Tip:** Does it look different if you scrape with BeautifulSoup compared to if you scrape it with Selenium?_
# * _**Tip:** For the last part, how do you pull out part of a string from a longer string?_
# * _**Tip:** `expand=False` is helpful if you want to assign a single new column when extracting_
# * _**Tip:** `(` and `)` mean something special in regular expressions, so you have to say "no really seriously I mean `(`" by using `\(` instead_
# * _**Tip:** if your `.*` is taking up too much stuff, you can try `.*?` instead, which instead of "take as much as possible" it means "take only as much as needed"_

# ### Imports

# In[1]:


import requests
from bs4 import BeautifulSoup

from selenium import webdriver
driver = webdriver.Chrome()
driver.get("http://kcna.kp")


# ### Get heds

# In[145]:


first_left_list = []
first_heds_left = driver.find_elements_by_class_name('harticle15_subtitle')
for item in first_heds_left:
    first_left_list.append(item.text.strip())
    
first_left_list


# In[172]:


first_right_list = []

first_heds_right = driver.find_elements_by_class_name('harticle3_subtitle')
for item in first_heds_right:
    first_right_list.append(item.text.strip())
first_right_list


# In[182]:


second_heds_left = driver.find_element_by_class_name('sub_wrap2')
second_heds_left2 = second_heds_left.find_elements_by_class_name('sub_title2')
second_left_list = []

for item in second_heds_left2:
    second_left_list.append(item.text.strip())
    
second_left_list


# In[187]:


second_heds_right = driver.find_elements_by_class_name('sub_wrap2')[1]
second_heds_right2 = second_heds_right.find_elements_by_class_name('sub_title2')
second_right_list = []

for item in second_heds_right2:
    second_right_list.append(item.text.strip())
    
second_right_list


# In[205]:


third_list = []
third_heds = driver.find_elements_by_class_name('first5')[0]
third_heds2 = third_heds.find_elements_by_tag_name('a')
for item in third_heds2:
    third_list.append(item.text.strip())
    
third_list


# In[207]:


fourth_list = []
fourth_heds = driver.find_elements_by_class_name('sub_title1')
for item in fourth_heds:
     fourth_list.append(item.text.strip())
fourth_list


# In[210]:


fifth_list = []
fifth_heds = driver.find_elements_by_class_name('harticle14')[0]
fifth_heds2 = fifth_heds.find_elements_by_tag_name('a')
for item in fifth_heds2:
     #full_heds_list.append(item.text.strip())
    fifth_list.append(item.text.strip())
fifth_list


# In[211]:


all_heds = first_left_list + first_right_list + second_left_list + second_right_list + third_list + fourth_list + fifth_list


# In[215]:


len(all_heds)


# ### Get on-clicks

# In[ ]:


hleft_article
hright_sidebar sidebar_spacing // or id=sidebar_content

find_element_by_tag_name('a').get_attribute('href')


# In[ ]:


# first_heds_left
# first_heds_right
# second_heds_left2
# second_heds_right2
# third_heds2
# fourth_heds
# fifth_heds2


# In[239]:


first_left_on_clicks = []
for item in first_heds_left:
    first_left_on_clicks.append(item.find_element_by_tag_name('a').get_attribute('onclick'))
first_left_on_clicks


# In[221]:


first_right_on_clicks = []
for item in first_heds_right:
    first_right_on_clicks.append(item.find_element_by_tag_name('a').get_attribute('onclick'))


# In[220]:


second_left_on_clicks = []
for item in second_heds_left2:
    second_left_on_clicks.append(item.find_element_by_tag_name('a').get_attribute('onclick'))


# In[219]:


second_right_on_clicks = []
for item in second_heds_right2:
    second_right_on_clicks.append(item.find_element_by_tag_name('a').get_attribute('onclick'))


# In[235]:


third_on_clicks = []
for item in third_heds2:
    third_on_clicks.append(item.get_attribute('onclick'))


# In[234]:


fourth_on_clicks = []
for item in fourth_heds:
    fourth_on_clicks.append(item.find_element_by_tag_name('a').get_attribute('onclick'))


# In[237]:


fifth_on_clicks = []
for item in fifth_heds2:
    fifth_on_clicks.append(item.get_attribute('onclick'))


# ### Get article IDs

# In[76]:


import re


# In[ ]:


article ID


# In[ ]:


first_left_on_clicks
first_right_on_clicks
second_left_on_clicks
second_right_on_clicks
third_on_clicks
fourth_on_clicks
fifth_on_clicks


# In[249]:


first_left_id_list = []
first_id = r"\(\"(\w{2}\d{6})"
for item in first_left_on_clicks:
    first_left_id_list.append(re.findall(first_id,item))
    
# each one is its own list, so I'm taking it out and putting each into one master list
actual_first_left_id_list = []
for item in first_left_id_list:
    for thing in item:
        actual_first_left_id_list.append(thing)
actual_first_left_id_list


# In[251]:


first_right_id_list = []
first_id = r"\(\"(\w{2}\d{6})"
for item in first_right_on_clicks:
    first_right_id_list.append(re.findall(first_id,item))
    
# each one is its own list, so I'm taking it out and putting each into one master list
actual_first_right_id_list = []
for item in first_right_id_list:
    for thing in item:
        actual_first_right_id_list.append(thing)


# In[254]:


second_left_id_list = []
first_id = r"\(\"(\w{2}\d{6})"
for item in second_left_on_clicks:
    second_left_id_list.append(re.findall(first_id,item))
    
# each one is its own list, so I'm taking it out and putting each into one master list
actual_second_left_id_list = []
for item in second_left_id_list:
    for thing in item:
        actual_second_left_id_list.append(thing)


# In[257]:


second_right_id_list = []
first_id = r"\(\"(\w{2}\d{6})"
for item in second_right_on_clicks:
    second_right_id_list.append(re.findall(first_id,item))
    
# each one is its own list, so I'm taking it out and putting each into one master list
actual_second_right_id_list = []
for item in second_right_id_list:
    for thing in item:
        actual_second_right_id_list.append(thing)


# In[260]:


third_id_list = []
first_id = r"\(\"(\w{2}\d{6})"
for item in third_on_clicks:
    third_id_list.append(re.findall(first_id,item))
    
# each one is its own list, so I'm taking it out and putting each into one master list
actual_third_id_list = []
for item in third_id_list:
    for thing in item:
        actual_third_id_list.append(thing)


# In[262]:


fourth_id_list = []
first_id = r"\(\"(\w{2}\d{6})"
for item in fourth_on_clicks:
    fourth_id_list.append(re.findall(first_id,item))
    
# each one is its own list, so I'm taking it out and putting each into one master list
actual_fourth_id_list = []
for item in fourth_id_list:
    for thing in item:
        actual_fourth_id_list.append(thing)


# In[263]:


fifth_id_list = []
first_id = r"\(\"(\w{2}\d{6})"
for item in fifth_on_clicks:
    fifth_id_list.append(re.findall(first_id,item))
    
# each one is its own list, so I'm taking it out and putting each into one master list
actual_fifth_id_list = []
for item in fifth_id_list:
    for thing in item:
        actual_fifth_id_list.append(thing)


# In[ ]:





# ### Putting it all together

# In[268]:


# first_left_on_clicks
# first_right_on_clicks
# second_left_on_clicks
# second_right_on_clicks
# third_on_clicks
# fourth_on_clicks
# fifth_on_clicks


# In[269]:


# actual_first_left_id_list
# actual_first_right_id_list
# actual_second_left_id_list
# actual_second_right_id_list
# actual_third_id_list
# actual_fourth_id_list
# actual_fifth_id_list


# In[270]:


# first_left_list
# first_right_list
# second_left_list
# second_right_list
# third_list
# fourth_list
# fifth_list


# In[281]:


import pandas as pd


# In[310]:


# all_heds
on_click_list = first_left_on_clicks + first_right_on_clicks + second_left_on_clicks + second_right_on_clicks + third_on_clicks + fourth_on_clicks + fifth_on_clicks


# In[311]:


all_id_list = actual_first_left_id_list + actual_first_right_id_list + actual_second_left_id_list + actual_second_right_id_list + actual_third_id_list + actual_fourth_id_list + actual_fifth_id_list


# In[312]:


df = pd.DataFrame(
    {'hed': all_heds,
     'on_click': on_click_list,
     'article_id': all_id_list
    })


# In[313]:


df


# In[314]:


df.to_csv('nk-news.csv', index=False)


# In[ ]:




