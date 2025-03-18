import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_echarts import st_echarts

# Load Dataset
day_df = pd.read_csv("df_day.csv")
hour_df = pd.read_csv("df_hour.csv")

# Konfigurasi halaman
st.set_page_config(
    page_title="Proyek Analisis | Bagas Nuryaman",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Header
st.title("🚲 **Proyek Analisis Data: Bike Sharing**")
st.write("**Nama:** Satria Dirgantara Nuryaman")
st.write("**Email:** satriadirgantaranuryaman15@gmail.com")
st.write("**ID Dicoding:** MC435D5Y1642")
st.divider()

# Sidebar Navigasi
st.sidebar.title("📊 Navigasi Analisis")
menu = st.sidebar.radio(
    "Pilih Analisis:", 
    ["📌 Perbandingan Penyewaan (2011 vs 2012)", 
     "🌦️ Pengaruh Cuaca terhadap Penyewaan",
     "🕒 Pola Penggunaan Sepeda dalam Sehari",
     "📅 Tren Penyewaan Sepeda per Bulan",
     "👥 Perbedaan Pola Member vs Non-Member"]
)

# 1️⃣ **Perbandingan Penyewaan Sepeda 2011 vs 2012**
if menu == "📌 Perbandingan Penyewaan (2011 vs 2012)":
    st.subheader("📌 Perbandingan Penyewaan Sepeda (2011 vs 2012)", divider='violet')
    st.write("")

    # Data Perbandingan
    perbandingan_tahun = day_df.groupby("Tahun")["Total"].sum().reset_index()
    perbandingan_jam = hour_df.groupby(['Tahun', 'Jam'], observed=False)['Total'].sum().reset_index()

    cl1, cl2, cl3 = st.columns([5,1,5])

    with cl1:
        st.write("📊 Perbandingan Penyewaan Sepeda 2011 vs 2012")
        # Data untuk ECharts
        series = [{
            "name": "Total Peminjaman",
            "type": "bar",
            "data": perbandingan_tahun['Total'].tolist(),
            "itemStyle": {"color": "#1f77b4"},
        }]

        # Opsi untuk ECharts
        chart_options = {
            "tooltip": {"trigger": "axis"},
            "xAxis": {"type": "category", "data": perbandingan_tahun['Tahun'].astype(str).tolist()},
            "yAxis": {"type": "value", "name": "Jumlah Peminjaman"},
            "series": series
        }

        # Tampilkan chart di Streamlit
        st_echarts(options=chart_options, height="500px")

    with cl3:
        st.write("📊 Perbandingan Penyewaan Sepeda per Jam (2011 vs 2012)")
        # Data untuk ECharts
        series = [{
            "name": "Total Peminjaman",
            "type": "bar",
            "data": perbandingan_jam['Total'].tolist(),
            "itemStyle": {"color": "#1f77b4"},
        }]

        # Opsi untuk ECharts
        chart_options = {
            "tooltip": {"trigger": "axis"},
            "xAxis": {"type": "category", "data": perbandingan_jam['Jam'].astype(str).tolist()},
            "yAxis": {"type": "value", "name": "Jumlah Peminjaman"},
            "series": series
        }

        # Tampilkan chart di Streamlit
        st_echarts(options=chart_options, height="500px")


    st.write("""
    📌 **Insight**:
    - **Tahun 2012** memiliki jumlah Penyewaan tertinggi.
    - **Ekspansi besar-besaran** oleh Capital Bike Share dengan penambahan **50 stasiun** di 2012.
    - **Cuaca lebih hangat** di 2012, yang mendorong lebih banyak orang untuk bersepeda.
    """)

# 2️⃣ **Pengaruh Cuaca terhadap Penyewaan Sepeda**
elif menu == "🌦️ Pengaruh Cuaca terhadap Penyewaan":
    st.subheader("🌦️ Pengaruh Cuaca terhadap Penyewaan Sepeda", divider='violet')

    Impact_Cuaca = day_df.groupby(by=['Tahun', 'Cuaca'], observed=False)['Total'].sum().reset_index()

    # Data untuk ECharts
    cuaca_categories = Impact_Cuaca['Cuaca'].unique().tolist()
    series = []
    for tahun in Impact_Cuaca['Tahun'].unique():
        data = Impact_Cuaca[Impact_Cuaca['Tahun'] == tahun]['Total'].tolist()
        series.append({"name": str(tahun), "type": "bar", "data": data})

    # Opsi untuk ECharts
    chart_options = {
        "tooltip": {"trigger": "axis"},
        "legend": {"data": [str(tahun) for tahun in Impact_Cuaca['Tahun'].unique()]},
        "xAxis": {"type": "category", "data": cuaca_categories},
        "yAxis": {"type": "value"},
        "series": series
    }

    # Tampilkan chart di Streamlit
    st_echarts(options=chart_options, height="500px")

    option = {
        "title": {"text": "Scatter Plot Suhu vs Peminjaman Sepeda"},
        "xAxis": {"name": "Suhu Terasa (°C)"},
        "yAxis": {"name": "Jumlah Peminjaman Sepeda"},
        "series": [
            {
                "symbolSize": 10,
                "data": day_df[["Suhu_Terasa", "Total"]].values.tolist(),
                "type": "scatter"
            }
        ]
    }

    st_echarts(options=option, height="500px")

    st.write("""
    📌 **Insight**:
    - **Cuaca cerah/berawan** memiliki jumlah Penyewaan tertinggi.
    - Penyewaan sepeda **berkurang drastis saat hujan atau salju**.
    - Suhu yang **terasa nyaman** (15-35°C) meningkatkan jumlah Penyewaan.
    - `Hangat` dan `Nyaman` merupakan keniakan yang sangat stabil dan signifikan bisa di lihat dari `scatterplot` di atas lonjakan `Jumlah Peminjaman` di saat `Suhu_Terasa` mencapai 15 Celcius sampai  35 Celcius.
    - Dan pada kesimpulannya bahwa `Cuaca` `Cerah/Berawan` dapat di katakan merupakan sebuah fakta dan bukti nyata bahwa dialah yang paling berkontribusi untuk `Total Peminjaman` `Capital Bike Share`.
    """)

# 3️⃣ **Pola Penggunaan Sepeda dalam Sehari**
elif menu == "🕒 Pola Penggunaan Sepeda dalam Sehari":
    st.subheader("🕒 Pola Penggunaan Sepeda dalam Sehari", divider='violet')

    # Definisikan urutan hari yang diinginkan
    urutan_hari = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']
    
    # Filter data untuk 2011 dan 2012, lalu urutkan berdasarkan urutan_hari
    data_2011 = hour_df[hour_df['Tahun'] == 2011].groupby('Hari', observed=False)['Total'].sum().reindex(urutan_hari)
    data_2012 = hour_df[hour_df['Tahun'] == 2012].groupby('Hari', observed=False)['Total'].sum().reindex(urutan_hari)

    # Data untuk ECharts
    series = [
        {"name": "2011", "type": "bar", "data": data_2011.values.tolist()},
        {"name": "2012", "type": "bar", "data": data_2012.values.tolist()}
    ]

    # Opsi untuk ECharts
    bar_options = {
        "tooltip": {"trigger": "axis"},
        "legend": {"data": ["2011", "2012"]},
        "xAxis": {"type": "category", "data": urutan_hari, "name": "Hari"},
        "yAxis": {"type": "value", "name": "Total Peminjaman"},
        "series": series
    }

    # Tampilkan bar chart di Streamlit
    st_echarts(options=bar_options, height="500px")

    st.write("""
    📌 **Insight**:
    - **Puncak penggunaan** terjadi pada **jam 8 pagi & jam 5-6 sore** (Morning & Evening Rush).
    - Lonjakan di **2012 lebih tajam**, menunjukkan sepeda menjadi **alat transportasi utama**.
    """)

# 4️⃣ **Tren Penyewaan Sepeda per Bulan**
elif menu == "📅 Tren Penyewaan Sepeda per Bulan":
    st.subheader("📅 Tren Penyewaan Sepeda per Bulan")

    # Kelompokkan total peminjaman per bulan untuk masing-masing tahun
    monthly_2011 = day_df[day_df['Tahun'] == 2011].groupby('Bulan', observed=False)['Total'].sum()
    monthly_2012 = day_df[day_df['Tahun'] == 2012].groupby('Bulan', observed=False)['Total'].sum()

    # Data untuk ECharts
    bulan_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des']
    series = [
        {"name": "2011", "type": "line", "data": monthly_2011.values.tolist(), "symbol": "circle"},
        {"name": "2012", "type": "line", "data": monthly_2012.values.tolist(), "symbol": "circle"}
    ]

    # Opsi untuk ECharts
    line_options = {
        "tooltip": {"trigger": "axis"},
        "legend": {"data": ["2011", "2012"]},
        "xAxis": {"type": "category", "data": bulan_labels, "name": "Bulan"},
        "yAxis": {"type": "value", "name": "Total Peminjaman"},
        "series": series
    }

    # Tampilkan line chart di Streamlit
    st_echarts(options=line_options, height="500px")


    # Mengelompokkan data
    season_total = day_df.groupby("Musim", observed=False)["Total"].sum()
    warna_musim = ['#AEC6CF', '#77DD77', '#FFB347', '#FF6961']

    # Konversi data ke format eCharts
    options = {
        "title": {"text": "Total Peminjaman Sepeda Berdasarkan Musim"},
        "xAxis": {"type": "category", "data": season_total.index.tolist()},
        "yAxis": {"type": "value"},
        "series": [{
            "data": season_total.values.tolist(),
            "type": "bar",
            "itemStyle": {"color": warna_musim},
        }]
    }

    # Tampilkan dengan Streamlit
    st_echarts(options=options)

    st.write("""
    📌 **Insight**:
    - Penyewaan menurun pada **Januari-Maret** (Musim Dingin) & meningkat tajam di **April-Juni**.
    - **Musim Gugur & Panas** menjadi favorit pengguna sepeda.
    """)

# 5️⃣ **Perbedaan Pola Member vs Non-Member**
elif menu == "👥 Perbedaan Pola Member vs Non-Member":
    st.subheader("👥 Perbedaan Pola Member vs Non-Member")

    # Kelompokkan data
    kategori_totals = day_df.groupby(
        day_df['Hari'].apply(lambda x: 'Libur' if x in ['Sabtu', 'Minggu'] else 'Kerja')
    )[['Member', 'Non_member']].sum().reset_index()

    # Konfigurasi opsi ECharts
    options = {
        "legend": {
            "data": ["Member", "Non-Member"],
            "top": "10%"
        },
        "xAxis": {
            "type": "category",
            "data": kategori_totals["Hari"].tolist(),
            "name": "Kategori Hari",
            "nameLocation": "middle",
            "nameGap": 25
        },
        "yAxis": {
            "type": "value",
            "name": "Total Peminjaman",
            "nameLocation": "middle",
            "nameGap": 35
        },
        "series": [
            {
                "name": "Member",
                "type": "bar",
                "data": kategori_totals["Member"].tolist(),
                "itemStyle": {"color": "#87CEEB"}  # skyblue
            },
            {
                "name": "Non-Member",
                "type": "bar",
                "data": kategori_totals["Non_member"].tolist(),
                "itemStyle": {"color": "#F08080"}  # lightcoral
            }
        ]
    }

    # Tampilan di Streamlit
    st_echarts(options=options, height="500px")


    st.write("""
    📌 **Insight**:
    - **Member lebih banyak di hari kerja**, menunjukkan penggunaan untuk aktivitas rutin (kerja/sekolah).
    - **Non-Member lebih banyak di akhir pekan**, menunjukkan penggunaan untuk rekreasi.
    """)

