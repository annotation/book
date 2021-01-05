#!/usr/bin/env python
# coding: utf-8

# <img align="right" src="images/ninologo.png" width="150"/>
# <img align="right" src="images/tf-small.png" width="125"/>
# <img align="right" src="images/dans.png" width="150"/>
# 
# # Hand-coding
# 
# While search is convenient in many cases, sometimes it gets tricky when you need that extra bit of control.
# That's the moment to revert back to hand-coding, while not altogether forgetting template search.
# 
# As an example, we program a *tablet calculator*.

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


# ## Numerals
# 
# There are several numeric systems in cuneiform.
# One of them involve the so-called ShinPP numerals.
# They form a set of glyphs with these numerical meanings:

# In[4]:


shinPP = dict(
    N41=0.2,
    N04=1,
    N19=6,
    N46=60,
    N36=180,
    N49=1800,
)

shinPPPat = '|'.join(shinPP)


# Now we want to find all the ShinPP numerals.
# We make use of the fact that we can construct our template.

# In[5]:


query = f'''
tablet
  sign grapheme={shinPPPat}
'''
results = A.search(query)
A.table(results, end=20, showGraphics=True)


# Let's see a few tablets in more detail:

# In[6]:


A.show(results, end=5, queryFeatures=False)


# ### A tablet calculator
# 
# Rather than displaying search results, you can also *process* them in your program.
# 
# Search results come as tuples of nodes that correspond directly to the elements
# of your search template.
# 
# We query for shinPP numerals on the faces of tablets.
# The result of the query is a list of tuples `(t, f, s)` consisting of
# a tablet node, a face node and a node for a sign of a shinPP numeral.
# 
# #### Rationale
# This task will require a higher level of programming skills and a deeper knowledge of how
# Python works.
# We include it in this tutorial to get the message across that Text-Fabric is not
# a black box that shields you from your data. Everything you handle in Text-Fabric is 
# open to further programming and processing of your own design and choosing.

# #### Data collection

# In[7]:


query = f'''
tablet
    face
        sign type=numeral grapheme={shinPPPat}
'''
results = A.search(query)


# We are going to put all these numerals in buckets: for each face on each tablet a separate bucket.

# In[8]:


numerals = {}
pNums = {}
for (tablet, face, sign) in results:
    pNums[F.catalogId.v(tablet)] = tablet
    numerals.setdefault(tablet, {}).setdefault(face, []).append(sign)
print(f'{len(pNums)} tablets')
print('\n'.join(list(pNums)[0:10]))
print('...')


# #### The calculator
# We define a function that given a tablet, adds the shinPP numerals by its faces.
# We also show the line art and a pretty transcription.
# 
# The function is a bit involved.

# In[9]:


# we generate Markdown strings and send them to the notebook formatter

def dm(x): display(Markdown(x))

def calcTablet(pNum): # pNum identifies the tablet in question
    # show a horizontal line in Markdown
    dm('---\n')     
    tablet = pNums.get(pNum, None)  # look up the node for this p-number
    if tablet is None:
        dm(f'**no results for {pNum}**')
        return                      # if not found the tablet has no ShinPP numerals: quit
    
    A.lineart(tablet, withCaption="top", width="200")   # show lineart
    faces = numerals[tablet]                    # get the buckets for the faces
    mySigns = []
    for (face, signs) in faces.items():         # work per face 
        mySigns.extend(signs)
        dm(f'*{F.type.v(face)}*')           # show the name of the face
        distinctSigns = {}                      # collect the distinct numerals
        for s in signs:
            distinctSigns.setdefault(A.atfFromSign(s), []).append(s)
        A.lineart(distinctSigns)      # display the list of signs
        total = 0                               # start adding up
        for (signAtf, signs) in distinctSigns.items():
            value = 0
            for s in signs:
                value += F.repeat.v(s) * shinPP[F.grapheme.v(s)]
            total += value
            amount = len(signs)                 # we report our calculation
            shinPPval = shinPP[F.grapheme.v(signs[0])]
            repeat = F.repeat.v(signs[0])
            print(f'{amount} x {signAtf} = {amount} x {repeat} x {shinPPval} = {value}')
        dm(f'**total** = **{total}**')
    A.prettyTuple([tablet] + mySigns, 1, queryFeatures=False) # show pretty transcription


# #### Calculate once

# In[10]:


calcTablet('P006377')


# #### Calculate ad lib
# Now the first 5 tablets.

# In[11]:


for tablet in sorted(pNums)[0:5]:
    calcTablet(tablet)


# ## More ...
# 
# The capabilities of search are endless.
# Often it is the quickest way to focus on a phenomenon, quicker than hand coding all the logic
# to retrieve your patterns.
# 
# That said, it is not a matter of either-or. You can use coding to craft your templates,
# and you can use coding to process your results.
# 
# It's an explosive mix. A later chapter in this tutorial shows
# even more [cases](cases.ipynb).
# 
# Have another look at
# [the manual](https://annotation.github.io/text-fabric/about/searchusage.html).

# ## Next
# 
# [signs](signs.ipynb)
# 
# *Back to the basics ...*
