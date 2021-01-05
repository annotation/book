#!/usr/bin/env python
# coding: utf-8

# <img align="right" src="images/ninologo.png" width="150"/>
# <img align="right" src="images/tf-small.png" width="125"/>
# <img align="right" src="images/dans.png" width="150"/>
# 
# # Quads
# 
# When simple signs get stacked we get composite signs.
# Here we call them *quads*. 
# There are several ways to compose quads from sub-quads: there is always
# an *operator* involved.
# And a composition can again be subjected to an other composition.
# And again ...

# In[1]:


get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')


# In[2]:


import sys, os
from tf.app import use


# In[3]:


A = use('uruk:clone', checkout="clone", hoist=globals())
# A = use('uruk', hoist=globals())


# We need our example tablet (again).
# It is particularly relevant to this chapter in our tutorial: 
# it contains the most deeply nested quad in the whole corpus.

# In[4]:


pNum = 'P005381'
query = '''
tablet catalogId=P005381
'''
results = A.search(query)
A.lineart(results[0][0], width=200)
A.show(results, withNodes=True)


# The components of quads are either sub-quads or signs.
# Sub-quads are also quads in TF, and they are always a composition.
# Whenever a member of a sub-quad is no longer a composition, it is a *sign*.
# 
# Let's try to unravel the structure of the biggest quad in this tablet.

# ## Find the quad
# 
# First we need to get the node of this quad. Above we have seen the source code of the tablet in which
# it occurs, from that we can pick the node of the case it is in:

# In[5]:


case = A.nodeFromCase(('P005381', 'obverse:2', '1'))
print(A.getSource(case))
A.pretty(case, withNodes=True)


# We can easily read off the node number of this big quad.
# 
# But we can also do it programmatically.
# 
# In order to identify our super-quad, we list all quad nodes that are part of this case.
# For every quad we list the node numbers of the signs contained in it.
# 
# In order to know what signs are contained in any given node, we use the feature `oslots`.
# Like the feature `otype`, this is a standard feature that is always available in a TF dataset.
# 
# Unlike `otype`, `oslots` is an *edge* feature: there is an edge between every node and every slot contained in it.
# 
# Whereas you use `F` to do stuff with node features, you use `E` to do business with edge features.
# 
# And whereas you use `F.feature.v(node)` to get the feature value of a node, you use 
# `E.oslots.s(node)` to get the nodes for which there is an `oslots` edge from `node` to it.

# In[6]:


for node in L.d(case, otype='quad'):
    print(f'{node:>6} {E.oslots.s(node)}')


# We see what the biggest quad is.
# We could have been a bit more friendly to our selves by showing the actual graphemes in the quads.

# In[7]:


for node in L.d(case, otype='quad'):
    print(f'{node:>6} {" ".join(F.grapheme.v(s) for s in E.oslots.s(node))}')


# So let us get the node of the biggest quad.

# In[8]:


bigQuad = sorted(
    (
        quad 
        for quad in L.d(case, otype='quad')
    ),
    key = lambda q: -len(E.oslots.s(q))
)[0]
bigQuad


# Lo and behold, it is precisely the big quad.
# 
# This is what we are talking about:

# In[9]:


A.lineart(bigQuad)


# ## Quad structure
# 
# Now we are going to retrieve its components by following *edges*.
# 
# When we converted the data to Text-Fabric, we have made
# *edges* from quad nodes to the nodes of their component quads and signs.
# 
# We also have made edges between sibling quads and signs.
# 
# We can distinguish between kinds of edges by means of edge features.
# 
# The edges that go down in a structure have a feature `sub`.
# 
# In order to follow the `sub` edges from a node, you use 
# 
# `E.sub.f(node)`.
# 
# This will give you a list of nodes that can be reached *from* `node` by following
# a `sub` edge.
# 
# Edges can be traveled in the opposite direction as well:
# 
# `E.sub.t(node)`.
# 
# This will give you the nodes from which there is a `sub` edge *to* `node`.

# In[10]:


E.sub.f(bigQuad)


# or, more friendly:

# In[11]:


for node in E.sub.f(bigQuad):
    print(f'{node:>6} {" ".join(F.grapheme.v(s) for s in E.oslots.s(node))}')


# Let us unravel the whole structure by means of a function:

# In[12]:


def unravelQuad(quad):
    if F.otype.v(quad) == 'sign':
        return F.grapheme.v(quad)
    subQuads = E.sub.f(quad)
    unraveledSubQuads = [unravelQuad(subQuad) for subQuad in subQuads]
    return f'<{", ".join(unraveledSubQuads)}>'

unravelQuad(bigQuad)


# ## Operators
# 
# Where have the operators gone?
# 
# They are present as a feature `op` of edges between sibling quads and signs.

# In[13]:


for child in E.sub.f(bigQuad):
    for (right, op) in E.op.f(child):
        print(child, op, right)


# Note, that whereas `E.sub.f` yields a list of nodes,
# `E.op.f` yields a list of pairs (node, op-value),
# because the `op` edges carry a value.
# 
# The best way to know this, is to consult the
# [Feature Doc](https://github.com/Nino-cunei/uruk/blob/master/docs/transcription.md).
# This link as always present below the cell where you called `Cunei` for the first time.

# Can we try to adapt the unravel function above to get the operators?
# 
# Yes:

# In[14]:


def unravelQuad(quad):
    if F.otype.v(quad) == 'sign':
        return F.grapheme.v(quad)
    subQuads = E.sub.f(quad)
    result = '<'
    for sq in subQuads:
        for (rq, operator) in E.op.f(sq):
            leftRep = unravelQuad(sq)
            rightRep = unravelQuad(rq)
            result += f'{leftRep} {operator} {rightRep}'
    result += '>'
    return result

unravelQuad(bigQuad)


# This technique is employed fully in the function `A.atfFromQuad()`:

# In[15]:


print(A.atfFromQuad(bigQuad))


# We have tested the function `A.atfFromQuad()` on all quads in the corpus, an it regenerates the exact ATF transliterations for them, except for two cases where the ATF has unnecessary brackets. See [checks](http://nbviewer.jupyter.org/github/Nino-cunei/uruk/blob/master/programs/checks.ipynb#Quads).

# ## Next
# 
# [jumps](jumps.ipynb)
# 
# *Leap to the next level ...*
