import streamlit as st
import pandas as pd

st.set_page_config(page_title="HKED Turnuva Takip", layout="wide")

@st.cache_data(ttl=60)
def load_data():
    # header=None olduğu için sütunlar 0'dan başlar
    df = pd.read_excel("HKED.xlsx", header=None)
    return df

df = load_data()

# Sütun isimlerini belirleyelim
# İndeks 2: Takım 1, İndeks 4: Takım 2
# İndeks 10, 11, 12, 13, 14: Katılımcıların tahminleri
katilimcilar = {10: 'TOLGA', 11: 'MUSTAFA', 12: 'IŞITAN', 13: 'YİĞİT', 14: 'CENK'}

st.title("🏆 HKED Tahmin Turnuvası")

# Maçları birleştirelim
df['MAC_ADI'] = df[2].astype(str) + " - " + df[4].astype(str)

# Admin Panel: Sonuç Girişi
st.sidebar.header("⚙️ Admin: Maç Sonuç Gir")
selected_match = st.sidebar.selectbox("Maç Seçin", df['MAC_ADI'].tolist())
res = st.sidebar.radio("Skor:", ["1", "0", "2"])

if st.sidebar.button("Kaydet"):
    # Kaydedilen sonucu bir dosyaya veya session_state'e aktarabiliriz
    st.session_state[selected_match] = res
    st.sidebar.success(f"{selected_match} sonucu {res} olarak kaydedildi!")

# Puan Hesaplama
skorlar = {isim: 0 for isim in katilimcilar.values()}

for idx, row in df.iterrows():
    mac_adi = row['MAC_ADI']
    # Eğer sonuç girildiyse (session_state'den al)
    if mac_adi in st.session_state:
        gercek_sonuc = st.session_state[mac_adi]
        
        # Her katılımcı için tahminleri kontrol et
        for col_idx, isim in katilimcilar.items():
            tahmin = str(row[col_idx])
            if tahmin == gercek_sonuc:
                skorlar[isim] += 1 # Doğru tahmin 1 puan

# Skor Tablosu
st.subheader("📊 Güncel Sıralama")
skor_df = pd.DataFrame(list(skorlar.items()), columns=['Katılımcı', 'Puan'])
st.table(skor_df.sort_values(by='Puan', ascending=False))
