#!/usr/bin/env python
# coding: utf-8

# <img align="right" src="images/ninologo.png" width="150"/>
# <img align="right" src="images/tf-small.png" width="125"/>
# <img align="right" src="images/dans.png" width="150"/>
# 
# # Jumps
# 
# Things do not only lie embedded in each other, they can also *point* to each other.
# The mechanism for that are *edges*. Edges are links between *nodes*.
# Like nodes, edges may carry feature values.
# 
# We learn how to deal with structure in a quantitative way.

# In[1]:


get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')


# In[2]:


import sys, os
import collections
from IPython.display import Markdown, display
from tf.app import use


# In[3]:


A = use('uruk:clone', checkout="clone", hoist=globals())
# A = use('uruk', hoist=globals())


# ## Measuring depth
# 
# Numbered lines in the transliterations indicate a hierarchy of cases within lines.
# How deep can cases go?
# We explore the distribution of cases with respect to their depth.
# 
# We need a function that computes the depth of a case.
# We program that function in such a way that it also works for *quads* (seen before),
# and *clusters* (will see later).
# 
# The idea of this function is:
# * if a structure does not have sub-structures, its depth is 1 or 0;
#   * it is 1 if the lowest level parts of the structure have a different name
#     such as quads versus signs;
#   * it is 0 if the lowest level parts of the structure have the same name,
#     such as cases in lines;
# * the depth of a structure is 1 more than the maximum of the depths of its sub-structures.
# 
# How do we find the sub-structures of a structure?
# By following *edges* with a `sub` feature, as we have seen in 
# [quads](quads.ipynb).

# In[4]:


def depthStructure(node, nodeType, ground):
    subDepths = [
        depthStructure(subNode, nodeType, ground) 
        for subNode in E.sub.f(node) 
        if F.otype.v(subNode) == nodeType
    ]
    if len(subDepths) == 0:
        return ground
    else:
        return max(subDepths) + 1


# ## Example: cases
# 
# We call up our example tablet and do a few basic checks on cases.
# 
# Note that there is also a feature **depth** that provides the depth at which a case is found,
# which is different from the depth a case has.

# In[5]:


pNum = 'P005381'
query = '''
tablet catalogId=P005381
'''
results = A.search(query)
A.show(results, withNodes=True, lineNumbers=True, showGraphics=False)


# In[6]:


line1 = T.nodeFromSection((pNum, 'obverse:1', '1'))
A.pretty(line1, showGraphics=False)
depthStructure(line1, 'case', 0)


# That makes sense, since case 1 is divided in one level of sub-cases: 1a and 1b.

# In[7]:


L.d(line1, otype='case')


# In[8]:


line2 = T.nodeFromSection((pNum, 'obverse:1', '2'))
A.pretty(line2, showGraphics=False)
depthStructure(line2, 'case', 0)


# Indeed, case 2 does not have a division in sub-cases.

# In[9]:


L.d(line2, otype='case')


# ## Counting by depth
# 
# For a variety of structures we'll find out how deep they go,
# and how depth is distributed in the corpus.

# ### Cases
# 
# We are going to collect all cases in buckets according to their depths.

# In[10]:


caseDepths = collections.defaultdict(list)

for n in F.otype.s('line'):
    caseDepths[depthStructure(n, 'case', 0)].append(n)
for n in F.otype.s('case'):
    caseDepths[depthStructure(n, 'case', 0)].append(n)

caseDepthsSorted = sorted(
    caseDepths.items(), 
    key=lambda x: (-x[0], -len(x[1])),
)

for (depth, casesOrLines) in caseDepthsSorted:
    print(f'{len(casesOrLines):>5} cases or lines with depth {depth}')


# We'll have some fun with this. We find two of the deepest cases, one on 
# a face that is as small as possible, one on a face that is as big as possible.
# 
# So we restrict ourselves to `caseDepths[4]`.
# 
# For all of these cases we find the face they are on, and the number of quads on that face.

# In[11]:


deepCases = caseDepths[4]
candidates = []

for case in deepCases:
    face = L.u(case, otype='face')[0]
    size = len(A.getOuterQuads(face))
    candidates.append((case, size))

sortedCandidates = sorted(
    candidates,
    key=lambda x: (x[1], x[0])
)
sortedCandidates


# We can do better than this!

# In[12]:


A.table(sortedCandidates)


# We can also assemble relevant information for this table by hand
# and put it in a markdown table.

# In[13]:


markdown = '''
case type | case number | tablet | face | size
------ | ---- | ---- | ---- | ----
'''.strip()
markdown += '\n'

bigCase = sortedCandidates[-1][0]
smallCase = sortedCandidates[0][0]

for (case, size) in sortedCandidates:
    caseType = F.otype.v(case)
    caseNum = F.number.v(case)
    face = L.u(case, otype='face')[0]
    tablet = L.u(case, otype='tablet')[0]
    markdown += f'''
{caseType} | {caseNum} | {A.cdli(tablet, asString=True)} | {F.type.v(face)} | {size}
'''.strip()
    markdown += '\n'

Markdown(markdown)


# Not surprisingly: the deepest cases are all lines.
# Because every case is enclosed by a line, which is one deeper than that case.
# 
# You can click on the P-numbers to view these tablets on CDLI.
# 
# We finally show the source lines that contain these deep cases.

# In[14]:


A.pretty(smallCase)
A.pretty(bigCase)


# With a bit of coding we can get another display:

# In[15]:


(smallPnum, smallColumn, smallCaseNum) = A.caseFromNode(smallCase)
(bigPnum, bigColumn, bigCaseNum) = A.caseFromNode(bigCase)

smallLineStr = '\n'.join(A.getSource(smallCase))
bigLineStr = '\n'.join(A.getSource(bigCase))

display(Markdown(f'''
**{smallPnum} {smallColumn} line {smallCaseNum}**

```
{smallLineStr}
```
'''))
A.lineart(smallPnum, width=200)

display(Markdown(f'''

---

**{bigPnum} {bigColumn} line {bigCaseNum}**

```
{bigLineStr}
```
'''))
A.photo(bigPnum, width=400)


# ### Quads
# 
# We just want to see how deep quads can get.

# In[16]:


quadDepths = collections.defaultdict(list)

for quad in F.otype.s('quad'):
    quadDepths[depthStructure(quad, 'quad', 1)].append(quad)

quadDepthsSorted = sorted(
    quadDepths.items(), 
    key=lambda x: (-x[0], -len(x[1])),
)

for (depth, quads) in quadDepthsSorted:
    print(f'{len(quads):>5} quads with depth {depth}')


# Lo and behold! There is just one quad of depth 3 and it is on our leading
# example tablet.
# 
# We have studied it already in [quads](quads.ipynb).

# In[17]:


bigQuad = quadDepths[3][0]
tablet = L.u(bigQuad, otype='tablet')[0]
A.lineart(bigQuad)
A.cdli(tablet)


# ### Clusters
# 
# Clusters are groups of consecutive quads between brackets.
# 
# Clusters can be nested.
# As with quads, we find the members of a cluster by following `sub` edges.

# #### Depths in clusters
# 
# We use familiar logic to get a hang of cluster depths.

# In[18]:


clusterDepths = collections.defaultdict(list)

for cl in F.otype.s('cluster'):
    clusterDepths[depthStructure(cl, 'cluster', 1)].append(cl)

clusterDepthsSorted = sorted(
    clusterDepths.items(), 
    key=lambda x: (-x[0], -len(x[1])),
)

for (depth, cls) in clusterDepthsSorted:
    print(f'{len(cls):>5} clusters with depth {depth}')


# Not much going on here.
# Let's pick a nested cluster.

# In[19]:


nestedCluster = clusterDepths[2][0]
tablet = L.u(nestedCluster, otype='tablet')[0]
quads = A.getOuterQuads(nestedCluster)
print(A.atfFromCluster(nestedCluster))
A.pretty(nestedCluster, withNodes=True)
A.lineart(quads[0], height=150)
A.cdli(tablet)


# #### Kinds of clusters
# 
# In our corpus we encounter several types of brackets:
# 
# * `( )a` for proper names
# * `[ ]` for uncertainty
# * `< >` for supplied material.
# 
# The next thing is to get on overview of the distribution of these kinds.

# In[20]:


clusterTypeDistribution = collections.Counter()

for cluster in F.otype.s('cluster'):
    typ = F.type.v(cluster)
    clusterTypeDistribution[typ] += 1

for (typ, amount) in sorted(
    clusterTypeDistribution.items(),
    key=lambda x: (-x[1], x[0]),
):
    print(f'{amount:>5} x a {typ:>8}-cluster')


# The conversion to TF has transformed `[...]` to a cluster of one sign with grapheme `…`.
# These are trivial clusters and we want to exclude them from further analysis, so we redo the counting.
# 
# First we make a sequence of all non-trivial clusters:

# In[21]:


realClusters = [
    c 
    for c in F.otype.s('cluster')
    if (
        F.type.v(c) != 'uncertain' or
        len(E.oslots.s(c)) > 1 or 
        F.grapheme.v(E.oslots.s(c)[0]) != '…'
    )
]
len(realClusters)


# Now we redo the same analysis, but we start with the filtered cluster sequence.

# In[22]:


clusterTypeDistribution = collections.Counter()

for cluster in realClusters:
    typ = F.type.v(cluster)
    clusterTypeDistribution[typ] += 1

for (typ, amount) in sorted(
    clusterTypeDistribution.items(),
    key=lambda x: (-x[1], x[0]),
):
    print(f'{amount:>5} x a {typ:>8}-cluster')


# #### Lengths of clusters
# 
# How long are clusters in general?
# There are two possible ways to measure the length of a cluster:
# 
# * the amount of signs it occupies;
# * the amount of top-level members it has (quads or signs)
# 
# By now, the pattern to answer questions like this is becoming familiar.
# 
# We express the logic in a function, that takes the way of measuring
# as a parameter.
# In that way, we can easily provide a cluster-length distribution based
# on measurements in signs and in quads.

# In[23]:


def computeDistribution(nodes, measure):
    distribution = collections.Counter()

    for node in nodes:
        m = measure(node)
        distribution[m] += 1

    for (m, amount) in sorted(
        distribution.items(),
        key=lambda x: (-x[1], x[0]),
    ):
        print(f'{amount:>5} x a measure of {m:>8}')


# In[24]:


def lengthInSigns(node):
    return len(L.d(node, otype='sign'))

def lengthInMembers(node):
    return len(E.sub.f(node))


# Now we can show the length distributions of clusters by just calling `computeDistribution()`:

# In[25]:


computeDistribution(realClusters, lengthInSigns)


# In[26]:


computeDistribution(realClusters, lengthInMembers)


# Of course, we want to see the longest cluster.

# In[27]:


longestCluster = [c for c in F.otype.s('cluster') if lengthInMembers(c) == 7][0]
A.pretty(longestCluster)


# #### Lengths of quads
# 
# If you look closely at the code for these functions, there is nothing in it that 
# is specific for clusters.
# 
# The measures are in terms of the totally generic `oslots` function, and the fairly generic
# `sub` edges, which are also defined for quads.
# 
# So, in one go, we can obtain a length distribution of quads.
# 
# Note that quads can also be sub-quads.

# In[28]:


computeDistribution(F.otype.s('quad'), lengthInSigns)


# In[29]:


computeDistribution(F.otype.s('quad'), lengthInMembers)


# In[30]:


longestQuad = [q for q in F.otype.s('quad') if lengthInSigns(q) == 5][0]
A.pretty(longestQuad)


# ## Next
# 
# [cases](cases.ipynb)
# 
# *In* case *you are serious ...*
