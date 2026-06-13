import streamlit as st
import pandas as pd
import requests

# 1. Veri Okuma (Excel'deki tahminler)
@st.cache_data(ttl=3600)
def load_excel():
    return pd.read_excel("NEW HKED.xlsx", header=None)

# 2. Canlı Skorları Çekme (API)
@st.cache_data(ttl=3600)
def get_api_results():
    url = "https://www.thesportsdb.com/api/v1/json/3/eventspastleague.php?id=4429"
    try:
        data = requests.get(url).json()
        results = {}
        if 'events' in data and data['events']:
            for e in data['events']:
                key = f"{e['strHomeTeam']} - {e['strAwayTeam']}"
                home = int(e['intHomeScore']) if e['intHomeScore'] else 0
                away = int(e['intAwayScore']) if e['intAwayScore'] else 0
                if home > away: res = "1"
                elif home < away: res = "2"
                else: res = "0"
                results[key] = res
        return results
    except:
        return {}

# 3. Puan Hesaplama (Katsayılı)
def calculate_points():
    df = load_excel()
    live_results = get_api_results()
    katilimcilar = {6: 'TOLGA', 7: 'MUSTAFA', 8: 'IŞITAN', 9: 'YİĞİT', 10: 'CENK'}
    puanlar = {isim: 0.0 for isim in katilimcilar.values()}

    for _, row in df.iterrows():
        mac_adi = row[0] # Excel 1. sütun
        if mac_adi in live_results:
            gercek_sonuc = live_results[mac_adi]
            
            # Katsayıları sütunlardan al: 1=3.sütun, 0=4.sütun, 2=5.sütun
            oran_map = {"1": 3, "0": 4, "2": 5}
            katsayi = float(row[oran_map[gercek_sonuc]])
            
            for col, isim in katilimcilar.items():
                if str(row[col]) == gercek_sonuc:
                    puanlar[isim] += katsayi
    return puanlar

# 4. Arayüz
st.title("🏆 HKED 2026 Puan Tablosu")
puanlar = calculate_points()

st.subheader("📊 Katsayıya Göre Güncel Sıralama")
puan_df = pd.DataFrame(list(puanlar.items()), columns=['İsim', 'Toplam Puan'])
st.table(puan_df.sort_values(by='Toplam Puan', ascending=False).reset_index(drop=True))
