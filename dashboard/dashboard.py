from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

def create_colors(values):
    # warna biru tua hanya untuk nilai tertinggi
    return ["#1f5f8b" if v == max(values) else "#9ecae1" for v in values]


def create_hourly_pattern_df(df):
    # rata-rata penyewaan per jam, dipisah hari kerja & akhir pekan/libur
    return df.pivot_table(index="hr", columns="workingday", values="cnt", aggfunc="mean")


def create_daily_df(df):
    # agregasi data per jam menjadi data per hari
    daily_df = df.groupby("dteday").agg({
        "cnt": "sum",
        "casual": "sum",
        "registered": "sum",
        "season": "first",
        "weathersit": "first",
        "temp_c": "first"
    }).reset_index()
    return daily_df


def create_season_df(daily_df):
    order = ["Spring", "Summer", "Fall", "Winter"]
    season_df = daily_df.groupby("season")["cnt"].mean().reindex(order).dropna()
    return season_df


def create_weather_df(daily_df):
    order = ["Cerah/Berawan", "Berkabut/Mendung", "Hujan/Salju Ringan"]
    weather_df = daily_df.groupby("weathersit")["cnt"].mean().reindex(order).dropna()
    return weather_df


def create_temp_df(daily_df):
    # binning suhu menjadi 4 kategori
    daily_df = daily_df.copy()
    daily_df["kategori_suhu"] = pd.cut(
        daily_df["temp_c"],
        bins=[0, 10, 20, 30, 50],
        labels=["Dingin (<=10C)", "Sejuk (10-20C)", "Hangat (20-30C)", "Panas (>30C)"]
    )
    temp_df = daily_df.groupby("kategori_suhu", observed=True)["cnt"].mean()
    return temp_df


# ==== Load data ====
# Path dibuat relatif terhadap file ini, jadi bisa dijalankan dari folder mana pun
main_df = pd.read_csv(Path(__file__).parent / "main_data.csv")
main_df["dteday"] = pd.to_datetime(main_df["dteday"])

min_date = main_df["dteday"].min()
max_date = main_df["dteday"].max()

# ==== Sidebar (filter) ====
with st.sidebar:
    st.header("🚲 Bike Sharing")
    rentang = st.date_input(
        label="Rentang Waktu",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# date_input mengembalikan 1 tanggal saat pengguna baru memilih tanggal awal
if len(rentang) != 2:
    st.info("Pilih tanggal akhir pada filter di sidebar.")
    st.stop()
start_date, end_date = rentang

filtered_df = main_df[(main_df["dteday"] >= str(start_date)) &
                      (main_df["dteday"] <= str(end_date))]

# ==== Siapkan DataFrame ====
hourly_df = create_hourly_pattern_df(filtered_df)
daily_df = create_daily_df(filtered_df)
season_df = create_season_df(daily_df)
weather_df = create_weather_df(daily_df)
temp_df = create_temp_df(daily_df)

# ===== Tampilan dashboard =====
st.header("Bike Sharing Dashboard 🚲")

st.subheader("Ringkasan Penyewaan")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total penyewaan", value=f"{daily_df['cnt'].sum():,}")
with col2:
    st.metric("Rata-rata per hari", value=f"{daily_df['cnt'].mean():,.0f}")
with col3:
    st.metric("Porsi pengguna terdaftar", value=f"{daily_df['registered'].sum() / daily_df['cnt'].sum():.1%}")

# ---- Pertanyaan 1 ---
st.subheader("Pertanyaan 1")
st.write("Pada jam berapa saja rata-rata penyewaan sepeda melebihi 300 sewa per jam pada hari kerja dibandingkan akhir pekan/libur selama periode 2011-2012, agar tim operasional dapat menjadwalkan distribusi sepeda pada jam-jam tersebut?")
fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(hourly_df.index, hourly_df["Hari Kerja"], marker="o", linewidth=2.5, color="#1f5f8b", label="Hari Kerja")
ax.plot(hourly_df.index, hourly_df["Akhir Pekan/Libur"], marker="o", linewidth=2.5, color="#9ecae1", label="Akhir Pekan/Libur")
ax.axhline(300, color="grey", linestyle="--", label="Ambang 300 sewa per jam")
ax.set_xlabel("Jam dalam sehari")
ax.set_ylabel("Rata-rata penyewaan per jam")
ax.set_xticks(range(0, 24))
ax.legend()
st.pyplot(fig)

# ---- Pertanyaan 2 ----
st.subheader("Pertanyaan 2")
st.write("Pada musim dan kondisi cuaca apa rata-rata penyewaan harian turun lebih dari 50% dibandingkan musim dan cuaca terbaiknya selama periode 2011-2012, agar tim pemasaran dan perawatan dapat merencanakan promosi serta jadwal perawatan pada periode tersebut?")
col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x=season_df.index, y=season_df.values, hue=season_df.index, palette=create_colors(season_df.values), legend=False, ax=ax)
    ax.axhline(season_df.max() * 0.5, color="grey", linestyle="--", label="50% dari musim terbaik")
    for container in ax.containers:
        ax.bar_label(container, fmt="%.0f", padding=3, bbox=dict(facecolor="white", edgecolor="none", pad=1))
    ax.set_ylim(0, season_df.max() * 1.15)
    ax.legend()
    ax.set_title("Rata-rata Penyewaan Harian per Musim", fontsize=14)
    ax.set_xlabel("")
    ax.set_ylabel("Rata-rata penyewaan per hari")
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x=weather_df.index, y=weather_df.values, hue=weather_df.index, palette=create_colors(weather_df.values), legend=False, ax=ax)
    ax.axhline(weather_df.max() * 0.5, color="grey", linestyle="--", label="50% dari cuaca terbaik")
    for container in ax.containers:
        ax.bar_label(container, fmt="%.0f", padding=3, bbox=dict(facecolor="white", edgecolor="none", pad=1))
    ax.set_ylim(0, weather_df.max() * 1.15)
    ax.legend()
    ax.set_title("Rata-rata Penyewaan Harian per Cuaca", fontsize=14)
    ax.set_xlabel("")
    ax.set_ylabel("Rata-rata penyewaan per hari")
    ax.tick_params(axis="x", labelsize=9)
    st.pyplot(fig)

# ---- Analisis lanjutan ----
st.subheader("Analisis Lanjutan: Penyewaan Berdasarkan Kategori Suhu")
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x=temp_df.index.astype(str), y=temp_df.values, hue=temp_df.index.astype(str), palette=create_colors(temp_df.values), legend=False, ax=ax)
for container in ax.containers:
    ax.bar_label(container, fmt="%.0f", padding=3, bbox=dict(facecolor="white", edgecolor="none", pad=1))
ax.set_ylim(0, temp_df.max() * 1.15)
ax.set_xlabel("")
ax.set_ylabel("Rata-rata penyewaan per hari")
st.pyplot(fig)


# ---- Analisis lanjutan: segmen waktu ----
st.subheader("Analisis Lanjutan: Kontribusi Segmen Waktu")
segmen = pd.cut(filtered_df["hr"], bins=[-1, 5, 9, 15, 19, 23],
                labels=["Dini hari (00-05)", "Pagi (06-09)", "Siang (10-15)", "Sore (16-19)", "Malam (20-23)"])
segmen_df = filtered_df.groupby(segmen, observed=True)["cnt"].sum()
segmen_df = segmen_df / segmen_df.sum() * 100

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x=segmen_df.index.astype(str), y=segmen_df.values, hue=segmen_df.index.astype(str), palette=create_colors(segmen_df.values), legend=False, ax=ax)
for container in ax.containers:
    ax.bar_label(container, fmt="%.1f%%", padding=3, bbox=dict(facecolor="white", edgecolor="none", pad=1))
ax.set_ylim(0, segmen_df.max() * 1.15)
ax.set_xlabel(None)
ax.set_ylabel("Persentase total penyewaan (%)")
st.pyplot(fig)

# ---- Analisis lanjutan: tingkat permintaan per musim ----
st.subheader("Analisis Lanjutan: Tingkat Permintaan Harian per Musim")
label_tingkat = ["Rendah (<3.000)", "Sedang (3.000-6.000)", "Tinggi (>6.000)"]
daily_df["tingkat_permintaan"] = pd.cut(daily_df["cnt"], bins=[0, 3000, 6000, 10000], labels=label_tingkat)
tingkat_df = pd.crosstab(daily_df["season"], daily_df["tingkat_permintaan"], normalize="index") * 100
tingkat_df = tingkat_df.reindex(columns=label_tingkat, fill_value=0)
tingkat_df = tingkat_df.reindex(["Spring", "Summer", "Fall", "Winter"]).dropna()

fig, ax = plt.subplots(figsize=(10, 5))
tingkat_df.plot(kind="bar", stacked=True, ax=ax, color=["#deebf7", "#9ecae1", "#1f5f8b"])
ax.set_xlabel(None)
ax.set_ylabel("Persentase hari (%)")
ax.tick_params(axis="x", rotation=0)
ax.legend(title=None, loc="upper center", bbox_to_anchor=(0.5, -0.08), ncol=3)
st.pyplot(fig)

st.caption("Sumber data: Bike Sharing Dataset (Capital Bikeshare), 2011-2012")
