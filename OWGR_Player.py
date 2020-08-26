#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: bradklassen
"""

from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
import numpy as np
import requests
import re

#%% Get IDs of all players currently ranked by OWGR

def player():

    # URL for all players currently ranked by Official World Golf Ranking
    url = 'http://www.owgr.com/en/Ranking.aspx?pageNo=1&pageSize=All&country=All'
    
    # Creates soup
    results_html = requests.get(url)
    results_soup = BeautifulSoup(results_html.text, 'lxml')
    
    # Creates empty lists
    a_tags_list = []
    digits = []
    
    # Finds all 'a' tags
    a_tags = results_soup.find_all('a')
    
    # Keeps href text from each 'a' tag
    for j in range(len(a_tags)):
        try:
            a_tags_list.append(a_tags[j]['href'])
        except:
            pass
    
    # Keep 'a' tags with '/players/player.'
    a_tags_list = [s for s in a_tags_list if 'PlayerProfile' in s]
    
    # Remove any string from elements in list (Only keep numbers) to get player ID's
    re_digits = re.compile(r'(-?(?:(?:\d+(?:\.\d*)?)|(?:\.\d+)))')
    for element in a_tags_list:
        digits += [str(n) for n in re_digits.findall(element)]
    
    # Remove leading '.' from player ID's
    player_ids = [s.strip('.') for s in digits]
    
    # Remove duplicate player ID's
    player_ids = list(set(player_ids))
    
    return(player_ids)

player_ids = player()

#%% Event data for each player

def acquire_data(player_ids):
    
    # Urls
    url_base_1 = 'http://www.owgr.com/Ranking/PlayerProfile.aspx?playerID='
    url_base_2 = '&year='
    
    # Creates empty lists
    events = []
    names = []
    
    # Player ID Loop
    for player_id in player_ids:
        
        print('ID: ' + str(player_id))
        
        html = urlopen(url_base_1 + str(player_id))
        soup = BeautifulSoup(html, 'lxml')
        
        # Get years athlete played
        years = []
        for option in soup.find_all('option'):
            years.append(option.text)
            
        years.remove('Counting Events')
        
        # Year loop
        for year in years:
            try:
                html = urlopen(url_base_1 + str(player_id) + url_base_2 + str(year))
                soup = BeautifulSoup(html, 'lxml')
                name = str(soup.find('h2').contents[0])
                trs = soup.find_all(id = 'player_results')
                for tr in trs:
                      tds = tr.find_all('td')
                      for td in tds:
                          events.append(td.text)
                          names.append(name)
            except:
                pass
            
    return(names, events)

names, events = acquire_data(player_ids)

#%% Clean data and create DataFrame

def clean_data(names, events):
    
    # Keeps every 9th element in list
    names_list = names[0::9]
    
    # Combines numerous lists into one for each record
    composite_list = [events[x:x+9] for x in range(0, len(events), 9)]
    
    # List of columns
    column_list = ['Event', 'Tour', 'Week', 'Year', 'Finish', 'Rank_Points', 
                   'Weight', 'Adjusted_Points', 'Rank_After']
    
    # Creates dataframe
    player_df = pd.DataFrame(composite_list, columns = column_list)
    
    # Creates Name column usign names_list
    player_df['Name'] = names_list
    
    # Replaces '-' with ''
    player_df.replace(to_replace = ['-',''], value = np.nan, inplace = True)
    
    # Re-orders dataframe
    player_df = player_df[['Name', 'Event', 'Tour', 'Week', 'Year', 'Finish',
                           'Rank_Points', 'Weight', 'Adjusted_Points', 'Rank_After']]
    
    # Convert to string and remove text from column
    player_df['Rank_After'] = player_df['Rank_After'].astype(str).str.extract('(\d+)')
    
    # Convert columns to numeric
    cols = player_df.columns.drop(['Name','Event','Tour', 'Finish'])
    player_df[cols] = player_df[cols].apply(pd.to_numeric, errors = 'coerce')
    
    # Sorts by dataframe year and week ascending
    player_df = player_df.sort_values(['Name', 'Year', 'Week'], ascending = True)
    
    # Creates new column indicating Professional or Amateur
    player_df['Pro/Am'] = 'Pro'
    
    # Assigns 'Am' to column for Amateur players
    player_df.loc[player_df['Name'].str.contains('\(Am\)'), 'Pro/Am'] = 'Am'
    player_df.loc[player_df['Name'].str.contains('\(AM\)'), 'Pro/Am'] = 'Am'
    player_df.loc[player_df['Name'].str.contains('\(am\)'), 'Pro/Am'] = 'Am'
    player_df.loc[player_df['Name'].str.contains('\(Am'), 'Pro/Am'] = 'Am'
    player_df.loc[player_df['Name'].str.contains('\(A\)'), 'Pro/Am'] = 'Am'
    player_df.loc[player_df['Name'].str.contains('\(A'), 'Pro/Am'] = 'Am'
    
    # Removes any indication of amateur from 'Name' column
    player_df['Name'] = player_df['Name'].str.replace('\(Am\)', '').str.replace('\(AM\)', '')\
    .str.replace('\(am\)', '').str.replace('\(Am', '').str.replace('\(A\)', '')\
    .str.replace('\(A', '')
    
    # Strips leading and trailing whitespace and period
    player_df['Name'] = player_df['Name'].str.strip().str.strip('\. ')
    
    # Strips leading and trailing whitespace
    player_df['Event'] = player_df['Event'].str.strip()
    
    # Deletes records where 'Name' is 'missed missed' or 'Missed missed'
    player_df = player_df[player_df['Name'] != 'missed missed']
    player_df = player_df[player_df['Name'] != 'Missed missed']
    
    # Ensures there are no duplicates
    player_df.drop_duplicates(inplace = True)
    
    return(player_df)

player_df = clean_data(names, events)

# Output as CSV
player_df.to_csv('../OWGR_Player.csv', index = False)