import os
import json
from bs4 import BeautifulSoup

html_path = "data/download_https___www_tradingview_com_markets_futures_quotes_metals__bf976704.html"
output_dir = "public/data_json"
output_json = os.path.join(output_dir, "metals_futures.json")

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

rows = soup.select('tr.row-RdUXZpkv.listRow')

headers = [
    "Symbol", "Name", "Price", "Change %", "Change", "High", "Low", "Tech Rating"
]

result = []
for tr in rows:
    tds = tr.find_all("td")
    if len(tds) < 7:
        continue

    # Extrae símbolo y nombre correctamente usando selectores internos del primer <td>
    symbol = ""
    name = ""
    first_td = tds[0]
    a_tag = first_td.find("a", class_="tickerName-GrtoTeat")
    sup_tag = first_td.find("sup", class_="tickerDescription-GrtoTeat")
    if a_tag:
        symbol = a_tag.get_text(strip=True)
    if sup_tag:
        name = sup_tag.get_text(strip=True)

    item = {
        "Symbol": symbol,
        "Name": name,
        "Price": tds[1].get_text(strip=True) if len(tds) > 1 else "",
        "Change %": tds[2].get_text(strip=True) if len(tds) > 2 else "",
        "Change": tds[3].get_text(strip=True) if len(tds) > 3 else "",
        "High": tds[4].get_text(strip=True) if len(tds) > 4 else "",
        "Low": tds[5].get_text(strip=True) if len(tds) > 5 else "",
        "Tech Rating": tds[6].get_text(strip=True) if len(tds) > 6 else "",
    }
    result.append(item)

with open(output_json, "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)

print(f"Extraídas {len(result)} filas")
print(f"Guardado en: {output_json}")
