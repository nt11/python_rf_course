import matplotlib.pyplot as plt
import matplotlib
import matpie as mp

matplotlib.use('TkAgg')  # Set the backend before doing anything else
plt.ion()               # Turn on interactive mode
a= 18
# Your plotting code here...
# For example:
plt.figure()
plt.plot([1, 2, 3], [1, 2, 3])
plt.show()
    #
    # # Keep the plots open
    # plt.ioff()              # Turn off interactive mode
    # plt.show(block=True)    # This will keep the window open


