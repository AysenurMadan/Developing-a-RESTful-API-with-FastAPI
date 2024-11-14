import pandas as pd

# CSV dosyasının tam yolunu belirt
file_path = r"C:\Users\aysen\OneDrive\Belgeler\Visual Studio Code\run_or_walk.csv"

# CSV dosyasını oku
df = pd.read_csv(file_path)

# Verinin ilk 10 satırını seç
sample_data = df.head(10)
print(sample_data)

