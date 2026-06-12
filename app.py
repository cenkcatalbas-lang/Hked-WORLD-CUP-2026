import streamlit as st
import pandas as pd

st.set_page_config(page_title="HKED Turnuva Takip", layout="wide")

# Havalı ve renkli bir başlık
st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>🏆 HKED Tahmin Turnuvası Canlı Puan Durumu 🏆</h1>", unsafe-align=True)
st.write("---")

@st.cache_data
def load_data():
    df = pd.read_excel("HKED.xlsx")
    df.columns = [str(c).strip() for c in df.columns]
    return df

try:
    df = load_data().copy()
    
    participants = ['TOLGA', 'MUSTAFA', 'IŞITAN', 'YİĞİT', 'CENK']
    scores = {p.strip(): 0.0 for p in participants}

    # Puan Hesaplama Motoru
    for index, row in df.iterrows():
        sonuc_val = row.get('SONUÇ', None)
        if pd.isna(sonuc_val) or str(sonuc_val).strip() == "" or str(sonuc_val).lower() == "oynanmadı":
            continue
            
        res = str(int(sonuc_val)) if isinstance(sonuc_val, (int, float)) else str(sonuc_val).strip()
        try:
            odd = float(row[res]) 
        except (ValueError, KeyError):
            odd = 0.0
        
        for p in participants:
            p_clean = p.strip()
            if pd.notna(row[p]):
                p_prediction = str(int(row[p])) if isinstance(row[p], (int, float)) else str(row[p])
                if p_prediction.strip() == res:
                    scores[p_clean] += odd

    # Puan Durumu Tablosunu Oluşturma
    leaderboard = pd.DataFrame(list(scores.items()), columns=['Katılımcı', 'Toplam Puan'])
    leaderboard = leaderboard.sort_values(by='Toplam Puan', ascending=False).reset_index(drop=True)
    leaderboard.index += 1

    # Arkadaşlarınızı kızdıracak esprili durum kartları
    lider = leaderboard.iloc[0]['Katılımcı']
    sonuncu = leaderboard.iloc[-1]['Katılımcı']
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success(f"👑 **HAFTANIN BİLGİNİ:** {lider}\n\nOynanan maçlar sonunda zirveye ambargo koydu. Futbol profesörü be!")
        
    with col2:
        st.error(f"🤡 **HAFTANIN BEYİNSİZİ:** {sonuncu}\n\nSolo test çarkının en dibinde. Maçları tersten mi tahmin ediyorsun kardeşim?")

    st.write("---")

    # Büyük ve renkli podyum metrikleri (İlk 3 Kişi)
    st.subheader("🏅 Kürsüdekiler")
    m1, m2, m3 = st.columns(3)
    
    with m1:
        if len(leaderboard) >= 1:
            st.metric(label="🥇 1. BİLGİN", value=leaderboard.iloc[0]['Katılımcı'], delta=f"{leaderboard.iloc[0]['Toplam Puan']:.2f} Puan")
    with m2:
        if len(leaderboard) >= 2:
            st.metric(label="🧢 2. TECRÜBESİZ", value=leaderboard.iloc[1]['Katılımcı'], delta=f"{leaderboard.iloc[1]['Toplam Puan']:.2f} Puan", delta_color="off")
    with m3:
        if len(leaderboard) >= 3:
            st.metric(label="😵‍💫 3. APTAL", value=leaderboard.iloc[2]['Katılımcı'], delta=f"{leaderboard.iloc[2]['Toplam Puan']:.2f} Puan", delta_color="inverse")

    st.write("---")

    # Renkli Genel Sıralama Tablosu
    st.subheader("📊 Tüm Gençlerin Puan Durumu")
    
    # Sıralamaya göre laf sokma sütunu ekliyoruz
    laf_sokmalar = {
        1: "🧠 Futbolu o yazmış gibi oynuyor.",
        2: "👀 Liderin ensesinde ama nefesi yetecek mi?",
        3: "🤷‍♂️ Ne uzalıyor ne kısalıyor, bildiğin düz insan.",
        4: "🤪 Bir sonraki maçta huni takması bekleniyor.",
        5: "🗑️ Tahmin yaparken gözünü kapatıyor galiba."
    }
    leaderboard['Mevcut Durum Analizi'] = leaderboard.index.map(laf_sokmalar)

    # Tabloyu renklendirmek ve büyük göstermek için formatlama
    st.dataframe(
        leaderboard.style.format({"Toplam Puan": "{:.2f}"})
        .background_gradient(subset=['Toplam Puan'], cmap='RdYlGn'), # Puanlara göre kırmızıdan yeşile renk geçişi
        use_container_width=True
    )

    st.write("---")
    st.subheader("📅 Tüm Fikstür, Tahminler ve Sonuçlar")
    st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"Bir hata oluştu: {e}")