
# coding: utf-8

# In[104]:


import mdptoolbox
import numpy as np
from math import ceil, log


# In[105]:


N = 6
isBadSide = np.array([1,1,1,0,0,0])
print (isBadSide)


# In[113]:


lose_case = sum(isBadSide)
prob_lose = (lose_case)*1./N
# estimated earning if not badside
earnings = np.where(isBadSide == 0)[0]
earnings = earnings + 1
print earnings
mean_earn = np.mean(earnings)
expected_earn = (1-prob_lose) * mean_earn
expected_earn



# In[107]:



# GEOMETRIC DISTRIBUTION
# required times for 1 in a million chance
req_times = (log(0.000001) - log(prob_lose)) / log(1-prob_lose)
req_times = ceil(req_times)
req_times

# we will have 'req_times' attempts
number_of_states = int(int(expected_earn) * req_times)
number_of_states += 1
number_of_states


# In[108]:


# state change vector, if it is 0 then return to terminal state, if not add number of states

state_change = np.zeros(isBadSide.size, dtype=int)
state_change = state_change + range(1,N+1)
ind = np.array(np.where(isBadSide == 1)[0], dtype=int)
state_change[ind] = 0 
state_change


# In[109]:


probs = np.zeros((2,number_of_states, number_of_states))
bank_roll_of_states = range(number_of_states)
bank_roll_of_states

# first action is roll
for i in range(number_of_states):
    indices = i + state_change
    indices = indices[np.where(indices != i)[0]]
    indices = indices[np.where(indices < number_of_states)[0]]
    probs[0, i, indices] = 1./N
    probs[0,i,-1] = prob_lose
    probs[0,i,-2] = 1. - np.sum(probs[0, i, :]) + probs[0,i,-2]   
    
probs[0, -1, :] = np.zeros(number_of_states)
probs[0, -1, -1] = 1.

# second action is stop
for i in range(number_of_states):
    probs[1, i, -1] = 1.




# In[110]:


# rewards is action and state and also next state based 

rewards = np.zeros((2, number_of_states, number_of_states))

# for roll
for i in range(number_of_states):
    rewards[0, i, :] = range(-i, number_of_states-i)
    rewards[0, i, -1] = -i


# In[111]:


vi = mdptoolbox.mdp.ValueIteration(probs, rewards, 1)
vi.run()


# In[112]:


vi.V

