import streamlit as st
import pandas as pd

st.set_page_config(page_title="HKED Turnuva", layout="wide")

@st.cache_data(ttl=60)
def load_data():
    # Dosya ismi tam olarak belirttiğiniz gibi
    return pd.read_excel("NEW HKED.xlsx", header=None)

try:
    df = load_data()
    st.title("🏆 HKED 2026 Tahmin Turnuvası")

    # Admin Panel
    st.sidebar.header("⚙️ Sonuç Girişi")
    # Maç listesi 0. sütunda
    selected_match = st.sidebar.selectbox("Maç Seçin", df[0].tolist())
    gercek_sonuc = st.sidebar.radio("Sonuç:", ["1", "0", "2"])
    
    if st.sidebar.button("Kaydet"):
        st.session_state[selected_match] = gercek_sonuc
        st.sidebar.success(f"Kaydedildi: {selected_match} -> {gercek_sonuc}")

    # Puan Hesaplama
    # Sütun 6: TOLGA, 7: MUSTAFA, 8: IŞITAN, 9: YİĞİT, 10: CENK
    katilimcilar = {6: 'TOLGA', 7: 'MUSTAFA', 8: 'IŞITAN', 9: 'YİĞİT', 10: 'CENK'}
    skorlar = {isim: 0.0 for isim in katilimcilar.values()}

    for _, row in df.iterrows():
        mac_adi = row[0]
        if mac_adi in st.session_state:
            sonuc = st.session_state[mac_adi]
            # Oranlar 3, 4, 5. sütunlarda (1, 0, 2 sırasıyla)
            oran_map = {"1": 3, "0": 4, "2": 5}
            oran = float(row[oran_map[sonuc]])
            
            for col_idx, isim in katilimcilar.items():
                if str(row[col_idx]) == sonuc:
                    skorlar[isim] += oran

    # Sıralama
    st.subheader("📊 Güncel Puan Durumu")
    skor_df = pd.DataFrame(list(skorlar.items()), columns=['Katılımcı', 'Toplam Puan'])
    st.table(skor_df.sort_values(by='Toplam Puan', ascending=False).reset_index(drop=True))

except Exception as e:
    st.error(f"Dosya okuma hatası: {e}")
    st.write("Dosyanızın tam isminin 'NEW HKED.xlsx' olduğundan ve projenin ana klasöründe bulunduğundan emin olun.")
