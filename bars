"""

Includes a function for producing bar charts for visualization of the data.
"""

from matplotlib import ticker
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import random

#def set_plot(i,Y,TopicTitles):
#    colors = [(random.randint(0,255),random.randint(0,255),random.randint(0,255)) for color in range(50)]
## These are the "Tableau 20" colors as RGB.  
#
#  
## Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.  
#    for i in range(len(colors)):  
#      r, g, b = colors[i]  
#      colors[i] = (r / 255., g / 255., b / 255.)
#    s = pd.Series(Y[i],index = np.arange(2002, 2015))
#    ax = plt.subplot(25/5,5,i+1)
#    x_formatter = ticker.ScalarFormatter(useOffset=False)
#    y_formatter = ticker.ScalarFormatter(useOffset=False)
#    ax.yaxis.set_major_formatter(y_formatter)
#    ax.xaxis.set_major_formatter(x_formatter)
#    ax.set_title(TopicTitles[i])
#    ax.set_ylabel('Number of Papers')
#    plt.subplots_adjust(wspace=0.4,hspace=1)
#    pd.Series.plot(s, kind='bar', color=colors[i],)
#    font = {
#        'weight' : 'normal',
#        'size'   : 9}
#
#    plt.rc('font', **font)
    
    
def bar_charts(number_of_topics, Y, TopicTitles):
   """Creates two figures of bar charts for the number of papers published 
      from 2002 to 2014 for each topic"""
   
   # random colors as RGB    
   colors = [(random.randint(0,255),random.randint(0,255),random.randint(0,255)) for i in range(number_of_topics)]
 
   # Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.  
   for i in range(len(colors)):  
      r, g, b = colors[i]  
      colors[i] = (r / 255., g / 255., b / 255.) 

#plt.title("Total Delay Incident Caused by Carrier")
   plt.figure(num=2,figsize=(18,16))
   for i in range(25):
        s = pd.Series(Y[i],index = np.arange(2002, 2015))
        ax = plt.subplot(25/5,5,i+1)
        x_formatter = ticker.ScalarFormatter(useOffset=False)
        y_formatter = ticker.ScalarFormatter(useOffset=False)
        ax.yaxis.set_major_formatter(y_formatter)
        ax.xaxis.set_major_formatter(x_formatter)
        ax.set_title(TopicTitles[i])
        ax.set_ylabel('Number of Papers')
        plt.subplots_adjust(wspace=0.4,hspace=1)
        #ax.set_xlabel('Year of Publication')
##Set tick colors:
#
##ax.tick_params(axis='x', colors='blue')
##ax.tick_params(axis='y', colors='red')
#
##Plot the data:
##my_colors = 'rgbkymc'  #red, green, blue, black, etc.
#        
        pd.Series.plot(s, kind='bar', color=colors[i],)
#        #plt.setp([a.get_xticklabels() for a in f.axes[:-1]], visible=False)
#        #plt.tight_layout(pad=1.08, h_pad=None, w_pad=None, rect=None)
        font = {
        'weight' : 'normal',
        'size'   : 9}

        plt.rc('font', **font)        
        plt.show()
        
   plt.figure(num=3)
   for i in range(25):
        s = pd.Series(Y[i+25],index = np.arange(2002, 2015))
        
        ax = plt.subplot(25/5,5,i+1)
        x_formatter = ticker.ScalarFormatter(useOffset=False)
        y_formatter = ticker.ScalarFormatter(useOffset=False)
        ax.yaxis.set_major_formatter(y_formatter)
        ax.xaxis.set_major_formatter(x_formatter)
        ax.set_title(TopicTitles[i+25])
        ax.set_ylabel('Number of Papers')
        plt.subplots_adjust(wspace=0.4,hspace=1)
        pd.Series.plot(s, kind='bar', color=colors[i],)
        #plt.setp([a.get_xticklabels() for a in f.axes[:-1]], visible=False)
        #plt.tight_layout(pad=1.08, h_pad=None, w_pad=None, rect=None)
        font = {
        'weight' : 'normal',
        'size'   : 9}
        plt.rc('font', **font)       
        plt.show()
         



