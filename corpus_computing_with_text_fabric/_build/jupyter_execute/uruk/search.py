#!/usr/bin/env python
# coding: utf-8

# <img align="right" src="images/ninologo.png" width="150"/>
# <img align="right" src="images/tf-small.png" width="125"/>
# <img align="right" src="images/dans.png" width="150"/>
# 
# # Search
# 
# Search is essential to get around in the corpus, and it is convenient as well.
# Whereas the whole point of Text-Fabric is to move around in the corpus programmatically,
# we show that
# [template based search](https://annotation.github.io/text-fabric/Use/Search/#search-templates)
# makes everything a lot more convenient ...
# 
# Along with showing how search works, we also point to pretty ways to display your search results.
# The good news is that `search` and `pretty` work well together. 

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


# ## The basics
# 
# Here is a very simple query: we look for tablets containing a numeral sign.

# In[4]:


query = '''
tablet
  sign type=numeral
'''

results = A.search(query)


# We can display the results in a table (here are the first 5):

# In[5]:


A.table(results, end=5, condenseType="line")


# We can combine all results that are on the same tablet:

# In[6]:


A.table(results, condensed=True, condenseType='line', end=5)


# And we can show them inside the face they occur in:

# In[7]:


A.show(results, condenseType='face', end=2, skipCols="1")


# The feature *type* is displayed because it occurs in the query.
# We can make the display a bit more compact by suppressing those features:

# In[8]:


A.show(results, condenseType='face', end=2, queryFeatures=False, skipCols="1")


# ## Finding a tablet
# 
# Suppose we have the *p-number* of a tablet.
# How do we find that tablet?
# Remembering from the feature docs that the p-numbers are stored in the feature
# `catalogId`, we can write a *search template*.

# In[9]:


query = '''
tablet catalogId=P005381
'''
results = A.search(query)
A.table(results)


# The function `A.table()` gives you a tabular overview of the results,
# with a link to the tablet on CDLI.
# 
# But we can also get more information by using `A.show()`:

# In[10]:


A.show(results)


# Several things to note here
# 
# * if you want to see the tablet on CDLI, you can click on the tablet header;
# * the display matches the layout on the tablet:
#   * faces and columns are delineated with red lines
#   * lines and cases are delineated with blue lines
#   * cases and subcases alternate their direction of division between horizontal and vertical:
#     lines are horizontally divided into cases, they are vertically divided into subcases, and they
#     in turn are horizontally divided in subsubcases, etc.
#   * quads and signs are delineated with grey lines
#   * clusters are delineated with brown lines (see further on)
#   * lineart is given for top-level signs and quads; those that are part of a bigger quad do not
#     get lineart;
#     
# It is possible to switch off the lineart.

# ## More info in the results
# You can show the line numbers that correspond to the ATF source files as well.
# Let us also switch off the lineart.

# In[11]:


query = '''
tablet catalogId=P005381
'''
results = A.search(query)
A.table(results, lineNumbers=True)
A.show(results, lineNumbers=True, showGraphics=False)


# There is a big quad in `obverse:2 line 1`. We want to call up the lineart for it separately.
# First step: make the nodes visible.

# In[12]:


query = '''
tablet catalogId=P005381
'''
results = A.search(query)
A.table(results, withNodes=True)
A.show(results, withNodes=True, showGraphics=False)


# We read off the node number of that quad and fetch the lineart.

# In[13]:


A.lineart(143015)


# ## Search templates
# Let's highlight all numerals on the tablet.
# 
# We prefer our results to be condensed per tablet for the next few shows.
# 
# We make that the temporary default:

# In[14]:


A.displaySetup(condensed=True)


# In[15]:


query = '''
tablet catalogId=P005381
  sign type=numeral
'''
results = A.search(query)
A.show(results, queryFeatures=False)


# We can do the same for multiple tablets. But now we highlight the undivided lines,
# just for variation.

# In[16]:


query = f'''
tablet catalogId=P003581|P000311
  line terminal
'''
results = A.search(query)


# In[17]:


A.table(results, showGraphics=False, withPassage=False)


# In[18]:


A.show(results, showGraphics=False, condenseType="tablet")


# In an other chapter of this tutorial, [steps](steps.ipynb) we encounter a grapheme with a double prime.
# There is only one, and we showed the tablet on which it occurs, without highlighting the grapheme in question.
# Now we can do the highlight:

# In[19]:


results = A.search('''
sign prime=2
''')


# In[20]:


A.show(results)


# ## Comparisons in templates: cases
# 
# Cases have a feature depth which indicate their nesting depth within a line.
# It is not the depth *of* that case, but the depth *at* which that case occurs.
# 
# Comparison queries are handy to select cases of a certain minimum or maximum depth.

# We'll work a lot with `condensed=False`, and `lineart` likewise, so let's make that the default:

# In[21]:


A.displaySetup(condensed=False, showGraphics=False)


# In[22]:


query = '''
case depth=3
'''
results = A.search(query)
A.table(results, end=10)


# Are there deeper cases?

# In[23]:


query = '''
case depth>3
'''
results = A.search(query)
A.table(results, end=10)


# Still deeper?

# In[24]:


query = '''
case depth>4
'''
results = A.search(query)
A.table(results, end=10)


# As a check: the cases with depth 4 should be exactly the cases with depth > 3:

# In[25]:


query = '''
case depth=4
'''
results = A.search(query)
A.table(results, end=10)
tc4 = len(results)


# Terminal cases at depth 1 are top-level divisions of lines that are not themselves divided further.

# In[26]:


query = '''
case depth=1 terminal
'''
results = A.search(query)
A.table(results, end=10)
tc1 = len(results)


# Now let us select both the terminal cases of level 1 and 4.
# They are disjunct, so the amounts should add up.

# In[27]:


query = '''
case depth=1|4 terminal
'''
results = A.search(query)
A.table(results, end=10)
tc14 = len(results)
print(f'{tc1} + {tc4} = {tc1 + tc4} = {tc14}')


# ## Regular expressions in templates
# We can use regular expressions in our search templates.
# 
# ### Digits in graphemes
# We search for non-numeral signs whose graphemes contains digits.

# In[28]:


A.displaySetup(condensed=True)


# In[29]:


query = '''
sign type=ideograph grapheme~[0-9]
'''
results = A.search(query)
A.table(results, withNodes=True, end=5)


# We can add a bit more context easily:

# In[30]:


query = '''
tablet
  face
    column
      line
        sign type=ideograph grapheme~[0-9]
'''
results = A.search(query)
A.table(results, condensed=False, end=10)


# ### Pit numbers
# 
# The feature `excavation` gives you the number of the pit where a tablet is found. 
# The syntax of pit numbers is a bit involved, here are a few possible values:
# 
# ```
# W 20497
# W 20335,3
# W 19948,10
# W 20493,26
# W 17890,b
# W 17729,o
# W 15920,b5
# W 17729,aq
# W 19548,a + W 19548,b
# W 17729,cn + W 17729,eq
# W 14337,a + W 14337,b + W 14337,c + W 14337,d + W 14337,e
# Ashm 1928-445b
# ```
# 
# Let's assume we are interested in `SZITA~a1` signs occurring in cases of depth 1.
# The following query finds them all:

# In[31]:


query = '''
tablet
  case depth=1
    sign grapheme=SZITA variant=a1
'''
results = A.search(query)


# Now we want to organize them by excavation number:

# In[32]:


signPerPit = {}

for (tablet, case, sign) in sorted(results):
    pit = F.excavation.v(tablet) or 'no pit information'
    signPerPit.setdefault(pit, []).append(sign)

for pit in sorted(signPerPit):
    print(f'{pit:<30} {len(signPerPit[pit]):>2}')


# We can restrict results to those on tablets found in certain pits by constraining the search template.
# If we are interested in pit `20274` we can use a regular expression that matches all 4 detailed pit numbers
# based on `20274`.
# So, we do not say 
# 
# ```
# excavation=20274
# ```
# but 
# 
# ```
# excavation~20274
# ```

# In[33]:


query = '''
tablet excavation~20274
  case depth=1
    sign grapheme=SZITA variant=a1
'''
results = A.search(query)
A.table(results, condensed=False, showGraphics=False)


# Or if we want to restrict ourselves to pit numbers with a `W`, we can say:

# In[34]:


query = '''
tablet excavation~W
  case depth=1
    sign grapheme=SZITA variant=a1
'''
results = A.search(query)


# ## Next
# 
# [relation](relation.ipynb)
# 
# *Relations in space ...*
