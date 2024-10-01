# %%
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd

# %%
def get_response(url):    
    resp = requests.get(url)
    return resp
    
def get_basic_info(soup):
    ems = (soup.find("div", class_ ="td-page-content")
               .find_all("p")[1]
               .find_all("em"))
    data = {}
    for i in ems:
        key, value, *_ = i.text.split(":")
        data[key.strip(" ")] = value.strip(" ")
    return data
    
def get_appearances(soup):
    lis = (soup.find("div", class_ ="td-page-content")
               .find("h4")
               .find_next()
               .find_all("li"))
    appearances = [i.text for i in lis]
    return appearances

def get_characters(url):
    resp = get_response(url)
    if resp.status_code != 200:
       print(f"Error, code: {resp.status_code}, {url}")
       return {}
    else:
        soup = BeautifulSoup(resp.text, "html.parser")
        data = get_basic_info(soup)
        data["Appearances"] = get_appearances(soup)
        return data

def get_links():
    url = "https://www.residentevildatabase.com/personagens/"
    resp = requests.get(url, "html.parser")
    soup_characters = BeautifulSoup(resp.text)
    anchors = (soup_characters.find("div", class_="td-page-content")
                              .find_all("a"))
    links = [i["href"] for i in anchors]
    return links

# %%
links = get_links()
data = []
for link in tqdm(links):
    d = get_characters(link)
    d["Link"] = link
    data.append(d)

# %%
df = pd.DataFrame(data)
df.to_parquet("re_characters_data.parquet", index=False)