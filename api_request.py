import pandas as pd
import requests
from census import Census

api_key = "1665e1c59ada7dd84ed2b2574ab6ccd282e2cd3f"


c = Census(api_key, year=2013)
census_data = c.acs5.get(("NAME", "B01003_001E"), {'for': 'metropolitan statistical area/micropolitan statistical area:*'})

census_pd = pd.DataFrame(census_data)
census_pd = census_pd.rename(columns={"B01003_001E": "Population",
                                      "NAME": "Name", "metropolitan statistical area/micropolitan statistical area": "MSA"})





census_data = c.acs5.get(("NAME", "B01003_001E"), {'for': 'metropolitan statistical area/micropolitan statistical area:*'})

census_pd = pd.DataFrame(census_data)


census_pd = census_pd.rename(columns={"B01003_001E": "Population",
                                      "NAME": "Name", "metropolitan statistical area/micropolitan statistical area": "MSA"})


teams = ['ARI', 'SDP', 'MIA', 'TBR', 'NYM', 'NYY', 'MIL', 'KCR', 'CLE', 'CIN', 'PIT', 'COL', 'BAL', 'MIN', 'SEA', 'SFG', 'OAK', 'DET', 'BOS', 'ATL', 'WSH', 'HOU', 'PHI', 'TEX', 'CHC', 'CWS', 'LAA', 'LAD', 'STL']
pop = []
print(census_pd.columns)
print(census_pd.head())

ari = census_pd[census_pd['MSA'].str.match('38060')]
pop.append(ari['Population'])
print(int(ari['Population']))
sd = census_pd[census_pd['MSA'].str.match('41740')]
pop.append(sd['Population'])
mia = census_pd[census_pd['MSA'].str.match('33100')]
pop.append(mia['Population'])
tb = census_pd[census_pd['MSA'].str.match('45300')]
pop.append(tb['Population'])
nym = census_pd[census_pd['MSA'].str.match('35620')]
pop.append(nym['Population'])
nyy = census_pd[census_pd['MSA'].str.match('35620')]
pop.append(nyy['Population'])
mil = census_pd[census_pd['MSA'].str.match('33340')]
pop.append(mil['Population'])
kc = census_pd[census_pd['MSA'].str.match('28140')]
pop.append(kc['Population'])
cle = census_pd[census_pd['MSA'].str.match('17460')]
pop.append(cle['Population'])
cin = census_pd[census_pd['MSA'].str.match('17140')]
pop.append(cin['Population'])
pit = census_pd[census_pd['MSA'].str.match('38300')]
pop.append(pit['Population'])
col = census_pd[census_pd['MSA'].str.match('19740')]
pop.append(col['Population'])
bal = census_pd[census_pd['MSA'].str.match('12580')]
pop.append(bal['Population'])
minn = census_pd[census_pd['MSA'].str.match('33460')]
pop.append(minn['Population'])
sea = census_pd[census_pd['MSA'].str.match('42660')]
pop.append(sea['Population'])
sf = census_pd[census_pd['MSA'].str.match('41860')]
pop.append(sf['Population'])
oak = census_pd[census_pd['MSA'].str.match('41860')]
pop.append(oak['Population'])
det = census_pd[census_pd['MSA'].str.match('19820')]
pop.append(det['Population'])
bos = census_pd[census_pd['MSA'].str.match('71650')]
pop.append(bos['Population'])
atl = census_pd[census_pd['MSA'].str.match('12060')]
pop.append(atl['Population'])
wsh = census_pd[census_pd['MSA'].str.match('47900')]
pop.append(wsh['Population'])
hou = census_pd[census_pd['MSA'].str.match('26420')]
pop.append(hou['Population'])
phi = census_pd[census_pd['MSA'].str.match('37980')]
pop.append(phi['Population'])
tex = census_pd[census_pd['MSA'].str.match('19100')]
pop.append(tex['Population'])
chc = census_pd[census_pd['MSA'].str.match('16980')]
pop.append(chc['Population'])
cws = census_pd[census_pd['MSA'].str.match('16980')]
pop.append(cws['Population'])
laa = census_pd[census_pd['MSA'].str.match('31100')]
pop.append(laa['Population'])
lad = census_pd[census_pd['MSA'].str.match('31100')]
pop.append(lad['Population'])
stl = census_pd[census_pd['MSA'].str.match('41180')]
pop.append(stl['Population'])

team_df = {'Team': teams,
           'City Pop': pop}
team_df = pd.DataFrame(team_df)
print(team_df.head())
team_df.to_csv('pop_data.csv')

print(team_df['City Pop'][0])