#!/usr/bin/env python
# coding: utf-8

# # Rock and Mineral Clubs
# 
# Scrape all of the rock and mineral clubs listed at https://rocktumbler.com/blog/rock-and-mineral-clubs/ (but don't just cut and paste!)
# 
# Save a CSV called `rock-clubs.csv` with the name of the club, their URL, and the city they're located in.
# 
# **Bonus**: Add a column for the state. There are a few ways to do this, but knowing that `element.parent` goes 'up' one element might be helpful.
# 
# * _**Hint:** The name of the club and the city are both inside of td elements, and they aren't distinguishable by class. Instead you'll just want to ask for all of the tds and then just ask for the text from the first or second one._
# * _**Hint:** If you use BeautifulSoup, you can select elements by attributes other than class or id - instead of `doc.find_all({'class': 'cat'})` you can do things like `doc.find_all({'other_attribute': 'blah'})` (sorry for the awful example)._
# * _**Hint:** If you love `pd.read_html` you might also be interested in `pd.concat` and potentially `list()`. But you'll have to clean a little more!_

# In[28]:


import requests
from bs4 import BeautifulSoup
import re


# In[2]:


response = requests.get('https://rocktumbler.com/blog/rock-and-mineral-clubs/')
doc = BeautifulSoup(response.text)


# ### just alabama info

# In[10]:


alabama_stuff = doc.find_all('section')[1]
alabama_stuff


# In[22]:


# club names
alabama_a = alabama_stuff.find_all('a')
for item in alabama_a:
    print(item.text.strip())


# In[58]:


# cities
alabama_tr = alabama_stuff.find_all('td')
count = 2
for item in alabama_tr[1:]:
    if count % 2:
        name_and_city = item.text.strip()
        print(name_and_city)
    count = count + 1


# In[86]:


alabama_tr = alabama_stuff.find_all('tr')
for item in alabama_tr[1:]:
    name = item.find('td').text.strip()
    print(name)    
    city = item.find_all('td')[1].text.strip()
    print(city)
    url = item.find('a')['href']
    print(url)
    state = alabama_stuff.find('h3').text.strip()
    state_finder = r"(.*) Rock and Mineral Clubs"
    state_name = re.findall(state_finder,state)
    for thing in state_name:
        print(thing)


# ### putting it all together

# In[98]:


stuff = doc.find_all('section')[1:51]


# In[134]:


rock_list = []
for item in stuff:
    trs = item.find_all('tr')
    for thing in trs[1:]:
        name = thing.find_all('td')[0].text.strip()
        city = thing.find_all('td')[1].text.strip()
        url = thing.find('a')['href']
        state = trs[0].find('h3').text.strip()
        state_finder = r"(.*) Rock and Mineral Clubs"
        state_name = re.findall(state_finder,state)
        for thingamabob in state_name:
            thingamabob
        rock_list.append({
            'name': name,
            'city': city,
            'url': url,
            'state': thingamabob
        })


# In[135]:


rock_list


# In[120]:


import pandas as pd


# In[136]:


df = pd.DataFrame(rock_list)


# In[137]:


df


# In[140]:


df.to_csv('rock-clubs.csv', index=False)

