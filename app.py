import streamlit as st
import pandas as pd
import requests

# 1. Veri Hazırlığı
@st.cache_data(ttl=3600)
def load_excel():
    # Sizin Excel dosyanız (İndeks 0: Maç, 6-10: Katılımcılar)
    return pd.read_excel("NEW HKED.xlsx", header=None)

@st.cache_data(ttl=3600)
def get_api_results():
    # TheSportsDB API'den sonuçları çek
    url = "https://www.thesportsdb.com/api/v1/json/3/eventspastleague.php?id=4429"
    data = requests.get(url).json()
    results = {}
    if 'events' in data and data['events']:
        for e in data['events']:
            # Maç ismini Excel'deki formatla eşleştiriyoruz (Basit bir eşleştirme)
            key = f"{e['strHomeTeam']} - {e['strAwayTeam']}"
            home = int(e['intHomeScore']) if e['intHomeScore'] else 0
            away = int(e['intAwayScore']) if e['intAwayScore'] else 0
            
            # Sonucu 1-0-2 formatına çevir
            if home > away: res = "1"
            elif home < away: res = "2"
            else: res = "0"
            results[key] = res
    return results

# 2. Puanlama Mantığı
def calculate_points():
    df = load_excel()
    live_results = get_api_results()
    katilimcilar = {6: 'TOLGA', 7: 'MUSTAFA', 8: 'IŞITAN', 9: 'YİĞİT', 10: 'CENK'}
    puanlar = {isim: 0 for isim in katilimcilar.values()}

    for _, row in df.iterrows():
        mac_adi = row[0] # Excel 1. sütun
        if mac_adi in live_results:
            gercek_sonuc = live_results[mac_adi]
            for col, isim in katilimcilar.items():
                if str(row[col]) == gercek_sonuc:
                    puanlar[isim] += 1 # Her doğru tahmin 1 puan
    return puanlar

# 3. Arayüz
st.title("🏆 HKED 2026 Dünya Kupası Tahminleri")
puanlar = calculate_points()

st.subheader("📊 Canlı Puan Tablosu")
puan_df = pd.DataFrame(list(puanlar.items()), columns=['İsim', 'Puan'])
st.table(puan_df.sort_values(by='Puan', ascending=False))
