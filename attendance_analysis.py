import pandas as pd
import numpy as np
from numpy import *
import matplotlib.pyplot as plt
from scipy import stats


master_df = pd.read_csv('MLB_Ind_Game_Data.csv', encoding='ISO-8859–1')
master_df = master_df.drop(['Code', 'R', 'RA', 'Inn', 'Rank', 'GB', 'Save', 'Time', 'Streak', 'Orig. Scheduled',
                            'Games Back', 'Date.1', 'Date', 'Day Code', 'Wins.1', 'Day_Date', 'Streak.1', 'Losses.1',
                            'D/N', 'Win', 'Loss'], axis=1)


teams = master_df['Team'].unique()
'''
deletes now-nonexistent teams (MTL) and duplicate codes (LAA/ANA, TBD/TBR)
'''
teams = delete(teams, [30, 31, 32, 33], axis=0)

'''
dataframe column values
'''
home_avg_attendance = []
fans_per_year = []
away_draw_power = []
win_pct = []
wins = []
fans_per_win = []
wins_per_season = []
base_attendances = []
city_pop = [2792127, 4268289, 5379176, 2734044, 4588680, 9488493, 9488493, 2122940, 2070965, 4295700, 6063540, 2025297,  #hardcoded from US Census Data (API)
            12874797, 12874797, 5673185, 2601465, 1560621, 3391191, 19716880, 19716880, 4402729, 5992766, 2358746,
            3138265, 3504628, 4402729, 2819241, 6575833, 5928000, 5759330]
'''
There are three teams that have had multiple three letter team IDs.
If statements align team IDs
'''
for i in range(0, len(master_df['Team'])):

    if master_df['Team'][i] == 'FLA':
        master_df['Team'][i] = 'MIA'
    if master_df['Home Team'][i] == 'FLA':
        master_df['Home Team'][i] = 'MIA'
    if master_df['Away Team'][i] == 'FLA':
        master_df['Away Team'][i] = 'MIA'

    if master_df['Team'][i] == 'ANA':
        master_df['Team'][i] = 'LAA'
    if master_df['Home Team'][i] == 'ANA':
        master_df['Home Team'][i] = 'LAA'
    if master_df['Away Team'][i] == 'ANA':
        master_df['Away Team'][i] = 'LAA'

    if master_df['Team'][i] == 'TBD':
        master_df['Team'][i] = 'TBR'
    if master_df['Home Team'][i] == 'TBD':
        master_df['Home Team'][i] = 'TBR'
    if master_df['Away Team'][i] == 'TBD':
        master_df['Away Team'][i] = 'TBR'

'''
loop calculates total win and win pct columns for final df
'''
for team in teams:
    overall_df = master_df[master_df['Team'] == team]
    win_count = len(overall_df[overall_df['Wins'] == 1])
    game_count = len(overall_df)
    wins.append(win_count)
    win_pct.append(round((win_count/game_count)*100, 2))

'''
loop calculating total home attendance and average home attendance/game for each team
'''
for team in teams:
    home_df = master_df[master_df['Home Team'] == team]
    total_attendance = home_df['Attendance'].sum()
    avg_attendance = home_df['Attendance'].mean()
    home_avg_attendance.append(round(avg_attendance,2))


'''
loop calculating average difference in attendance vs. the norm for each team when they play away
'''
for team in teams:
    opp_df = master_df[master_df['Away Team'] == team]
    avg_draw_diff = opp_df['Attendance vs Avg'].mean()
    away_draw_power.append(round(avg_draw_diff,2))



'''
loop calculating average yearly attendance (81 home games in an MLB season)
'''
for value in home_avg_attendance:
    fans_per_year.append(value*81)


'''
creating final dataframe
'''
final_df = {'Team': teams,
            'Avg. Home Attendance': home_avg_attendance,
            'Fans/yr': fans_per_year,
            'Away draw power': away_draw_power,
            'Win %': win_pct,
            'Total Wins': wins,
            'City Pop': city_pop}


for i in range(0,len(final_df['Team'])):
    wins_per_season.append(round(final_df['Total Wins'][i]/7, 2))

attendance_per_cap = []
for i in range(0,len(final_df['Team'])):
    attendance_cap = final_df['Fans/yr'][i]/final_df['City Pop'][i]
    attendance_per_cap.append(attendance_cap)

final_df['Attendance per capita'] = attendance_per_cap
final_df['Avg. Wins/Season'] = wins_per_season
final_df['Base Attendance'] = base_attendances


x = np.linspace(0, 100)
slope, intercept, r_value, p_value, std_err0r = stats.linregress(final_df['Avg. Wins/Season'],
                                                                 final_df['Avg. Home Attendance'])
y = slope*x + intercept


for i in range(0,len(final_df['Team'])):
    base_attendance = (final_df['Avg. Wins/Season'][i] * slope + intercept)
    base_attendance = final_df['Avg. Home Attendance'][i] - base_attendance
    base_attendances.append(round(base_attendance, 2))



final_df = pd.DataFrame(final_df)
final_df[['Avg. Home Attendance',
          'Fans/yr', 'Away draw power']] = final_df[['Avg. Home Attendance',
                                                     'Fans/yr', 'Away draw power']].astype(int)

final_df = final_df.sort_values(by=['Avg. Home Attendance'], ascending=False)
final_df = final_df.reset_index()
final_df.to_csv('presentation_data.csv')


final_rank = []
ranking_df = final_df.drop(['Fans/yr', 'Win %', 'Total Wins', 'Avg. Wins/Season', 'index'], axis=1)
ranking_df['Rank 1'] = ranking_df['Avg. Home Attendance'].rank()
ranking_df['Rank 2'] = ranking_df['Away draw power'].rank()
ranking_df['Rank 3'] = ranking_df['Base Attendance'].rank()
ranking_df['Rank 4'] = ranking_df['Attendance per capita'].rank()

for i in range(0, len(ranking_df['Team'])):
    rank = (ranking_df['Rank 1'][i] + ranking_df['Rank 2'][i] + ranking_df['Rank 3'][i] + ranking_df['Rank 4'][i])/4
    final_rank.append(rank)

ranking_df['Final Rank'] = final_rank
ranking_df = ranking_df.drop(['Avg. Home Attendance', 'Away draw power', 'Base Attendance', 'City Pop',
                              'Attendance per capita', 'Rank 1', 'Rank 2', 'Rank 3', 'Rank 4'], axis=1)

ranking_df = ranking_df.sort_values(by='Final Rank', ascending=False)
ranking_df = ranking_df.reset_index()
ranking_df.to_csv('final_ranking.csv')

plt.figure(figsize=(20, 10))
plt.bar(final_df['Team'], final_df['Avg. Home Attendance'])
plt.title('Average Attendance per Home Game')
plt.xlabel('Team')
plt.ylabel('Avg. Home Attendance')
plt.savefig('figure1.png')


plt.figure(figsize=(20, 10))
plt.scatter(final_df['Avg. Wins/Season'], final_df['Avg. Home Attendance'], label='Original Data')
plt.plot(x, y, 'r', label='Fitted Line')
plt.title('Attendance vs. Wins Regression')
plt.legend(loc=3, prop={'size': 20})
plt.xlim(65, 96)
plt.ylim(0, 50000)
plt.xlabel('Avg. Wins/Season')
plt.ylabel('Avg. Home Attendance')
plt.savefig('figure2.png')


away_draw_df = final_df.sort_values(by='Away draw power', ascending=False)
plt.figure(figsize=(20, 10))
plt.title('Away Draw Power')
plt.ylabel('Fans draw vs. average')
plt.xlabel('Team')
plt.bar(away_draw_df['Team'], away_draw_df['Away draw power'])
plt.savefig('figure3.png')


attendance_per_cap_df = final_df.sort_values(by='Attendance per capita', ascending=False)
plt.figure(figsize=(20, 10))
plt.bar(attendance_per_cap_df['Team'], attendance_per_cap_df['Attendance per capita'])
plt.ylabel('Attendance per citizen in metro area (2013 Census)')
plt.xlabel('Team')
plt.title('Attendance per capita')
plt.savefig('figure4.png')

plt.figure(figsize=(20, 10))
plt.bar(ranking_df['Team'], ranking_df['Final Rank'])
plt.ylabel('Average Ranking')
plt.xlabel('Team')
plt.title('Final Ranking')
plt.savefig('figure5.png')
