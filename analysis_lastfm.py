# -*- coding: utf-8 -*-
"""
INLS490-P#2-CHECKPOINT#2

By Yaxue Guo, April 20, 2018

"""

from pandas import Series, DataFrame
import pandas as pd
import numpy as np
import codecs

# read two .dat file into dataframe without hierachical indexing  
# for further groupby operation
# merge two df to combine data 
user_artists_df = pd.read_table('user_artists.dat', encoding="utf-8",sep="\t")
artists_df = pd.read_table('artists.dat',encoding="utf-8",sep="\t")
ua_merge = user_artists_df.merge(artists_df, left_on="artistID", right_on="id")

'''1-who are the top artists?'''
# Use groupby to get groupby object - split 
g_weightbyartist = ua_merge.weight.groupby(ua_merge['artistID'])
# Calculate song plays across all users for artists from groupby obj
# -apply & -combine
s_weightbyartist = g_weightbyartist.sum()
print('\n'+ '!'*40 +'\n')
print('1. who are the top artists?')
# Put top 10 artists and weights in to series
s1 = s_weightbyartist.sort_values(ascending=False).head(10)
# Iterate through Series and grab artist name from another df by id
for (key,value) in s1.iteritems():
    print('    ',artists_df[artists_df.id==key].name.item(),'(',key,')  ',
          value,sep='')

'''2-what artists have most listeners?'''
# Same logic with question 1
g_listenerbyartist = ua_merge.userID.groupby(ua_merge['artistID'])
s_listenerbyartist = g_listenerbyartist.count()
print('\n'+ '!'*40 +'\n')
print('2. what artists have most listeners?')
s2 = s_listenerbyartist.sort_values(ascending=False).head(10)
for (key,value) in s2.iteritems():
    print('    ',artists_df[artists_df.id==key].name.item(),'(',key,')  ',
          value, sep='')

'''3-who are the top users in terms of play counts?'''
# Same logic with question 1
g_weightbyuser = ua_merge.weight.groupby(ua_merge['userID'])
s_weightbyuser = g_weightbyuser.sum()
print('\n'+ '!'*40 +'\n')
print('3. who are the top users?')
s3 =s_weightbyuser.sort_values(ascending=False).head(10)
for (key,value) in s3.iteritems():
    print('    ',key,'  ',value)

'''4-what artists ave the highest average number of plays per listener?'''
print('\n'+ '!'*40 +'\n')
print('4. what artists ave the highest average number of plays per listener?')
# use simple series caculation to get average plays per listner
s_avgplaysperlistener = s_weightbyartist/s_listenerbyartist
# sort values and get top 10, store in series
s4 = s_avgplaysperlistener.sort_values(ascending=False).head(10)
# iterate through series items and print the top 10 out
for (key,value) in s4.iteritems():
    print('    ',artists_df[artists_df.id==key].name.item(),'(',key,')  ',sep='')
    print('        total number of plays: ', s_weightbyartist[key])
    print('        total number of listeners: ', s_listenerbyartist[key])
    print('        average number: ', "{0:.2f}".format(value))
    
'''5-What artists with at least 50 listeners have the highest average number 
of plays per listener?'''
print('\n'+ '!'*40 +'\n')
print('5: What artists with at least 50 listeners have the highest average number of plays per listener?')
# create a new dataframe to store artist, listener, and average plays per listener information
df5 = pd.DataFrame({'listener/artist':s_listenerbyartist,
                    'avgplays/listener':s_avgplaysperlistener, 
                    'artistID': s_listenerbyartist.index})
# filter artist with more than 50 listeners first and get top 10 artists with avg plays per listener
s5 = df5[df5['listener/artist']>50]['avgplays/listener'].sort_values(ascending=False).head(10)
for (key,value) in s5.iteritems():
    print('    ',artists_df[artists_df.id==key].name.item(),'(',key,')  ',sep='')
    print('        total number of plays: ', s_weightbyartist[key])
    print('        total number of listeners: ', s_listenerbyartist[key])
    print('        average number: ',"{0:.2f}".format(value))

'''6-Do users with five or more friends listen to more songs?'''
print('\n'+ '!'*40 +'\n')
print('6: Do users with five or more friends listen to more songs?')
# load user-friends data into dataframe 
user_friends_df = pd.read_table('user_friends.dat',encoding="utf-8",sep="\t")
# calculate each users' friend amount
s6_uf = user_friends_df.friendID.groupby(user_friends_df.userID).nunique()
# calculate each users' plays amount
s6_uw = user_artists_df.weight.groupby(user_artists_df.userID).sum()
# create a new data frame storing friend, play information for each user
df6 = pd.DataFrame({'friend':s6_uf, 'weight':s6_uw, 'userID': s6_uf.index})
#calculate the average play amounts by users with less than 5 friends
ls_friend = (df6[df6.friend<5]['weight'].sum())/(df6[df6.friend<5]['userID'].count())
#calculate the average play amounts by users with >= 5 friends
mr_friend = (df6[df6.friend>=5]['weight'].sum())/(df6[df6.friend>=5]['userID'].count())
print('    Number of listened songs of users(< 5 friends): ', "{0:.2f}".format(ls_friend))
print('    Number of listened songs of users(>= 5 friends): ', "{0:.2f}".format(mr_friend))
if ls_friend < mr_friend:
    print('    So users with five or more friends listen to more songs')
elif ls_friend > mr_friend:
    print('    So users with five or more friends listen to less songs')
else:
    print('    Friend amounts does not influence.')
    
'''7-How similar are two artists?'''
print('\n'+ '!'*40 +'\n')
print('7: How similar are two artists?')
# define a function to caculate the similarity between two artists using Jaccard index
def artist_sim(aid1, aid2):
    # get two artists's user set
    artist_1 = user_artists_df[user_artists_df['artistID']==aid1]['userID']
    artist_2 = user_artists_df[user_artists_df['artistID']==aid2]['userID']
    # get the user set interection as Jaccard index numerator
    artist_intersection = pd.Series(list(set(artist_1).intersection(set(artist_2))))
    # get the user set union as Jaccard index nonminator
    artist_union = pd.Series(list(set(artist_1).union(set(artist_2))))
    # calculate the Jaccard index
    jaccard_index =  artist_intersection.count()/artist_union.count()
    return jaccard_index
s_artistpair = Series([562,89,289,289,67,735], index=[735,735,735,89,89,67]) 
print('    (Below are sample similarity of two artists:)')
for (key,value) in s_artistpair.iteritems():
    print('   ',artists_df[artists_df.id==key].name.item(),' ',
          artists_df[artists_df.id==value].name.item(),'      -Jaccard index: '
          ,"{0:.2f}".format(artist_sim(key, value)))

'''8-Analysis of top tagged artists'''   
print('\n'+ '!'*40 +'\n')
print('8：Analysis of top tagged artists.')
tag_artist = pd.read_table('user_taggedartists.dat', encoding="utf-8",sep="\t")
# get the current 10 top-tagged artists
toptag_artist = tag_artist .tagID.groupby(tag_artist.artistID).count().sort_values(ascending=False).head(10)
# combine year and month columns
tag_artist.year = tag_artist.year.map(str) + '-' + tag_artist.month.map(str)
tag_artist  = tag_artist.rename(columns={'year':'year-month'})
# use hierachical index to calculate artists' tag numbers per month every year
tag = tag_artist.groupby(['year-month','artistID']).count()
tag = tag.rename(columns={'tagID':'tagCounts'})
# delete abnormal records from last century
tag = tag[4:]
# multi-index sorting by tag counts
tag = tag.sort_values(by='tagCounts', ascending = False).swaplevel(0,1).sort_index(level=1, sort_remaining = False).swaplevel(0,1)
# keep top 10 for each month
tag = tag.groupby(level='year-month').head(10)
# reset index for tag dataframe, change artist id to a column
tag.reset_index(inplace=True)
# use for loop to iterate through each artist in current top 10 
# check if is in history top 10 for each month, if so, keep counting time
# print the first time when entering top 10 
for artist, weight in toptag_artist.iteritems():
   i = 0
   print('    ',artists_df[artists_df.id==artist].name.item(),'(',artist,'):  num tags = ',toptag_artist[artist],sep='')
   for index, row in tag.iterrows():
       if artist == row['artistID']:
           i += 1
           if i ==1:
               print("      first time in top 10:", row['year-month'])
   print("      total months in top 10: ", i,'\n')





