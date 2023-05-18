from bs4 import BeautifulSoup
import requests
import pandas as pd

page_to_scrape = requests.get("https://www.espn.com/soccer/stats/_/league/ENG.1/season/2017/english-premier-league")
soup = BeautifulSoup(page_to_scrape.text, "html.parser")
titles = soup.find("header", class_="db Site__Header__Wrapper sticky top-0")
unwanted1 = soup.find("ul", class_="tabs__list")

# Remove the element if found
if titles:
    titles.extract()

if unwanted1:
    unwanted1.extract()

goals = soup.findAll("td", class_="tar")
scorers = soup.findAll("a", class_="AnchorLink")

data = []
for i in range(len(goals)):
    scorer = scorers[i].text
    goal = goals[i].text
    data.append([scorer, goal])

df = pd.DataFrame(data, columns=["Scorer", "Goals"])
print(df)

