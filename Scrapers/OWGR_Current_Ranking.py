#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: bradklassen
"""

#Import libraries     
from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
import numpy as np
import os
import pathlib

#Url
url = 'http://www.owgr.com/ranking?pageSize=All&country=All'

#Create soup
html = urlopen(url)
soup = BeautifulSoup(html, 'lxml')

#Create empty list to append data to
data = []    

#Find all rows
trs = soup.find_all('tr')

#Loop through rows
for tr in trs:
      tds = tr.find_all('td')
      for td in tds:
          data.append(td.text)

#Combines numerous lists into one for each record
composite_list = [data[x:x+11] for x in range(0, len(data),11)]

#List of columns
column_list = ['This_Week','Last_Week','End_2018','Blank','Name','Average_Points',
               'Total_Points','Events_Played_Divisor','Points_Lost_2019',
               'Points_Gained_2019','Events_Played_Actual']

#Creates dataframe
ranking_df = pd.DataFrame(composite_list, columns=column_list)

#Deletes unnecessary column 
del ranking_df['Blank']

#Finds week number
week = str(soup.find('h2').contents[0])

#Assigns week value to column 'Week'
ranking_df['Week'] = week

#Replaces '-' with ''
ranking_df.replace(to_replace = ['-',''], value = np.nan, inplace = True)

#Removes text from column
ranking_df['Week'] = ranking_df['Week'].str.extract('(\d+)')

#Convert columns to numeric
cols = ranking_df.columns.drop('Name')
ranking_df[cols] = ranking_df[cols].apply(pd.to_numeric, errors='coerce')

#Re-orders dataframe
ranking_df = ranking_df[['Week','This_Week','Last_Week','End_2018','Name',
                         'Average_Points','Total_Points','Events_Played_Divisor',
                         'Points_Lost_2019','Points_Gained_2019','Events_Played_Actual']]

#Creates new column indicating Professional or Amateur
ranking_df['Pro/Am'] = 'Pro'

#Assigns 'Am' to column for Amateur players
ranking_df.loc[ranking_df['Name'].str.contains('\(Am\)'), 'Pro/Am'] = 'Am'
ranking_df.loc[ranking_df['Name'].str.contains('\(AM\)'), 'Pro/Am'] = 'Am'
ranking_df.loc[ranking_df['Name'].str.contains('\(am\)'), 'Pro/Am'] = 'Am'
ranking_df.loc[ranking_df['Name'].str.contains('\(Am'), 'Pro/Am'] = 'Am'
ranking_df.loc[ranking_df['Name'].str.contains('\(A\)'), 'Pro/Am'] = 'Am'
ranking_df.loc[ranking_df['Name'].str.contains('\(A'), 'Pro/Am'] = 'Am'

#Removes any indication of amateur from 'Name' column
ranking_df['Name'] = ranking_df['Name'].str.replace('\(Am\)', '')\
.str.replace('\(AM\)', '').str.replace('\(am\)', '').str.replace('\(Am', '')\
.str.replace('\(A\)', '').str.replace('\(A', '')

#Strips leading whitespace and period
ranking_df['Name'] = ranking_df['Name'].str.strip().str.strip('\. ')

#Ensures there are no duplicates
ranking_df.drop_duplicates(inplace=True)

#Creates data path
data_path = pathlib.Path(os.getcwd())/"GitHub"/"OWGR_Scraper"/"Data" 

#Output as CSV
ranking_df.to_csv(str(data_path) + "/" +str(week).title().replace(" ", "_") + '.csv', index=False)
ranking_df.to_csv(str(data_path) + "/OWGR_Ranking.csv", index=False)