#!/usr/bin/env python3

###  plotting output from DiagenesisModel ###

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import glob
    
    
def plotSpatial(df, filename, benchmarkComp):
    '''
    Plot a depth profile for all solution variables at fixed time.

    Parameters
    ----------
    df : DataFrame
        Contents of ASCII file from DiagenesisModel stored as pandas df.
    filename : STR
        Name of the data file w/o extension, the plot will be saved under the same name.
    benchmarkComp : BOOL
        Switch for optionally plotting the fig3e benchmark data. 

    Returns
    -------
    None.

    '''
    
    Xs = 131.9/0.1 # depth scaling constant
    x = np.array(df.x*Xs)
    
    fig = plt.figure(figsize=(12,10))
    plt.plot(x,np.array(df.AR),label='AR')
    plt.plot(x,np.array(df.CA),label='CA')
    plt.plot(x,np.array(df.phi),label='phi')
    plt.plot(x,np.array(df.ca),label='Ca')
    plt.plot(x,np.array(df.co),label='CO')
    
    plotHeaviside(x/Xs)
    
    # if benchmark, plot the Fig3e data for comparison
    if (benchmarkComp):
        plotFig3e()
    
    plt.legend(loc='lower right')
    plt.xlabel('x (cm)')
    plt.ylabel('Concentrations')
    plt.xlim(0,500)
    plt.ylim(0,2.3)
    plt.savefig('%s.png'%(filename),bbox_inches='tight')
    plt.clf()
    
    
def plotTemporal(df, filename):
      '''
      Plot the time series at fixed depth for all solution variables from the 
      output of lheureux.f

      Parameters
      ----------
      df : DataFrame
          Contents of amarlx output file from lheureux.f stored as pandas df.
      filename : STR
          Name of the data file w/o extension, the plot will be saved under the same name.

      Returns
      -------
      None.

      '''
      Ts = 131.9/0.1**2 # time scaling constant
      t_plot = np.array(df.x*Ts/1000)
      
      fig = plt.figure(figsize=(12,10))
      plt.plot(t_plot, np.array(df.AR), label=df.columns[1])
      plt.plot(t_plot, np.array(df.CA), label=df.columns[2])
      plt.plot(t_plot, np.array(df.phi), label=df.columns[5])
      plt.plot(t_plot, np.array(df.ca), label=df.columns[3])
      plt.plot(t_plot, np.array(df.co), label=df.columns[4])
      plt.legend()
      plt.xlim(0,np.array(t_plot)[-1])
      plt.ylim(0,2.3)
      plt.xlabel('t (ka)')
      plt.ylabel('Concentrations') 
      plt.savefig('%s.png'%(filename),bbox_inches='tight')
      plt.clf()  


def plotFig3e():
    # plot the digitized Figure 3e vals from L'Heureux (2018)
    # This is the 'steady-state' case, phi_0 = 0.6, phi_init = 0.5
    # as an addition to a plot from code output
    
    
    # use default colour sequence from matplotlib to match data
    # order should be AR, CA, Po, Ca, Co
    colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
    
    bm = pd.read_csv('fig3e.csv')
    plt.scatter(np.array(bm.ARX), np.array(bm.ARY), label='bm_AR',marker='x',color=colors[0])
    plt.scatter(np.array(bm.CAX), np.array(bm.CAY), label='bm_CA',marker='x',color=colors[1])
    plt.scatter(np.array(bm.PoX), np.array(bm.PoY), label='bm_phi',marker='x',color=colors[2])
    plt.scatter(np.array(bm.CaX), np.array(bm.CaY), label='bm_ca',marker='x',color=colors[3])
    plt.scatter(np.array(bm.CoX), np.array(bm.CoY), label='bm_co',marker='x',color=colors[4])


def plotHeaviside(x):
    # plot the function used to define the ADZ
    
    # for now we hard-code these parameter values
    ADZ_top = 50
    ADZ_bot = 150
    x_scale = 131.9/0.1
    
    smoothK = 500
    
    h = 0.5**2 * ( 1 + np.tanh(smoothK*(x - (ADZ_top/x_scale))))*\
                 ( 1 + np.tanh(smoothK*((ADZ_bot/x_scale) - x)))
    plt.plot(x*x_scale, h, label='Heaviside', color='black', linestyle='--')



##############################################################################
def plotFrame(X, x, t, nnx, movieDir, U, W):
    
    # take current solution vars
    filename = '%s/solution_%.6f.png'%(movieDir, t)
    
    # plot spatial profile for all vars
    fig, axs = plt.subplots(2,1,sharex = True, figsize=(10,14),gridspec_kw={'height_ratios': [2, 1]})
    
    axs[0].plot(x,X[0:nnx],label='AR')
    axs[0].plot(x,X[nnx:2*nnx],label='CA')
    axs[0].plot(x,X[4*nnx:5*nnx],label='phi')
    axs[0].plot(x,X[2*nnx:3*nnx],label='c_ca')
    axs[0].plot(x,X[3*nnx:4*nnx],label='c_co')
    axs[0].legend(loc='upper right')
    axs[0].set(ylabel='Concentrations', xlim=(0,500), ylim=(0,1.75))
    
    axs[1].plot(x, U, label='U')
    axs[1].plot(x, W, label='W')
    axs[1].legend(loc='upper right')

    axs[1].set(xlim=(0,500), ylim=(-5,5), xlabel='x (cm)', ylabel='Velocities')
    
    # annotate with time
    axs[0].text(20, 1.7,'t = %.3e'%(t))
    fig.subplots_adjust(wspace=0, hspace=0.1)
    
    # save figure to a given directory
    plt.savefig(filename,bbox_inches='tight')
    plt.close()
    





































