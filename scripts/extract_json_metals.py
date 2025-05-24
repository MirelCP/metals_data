import os
import json
from bs4 import BeautifulSoup
import glob

# Apunta a la carpeta correcta
data_dir = os.path.join(os.path.dirname(__file__), "data")
html_files = glob.glob(os.path.join(data_dir, "*.html"))
if not html_files:
    raise FileNotFoundError("❌ No se encontró ningún archivo .html en la carpeta.")

html_files.sort(key=os.path.getmtime, reverse=True)
html_path = html_files[0]
print(f"Usando HTML: {html_path}")
output_dir = "data_json"
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
    tds = tr.find_all("td", recursive=False)
    # Normalmente las filas relevantes tienen al menos 7 columnas (puede variar si hay celdas ocultas)
    if len(tds) < 6:
        continue

    # Primer TD: símbolo y nombre
    symbol = ""
    name = ""
    # Algunos TD pueden tener diferentes anidamientos de etiquetas
    try:
        a_tag = tds[0].find("a", class_="tickerNameBox-GrtoTeat") or tds[0].find("a", class_="tickerName-GrtoTeat")
        if a_tag:
            symbol = a_tag.get_text(strip=True)
        sup_tag = tds[0].find("sup", class_="tickerDescription-GrtoTeat")
        if sup_tag:
            name = sup_tag.get_text(strip=True)
    except Exception as e:
        pass

    # Los siguientes TD son los valores, puede haber celdas vacías visuales
    price        = tds[1].get_text(strip=True) if len(tds) > 1 else ""
    change_pct   = tds[2].get_text(strip=True) if len(tds) > 2 else ""
    change       = tds[3].get_text(strip=True) if len(tds) > 3 else ""
    high         = tds[4].get_text(strip=True) if len(tds) > 4 else ""
    low          = tds[5].get_text(strip=True) if len(tds) > 5 else ""
    tech_rating  = tds[6].get_text(strip=True) if len(tds) > 6 else ""

    # Si no hay símbolo, ignora la fila
    if not symbol:
        continue

    item = {
        "Symbol": symbol,
        "Name": name,
        "Price": price,
        "Change %": change_pct,
        "Change": change,
        "High": high,
        "Low": low,
        "Tech Rating": tech_rating,
    }
    result.append(item)

with open(output_json, "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)

print(f"Extraídas {len(result)} filas")
print(f"Guardado en: {output_json}")
