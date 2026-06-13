import streamlit as st
import pandas as pd

# 1. Veri Okuma
@st.cache_data(ttl=60)
def load_data():
    # header=None diyerek başlık satırı olmadığını belirtiyoruz
    df = pd.read_excel("HKED.xlsx", header=None)
    # İlk sütuna "MAÇ" adını veriyoruz
    df.columns = ['MAÇ'] + [f'KATILIMCI_{i}' for i in range(1, len(df.columns))]
    return df

df = load_data()
participants = ['TOLGA', 'MUSTAFA', 'IŞITAN', 'YİĞİT', 'CENK']

st.title("🏆 HKED Tahmin Turnuvası")

# 2. Admin Paneli (Veri Giriş Bölümü)
with st.sidebar:
    st.header("⚙️ Maç Sonucu Gir")
    selected_match = st.selectbox("Maç Seçin", df['MAÇ_ADI'].tolist())
    match_result = st.radio("Sonuç:", ["1", "0", "2"])
    
    if st.button("Sonucu Kaydet"):
        # Seçilen maçın satırını bulup Excel'de güncelle
        df.loc[df['MAÇ_ADI'] == selected_match, 'SONUÇ'] = match_result
        df.to_excel("HKED.xlsx", index=False)
        st.success(f"{selected_match} sonucu güncellendi!")
        st.rerun()

# 3. Puan Tablosu Hesaplama
# (Burada 'SONUÇ' sütunu boşsa hesaplamaya dahil etmez)
scores = {p: 0 for p in participants}
for _, row in df.iterrows():
    res = str(row['SONUÇ'])
    if res in ["1", "0", "2"]:
        for p in participants:
            if str(row[p]) == res:
                scores[p] += 1 # Veya oran üzerinden hesaplama

st.subheader("📊 Güncel Sıralama")
st.dataframe(pd.DataFrame(list(scores.items()), columns=['Katılımcı', 'Puan']))
