# %%
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd

# %%
def get_response(url):    
    resp = requests.get(url)
    return resp
    
def get_info_basicas(soup):
    ems = (soup.find("div", class_ ="td-page-content")
               .find_all("p")[1]
               .find_all("em"))
    data = {}
    for i in ems:
        chave, valor, *_ = i.text.split(":")
        data[chave.strip(" ")] = valor.strip(" ")
    return data
    
def get_aparicoes_personagens(soup):
    lis = (soup.find("div", class_ ="td-page-content")
               .find("h4")
               .find_next()
               .find_all("li"))
    aparicoes = [i.text for i in lis]
    return aparicoes

def get_personagens(url):
    resp = get_response(url)
    if resp.status_code != 200:
       print(f"Erro, código: {resp.status_code}, {url}")
       return {}
    else:
        soup = BeautifulSoup(resp.text, "html.parser")
        data = get_info_basicas(soup)
        data["Aparicoes"] = get_aparicoes_personagens(soup)
        return data

def get_links():
    url = "https://www.residentevildatabase.com/personagens/"
    resp = requests.get(url, "html.parser")
    soup_personagens = BeautifulSoup(resp.text)
    ancoras = (soup_personagens.find("div", class_="td-page-content")
                               .find_all("a"))
    links = [i["href"] for i in ancoras]
    return links

# %%
links = get_links()
data = []
for link in tqdm(links):
    d = get_personagens(link)
    d["Link"] = link
    data.append(d)

# %%
df = pd.DataFrame(data)
df.to_parquet("dados_re.parquet", index=False)