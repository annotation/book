#!/usr/bin/env python
# coding: utf-8

# <img align="right" src="images/ninologo.png" width="150"/>
# <img align="right" src="images/tf-small.png" width="125"/>
# <img align="right" src="images/dans.png" width="150"/>
# 
# # Imagery
# 
# The **Cuneiform Digital Library Initiative** [CDLI](https://cdli.ucla.edu)
# contains photographic and lineart imagery for tablets and individual ideographs in the
# [Uruk IV/III](http://cdli.ox.ac.uk/wiki/doku.php?id=proto-cuneiform)
# corpus.
# 
# Here we show how we can employ them.
# 
# More details of the provenance of the images can be found
# in [about](https://github.com/Nino-cunei/uruk/blob/master/docs/images.md).

# ## The `lineart` and `photo` and `cdli` functions
# 
# We have made utility functions `lineart(nodes)` and `photo(nodes)` in the *cunei* module.
# They look up the photos and linearts for nodes, and show them in a row.
# 
# The `cdli(node)` function produces a link to the archival page of the tablet corresponding to `node`.
# 
# **Caveat:** We will use a few functions we have not explained before.
# See this chapter as a showcase of what can be done.
# You want to return to this after you have digested further chapters.

# ## Start up
# 
# We import the Python modules we need.

# In[1]:


get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')


# In[2]:


import sys, os
from tf.app import use


# We set up our working locations on the file system.

# In[3]:


A = use('uruk:clone', checkout="clone", hoist=globals())
# A = use('uruk', hoist=globals())


# ## Tablets
# 
# We will work with two example tablets.

# In[4]:


pNum1 = 'P000014'
pNum2 = 'P000022'


# Let's first show the pretty displays of their transcriptions.

# In[5]:


p1Node = T.tabletNode(pNum1)
p2Node = T.tabletNode(pNum2)


# In[6]:


A.pretty(p2Node)


# If you want only one face, you can do that.

# In[7]:


for f in L.d(p2Node, otype='face'):
  A.pretty(f)


# Or we could do it per column:

# In[8]:


for f in L.d(p2Node, otype='column'):
  A.pretty(f, withNodes=True)


# We start with showing one photo.
# Note, that if you click on the photo, 
# you will be taken to a higher resolution version on CDLI.
# 
# And if you click on the caption, you will be taken to the main page for the tablet on CDLI.

# In[9]:


A.photo(pNum1)


# If you want it smaller, you can set the width.
# 
# The width may be an integer indicating the amount of pixels, or any string that is acceptable
# as a measure in
# [CSS](https://developer.mozilla.org/en-US/docs/Web/CSS/length).

# In[10]:


A.photo(pNum1, width=200)


# In[11]:


A.photo(pNum1, width="10em")


# If you do not want to show the caption, say:

# In[12]:


A.photo(pNum1, width=100, withCaption=False)


# You can position the caption:

# In[13]:


A.photo(pNum1, width=100, withCaption='top')


# In[14]:


A.photo(pNum1, width=100, withCaption='left')


# In[15]:


A.photo(pNum1, width=100, withCaption='right')


# Instead of providing a P-number, you can also specify a node:

# In[16]:


tablet1 = T.nodeFromSection((pNum1,))
tablet2 = T.nodeFromSection((pNum2,))


# If you want to show them in a row:

# In[17]:


A.photo([tablet1, tablet2], height="200")


# If you want to show the links only, not the images themselves:

# In[18]:


A.photo([tablet1, tablet2], asLink=True)


# If you also want the links to the main pages on CDLI:

# In[19]:


A.photo([tablet1, tablet2], asLink=True, withCaption='bottom')


# ## Lineart
# 
# ### Tablets
# 
# We show the lineart for our example tablets:

# In[20]:


A.lineart([pNum1, pNum2])


# Again, we can identify the tablets equally well with their nodes.
# Let's make them smaller:

# In[21]:


A.lineart([tablet1, tablet2], width=100)


# We can set a height and a width, they act as maximum constraints.

# In[22]:


A.lineart([tablet1, tablet2], width=200, height=100)


# If you insist that the width should be fully realized, you can use a `!` in fron of the value.

# In[23]:


A.lineart([tablet1, tablet2], width='!200', height=100)


# Note that this distorts the aspect ratio.
# But sometimes you may want that.

# In[24]:


A.lineart([tablet1, tablet2], width='!200', height='!200')


# ### Keys
# 
# Some tablets have additional linearts.
# We can select them by their *key*. 
# The default lineart is keyed by the empty string,
# and this one will be chosen if you do not pass a key, as we did above.
# 
# In order to know which keys there are for a tablet, just call lineart with a non-existing key:

# In[25]:


pNum3 = 'P003553'


# In[26]:


A.lineart(pNum3, key='xxx')


# So this tablet has the empty key, and also key `d`.
# Let's get the latter one:

# In[27]:


A.lineart(pNum3, key='d')


# A bit smaller:

# In[28]:


A.lineart(pNum3, key='d', width=600)


# We navigate to a famous example tablet and show the lineart.

# In[29]:


pNumX = 'P005381'


# In[30]:


A.lineart(pNumX, width=300)


# We also want to see the transcription.

# In[31]:


tabletX = T.nodeFromSection((pNumX,))
sourceLines = A.getSource(tabletX)
print('\n'.join(sourceLines))


# ### Ideographs
# 
# We want to show the ideographs for case `1.a` in column 1.
# 
# If you click on an ideograph, you will be taken to the image file on CDLI.
# However, due to some discrepancies between the ideographs in the CDLI big list and their
# download package, some of these links may be broken.

# In[32]:


case = A.nodeFromCase((pNumX, 'obverse:1', '1a'))
for ideo in A.getOuterQuads(case):
    A.lineart(ideo, withCaption=False, height=50)


# Note that the images are stacked vertically.

# ### Images in a row
# 
# You can also have `lineart()` put images in a row.
# Just pass multiple nodes to it.
# 
# In this case we also show the captions.
# The link under the caption goes to a big list on CDLI with all ideographs.

# In[33]:


A.lineart(A.getOuterQuads(case), height=50)


# You can also call up these images by the name of the quad or sign:

# In[34]:


A.lineart(['2(N14)', 'SZE~a', 'SAL', 'TUR3~a', 'NUN~a'], height=50, withCaption='top')


# ## Existence of images
# 
# Sometimes you want to test whether an image exists.
# So far, if an image does not exist, a placeholder warning text is output.
# 
# But if you say `warning=False`, the empty string is output.
# 
# That makes it easy to test whether an image is present and do something about it.

# In[35]:


pNum3 = 'P000013'


# In[36]:


A.lineart(pNum3)


# In[37]:


A.lineart(pNum3, warning=False)


# If we prefer lineart, but in its absence accept a photo, we can say:

# In[38]:


A.lineart(pNum3, warning=False) or A.photo(pNum3)


# When there is lineart, it will be chosen:

# In[39]:


A.lineart(pNum2, warning=False) or A.photo(pNum2)


# Likewise, you can test wether there is lineart for ideographs:

# In[40]:


A.lineart('SZE', warning=False) or 'no lineart for SZE'


# In[41]:


A.lineart('SZE~a', warning=False) or 'no lineart for SZE~a'


# An other, direct way to test whether an image is present is this:

# In[42]:


'SZE' in A.imagery('ideograph', 'lineart')


# In[43]:


'SZE~a' in A.imagery('ideograph', 'lineart')


# In[44]:


'P000013' in A.imagery('tablet', 'lineart')


# In[45]:


'P000013' in A.imagery('tablet', 'photo')


# You can also get the lists of things for which there are images:

# In[46]:


ideos = A.imagery('ideograph', 'lineart')
len(ideos)


# In[47]:


print(' '.join(sorted(ideos)[0:100]))


# We make a list of all UKKIN ideographs:

# In[48]:


ukkin = sorted(i for i in ideos if 'UKKIN' in i)
A.lineart(ukkin, height=30, withCaption=False)


# Or a bit bigger, vertically stacked:

# In[49]:


for u in ukkin:
    A.lineart(u, width=50, withCaption='right')


# ## Annotated images
# 
# If you want to use an annotated image in a markdown cell, just copy one of the
# images you find in the (new) `cdli-imagery` directory over to the `images` directory
# (or any near directory you like). You might want to give it an other name.
# 
# Use an image editor to annotate the image, and use it like this:
# 
# ```
# ![dummy](images/P005381_l-obverse-1a.png)
# ```

# ![dummy](images/P005381_l-obverse-1a.png)

# If you want to resize, do this
# 
# ```html
# <img src="images/P005381_l-obverse-1a.png" width="200" />
# ```

# <img src="images/P005381_l-obverse-1a.png" width="200" />

# ## Online images
# 
# If you do not need to call up images in your notebook, but you want the online
# links to their counterparts on CDLI, that is also possible.
# 
# **N.B.:** Some of these links might be broken.

# In[50]:


A.lineart(['2(N14)', 'SZE~a', 'SAL', 'TUR3~a', 'NUN~a'], asLink=True, width=50)


# ## Next
# 
# [steps](steps.ipynb)
# 
# *One step at a time ...*
