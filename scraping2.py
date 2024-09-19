import requests
from bs4 import BeautifulSoup
import csv

url = 'https://myanimelist.net/topmanga.php?type=oneshots'

response = requests.get(url)
response.raise_for_status()
soup = BeautifulSoup(response.text, 'html.parser')

ranks = soup.select('td.rank span.top-anime-rank-text')
titles = soup.select('h3.manga_h3 a')
info_divs = soup.select('div.information')
scores = soup.select('div.js-top-ranking-score-col span.score-label')

with open('manga_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Rank', 'Title', 'Manga Type', 'Published Date', 'Members', 'Score']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for i in range(len(ranks)):
        rank = ranks[i].get_text(strip=True) if i < len(ranks) else 'N/A'
        title = titles[i].get_text(strip=True) if i < len(titles) else 'N/A'
        
        info_text = info_divs[i].get_text(separator='|', strip=True).split('|')
        mangatype = info_text[0].strip() if len(info_text) > 0 else 'N/A'
        published_date = info_text[1].strip() if len(info_text) > 1 else 'N/A'
        members = info_text[2].strip() if len(info_text) > 2 else 'N/A'
        
        score = scores[i].get_text(strip=True) if i < len(scores) else 'N/A'
        
        writer.writerow({
            'Rank': rank,
            'Title': title,
            'Manga Type': mangatype,
            'Published Date': published_date,
            'Members': members,
            'Score': score
        })

print("Data has been written to manga_data.csv")
