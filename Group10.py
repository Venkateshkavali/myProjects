# -*- coding: utf-8 -*-
"""
Created on Wed May 13 16:34:19 2020

@author: 
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import sqlite3
from sqlite3 import Error
#import gzip
import seaborn as sns
from sklearn.preprocessing import RobustScaler
#from sklearn.model_selection import train_test_split
#from sklearn.model_selection import StratifiedKFold



def create_connection(db_file, delete_db=False):
    if delete_db and os.path.exists(db_file):
        os.remove(db_file)
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        conn.execute("PRAGMA foreign_keys = 1")
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)
        
def credit_fraud(filename):
    k1=str(0)
    k2=str(1)
    list1 = []
    list2= []
    df=pd.read_csv(filename)
    
    with open(filename, 'rt') as f:
        f = f.read()
    lines = f.splitlines()
    '''for i in range(len(lines)):
        list1.append(lines[i].split(','))'''
    conn = create_connection(db_file)   
    cur = conn.cursor()
    with conn:
        '''for k in range(1,len(list1)-1):
            sql_statement="insert into credit_fraud values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) ;"
            cur.execute(sql_statement,tuple(list1[k]))'''
        sql_statement="select count(time) from credit_fraud"                        ### Total Transactions
        cur.execute(sql_statement)
        a=cur.fetchall()
        print(a)
        sql_statement="select count(class) from credit_fraud where class=\'\"%s\"\';"%(k1)  ###Normal Transaction
        cur.execute(sql_statement)
        b=cur.fetchall()
        print(b)
        sql_statement="select count(class) from credit_fraud where class=\'\"%s\"\';"%(k2)  ###Fraud transaction
        cur.execute(sql_statement)
        c=cur.fetchall()
        print(c)
    percent_fraud=(c[0][0]/a[0][0])*100
    percent_normal=(b[0][0]/a[0][0])*100
    percent_fraud=round(percent_fraud,2)
    percent_normal=round(percent_normal,2)
    print('Percentage of Nomal Transactions is ',percent_normal)
    print('Percentage of Fraud Transactions is ',percent_fraud)
    colors = ["#0101DF", "#DF0101"]
    sns.countplot('Class', data=df, palette=colors)
    plt.title('Class Distributions \n (0: Normal || 1: Fraud)', fontsize=14)
    fig, ax = plt.subplots(1, 2, figsize=(18,4))

    amount_val = df['Amount'].values
    time_val = df['Time'].values

    sns.distplot(amount_val, ax=ax[0], color='r')
    ax[0].set_title('Distribution of Transaction Amount', fontsize=14)
    ax[0].set_xlim([min(amount_val), max(amount_val)])

    sns.distplot(time_val, ax=ax[1], color='b')
    ax[1].set_title('Distribution of Transaction Time', fontsize=14)
    ax[1].set_xlim([min(time_val), max(time_val)])


    plt.show()

    ###############################################################
    rob_scaler = RobustScaler()

    df['scaled_amount'] = rob_scaler.fit_transform(df['Amount'].values.reshape(-1,1))
    df['scaled_time'] = rob_scaler.fit_transform(df['Time'].values.reshape(-1,1))

    df.drop(['Time','Amount'], axis=1, inplace=True)

    scaled_amount = df['scaled_amount']
    scaled_time = df['scaled_time']

    df.drop(['scaled_amount', 'scaled_time'], axis=1, inplace=True)
    df.insert(0, 'scaled_amount', scaled_amount)
    df.insert(1, 'scaled_time', scaled_time)
    
    #################################################################

    df.head()

    fig, ax = plt.subplots(1, 2, figsize=(18,4))

    amount_val = df['scaled_amount'].values
    time_val = df['scaled_time'].values

    sns.distplot(amount_val, ax=ax[0], color='r')
    ax[0].set_title('Distribution of Transaction Amount', fontsize=14)
    ax[0].set_xlim([min(amount_val), max(amount_val)])

    sns.distplot(time_val, ax=ax[1], color='b')
    ax[1].set_title('Distribution of Transaction Time', fontsize=14)
    ax[1].set_xlim([min(time_val), max(time_val)])

    plt.show()

    ####################################################################
    print('Normal', round(df['Class'].value_counts()[0]/len(df) * 100,2), '% of the dataset')
    print('Frauds', round(df['Class'].value_counts()[1]/len(df) * 100,2), '% of the dataset')

    ######################################################################
    
    df = df.sample(frac=1)

    # amount of fraud classes 492 rows.
    fraud_df = df.loc[df['Class'] == 1]
    non_fraud_df = df.loc[df['Class'] == 0][:492]

    normal_distributed_df = pd.concat([fraud_df, non_fraud_df])
    
    # Shuffle dataframe rows
    new_df = normal_distributed_df.sample(frac=1, random_state=42)

    #new_df.head()
    
    ######################################################################
    ########################################################
    print('Distribution of the Classes in the subsample dataset')
    print(new_df['Class'].value_counts()/len(new_df))

    sns.countplot('Class', data=new_df, palette=colors)
    plt.title('Equally Distributed Classes', fontsize=14)
    plt.show()
    # Make sure we use the subsample in our correlation

    f, (ax1, ax2) = plt.subplots(2, 1, figsize=(24,20))

    # Entire DataFrame
    corr = df.corr()
    sns.heatmap(corr, cmap='coolwarm_r', annot_kws={'size':20}, ax=ax1)
    ax1.set_title("Imbalanced Correlation Matrix \n (don't use for reference)", fontsize=14)
    
    sub_sample_corr = new_df.corr()
    sns.heatmap(sub_sample_corr, cmap='coolwarm_r', annot_kws={'size':20}, ax=ax2)
    ax2.set_title('SubSample Correlation Matrix \n (use for reference)', fontsize=14)
    plt.show()

    ################columndata####################
    
    f, axes = plt.subplots(ncols=4, figsize=(20,4))

    # Negative Correlations with our Class (The lower our feature value the more likely it will be a fraud transaction)
    sns.boxplot(x="Class", y="V17", data=new_df, palette=colors, ax=axes[0])
    axes[0].set_title('V17 vs Class Negative Correlation')

    sns.boxplot(x="Class", y="V14", data=new_df, palette=colors, ax=axes[1])
    axes[1].set_title('V14 vs Class Negative Correlation')


    sns.boxplot(x="Class", y="V12", data=new_df, palette=colors, ax=axes[2])
    axes[2].set_title('V12 vs Class Negative Correlation')
    

    sns.boxplot(x="Class", y="V10", data=new_df, palette=colors, ax=axes[3])
    axes[3].set_title('V10 vs Class Negative Correlation')

    plt.show()


    f, axes = plt.subplots(ncols=4, figsize=(20,4))

    # Positive correlations (The higher the feature the probability increases that it will be a fraud transaction)
    sns.boxplot(x="Class", y="V11", data=new_df, palette=colors, ax=axes[0])
    axes[0].set_title('V11 vs Class Positive Correlation')

    sns.boxplot(x="Class", y="V4", data=new_df, palette=colors, ax=axes[1])
    axes[1].set_title('V4 vs Class Positive Correlation')


    sns.boxplot(x="Class", y="V2", data=new_df, palette=colors, ax=axes[2])
    axes[2].set_title('V2 vs Class Positive Correlation')


    sns.boxplot(x="Class", y="V19", data=new_df, palette=colors, ax=axes[3])
    axes[3].set_title('V19 vs Class Positive Correlation')

    plt.show()

    #############################################################
    from scipy.stats import norm

    f, (ax1, ax2, ax3) = plt.subplots(1,3, figsize=(20, 6))

    v14_fraud_dist = new_df['V14'].loc[new_df['Class'] == 1].values
    sns.distplot(v14_fraud_dist,ax=ax1, fit=norm, color='#FB8861')
    ax1.set_title('V14 Distribution \n (Fraud Transactions)', fontsize=14)

    v12_fraud_dist = new_df['V12'].loc[new_df['Class'] == 1].values
    sns.distplot(v12_fraud_dist,ax=ax2, fit=norm, color='#56F9BB')
    ax2.set_title('V12 Distribution \n (Fraud Transactions)', fontsize=14)


    v10_fraud_dist = new_df['V10'].loc[new_df['Class'] == 1].values
    sns.distplot(v10_fraud_dist,ax=ax3, fit=norm, color='#C5B3F9')
    ax3.set_title('V10 Distribution \n (Fraud Transactions)', fontsize=14)

    plt.show()
    #######################################################################
    # # -----> V14 Removing Outliers (Highest Negative Correlated with Labels)
    v14_fraud = new_df['V14'].loc[new_df['Class'] == 1].values
    q25, q75 = np.percentile(v14_fraud, 25), np.percentile(v14_fraud, 75)
    print('Quartile 25: {} | Quartile 75: {}'.format(q25, q75))
    v14_iqr = q75 - q25
    print('iqr: {}'.format(v14_iqr))

    v14_cut_off = v14_iqr * 1.5
    v14_lower, v14_upper = q25 - v14_cut_off, q75 + v14_cut_off
    print('Cut Off: {}'.format(v14_cut_off))
    print('V14 Lower: {}'.format(v14_lower))
    print('V14 Upper: {}'.format(v14_upper))

    outliers = [x for x in v14_fraud if x < v14_lower or x > v14_upper]
    print('Feature V14 Outliers for Fraud Cases: {}'.format(len(outliers)))
    print('V10 outliers:{}'.format(outliers))

    new_df = new_df.drop(new_df[(new_df['V14'] > v14_upper) | (new_df['V14'] < v14_lower)].index)
    print('----' * 44)

    # -----> V12 removing outliers from fraud transactions
    v12_fraud = new_df['V12'].loc[new_df['Class'] == 1].values
    q25, q75 = np.percentile(v12_fraud, 25), np.percentile(v12_fraud, 75)
    v12_iqr = q75 - q25

    v12_cut_off = v12_iqr * 1.5
    v12_lower, v12_upper = q25 - v12_cut_off, q75 + v12_cut_off
    print('V12 Lower: {}'.format(v12_lower))
    print('V12 Upper: {}'.format(v12_upper))
    outliers = [x for x in v12_fraud if x < v12_lower or x > v12_upper]
    print('V12 outliers: {}'.format(outliers))
    print('Feature V12 Outliers for Fraud Cases: {}'.format(len(outliers)))
    new_df = new_df.drop(new_df[(new_df['V12'] > v12_upper) | (new_df['V12'] < v12_lower)].index)
    print('Number of Instances after outliers removal: {}'.format(len(new_df)))
    print('----' * 44)


    # Removing outliers V10 Feature
    v10_fraud = new_df['V10'].loc[new_df['Class'] == 1].values
    q25, q75 = np.percentile(v10_fraud, 25), np.percentile(v10_fraud, 75)
    v10_iqr = q75 - q25

    v10_cut_off = v10_iqr * 1.5
    v10_lower, v10_upper = q25 - v10_cut_off, q75 + v10_cut_off
    print('V10 Lower: {}'.format(v10_lower))
    print('V10 Upper: {}'.format(v10_upper))
    outliers = [x for x in v10_fraud if x < v10_lower or x > v10_upper]
    print('V10 outliers: {}'.format(outliers))
    print('Feature V10 Outliers for Fraud Cases: {}'.format(len(outliers)))
    new_df = new_df.drop(new_df[(new_df['V10'] > v10_upper) | (new_df['V10'] < v10_lower)].index)
    print('Number of Instances after outliers removal: {}'.format(len(new_df)))
    ########################################################################
    f,(ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(20,6))

    colors = ['#B3F9C5', '#f9c5b3']
              # Boxplots with outliers removed
              # Feature V14
    sns.boxplot(x="Class", y="V14", data=new_df,ax=ax1, palette=colors)
    ax1.set_title("V14 Feature \n Reduction of outliers", fontsize=14)
    ax1.annotate('Fewer extreme \n outliers', xy=(0.98, -17.5), xytext=(0, -12),
    arrowprops=dict(facecolor='black'),
    fontsize=14)

    # Feature 12
    sns.boxplot(x="Class", y="V12", data=new_df, ax=ax2, palette=colors)
    ax2.set_title("V12 Feature \n Reduction of outliers", fontsize=14)
    ax2.annotate('Fewer extreme \n outliers', xy=(0.98, -17.3), xytext=(0, -12),
    arrowprops=dict(facecolor='black'),
    fontsize=14)

    # Feature V10
    sns.boxplot(x="Class", y="V10", data=new_df, ax=ax3, palette=colors)
    ax3.set_title("V10 Feature \n Reduction of outliers", fontsize=14)
    ax3.annotate('Fewer extreme \n outliers', xy=(0.95, -16.5), xytext=(0, -12),
            arrowprops=dict(facecolor='black'),
            fontsize=14)


    plt.show()
             
    
def credit_fraud_table(db_file):
    conn = create_connection(db_file)   
    cur = conn.cursor()
    create_table_sql=''' create table credit_fraud ( Time float not null,
    V1 float not null,
    V2 float not null,
    V3 float not null,
    V4 float not null,
    V5 float not null,
    V6 float not null,
    V7 float not null,
    V8 float not null,
    V9 float not null,
    V10 float not null,
    V11 float not null,
    V12 float not null,
    V13 float not null,
    V14 float not null,
    V15 float not null,
    V16 float not null,
    V17 float not null,
    V18 float not null,
    V19 float not null,
    V20 float not null,
    V21 float not null,
    V22 float not null,
    V23 float not null,
    V24 float not null,
    V25 float not null,
    V26 float not null,
    V27 float not null,
    V28 float not null,
    Amount float not null,
    Class integer not null
    );
    '''
    create_table(conn, create_table_sql)
    
    #raise NotImplementedError()

# create table
db_file = 'C:/Users/venka/.spyder-py3/group10.db'
#credit_fraud_table(db_file)