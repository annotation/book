#!/usr/bin/env python
# coding: utf-8

# <img align="right" src="images/tf-small.png" width="128"/>
# <img align="right" src="images/phblogo.png" width="128"/>
# <img align="right" src="images/dans.png"/>
# 
# ---
# Start with [convert](https://nbviewer.jupyter.org/github/annotation/banks/blob/master/programs/convert.ipynb)
# 
# ---

# # Share the Banks example corpus

# In[1]:


get_ipython().run_cell_magic('sh', '', '\ntext-fabric-zip annotation/banks/tf')


# ## Share the similarity feature as a module
# 
# We do not attach the similarity data to a release, since we intend to update this data quite a few times
# after tweaking the parameters of the algorithm by which we create it.
# 
# That means that users will get this data from the latest commit.
# 
# So we make sure that the similarity data is committed and pushed to GitHub.
