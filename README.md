# Proyek Analisis Data: Bike Sharing Dataset

Analisis data penyewaan sepeda (Capital Bikeshare, 2011-2012) beserta dashboard Streamlit.

## Pertanyaan Bisnis
1. Pada jam berapa saja rata-rata penyewaan sepeda melebihi 300 sewa per jam pada hari kerja dibandingkan akhir pekan/libur selama periode 2011-2012, agar tim operasional dapat menjadwalkan distribusi sepeda pada jam-jam tersebut?
2. Pada musim dan kondisi cuaca apa rata-rata penyewaan harian turun lebih dari 50% dibandingkan musim dan cuaca terbaiknya selama periode 2011-2012, agar tim pemasaran dan perawatan dapat merencanakan promo serta jadwal maintenance pada periode tersebut?

## Struktur Direktori
```
submission
|── dashboard
│   |── main_data.csv
│   |__ dashboard.py
├── data
│   |── day.csv
│   |__ hour.csv
|── notebook.ipynb
|── README.md
|── requirements.txt
|__ url.txt
```

## Setup Environment
```
python -m venv venv
venv\Scripts\activate        # untuk Windows
pip install -r requirements.txt
```

## Menjalankan Notebook
Jalankan `notebook.ipynb` dari folder `submission` (membaca `data/day.csv` dan `data/hour.csv`).
Menjalankan seluruh sel akan membuat ulang `dashboard/main_data.csv`.

## Menjalankan Dashboard
```
cd submission
streamlit run dashboard/dashboard.py
```
Dashboard terbuka di http://localhost:8501.
