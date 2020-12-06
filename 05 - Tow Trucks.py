#!/usr/bin/env python
# coding: utf-8

# # Texas Tow Trucks (`.apply` and `requests`)
# 
# We're going to scrape some [tow trucks in Texas](https://www.tdlr.texas.gov/tools_search/).

# ## Import your imports

# In[2]:


import pandas as pd

from selenium import webdriver
driver = webdriver.Chrome()
driver.get("https://www.tdlr.texas.gov/tools_search/")


# ## Search for the TLDR Number `006565540C`, and scrape the information on that company
# 
# Using [license information system](https://www.tdlr.texas.gov/tools_search/), find information about the tow truck number above, displaying the
# 
# - The business name
# - Owner/operator
# - Phone number
# - License status (Active, Expired, Etc)
# - Physical address
# 
# If you can't figure a 'nice' way to locate something, your two last options might be:
# 
# - **Find a "parent" element, then dig inside**
# - **Find all of a type of element** (like we did with `td` before) and get the `[0]`, `[1]`, `[2]`, etc
# - **XPath** (inspect an element, Copy > Copy XPath)
# 
# These kinds of techniques tend to break when you're on other result pages, but... maybe not! You won't know until you try.
# 
# > - *TIP: When you use xpath, you CANNOT use double quotes or Python will get confused. Use single quotes.*
# > - *TIP: You can clean your data up if you want to, or leave it dirty to clean later*
# > - *TIP: The address part can be tough, but you have a few options. You can use a combination of `.split` and list slicing to clean it now, or clean it later in the dataframe with regular expressions. Or other options, too, probably*

# In[4]:


# click tldr button
tldr_button = driver.find_element_by_id('mcrbutton')
tldr_button.click()


# In[6]:


# click into tldr textbox and input text
textbox = driver.find_element_by_id('mcrdata')
textbox.send_keys('006565540C')


# In[7]:


# click submit
submit_button = driver.find_element_by_id('submit3')
submit_button.click()


# In[39]:


master_table = driver.find_elements_by_tag_name('tr')
company_table = master_table[5].find_element_by_tag_name('td')
name = company_table.text.strip()
name


# In[43]:


owner_getter = master_table[6].find_element_by_tag_name('td')
owner = owner_getter.text.strip()
owner


# In[44]:


phone_getter = master_table[7].find_element_by_tag_name('td')
phone = phone_getter.text.strip()
phone


# In[47]:


status_getter = master_table[8]
status = status_getter.text.strip()
status


# In[54]:


import re


# In[58]:


address_text


# In[100]:


address_getter = master_table[9].find_elements_by_tag_name('td')[1]
address_text = address_getter.text.strip()
address_text2 = re.sub("\n",' ',address_text)
address_regex = r"Physical: (.*)"
address_list = re.findall(address_regex,address_text2)
for item in address_list:
    address = item
address


# In[ ]:





# # Adapt this to work inside of a single cell
# 
# Double-check that it works. You want it to print out all of the details.

# In[110]:


driver.get("https://www.tdlr.texas.gov/tools_search/")

# navigate page, search, submit
tldr_button = driver.find_element_by_id('mcrbutton')
tldr_button.click()
textbox = driver.find_element_by_id('mcrdata')
textbox.send_keys('006565540C')
submit_button = driver.find_element_by_id('submit3')
submit_button.click()

# output info

# company name
master_table = driver.find_elements_by_tag_name('tr')
company_table = master_table[5].find_element_by_tag_name('td')
name_text = company_table.text.strip()
name_regex = r"Name:    (.*)"
name_list = re.findall(name_regex,name_text)
for item in name_list:
    name = item
print(name)

# owner
owner_getter = master_table[6].find_element_by_tag_name('td')
owner_text = owner_getter.text.strip()
owner_regex = r"Owner/Officer:   (.*)"
owner_list = re.findall(owner_regex,owner_text)
for item in owner_list:
    owner = item
print(owner)

# phone
phone_getter = master_table[7].find_element_by_tag_name('td')
phone_text = phone_getter.text.strip()
phone_regex = r"Phone:   (.*)"
phone_list = re.findall(phone_regex,phone_text)
for item in phone_list:
    phone = item
print(phone)

# status
status_getter = master_table[8]
status_text = status_getter.text.strip()
status_regex = r"Certificate Information: Status:  (.*)"
status_list = re.findall(status_regex,status_text)
for item in status_list:
    status = item
print(status)

# address
address_getter = master_table[9].find_elements_by_tag_name('td')[1]
address_text = address_getter.text.strip()
address_text2 = re.sub("\n",' ',address_text)
address_regex = r"Physical: (.*)"
address_list = re.findall(address_regex,address_text2)
for item in address_list:
    address = item
print(address)


# # Using .apply to find data about SEVERAL tow truck companies
# 
# The file `trucks-subset.csv` has information about the trucks, we'll use it to find the pages to scrape.
# 
# ### Open up `trucks-subset.csv` and save it into a dataframe

# In[112]:


df = pd.read_csv('trucks-subset.csv')
df


# ## Go through each row of the dataset, displaying the URL you will need to scrape for the information on that row
# 
# You don't have to actually use the search form for each of these - look at the URL you're on, it has the number in it!
# 
# For example, one URL might look like `https://www.tdlr.texas.gov/tools_search/mccs_display.asp?mcrnumber=006565540C`.
# 
# - *TIP: Use .apply and a function*
# - *TIP: You'll need to build this URL from pieces*
# - *TIP: You probably don't want to `print` unless you're going to fix it for the next question 
# - *TIP: pandas won't showing you the entire url! Run `pd.set_option('display.max_colwidth', None)` to display aaaalll of the text in a cell*

# In[118]:


def scrape_trucks(df):
    slug = df['TDLR Number']
    link = f'https://www.tdlr.texas.gov/tools_search/mccs_display.asp?mcrnumber={slug}'
    print(link)


# In[119]:


df.apply(scrape_trucks, axis=1)


# ### Save this URL into a new column of your dataframe, called `url`
# 
# - *TIP: Use a function and `.apply`*
# - *TIP: Be sure to use `return`*

# In[120]:


def scrape_trucks(df):
    slug = df['TDLR Number']
    link = f'https://www.tdlr.texas.gov/tools_search/mccs_display.asp?mcrnumber={slug}'
    
    data = {}
    data['TDLR_number'] = df['TDLR Number']
    data['url'] = link
    
    return pd.Series(data)


# In[121]:


df.apply(scrape_trucks, axis=1)


# ## Go through each row of the dataset, printing out information about each tow truck company.
# 
# Now will be **scraping** inside of your function.
# 
# - The business name
# - Owner/operator
# - Phone number
# - License status (Active, Expired, Etc)
# - Physical address
# 
# Just print it out for now.
# 
# - *TIP: use .apply*
# - *TIP: You'll be using the code you wrote before, but converted into a function*
# - *TIP: Remember how the TDLR Number is in the URL? You don't need to do the form submission if you don't want!*
# - *TIP: Make sure you adjust any variables so you don't scrape the same page again and again*

# In[159]:


data = {}
def scrape_trucks(df):
    slug = df['TDLR Number']
    link = f'https://www.tdlr.texas.gov/tools_search/mccs_display.asp?mcrnumber={slug}'
    driver.get(link)
    
    # company name
    master_table = driver.find_elements_by_tag_name('tr')
    company_table = master_table[5].find_element_by_tag_name('td')
    name_text = company_table.text.strip()
    name_regex = r"Name:    (.*)"
    name_list = re.findall(name_regex,name_text)
    for item in name_list:
        name = item
            
    # owner
    owner_getter = master_table[6].find_element_by_tag_name('td')
    owner_text = owner_getter.text.strip()
    owner_regex = r"Owner/Officer:   (.*)"
    owner_list = re.findall(owner_regex,owner_text)
    for item in owner_list:
        owner = item
    data['owner'] = owner

    # phone
    owner_getter2 = master_table[7].find_element_by_tag_name('td').get_attribute('width')
    if len(owner_getter2) > 0:
        owner_getter = master_table[7].find_element_by_tag_name('td')
        owner_text = owner_getter.text.strip()
        owner_regex = r"Owner/Officer:   (.*)"
        owner_list = re.findall(owner_regex,owner_text)
        for item in owner_list:
            owner2 = item
        owner_getter = master_table[8].find_element_by_tag_name('td')
        owner_text = owner_getter.text.strip()
        owner_regex = r"Owner/Officer:   (.*)"
        owner_list = re.findall(owner_regex,owner_text)
        for item in owner_list:
            owner3 = item
        data['owner'] = owner + " " + owner2 + " " + owner3
        
        phone_getter = master_table[9].find_element_by_tag_name('td')
        phone_text = phone_getter.text.strip()
        phone_regex = r"Phone:   (.*)"
        phone_list = re.findall(phone_regex,phone_text)
        for item in phone_list:
            phone = item
        data['phone'] = phone
            
        count = 10
    else:
        phone_getter = master_table[7].find_element_by_tag_name('td')
        phone_text = phone_getter.text.strip()
        phone_regex = r"Phone:   (.*)"
        phone_list = re.findall(phone_regex,phone_text)
        for item in phone_list:
            phone = item
        data['phone'] = phone
        
        count = 8

    # status
    status_getter = master_table[count]
    status_text = status_getter.text.strip()
    status_regex = r"Certificate Information: Status:  (.*)"
    status_list = re.findall(status_regex,status_text)
    for item in status_list:
        status = item
    
    count = count + 1

    # address
    address_getter = master_table[count].find_elements_by_tag_name('td')[1]
    address_text = address_getter.text.strip()
    address_text2 = re.sub("\n",' ',address_text)
    address_regex = r"Physical: (.*)"
    address_list = re.findall(address_regex,address_text2)
    for item in address_list:
        address = item
    
    data['TDLR_number'] = df['TDLR Number']
    data['url'] = link
    data['company_name'] = name
#     data['owner'] = owner
#     data['phone'] = phone
    data['status'] = status
    data['address'] = address
    
    return pd.Series(data)


# In[160]:


df2 = df.apply(scrape_trucks, axis=1)
df2


# ## Scrape the following information for each row of the dataset, and save it into new columns in your dataframe.
# 
# - The business name
# - Owner/operator
# - Phone number
# - License status (Active, Expired, Etc)
# - Physical address
# 
# It's basically what we did before, but using the function a little differently.
# 
# - *TIP: Same as above, but you'll be returning a `pd.Series` and the `.apply` line is going to be a lot longer*
# - *TIP: Save it to a new dataframe!*
# - *TIP: Make sure you change your `df` variable names correctly if you're cutting and pasting - there are a few so it can get tricky*

# In[ ]:


# oops I already did this in the function I just wrote


# ### Save your dataframe as a CSV named `tow-trucks-extended.csv`

# In[147]:


df2.to_csv('tow-trucks-extended.csv', index=False)


# ### Re-open your dataframe to confirm you didn't save any extra weird columns

# In[148]:


pd.set_option("display.max_colwidth", 200)
df3 = pd.read_csv("tow-trucks-extended.csv")
df3.head()


# ## Process the entire `tow-trucks.csv` file
# 
# We just did it on a short subset so far. Now try it on all of the tow trucks. **Save as the same filename as before**

# In[168]:


df4 = pd.read_csv('tow-trucks.csv')


# In[169]:


data = {}
def scrape_trucks(df4):
    slug = df4['TDLR Number']
    link = f'https://www.tdlr.texas.gov/tools_search/mccs_display.asp?mcrnumber={slug}'
    driver.get(link)
    
    # company name
    master_table = driver.find_elements_by_tag_name('tr')
    company_table = master_table[5].find_element_by_tag_name('td')
    name_text = company_table.text.strip()
    name_regex = r"Name:    (.*)"
    name_list = re.findall(name_regex,name_text)
    for item in name_list:
        name = item
            
    # owner
    owner_getter = master_table[6].find_element_by_tag_name('td')
    owner_text = owner_getter.text.strip()
    owner_regex = r"Owner/Officer:   (.*)"
    owner_list = re.findall(owner_regex,owner_text)
    for item in owner_list:
        owner = item
    data['owner'] = owner

    # phone
    # checking if there's a second or third tag with <td width = 400" because only owner name tds have a specific width
    owner_getter2 = master_table[8].find_element_by_tag_name('td').get_attribute('width')
    owner_getter3 = master_table[7].find_element_by_tag_name('td').get_attribute('width')
    if len(owner_getter2) > 0:
        owner_getter = master_table[7].find_element_by_tag_name('td')
        owner_text = owner_getter.text.strip()
        owner_regex = r"Owner/Officer:   (.*)"
        owner_list = re.findall(owner_regex,owner_text)
        for item in owner_list:
            owner2 = item
        owner_getter = master_table[8].find_element_by_tag_name('td')
        owner_text = owner_getter.text.strip()
        owner_regex = r"Owner/Officer:   (.*)"
        owner_list = re.findall(owner_regex,owner_text)
        for item in owner_list:
            owner3 = item
        data['owner'] = owner + " " + owner2 + " " + owner3
        
        phone_getter = master_table[9].find_element_by_tag_name('td')
        phone_text = phone_getter.text.strip()
        phone_regex = r"Phone:   (.*)"
        phone_list = re.findall(phone_regex,phone_text)
        for item in phone_list:
            phone = item
        data['phone'] = phone
            
        count = 10   
        
    elif len(owner_getter3) > 0:
        owner_getter = master_table[7].find_element_by_tag_name('td')
        owner_text = owner_getter.text.strip()
        owner_regex = r"Owner/Officer:   (.*)"
        owner_list = re.findall(owner_regex,owner_text)
        for item in owner_list:
            owner2 = item
        data['owner'] = owner + " " + owner2
        
        phone_getter = master_table[8].find_element_by_tag_name('td')
        phone_text = phone_getter.text.strip()
        phone_regex = r"Phone:   (.*)"
        phone_list = re.findall(phone_regex,phone_text)
        for item in phone_list:
            phone = item
        data['phone'] = phone
            
        count = 9
    
    else:
        phone_getter = master_table[7].find_element_by_tag_name('td')
        phone_text = phone_getter.text.strip()
        phone_regex = r"Phone:   (.*)"
        phone_list = re.findall(phone_regex,phone_text)
        for item in phone_list:
            phone = item
        data['phone'] = phone
        
        count = 8

    # status
    status_getter = master_table[count]
    status_text = status_getter.text.strip()
    status_regex = r"Certificate Information: Status:  (.*)"
    status_list = re.findall(status_regex,status_text)
    for item in status_list:
        status = item
    
    count = count + 1

    # address
    address_getter = master_table[count].find_elements_by_tag_name('td')[1]
    address_text = address_getter.text.strip()
    address_text2 = re.sub("\n",' ',address_text)
    address_regex = r"Physical: (.*)"
    address_list = re.findall(address_regex,address_text2)
    for item in address_list:
        address = item
    
    data['TDLR_number'] = df4['TDLR Number']
    data['url'] = link
    data['company_name'] = name
#     data['owner'] = owner
#     data['phone'] = phone
    data['status'] = status
    data['address'] = address
    
    return pd.Series(data)


# In[170]:


df4 = df4.apply(scrape_trucks, axis=1)


# In[171]:


df4


# In[172]:


df4.to_csv('tow-trucks-extended.csv', index=False)

