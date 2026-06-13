import streamlit as st
import requests
import pandas as pd

# FIFA Dünya Kupası ID'si: 4429
LEAGUE_ID = "4429"

@st.cache_data(ttl=3600)
def get_world_cup_data():
    url = f"https://www.thesportsdb.com/api/v1/json/3/eventsnextleague.php?id={LEAGUE_ID}"
    response = requests.get(url)
    data = response.json()
    
    events = data.get('events', [])
    if not events: return pd.DataFrame()
    
    rows = []
    for e in events:
        rows.append({
            'Maç': f"{e['strHomeTeam']} - {e['strAwayTeam']}",
            'Tarih': e['dateEvent'],
            'Stadyum': e['strVenue']
        })
    return pd.DataFrame(rows)

st.title("🏆 FIFA Dünya Kupası 2026 Tahmin Sistemi")

df = get_world_cup_data()

if not df.empty:
    st.subheader("📅 Yaklaşan Maçlar")
    st.table(df)
    
    # Kullanıcı tahmin formu
    with st.form("tahmin_formu"):
        secili_mac = st.selectbox("Tahmin Yapacağınız Maç:", df['Maç'].tolist())
        tahmin = st.radio("Tahmininiz (1-0-2):", ["1", "0", "2"])
        submit = st.form_submit_button("Tahmini Kaydet")
        
        if submit:
            st.session_state[secili_mac] = tahmin
            st.success(f"{secili_mac} için tahmininiz alındı: {tahmin}")
else:
    st.warning("Şu an yaklaşan maç verisi bulunamadı.")
    
