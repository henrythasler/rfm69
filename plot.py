import matplotlib.pyplot as plt
import numpy as np
import math

print '**Plotting results**'
fig, ax = plt.subplots( nrows=1, ncols=1 )  # create figure & 1 axis
fig.set_size_inches(8, 6)
npzfile = np.load("data.npz")

time = npzfile['x']
data = npzfile['y']

ax.step(time, data, linewidth=1, where='post')
ax.grid(True)
plt.show()