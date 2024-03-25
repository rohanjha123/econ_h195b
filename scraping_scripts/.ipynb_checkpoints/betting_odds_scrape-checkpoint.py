from bs4 import BeautifulSoup
import pandas as pd
import requests

starting_season = 2008 # earliest is 1952
ending_season = 2022 # latest is 2023

covered_seasons = range(starting_season, ending_season+1)

columns = []
data = []
for season in covered_seasons:
    season_req = requests.get("https://www.sportsoddshistory.com/nfl-game-season/?y=" + str(season))
    soup = BeautifulSoup(season_req.content, "html.parser")
    reg_season_tables = soup.find_all('h3')[3:-2]
    for week in reg_season_tables:
        samp_week_table = week.find_next('table')
        if columns == []:
            columns = ['Season'] + ['Week'] + [th.text.strip() for th in samp_week_table.find_all('th')]
        elif columns[2:] != [th.text.strip() for th in samp_week_table.find_all('th')]:
            print(f'issue in season {season} week {week}' )
        for row in samp_week_table.find('tbody').find_all('tr'):
            row_data = [season] + [str(week).split(' - ')[1].split('<')[0].split(' ')[1]] + [td.text.strip() for td in row.find_all('td')]
            data.append(row_data)

df = pd.DataFrame(data, columns=columns)
df.to_csv('NFL_Betting_Odds.csv')