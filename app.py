import streamlit as st
import pandas as pd

st.set_page_config(page_title="HKED Turnuva", layout="wide")

# Veriyi hatasız okuma fonksiyonu
@st.cache_data(ttl=60)
def load_data():
    # Türkçe karakter sorunu için cp1254 kullanıyoruz
    return pd.read_csv("NEW HKED.xlsx - Sheet1.csv", header=None, encoding='cp1254')

try:
    df = load_data()
    st.title("🏆 HKED 2026 Tahmin Turnuvası")

    # Admin Panel
    st.sidebar.header("⚙️ Sonuç Girişi")
    selected_match = st.sidebar.selectbox("Maç Seçin", df[0].tolist())
    gercek_sonuc = st.sidebar.radio("Sonuç:", ["1", "0", "2"])
    
    if st.sidebar.button("Kaydet"):
        st.session_state[selected_match] = gercek_sonuc
        st.sidebar.success(f"Kaydedildi: {selected_match} -> {gercek_sonuc}")

    # Puan Hesaplama
    katilimcilar = {6: 'TOLGA', 7: 'MUSTAFA', 8: 'IŞITAN', 9: 'YİĞİT', 10: 'CENK'}
    skorlar = {isim: 0.0 for isim in katilimcilar.values()}

    for _, row in df.iterrows():
        mac_adi = row[0]
        if mac_adi in st.session_state:
            sonuc = st.session_state[mac_adi]
            # Oranları 3, 4, 5 sütunlarından al
            oran_map = {"1": 3, "0": 4, "2": 5}
            try:
                oran = float(row[oran_map[sonuc]])
            except:
                oran = 1.0
            
            for col_idx, isim in katilimcilar.items():
                if str(row[col_idx]) == sonuc:
                    skorlar[isim] += oran

    # Sıralama
    st.subheader("📊 Güncel Puan Durumu")
    skor_df = pd.DataFrame(list(skorlar.items()), columns=['Katılımcı', 'Toplam Puan'])
    st.table(skor_df.sort_values(by='Toplam Puan', ascending=False).reset_index(drop=True))

except Exception as e:
    st.error(f"Sistem Hatası: {e}")
