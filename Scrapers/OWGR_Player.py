#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: bradklassen
"""

#Import Libraries
from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
import numpy as np
import os
import pathlib

#Urls
url_base_1 = 'http://www.owgr.com/Ranking/PlayerProfile.aspx?playerID='
url_base_2 = '&year='

#Creates empty lists
events = []
names = []
names_list = []

#Player ID Loop
for i in range(18075,18085):
    print('Player ID: ' + str(i))
    #Year Loop (beginning in 1985)
    for j in range(1985,2020):
        try:
            html = urlopen(url_base_1 + str(i) + url_base_2 + str(j))
            soup = BeautifulSoup(html, 'lxml')
            name = str(soup.find('h2').contents[0])
            trs = soup.find_all(id='player_results')
            for tr in trs:
                  tds = tr.find_all('td')
                  for td in tds:
                      events.append(td.text)
                      names.append(name)
        except:
            pass

#Keeps every 9th element in list
names_list = names[0::9]

#Combines numerous lists into one for each record
composite_list_1 = [events[x:x+9] for x in range(0, len(events),9)]

#List of columns
column_list = ['Event','Tour','Week','Year','Finish','Rank_Points','Weight',
               'Adjusted_Points','Rank_After']

#Creates dataframe
player_df = pd.DataFrame(composite_list_1, columns=column_list)

#Creates Name column usign names_list
player_df['Name'] = names_list

#Replaces '-' with ''
player_df.replace(to_replace = ['-',''], value = np.nan, inplace = True)

#Re-orders dataframe
player_df = player_df[['Name','Event','Tour','Week','Year','Finish','Rank_Points',
                       'Weight','Adjusted_Points','Rank_After']]

#Convert to string and remove text from column
player_df['Rank_After'] = player_df['Rank_After'].astype(str).str.extract('(\d+)')

#Convert columns to numeric
cols = player_df.columns.drop(['Name','Event','Tour'])
player_df[cols] = player_df[cols].apply(pd.to_numeric, errors='coerce')

#Sorts by dataframe year and week ascending
player_df = player_df.sort_values(['Year', 'Week'], ascending=True)

#Creates new column indicating Professional or Amateur
player_df['Pro/Am'] = 'Pro'

#Assigns 'Am' to column for Amateur players
player_df.loc[player_df['Name'].str.contains('\(Am\)'), 'Pro/Am'] = 'Am'
player_df.loc[player_df['Name'].str.contains('\(AM\)'), 'Pro/Am'] = 'Am'
player_df.loc[player_df['Name'].str.contains('\(am\)'), 'Pro/Am'] = 'Am'
player_df.loc[player_df['Name'].str.contains('\(Am'), 'Pro/Am'] = 'Am'
player_df.loc[player_df['Name'].str.contains('\(A\)'), 'Pro/Am'] = 'Am'
player_df.loc[player_df['Name'].str.contains('\(A'), 'Pro/Am'] = 'Am'

#Removes any indication of amateur from 'Name' column
player_df['Name'] = player_df['Name'].str.replace('\(Am\)', '').str.replace('\(AM\)', '')\
.str.replace('\(am\)', '').str.replace('\(Am', '').str.replace('\(A\)', '')\
.str.replace('\(A', '')

#Strips leading whitespace and period
player_df['Name'] = player_df['Name'].str.strip().str.strip('\. ')

#Deletes records where 'Name' is 'missed missed' or 'Missed missed'
player_df = player_df[player_df['Name'] != 'missed missed']
player_df = player_df[player_df['Name'] != 'Missed missed']

#Ensures there are no duplicates
player_df.drop_duplicates(inplace=True)

#Creates data path
data_path = pathlib.Path(os.getcwd())/"GitHub"/"OWGR_Scraper"/"Data" 

#Output as CSV
player_df.to_csv(str(data_path) + "/OWGR_Player.csv", index=False)