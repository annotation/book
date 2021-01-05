#!/usr/bin/env python
# coding: utf-8

# <img align="right" src="images/ninologo.png" width="150"/>
# <img align="right" src="images/tf-small.png" width="125"/>
# <img align="right" src="images/dans.png" width="150"/>
# 
# # Relation
# 
# You can search for spatial ways that nodes hangs together in text: adjacent, embedded, same starting position, etc.

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


# ## Search for spatial patterns
# A few words on the construction of search templates.
# 
# The idea is that you mimick the things you are looking for
# in your search template.
# Embedded things are mimicked by indentation.
# 
# Let's search for a line with a case in it that is not further divided,
# in which there is a numeral and an ideograph.
# 
# Here is our first attempt, and we show the first tablet only.
# Note that you can have comments in a search template.
# Lines that start with `#` are ignored.

# In[4]:


query = '''
line
  case terminal=1
% order is not important
    sign type=ideograph
    sign type=numeral
'''
results = A.search(query)


# First a glance at the first 3 items in tabular view.

# In[5]:


A.table(results, end=2, showGraphics=False)


# Ah, we were still in condensed mode.
# 
# For this query the table is more perspicuous in normal mode, so we tell not to condense.

# In[6]:


A.table(results, condensed=False, end=7, showGraphics=False)


# Now the results on the first tablet, condensed by line.

# In[7]:


A.show(results, end=1, condenseType="line")


# The order between the two signs is not defined by the template,
# despite the fact that the line with the ideograph
# precedes the line with the numeral.
# Results may have the numeral and the ideograph in any order. 
# 
# In fact, the highlights above represent multiple results.
# If a case has say 2 numerals and 3 ideographs, there are 6 possible
# pairs.
# 
# By default, results are shown in *condensed* mode.
# That means that results are shown per tablet, and on the result tablets
# everything that is in some result is being highlighted.
# 
# It is also possible to see the uncondensed results.
# That gives you an exact picture of each real result constellation.
# 
# In order to illustrate the difference, we focus on one tablet and one case.
# This case has 3 numerals and 2 ideographs, so we expect 6 results.

# In[8]:


query = '''
tablet catalogId=P448702
  line
    case terminal=1 number=2a
      sign type=ideograph
      sign type=numeral
'''
results = A.search(query)


# We show them condensed (by default), so we expect 1 line with all ideographs and numerals in case `2a'` highlighted.

# In[9]:


A.show(results, showGraphics=False, condenseType="line")


# Now the same results in uncondensed mode. Expect 6 times the same line with
# different highlighted pairs of signs.
# 
# Note that we can apply different highlight colors to different parts of the result.
# The words in the pair are member 4 and 5.
# 
# The members that we do not map, will not be highlighted.
# The members that we map to the empty string will be highlighted with the default color.
# 
# **NB:** Choose your colors from the
# [CSS specification](https://developer.mozilla.org/en-US/docs/Web/CSS/color_value).

# In[10]:


A.displaySetup(condensed=False, skipCols="1", colorMap={2: '', 3: 'cyan', 4: 'magenta'}, showGraphics=False, condenseType="line", queryFeatures=False)


# In[11]:


A.show(results)


# Color mapping works best for uncondensed results. If you condense results, some nodes may occupy
# different positions in different results. It is unpredictable which color will be used 
# for such nodes:

# In[12]:


A.show(results, condensed=True)


# In[13]:


A.displayReset()


# You can enforce order.
# We modify the template a little to state a
# relational condition, namely that the ideograph follows the numeral.

# In[14]:


query = '''
tablet catalogId=P448702
  line
    case terminal=1 number=2a
      sign type=ideograph
      > sign type=numeral
'''
results = A.search(query)
A.table(results, condensed=False, showGraphics=False)


# Still six results.
# No wonder, because the case has first three numerals in a row and then 2 ideographs.
# 
# Do you want the ideograph and the numeral to be *adjacent* as well?
# We only have to add 1 character to the template to make it happen.

# In[15]:


query = '''
tablet catalogId=P448702
  line
    case terminal=1 number=2a
      sign type=ideograph
      :> sign type=numeral
'''
results = A.search(query)


# In[16]:


A.table(results, condensed=False, showGraphics=False)


# In[17]:


A.displaySetup(
    condensed=False, skipCols="1",
    colorMap={2: '', 3: 'cyan', 4: 'magenta'},
    showGraphics=False, condenseType="line", queryFeatures=False
)


# In[18]:


A.show(results, condensed=False) 


# In[19]:


A.displayReset()


# By now it pays off to study the possibilities of
# [search templates](https://annotation.github.io/text-fabric/Use/Search/#search-templates).
# 
# If you want a reminder of all possible spatial relationships between nodes, you can call it up
# here in your notebook:

# In[20]:


S.relationsLegend()


# ## Relational patterns: quads
# 
# Quads are compositions of signs by means of *operators*, such as `.` and `x`.
# The operators are coded as an *edge* feature with values. The `op`-edges are between the signs/quads that are combined,
# and the values of the `op` edges are the names of the operators in question.
# 
# Which operators do we have?

# In[21]:


for (op, freq) in E.op.freqList():
    print(f'{op} : {freq:>5}x')


# Between how many sign pairs do we have an operator?

# In[22]:


query = '''
sign
-op> sign
'''
results = A.search(query)


# Lets specifically ask for the `x` operator:

# In[23]:


query = '''
sign
-op=x> sign
'''
results = A.search(query)


# Less than expected?
# 
# We must not forget the combinations between quads and between quads and signs.
# 
# We write a function that gives all pairs of sign/quads connected by a specific operator.
# 
# This is a fine illustration of how you can use programming to compose search templates,
# instead of writing them out yourself.

# In[24]:


def getCombi(op):
    types = ('sign', 'quad')
    allResults = []
    for type1 in types:
        for type2 in types:
            query = f'''
{type1}
-op{op}> {type2}
'''
            results = A.search(query, silent=True)
            print(f'{len(results):>5} {type1} {op} {type2}')
            allResults += results
    print(f'{len(allResults):>5} {op}')


# Now we can count all combinations with `x`:

# In[25]:


getCombi('=x')


# In[26]:


getCombi('=.')


# In[27]:


getCombi('=&')


# In[28]:


getCombi('=+')


# In exact agreement with the results of `E.op.freqList()` above.
# But we are more flexible!
# 
# We can ask for more operators at the same time.

# In[29]:


getCombi('=x|+')


# In[30]:


getCombi('~[^a-z]')


# Finally, we zoom in on the rare cases where the operator is `x` used between a quad and a sign.
# We want to see the show the lines where they occur.

# In[31]:


query = '''
line
  quad
  -op=x> sign
'''
results = A.search(query)
A.show(results, withNodes=True, showGraphics=True, condenseType="line")


# Hint: if you want to see where these lines come from, hover over the line indicator, or click on it.
# 
# Alternatively, you can set the condense type to tablet.
# And note that we have set the base type to `quad`, so that the pretty display does not unravel the quads.

# In[32]:


A.show(results, withNodes=True, showGraphics=True, condenseType="tablet", baseTypes="quad")


# ## Next
# 
# [quantifier](quantifier.ipynb)
# 
# *There is more ...*
