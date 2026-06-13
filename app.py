import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="HKED Canlı Skor", layout="wide")

# 1. Veri Çekme (API üzerinden)
@st.cache_data(ttl=3600) # 1 saatte bir güncelle
def get_live_data():
    url = "https://www.thesportsdb.com/api/v1/json/3/eventspastleague.php?id=4328"
    response = requests.get(url)
    data = response.json()
    
    # JSON verisini düzenli bir tabloya çevirelim
    rows = []
    for event in data['events']:
        rows.append({
            'Maç': f"{event['strHomeTeam']} vs {event['strAwayTeam']}",
            'Ev_Skor': event['intHomeScore'],
            'Deplasman_Skor': event['intAwayScore']
        })
    return pd.DataFrame(rows)

st.title("🏆 HKED Canlı Tahmin Turnuvası")

try:
    df = get_live_data()
    st.subheader("📊 Son Oynanan Maçlar")
    st.dataframe(df)

    # 2. Tahminler (API'den gelen maçları seçmek için)
    st.sidebar.header("⚙️ Tahmin Girişi")
    selected_match = st.sidebar.selectbox("Maç Seçin", df['Maç'].tolist())
    tahmin = st.sidebar.radio("Tahmininiz:", ["1", "0", "2"])

    if st.sidebar.button("Kaydet"):
        st.session_state[selected_match] = tahmin
        st.sidebar.success(f"{selected_match} için tahmininiz: {tahmin}")

    st.info("Sistem artık API ile otomatik çalışıyor! Manuel Excel yüklemenize gerek kalmadı.")

except Exception as e:
    st.error(f"API verisi alınamadı: {e}")
