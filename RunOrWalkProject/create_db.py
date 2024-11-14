import sqlite3
import pandas as pd
# CSV dosyasını oku
file_path = r"C:\Users\aysen\OneDrive\Belgeler\Visual Studio Code\run_or_walk.csv"
df = pd.read_csv(file_path)

# İlk 10 satırı seç
sample_data = df.head(10)

# SQLite veritabanı bağlantısını oluştur
conn = sqlite3.connect('activities.db')
c = conn.cursor()

# Mevcut tabloyu sil (eğer varsa)
c.execute('DROP TABLE IF EXISTS activities')

# Tabloyu yeniden oluştur
c.execute('''
    CREATE TABLE IF NOT EXISTS activities (
        id INTEGER PRIMARY KEY,
        username TEXT,
        activity TEXT,
        date TEXT,
        time TEXT,
        acceleration_x REAL,
        acceleration_y REAL,
        acceleration_z REAL,
        gyro_x REAL,
        gyro_y REAL,
        gyro_z REAL
    )
''')

# İlk 10 satırdan veriyi alıp tabloya ekle
for index, row in sample_data.iterrows():
    c.execute('''
        INSERT INTO activities (username, activity, date, time, acceleration_x, acceleration_y, acceleration_z, gyro_x, gyro_y, gyro_z) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (row['username'], row['activity'], row['date'], row['time'], 
          row['acceleration_x'], row['acceleration_y'], row['acceleration_z'], 
          row['gyro_x'], row['gyro_y'], row['gyro_z']))

# Değişiklikleri kaydet ve bağlantıyı kapat
conn.commit()
conn.close()

print("Veritabanı oluşturuldu ve veriler başarıyla eklendi.")