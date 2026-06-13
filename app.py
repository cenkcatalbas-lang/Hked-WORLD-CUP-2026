import streamlit as st
import pandas as pd

st.set_page_config(page_title="HKED Turnuva Takip", layout="wide")

# Veriyi oku
@st.cache_data(ttl=60)
def load_data():
    return pd.read_excel("HKED.xlsx")

df = load_data()
participants = ['TOLGA', 'MUSTAFA', 'IŞITAN', 'YİĞİT ', 'CENK']

st.title("🏆 HKED Tahmin Turnuvası")

# Sidebar: Maç Sonuç Girişi
st.sidebar.header("⚙️ Admin: Maç Sonuçları")
results = {}

for index, row in df.iterrows():
    # Mevcut sonucu Excel'den al (eğer varsa)
    default_val = str(row.get('SONUÇ', "Oynanmadı"))
    
    res = st.sidebar.selectbox(
        f"{row['TAKIM - 1']} vs {row['TAKIM - 2']}",
        options=["Oynanmadı", "1", "0", "2"],
        index=["Oynanmadı", "1", "0", "2"].index(default_val) if default_val in ["1", "0", "2"] else 0,
        key=f"match_{index}"
    )
    if res != "Oynanmadı":
        results[index] = res

# Puan Hesaplama
scores = {p.strip(): 0.0 for p in participants}
for idx, res in results.items():
    row = df.iloc[idx]
    # Varsayılan puan 1.0 olsun (oran yoksa)
    odd = float(row.get(int(res), 1.0))
    for p in participants:
        if str(row[p.strip()]) == res:
            scores[p.strip()] += odd

# Puan Tablosu
leaderboard = pd.DataFrame(list(scores.items()), columns=['Katılımcı', 'Toplam Puan'])
leaderboard = leaderboard.sort_values(by='Toplam Puan', ascending=False).reset_index(drop=True)

st.subheader("📊 Güncel Sıralama")
st.dataframe(leaderboard.style.format({"Toplam Puan": "{:.2f}"}), use_container_width=True)
