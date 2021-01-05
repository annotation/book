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

# # Use the Banks example corpus

# ## Load TF
# 
# We are going to load the new data: all features.
# 
# We start a new instance of the TF machinery.

# In[1]:


get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')


# In[2]:


import os
import re

from tf.fabric import Fabric


# In[3]:


GH_BASE = os.path.expanduser('~/github')
ORG = 'annotation'
REPO = 'banks'
FOLDER = 'tf'
TF_DIR = f'{GH_BASE}/{ORG}/{REPO}/{FOLDER}'

VERSION = '0.2'

TF_PATH = f'{TF_DIR}/{VERSION}'
TF = Fabric(locations=TF_PATH)


# We ask for a list of all features:

# In[4]:


allFeatures = TF.explore(silent=True, show=True)
loadableFeatures = allFeatures['nodes'] + allFeatures['edges']
loadableFeatures


# We load all features:

# In[5]:


api = TF.load(loadableFeatures, silent=False)


# You see that all files are marked with a `T`.
# 
# That means that Text-Fabric loads the features by reading the plain text `.tf` files.
# But after reading, it makes a binary equivalent and stores it as a `.tfx`
# file in the hidden `.tf` directory next to it.
# 
# Furthermore, you see some lines marked with `C`. Here Text-Fabric is computing derived data,
# mostly about sections, the order of nodes, and the relative positions of nodes with respect to the slots they
# are linked to.
# 
# The results of this pre-computation are also stored in that hidden `.tf` directory.
# 
# The next time, Text-Fabric loads the data from their binary `.tfx` files, which is much faster.
# And the pre-computation step will be skipped.
# 
# If the binary files get outdated Text-Fabric will recompile and recompute everything automatically.
# 
# So let's load again.

# In[6]:


TF = Fabric(locations=TF_PATH)
api = TF.load(loadableFeatures, silent=False)


# Where there were `T`s before, there are now `B`s.

# ### Hoisting
# 
# We can access all TF data programmatically by using `A.api.Features`, or `A.api.F` (same thing) and a bunch of
# other API members. 
# 
# But if we working with a single data source, we hoist those API members to the global namespace.
# 
# Now you can directly refer to `F` and friends.

# In[7]:


api.makeAvailableIn(globals())


# As a result, you have an overview of the names you can use.

# ## Exploration
# 
# Finally, let's explore this set by means of Text-Fabric.
# 
# ### Frequency list
# 
# We can get ordered frequency lists for the values of all features.
# 
# First the words:

# In[8]:


F.letters.freqList()


# For the node types we can get info by calling this:

# In[9]:


C.levels.data


# It means that chapters are 49.5 words long on average, and that the chapter nodes are 101 and 102.
# 
# And you see that we have 99 words.

# ## Add to the banks corpus
# 
# We are going to make a relationship between each pair of words, and we annotate each related pair with how similar they are.
# 
# We measure the similarity by looking at the distinct letters in each word (lowercase), and computing the percentage of
# how many letters they have in common with respect to how many letters they jointly have.
# 
# This will become a symmetric edge feature. Symmetric means, that if a and b are similar, then b and a as well, with the
# same similarity.
# 
# We only store one copy of each symmetric pair of edges.
# 
# We can then use
# [`E.sim.b(node)`](https://annotation.github.io/text-fabric/Api/Features/#edge-features)
# to find all nodes that are parallel to node.
# 
# If words do not have letters in common, their similarity is 0, and we do not make an edge.

# ### Preparation
# 
# We pre-compute all letter sets for all words.

# In[10]:


def makeSet(w):
  return set(F.letters.v(w).lower())


# In[11]:


words = {}

for w in F.otype.s('word'):
  words[w] = makeSet(w)
    
nWords = len(words)
print(f'{nWords} words')


# In[12]:


def sim(wSet, vSet):
  return int(round(100 * len(wSet & vSet) / len(wSet | vSet)))


# ### Compute all similarities
# 
# We are going to perform all comparisons.
# 
# Since there are 99 words, this will amount to only 5000 comparisons.
# 
# For a big corpus, this amount will quickly grow with the number of items to be compared.
# 
# See for example the similarities in the 
# [Quran](https://nbviewer.jupyter.org/github/q-ran/quran/blob/master/programs/parallels.ipynb).

# In[13]:


def computeSim():
  similarity = {}

  wordNodes = sorted(words.keys())
  nWords = len(wordNodes)

  nComparisons = nWords * (nWords - 1) // 2

  print(f'{nComparisons} comparisons to make')

  TF.indent(reset=True)

  co = 0
  si = 0
  stop = False
  for i in range(nWords):
    nodeI = wordNodes[i]
    wordI = words[nodeI]
    for j in range(i + 1, nWords):
      nodeJ = wordNodes[j]
      wordJ = words[nodeJ]
      s = sim(wordI, wordJ)
      co += 1
      if s:
        similarity[(nodeI, nodeJ)] = sim(wordI, wordJ)
        si += 1
    if stop:
      break

  TF.info(f'{co:>4} comparisons and {si:>4} similarities')
  return similarity


# In[14]:


similarity = computeSim()


# In[15]:


print(min(similarity.values()))
print(max(similarity.values()))


# In[16]:


eq = [x for x in similarity.items() if x[1] >= 100]
neq = [x for x in similarity.items() if x[1] <= 50]


# In[17]:


print(eq[0])
print(neq[0])


# In[18]:


print(len(eq))
print(len(neq))


# In[19]:


print(eq[0][0][0], F.letters.v(eq[0][0][0]))
print(eq[0][0][1], F.letters.v(eq[0][0][1]))


# In[20]:


print(neq[0][0][0], F.letters.v(neq[0][0][0]))
print(neq[0][0][1], F.letters.v(neq[0][0][1]))


# ### Add parallels to the TF dataset
# 
# We now add this information to the Banks dataset as an *edge feature*.

# In[21]:


metaData = {
  '': {
    'name': 'Banks (similar words)',
    'converters': 'Dirk Roorda',    
    'sourceUrl': 'https://nbviewer.jupyter.org/github/annotation/tutorials/blob/master/text-fabric/use.ipynb',
    'version': '0.2',
  },
  'sim': {
    'valueType': 'int',
    'edgeValues': True,
    'description': 'similarity between words, as a percentage of the common material wrt the combined material',
  },
}


# In[22]:


simData = {}
for ((f, t), d) in similarity.items():
  simData.setdefault(f, {})[t] = d


# In[23]:


FOLDER_SIM = 'sim/tf'
path = f'{ORG}/{REPO}/{FOLDER_SIM}'
location = f'{GH_BASE}/{path}'
module = VERSION


# In[24]:


TF.save(edgeFeatures=dict(sim=simData), metaData=metaData, location=location, module=module)

