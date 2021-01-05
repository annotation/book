#!/usr/bin/env python
# coding: utf-8

# <img align="right" src="images/ninologo.png" width="150"/>
# <img align="right" src="images/tf-small.png" width="125"/>
# <img align="right" src="images/dans.png" width="150"/>
# 
# # Quantifiers
# 
# So far we have seen only very positive templates.
# They express what you want to see in the result.
# 
# It is also possible to state conditions about what you do not want to see in the results.
# 
# You can express whether sub-searches have or have not results.
# This adds considerably to the power of expression of search templates.

# In[1]:


get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')


# In[2]:


import sys, os
import collections
from IPython.display import display, Markdown
from tf.app import use


# In[3]:


A = use('uruk:clone', checkout="clone", hoist=globals())
# A = use('uruk', hoist=globals())


# ## Tablets without case divisions
# 
# Let's find all tablets in which all lines are undivided, i.e. lines without cases.

# In[4]:


query = '''
tablet
/without/
  case
/-/
'''


# The expression
# 
# ```
# /without/
# template
# /-/
# ```
# 
# is a [quantifier](https://annotation.github.io/text-fabric/Use/Search/#quantifiers).
# 
# It poses a condition on the preceding line in the template, in this case the `tablet`.
# And the condition is that the template
# 
# ```
# tablet
#   case
# ```
# 
# does not have results.

# In[5]:


results = A.search(query)


# In[6]:


A.show(results, end=2)


# Now let's find cases without numerals.

# In[7]:


query = '''
case
/without/
  sign type=numeral
/-/
'''
results = A.search(query)


# We show a few.

# In[8]:


A.show(results, end=2)


# Now we can use this to get something more sophisticated: the tablets that do not have numerals in their cases. So only undivided lines may contain numerals.
# 
# Let's find tablets that do have cases, but just no cases with numerals.

# In[9]:


query = '''
tablet
/where/
  case
/have/
  /without/
    sign type=numeral
  /-/
/-/
/with/
  case
/-/
'''


# In[10]:


results = A.search(query) 


# In[11]:


A.show(results, end=2)


# Can we find such tablet which do have numerals on their undivided lines.
# 
# We show here a way to use the results of one query in another one: 
# *custom sets*.
# 
# We put the set of tablets with cases but without numerals in cases in a set called `cntablet`.
# 
# We run the query again, but now in shallow mode, so that the result is a set.
# 
# By the way: read more about custom sets and shallow mode in the description of
# [`A.search()`](https://annotation.github.io/text-fabric/Api/General/#search-api).

# In[12]:


results = A.search(query, shallow=True)
customSets = dict(cntablet=results)


# Now we can perform a very simple query for numerals on this set: we want tablets with numerals.
# By restricting ourselves to this set, we now that these numerals must occur on undivided lines.

# In[13]:


query = '''
cntablet
  sign type=numeral
'''
results = A.search(query, sets=customSets)


# In[14]:


A.show(results, end=2, queryFeatures=False)


# We could have found these results by one query as well.
# Judge for yourself which method causes the least friction.

# In[15]:


query = '''
tablet
/without/
  case
    sign type=numeral
/-/
/with/
  case
/-/
  sign type=numeral
'''
results = A.search(query)
A.show(results, end=2, queryFeatures=False)


# ## Next
# 
# [hand](hand.ipynb)
# 
# *Give it a hand ...*
