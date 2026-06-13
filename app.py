import streamlit as st
import pandas as pd

st.set_page_config(page_title="HKED Turnuva Tahmin", layout="wide")

@st.cache_data(ttl=60)
def load_data():
    # Artık dosyanızda başlık olmadığını varsayarak okuyoruz (header=None)
    # Eğer ilk satırda başlık varsa 'header=0' yapın.
    df = pd.read_csv("NEW HKED.xlsx - Sheet1.csv", header=None)
    return df

try:
    df = load_data()
    
    # 0. Sütun: Maç Adı
    # 3, 4, 5. Sütunlar: Oranlar (1, 0, 2)
    # 6, 7, 8, 9, 10. Sütunlar: Katılımcılar
    
    st.title("🏆 HKED 2026 Tahmin Turnuvası")

    st.sidebar.header("⚙️ Admin: Maç Sonucu Gir")
    # Maç listesi artık 0. sütunda
    selected_match = st.sidebar.selectbox("Maç Seçin", df[0].tolist())
    
    gercek_sonuc = st.sidebar.radio("Maçın Gerçek Sonucu:", ["1", "0", "2"])
    
    if st.sidebar.button("Kaydet"):
        st.session_state[selected_match] = gercek_sonuc
        st.sidebar.success(f"{selected_match} sonucu {gercek_sonuc} olarak kaydedildi!")

    # Puan Hesaplama
    # Sütun 6: TOLGA, 7: MUSTAFA, 8: IŞITAN, 9: YİĞİT, 10: CENK
    katilimcilar = {6: 'TOLGA', 7: 'MUSTAFA', 8: 'IŞITAN', 9: 'YİĞİT', 10: 'CENK'}
    skorlar = {isim: 0.0 for isim in katilimcilar.values()}

    for idx, row in df.iterrows():
        mac_adi = row[0]
        if mac_adi in st.session_state:
            sonuc = st.session_state[mac_adi]
            
            # Oranları sütun 3, 4, 5'ten al (1: col 3, 0: col 4, 2: col 5)
            oran_map = {"1": 3, "0": 4, "2": 5}
            oran = float(row[oran_map[sonuc]])
            
            for col_idx, isim in katilimcilar.items():
                if str(row[col_idx]) == sonuc:
                    skorlar[isim] += oran

    st.subheader("📊 Güncel Puan Durumu")
    skor_df = pd.DataFrame(list(skorlar.items()), columns=['Katılımcı', 'Toplam Puan'])
    st.table(skor_df.sort_values(by='Toplam Puan', ascending=False).reset_index(drop=True))

except Exception as e:
    st.error(f"Dosya okuma hatası: {e}")
