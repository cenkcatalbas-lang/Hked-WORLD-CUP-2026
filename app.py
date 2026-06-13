import streamlit as st
import pandas as pd

st.set_page_config(page_title="HKED Turnuva Takip", layout="wide")

@st.cache_data(ttl=60)
def load_data():
    df = pd.read_excel("HKED.xlsx")
    # Sütun isimlerini burada temizleyelim ki her yerde kullanabilelim
    df.columns = [str(col).strip().upper() for col in df.columns]
    return df

try:
    df = load_data()
    participants = ['TOLGA', 'MUSTAFA', 'IŞITAN', 'YİĞİT', 'CENK']

    st.title("🏆 HKED Tahmin Turnuvası")

    st.sidebar.header("⚙️ Admin: Maç Sonuçları")
    results = {}

    for index, row in df.iterrows():
        # Sütun isimleri artık temizlendiği için "TAKIM - 1" gibi çağırabiliriz
        match_name = f"{row['TAKIM - 1']} vs {row['TAKIM - 2']}"
        
        res = st.sidebar.selectbox(
            match_name,
            options=["Oynanmadı", "1", "0", "2"],
            key=f"match_{index}"
        )
        
        if res != "Oynanmadı":
            results[index] = res

    # Puan Hesaplama
    scores = {p: 0.0 for p in participants}
    
    for idx, res in results.items():
        row = df.iloc[idx]
        # Excel'de 1, 0, 2 başlıkları olduğu varsayıldı
        try:
            odd = float(row[str(res)])
        except:
            odd = 1.0 
            
        for p in participants:
            # Excel'deki tahmin sütunları büyük harfle eşleşmeli
            if str(row[p]) == res:
                scores[p] += odd

    # Sıralama
    leaderboard = pd.DataFrame(list(scores.items()), columns=['Katılımcı', 'Toplam Puan'])
    leaderboard = leaderboard.sort_values(by='Toplam Puan', ascending=False).reset_index(drop=True)
    leaderboard.index += 1

    st.subheader("📊 Güncel Sıralama")
    st.dataframe(leaderboard.style.format({"Toplam Puan": "{:.2f}"}), use_container_width=True)

except Exception as e:
    st.error(f"Hata oluştu: {e}")
    st.write("Lütfen Excel dosyanızın sütun başlıklarını kontrol edin (TOLGA, MUSTAFA, IŞITAN, YİĞİT, CENK, 1, 0, 2 isimlerinde olduğundan emin olun).")
