# -*- coding: utf-8 -*-
"""
Includes a function for visualization of data with a stack plot.
"""
from matplotlib import pyplot as plt
from matplotlib import ticker
import random

def stack(number_of_topics, TopicTitles, X, Y):
    """
    Create a stack plot for the number of papers published
    from 2002 to 2014 for each topic
    """
    # random colors as RGB
    colors = [(random.randint(0, 255), random.randint(0, 255),
               random.randint(0, 255)) for i in range(number_of_topics)]

    # Scale the RGB values to the [0, 1] range, which is the format
    # matplotlib accepts.
    for i in range(len(colors)):
        r, g, b = colors[i]
        colors[i] = (r / 255., g / 255., b / 255.)

    plt.figure(num=1, figsize=(30, 27))
    ax1 = plt.subplot()
    x_formatter = ticker.ScalarFormatter(useOffset=False)
    y_formatter = ticker.ScalarFormatter(useOffset=False)
    ax1.yaxis.set_major_formatter(y_formatter)
    ax1.xaxis.set_major_formatter(x_formatter)
    ax1.set_ylabel('Number of Papers')
    ax1.set_xlabel('Year of Publication')
    polys = ax1.stackplot(X, Y, colors=colors)

    legendProxies = []
    for poly in polys:
        legendProxies.append(plt.Rectangle((0, 0), 1, 1,
                             fc=poly.get_facecolor()[0]))

    plt.legend(legendProxies, TopicTitles, prop={'size':8})
    plt.tight_layout(pad=1.08, h_pad=None, w_pad=None, rect=None)
    plt.show()
