# What is Q?
# Q[s,a] = immediate reward + discounted reward

# How to use Q?
# Pi(s) = argmax-a(Q[s,a])

# Two finer points
# - Success depends on exploration
# - Choose random action with prob C


# State to consider:
# adjusted close/SMA, Bollinger Band Value
# P/E ratio
# Holding stock
# return since entry

# Discretizing number


# Summary

# Advantages
# The main advantage of a model-free approach like Q-Learning over model-based techniques is that it can easily be applied to domains where all states and/or transitions are not fully defined.
# As a result, we do not need additional data structures to store transitions T(s, a, s') or rewards R(s, a).
# Also, the Q-value for any state-action pair takes into account future rewards. Thus, it encodes both the best possible value of a state (maxa Q(s, a)) as well as the best policy in terms of the action that should be taken (argmaxa Q(s, a)).

# Issues
# The biggest challenge is that the reward (e.g. for buying a stock) often comes in the future - representing that properly requires look-ahead and careful weighting.
# Another problem is that taking random actions (such as trades) just to learn a good strategy is not really feasible (you'll end up losing a lot of money!).
# In the next lesson, we will discuss an algorithm that tries to address this second problem by simulating the effect of actions based on historical data.
