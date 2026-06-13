# Puan Hesaplama döngüsünü şu şekilde değiştirin:

# Önce DataFrame sütunlarını temizleyelim
df.columns = [col.strip().upper() for col in df.columns]

# Katılımcı isimlerini de aynı formata getirelim
participants = ['TOLGA', 'MUSTAFA', 'IŞITAN', 'YİĞİT', 'CENK']

# Puan Hesaplama Motoru
for idx, res in results.items():
    row = df.iloc[idx]
    try:
        odd = float(row[str(res)])
    except:
        odd = 1.0 
        
    for p in participants:
        # Excel'deki sütun ismini bulmaya çalışalım
        if p in row.index:
            if str(row[p]) == res:
                scores[p] += odd
