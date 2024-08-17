import requests
from bs4 import BeautifulSoup
import pandas as pd

# Funktion zum Abrufen von Ticker-Symbolen vom S&P 500
def get_sp500_tickers():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    table = pd.read_html(url, header=0)[0]
    return table['Symbol'].tolist()

# Funktion zum Abrufen von DAX Ticker-Symbolen
def get_dax_tickers():
    urls = [
        'https://www.dividendmax.com/market-index-constituents/dax-40',
        'https://www.dividendmax.com/market-index-constituents/dax-40?page=2'
    ]
    
    all_tickers = []
    
    for url in urls:
        response = requests.get(url)
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Finde die Tabelle auf der Seite
        table = soup.find('table', {'aria-label': 'Constituents of DAX 40'})
        
        # Extrahiere die Ticker-Symbole aus der Tabelle
        rows = table.find_all('tr')[1:]  # Überspringe die Header-Zeile
        
        for i, row in enumerate(rows):
            cells = row.find_all('td')
            if len(cells) > 1:
                ticker = cells[1].text.strip()
                all_tickers.append(ticker)
    
    return all_tickers

# Funktion zum Abrufen von MDAX Ticker-Symbolen
def get_mdax_tickers():
    url = 'https://en.wikipedia.org/wiki/MDAX'
    table = pd.read_html(url, header=0)[3]
    return table['Ticker symbol'].tolist()

# Funktion zum Abrufen von Dow Jones Ticker-Symbolen
def get_dow_jones_tickers():
    url = 'https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average'
    table = pd.read_html(url, header=0)[1]
    return table['Symbol'].tolist()

# Funktion zum Abrufen von NASDAQ-100 Ticker-Symbolen
def get_nasdaq100_tickers():
    url = 'https://en.wikipedia.org/wiki/NASDAQ-100'
    table = pd.read_html(url, header=0)[3]
    return table['Ticker'].tolist()

# Abrufen der Ticker-Symbole für alle genannten Indizes
sp500_tickers = get_sp500_tickers()
dax_tickers = get_dax_tickers()
mdax_tickers = get_mdax_tickers()
dow_jones_tickers = get_dow_jones_tickers()
nasdaq100_tickers = get_nasdaq100_tickers()

# Zusammenfügen der Listen und Entfernen von Duplikaten
all_tickers = list(set(sp500_tickers + dax_tickers + mdax_tickers + dow_jones_tickers + nasdaq100_tickers))

# Ausgabe der Anzahl und einiger Ticker-Symbole zur Überprüfung
print(f"Anzahl der kombinierten Ticker: {len(all_tickers)}")
print(all_tickers[:10])  # Zeige die ersten 10 Ticker zur Überprüfung

# Speichern der kombinierten Liste als CSV-Datei
df_tickers = pd.DataFrame(all_tickers, columns=['Ticker'])
df_tickers.to_csv('combined_tickers.csv', index=False)
