import math
import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt


def _points(number):
    """
     Calculates how many points a customer earns on a purchase
     input: float, int
     output: float
     """   
    return (math.ceil(number / 100) * 100) / 10


def _get_total_points_redeemed(df):
    """
    Calculates how many points a customer redeemed based on 
    the value of the purchase. Works with a DataFrame which 
    contains columns 'point_differential' and 'value'.
    input: DataFrame
    output: float
    """
    if sum(df['point_differential']) != 0: 
        total_points_redeemed = \
            sum([(math.floor((x - y) / 1000) * 1000) 
                 for x,y 
                 in zip([_points(df['value'].iloc[transaction]) 
                         for transaction 
                         in range(len(df))],df['point_differential'])])
    else:
        total_points_redeemed = 0      
    return total_points_redeemed


def fill_missing_data(df):
    """
    Using a table with individual transactions for each customer
    calculates aggregate statistics and fills in columns of 
    'number_of_purchases', 'value_of_purchases','total_points_redeemed',
    'total_standard_points'.
    
    input: DataFrame
    output: DataFrame
    """
    agg_data = pd.DataFrame()
    number_of_purchases = []
    value_of_purchases = []
    total_points_redeemed = []
    user_id = []
    total_standard_points = []

    for i, d in df.groupby(df.user_id):
        total_standard_points.append(sum(d['value'].apply(_points)))
        total_points_redeemed.append(_get_total_points_redeemed(d))
        number_of_purchases.append(len(d.index))
        value_of_purchases.append(d['value'].sum())
        user_id.append(d['user_id'].iloc[0])

    agg_data['user_id'] = user_id
    agg_data['number_of_purchases'] = number_of_purchases
    agg_data['value_of_purchases'] = value_of_purchases
    agg_data['total_points_redeemed'] = total_points_redeemed
    agg_data['total_standard_points'] = total_standard_points
    
    return agg_data


###
# Plotting utilities
###

def get_mean_error(overall, group_a, group_b):
    
    mean_o = sum(overall)/len(overall)
    mean_a = sum(group_a)/len(group_a)
    mean_b = sum(group_b)/len(group_b)

    error_o = stats.sem(overall)
    error_a = stats.sem(group_a)
    error_b = stats.sem(group_b)
    
    mean_ = [mean_o, mean_a, mean_b]
    error_ = [error_o, error_a, error_b]
    
    return mean_,error_

def bars(list_means, list_errors, title, ylabel,ax):
    bar_width = 0.35
    index = np.arange(len(list_means))
    
    if len(list_means) == 3:
        color = ['k','r','b']
        xtick_labels = ('Overall', 'Enrolled','Control')
    else:
        color = ['r','b']
        xtick_labels = ('Enrolled','Control')

    rects = ax.bar(range(len(list_means)), 
                   list_means, bar_width, color=['k','r','b'], 
                   yerr=list_errors, alpha=0.5, 
                   error_kw=dict(ecolor='black', lw=2, capsize=5, capthick=2))

    plt.title(title,size=15)
    plt.xticks(index + bar_width / 2,xtick_labels,size=13)
    plt.ylabel(ylabel,size=13)
    plt.xlabel('Loyalty program', size=13)
    plt.yticks(np.round(np.linspace(0,max(list_means)+50,6),1),size=13)
    plt.legend()