from time import sleep
import requests
import json
from bs4 import BeautifulSoup as soup
import re
import csv


chan_url = "https://www.4chan.org"

r = requests.get(chan_url)

chan_html = soup(r.text,'html.parser')

d = {}

link = '//boards.4chan.org/pol/'

# pattern = r'(org/).*[/]'

print(link.split('/'))


# print(chan_html.find_all('a', class_='boardlink'))
for board in chan_html.find_all('a', class_='boardlink',href=True):
    d[board.text] = board['href'].split('/')[-2]

print(d.values())

# boards_endpoint = "https://a.4cdn.org/boards.json"


# boards_json = requests.get(boards_endpoint)

# boards_json = boards_json.json()

# print(boards_json["boards"])

# print("All Boards")

# boards = []

# for board in (boards_json["boards"]):
#     print(board["title"]," ",board["pages"])
#     boards.append(board)

with open(f'4chan_dataset2.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["id", "text", "board","short"])
    for board in d.keys():
        for page in range(1,11):
            # print(board["title"],page)
            sleep(1)
            boards_endpoint = f"https://a.4cdn.org/{d[board]}/{page}.json"
            # print(board,page,boards_endpoint)
            
            boards_json = requests.get(boards_endpoint)
            if(str(boards_json.status_code) == '404'):
                break
            posts = boards_json.json()['threads']
            
            for post in posts:
                # print(post["posts"])
                for i in post["posts"]:
                    ids,text = None,None
                    if(i["no"]):
                        ids= i["no"]
                    if("com" in i.keys()):
                        text = i["com"]
                        
                    soup = soup(str(text))
                    writer.writerow([ids,soup.text,board,d[board]])
                            