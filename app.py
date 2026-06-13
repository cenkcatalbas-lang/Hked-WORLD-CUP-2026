import streamlit as st
import pandas as pd

# 1. Sayfa Ayarları
st.set_page_config(page_title="HKED Turnuva Takip", layout="wide")

# 2. Veri Okuma Fonksiyonu
@st.cache_data(ttl=60)
def load_data():
    # Excel'i başlık olmadan okuyoruz
    df = pd.read_excel("HKED.xlsx", header=None)
    return df

# 3. Veriyi Yükle
try:
    df = load_data()
    
    st.title("🏆 HKED Tahmin Turnuvası Veri Kontrolü")
    st.write("### Excel Dosyanızdan Okunan İlk 5 Satır:")
    st.dataframe(df)
    
    st.write("---")
    st.write("### Sütun İsimleri (Index Numaraları):")
    st.write(df.columns.tolist())
    
    st.info("Yukarıdaki tabloda hangi sütun 'Maç Adı', hangisi 'Katılımcı isimleri'? Lütfen bana sütun numaralarını (örneğin: 0, 1, 2...) söyleyin, sistemi hemen aktif edelim.")

except Exception as e:
    st.error(f"Dosya okuma hatası: {e}")
    st.write("Lütfen 'HKED.xlsx' dosyasının projenin ana klasöründe olduğundan emin olun.")
