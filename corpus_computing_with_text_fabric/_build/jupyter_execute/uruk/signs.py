#!/usr/bin/env python
# coding: utf-8

# <img align="right" src="images/ninologo.png" width="150"/>
# <img align="right" src="images/tf-small.png" width="125"/>
# <img align="right" src="images/dans.png" width="150"/>
# 
# # Signs
# 
# Signs are the building blocks in the transcriptions.
# They correspond to the individual "glyphs" on the tablet.
# 
# However, we have inserted a few *empty* signs, which we can leave out subsequently ...

# We need a few extra modules.

# In[1]:


get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')


# In[2]:


import sys, os
import collections
from IPython.display import Markdown
from tf.app import use


# In[3]:


A = use('uruk:clone', checkout="clone", hoist=globals())
# A = use('uruk', hoist=globals())


# ## Showing signs
# 
# The main characteristic of a sign is its **grapheme**.
# Everything we do with signs, is complicated by the fact that signs can be *repeated*, and *augmented* with
# *primes*, *variants*, *modifiers* and *flags*.
# 
# Before we go on, we call up our example tablet.
# 
# If you want to output multiple text items in an output cell, you have to `print()` it.

# In[4]:


pNum = 'P005381'
query = '''
tablet catalogId=P005381
'''
results = A.search(query)
A.show(results, withNodes=True)


# We navigate to the last sign in line 1 in column 2 on the obverse face:

# In[5]:


case = A.nodeFromCase((pNum, 'obverse:2', '1'))
sign1 = L.d(case, otype='sign')[-1]
print(sign1)


# That must be the right barcode.
# 
# We can retrieve the ATF transliteration:

# In[6]:


print(A.atfFromSign(sign1))


# Note that we get the ATF for a sign by means of `A.atfFromSign(node)`.
# We get also the augments such as primes and modifiers and variant.
# We get the flags if we say so by `flags=True`.
# 
# Take for example the first sign on line 3 in column 1 on the obverse face:

# In[7]:


case = A.nodeFromCase((pNum, 'obverse:1', '3'))
sign2 = L.d(case, otype='sign')[0]
print(sign2)
print(A.atfFromSign(sign2))
print(A.atfFromSign(sign2, flags=True))


# Secondly, we want to get pointers to the locations of these signs in the corpus.

# In[8]:


A.pretty(sign1, withNodes=True)
A.pretty(sign2, withNodes=True)


# Click the links below `sign` and you are taken to the CDLI page for this tablet.
# 
# If we want to enlarge the sign, we can call it up with the lineart function.

# In[9]:


A.lineart([sign1, sign2], width=200)


# **N.B.**
# 
# For concepts that span one or more transliteration lines,
# such as *tablet*, *face*, *column*, *line*, *case*, *comment*, you can get the source
# material by requesting the feature **srcLn**, as we have seen before.
# 
# For *inline* concepts, such as *clusters*, *quads*, and *signs*,
# there are functions in `A.`.
# 
# For signs we have:
# 
# * `atfFromSign(sign, flags=False)`
# 
#   Returns the ATF representation for a sign, including primes, repeats, variants, modifiers,
#   and, optionally, flags.

# The unaugmented transliteration of a single sign can be obtained from the feature **grapheme**:

# In[10]:


print(F.grapheme.v(sign1))
print(F.grapheme.v(sign2))


# Let's pretty-print the line in which sign2 occurs:

# In[11]:


A.pretty(L.u(sign2, otype='line')[0])


# ## Occurrences of a sign
# 
# Now we are using something we learned before: we want all signs with exactly
# the grapheme `GU7`, regardless of augments or flags:

# In[12]:


gu7s = F.grapheme.s('GU7')
len(gu7s)


# Or, with a search template:

# In[13]:


results = A.search('''
sign grapheme=GU7
''')


# ### With `table()` and `show()`
# The simplest way to show the results is with `A.table()` for a compact tabular view, or with
# `A.show()` with a full context view.
# 
# We show a tabular view of 3 occurrences, including node numbers.
# The show view can be quite unwieldy, so we show a only 3 tablets.

# In[14]:


A.table(results, withNodes=True, end=3)


# In[15]:


A.show(results, end=3, showGraphics=False)


# ### As a plain list
# 
# There are a few hundred occurrences, we show a bit more context for them, like we did before.
# We show the full grapheme, with all its augments, **and flags**.
# We also show the full source line.

# In[16]:


for g in gu7s[0:10]:
    t = L.u(g, otype='tablet')[0]
    cl = A.lineFromNode(g)
    pNum = T.sectionFromNode(t)[0]
    gRep = A.atfFromSign(g, flags=True)

    line = F.srcLn.v(cl)

    print(f'{gRep:<7} {pNum} {line}')


# ### As a linked table
# 
# We can make it more user friendly: we can link each occurrence to its page on CDLI, and
# put everything in a Markdown table.
# 
# We have a function to generate the link: `A.cdli()`.
# 
# We build a markdown table.
# 
# We write a function for this, because we want to do it again.
# 
# First we use the function to write the first 10 to the screen,
# and then to write the whole set to a directory on your file system.

# In[17]:


def showSigns(signs, amount=None):

    markdown = '''
    sign | tablet | line
    ---- | ------ | ----
    '''.strip()

    for g in (
        signs if amount is None else signs[0:amount]
    ):
        t = L.u(g, otype='tablet')[0]
        cl = A.lineFromNode(g)
        gRep = A.atfFromSign(g, flags=True)
        line = F.srcLn.v(cl).replace('|', '&#124;')

        markdown += f'\n{gRep} | {A.cdli(t, asString=True)} | {line}'

    markdown += '\n'
    return markdown


# In[18]:


Markdown(showSigns(gu7s, 3))


# A bit more please ...

# In[19]:


Markdown(showSigns(gu7s, 10))


# ### Everything to file
# 
# We give you the whole list, in a Markdown file,
# on your local system.

# In[20]:


with open(f'{A.tempDir}/gu7.md', 'w') as fh:
    fh.write(showSigns(gu7s))

print(f'data written to file {A.tempDir}/gu7.md')


# <img src="images/atomMarkdown.png" width="600" align="right"/>
# 
# Have a look!
# 
# **Tip:** Open the file in [Atom](https://github.com/atom/atom).
# Switch to preview by Ctr+Shift+M (in Atom).
# 
# Again, the tablet links are clickable, and bring you straight to CDLI.
# 
# 

# ## Frequency lists
# 
# We use a bit more power of Text-Fabric by generating frequency lists.
# 
# ### Graphemes
# 
# We just studied the `GU7` grapheme a bit.
# Suppose we want to get an overview of all graphemes?
# 
# There is a generic Text-Fabric function to give us that.
# For each feature you can call up a frequency list of its values.

# In[21]:


graphemes = F.grapheme.freqList()
len(graphemes)


# We show the top-20:

# In[22]:


graphemes[0:20]


# **N.B.:**
# 
# * empty graphemes: `('', 12440),` These have been inserted by the conversion
#   to Text-Fabric inside comments, in order to link them to the tablets.
# * ellipsis graphemes: correspond to the `...` in ATF, usually within an uncertainty
#   cluster `[...]`

# ### Augments
# 
# We can quickly get an overview of all kinds of augments: primes ,variants, modifiers, flags.

# #### Prime
# 
# The prime is a feature with values: 2, 1 or 0. 
# The number indicates the number of primes.
# Below you see how often that occurs.
# Note that we count all primes here: on signs, case numbers and column numbers.

# In[23]:


for (value, frequency) in F.prime.freqList():
    print(f'{frequency:>5} x {value}')


# #### Variant
# 
# The variant or *allograph* is what occurs after the grapheme and after the `~` symbol, which should be digits and/or
# lowercase letters except the `x`.
# 
# Here is the frequency list of variant values.

# In[24]:


for (value, frequency) in F.variant.freqList():
    print(f'{frequency:>5} x {value}')


# #### Modifier
# 
# The modifier is what occurs after the grapheme and after the `@` symbol
# It consists of digits and/or
# lowercase letters except the `x`.
# 
# Sometimes modifiers occur inside a repeat, then we have stored the modifier in the feature
# *modifierInner*, as in
# 
# ```
# 7(N34@f)
# ```
# 
# Here is the frequency list of *modifier* and *modifierInner* values.

# In[25]:


for (value, frequency) in F.modifier.freqList():
    print(f'{frequency:>5} x {value}')


# In[26]:


for (value, frequency) in F.modifierInner.freqList():
    print(f'{frequency:>5} x {value}')


# ### Full signs
# 
# We make a frequency list of all full signs, i.e. the grapheme including variant, modifier, and prime.
# We show them as they appear in transcriptions.
# 
# We only deal with instances which are not contained in a quad.
# 
# This is no longer the frequency distribution of the values of a single feature,
# so we have to do the coding ourselves.

# In[27]:


fullGraphemes = collections.Counter()

for n in F.otype.s('sign'):
    grapheme = F.grapheme.v(n)
    if grapheme == '' or grapheme == '…' or grapheme == 'X':
        continue
    fullGrapheme = A.atfFromSign(n)
    fullGraphemes[fullGrapheme] += 1
    
len(fullGraphemes)


# Or with a query:

# In[28]:


query = '''
sign type=ideograph|numeral
'''
fullGraphemesQ = {A.atfFromSign(r[0]) for r in A.search(query, silent=True)}
len(fullGraphemesQ)


# There! We have counted all incarnations of full graphemes, and there are 1476 distinct ones.
# 
# We show the top-20, sorted by frequency.
# 
# We specify a `key` function, that given an (value, amount) pair returns
# (-amount, value).
# This determines the order after sorting. Signs with a high value of amount come
# before signs with a low value.

# In[29]:


for (value, frequency) in sorted(
    fullGraphemes.items(), 
    key=lambda x: (-x[1], x[0]),
)[0:20]:
    print(f'{frequency:>5} x {value}')


# ### Writing results to file
# 
# We also want to write the results to files in your `_temp` directory, within this repo.
# 
# `writeFreqs` writes distribution data of data items called `dataName`
# to a file `fileName.txt`.
# In fact, it writes two files: 
# * `fileName-alpha.txt`, ordered by data items
# * `fileName-freq.txt`, ordered by frequency.

# In[30]:


def writeFreqs(fileName, data, dataName):
    print(f'There are {len(data)} {dataName}s')

    for (sortName, sortKey) in (
        ('alpha', lambda x: (x[0], -x[1])),
        ('freq', lambda x: (-x[1], x[0])),
    ):
        with open(f'{A.tempDir}/{fileName}-{sortName}.txt', 'w') as fh:
            for (item, freq) in sorted(data, key=sortKey):
                if item != '':
                    fh.write(f'{freq:>5} x {item}\n')


# In[31]:


writeFreqs('grapheme-plain', F.grapheme.freqList(), 'bare grapheme')


# In[32]:


writeFreqs('grapheme-full', fullGraphemes.items(), 'full grapheme')


# Now have a look at your {{A.tempDir}} and you see two generated files:
# 
# * `graphemes-plain-alpha.txt` (sorted by grapheme)
# * `graphemes-plain-freq.txt` (sorted by frequency)
# * `graphemes-full-alpha.txt` (sorted by grapheme)
# * `graphemes-full-freq.txt` (sorted by frequency)

# ## Next
# 
# [quads](quads.ipynb)
# 
# *Things never stay simple ...*
