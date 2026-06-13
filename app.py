import streamlit as st
import pandas as pd
import requests

@st.cache_data(ttl=3600)
def load_excel():
    return pd.read_excel("NEW HKED.xlsx", header=None)

@st.cache_data(ttl=3600)
def get_api_results():
    url = "https://www.thesportsdb.com/api/v1/json/3/eventspastleague.php?id=4429"
    try:
        data = requests.get(url).json()
        results = {}
        if 'events' in data and data['events']:
            for e in data['events']:
                key = f"{e['strHomeTeam']} - {e['strAwayTeam']}"
                home, away = int(e['intHomeScore'] or 0), int(e['intAwayScore'] or 0)
                if home > away: res = "1"
                elif home < away: res = "2"
                else: res = "0"
                results[key] = {'sonuc': res, 'skor': f"{home}-{away}"}
        return results
    except: return {}

st.title("🏆 HKED 2026 Tahmin ve Skor Paneli")

df = load_excel()
live_results = get_api_results()
katilimcilar = {6: 'TOLGA', 7: 'MUSTAFA', 8: 'IŞITAN', 9: 'YİĞİT', 10: 'CENK'}

# 1. Puan Hesaplama
puanlar = {isim: 0.0 for isim in katilimcilar.values()}
detaylar = []

for _, row in df.iterrows():
    mac = row[0]
    if mac in live_results:
        gercek = live_results[mac]['sonuc']
        skor = live_results[mac]['skor']
        oran_map = {"1": 3, "0": 4, "2": 5}
        katsayi = float(row[oran_map[gercek]])
        
        tahminler = {isim: str(row[col]) for col, isim in katilimcilar.items()}
        for isim, tahmin in tahminler.items():
            if tahmin == gercek:
                puanlar[isim] += katsayi
        
        detaylar.append({'Maç': mac, 'Gerçek Skor': skor, 'Sonuç': gercek, **tahminler})

# 2. Puan Tablosu
st.subheader("📊 Güncel Sıralama")
puan_df = pd.DataFrame(list(puanlar.items()), columns=['İsim', 'Toplam Puan'])
st.table(puan_df.sort_values(by='Toplam Puan', ascending=False).reset_index(drop=True))

# 3. Detaylı Analiz
st.subheader("📝 Maç Sonuçları ve Tahminler")
st.dataframe(pd.DataFrame(detaylar))
