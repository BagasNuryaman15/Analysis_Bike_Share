import streamlit as st
import pandas as pd
from babel import numbers
import plotly.express as px
import plotly.graph_objects as go

# Konfigurasi halaman
st.set_page_config(
    page_title="Dashboard Analisis Penyewaan Sepeda",
    page_icon="🚲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Fungsi untuk memuat data
@st.cache_data
def load_data():
    # Load data
    day_df = pd.read_csv('day_df_cleaned.csv')
    hour_df = pd.read_csv('hour_df_cleaned.csv')

    # Mengubah kolom Tanggal menjadi datetime
    day_df['Tanggal'] = pd.to_datetime(day_df['Tanggal'])
    hour_df['Tanggal'] = pd.to_datetime(hour_df['Tanggal'])

    return day_df, hour_df

# Memuat data
try:
    day_df, hour_df = load_data()
    data_loaded = True
except Exception as e:
    st.error(f"Error saat memuat data: {e}")
    st.info("Upload file CSV untuk melanjutkan")
    data_loaded = False
    
    # Opsi untuk mengunggah file
    day_file = st.file_uploader("Upload cleaned_day_df.csv", type=['csv'])
    hour_file = st.file_uploader("Upload cleaned_hour_df.csv", type=['csv'])
    
    if day_file and hour_file:
        day_df = pd.read_csv(day_file)
        hour_df = pd.read_csv(hour_file)
        
        day_df['Tanggal'] = pd.to_datetime(day_df['Tanggal'])
        hour_df['Tanggal'] = pd.to_datetime(hour_df['Tanggal'])
        
        data_loaded = True

# All about function
# 1. Format number
def format_number(number):
    return numbers.format_number(number, locale='id_ID')

# 2. Filter tanggal
def create_date_filter(container, dataframe, key_suffix=""):
    tanggal_awal = container.date_input('Filter Tanggal:', 
                                value=(dataframe['Tanggal'].min(), dataframe['Tanggal'].max()),
                                min_value=dataframe['Tanggal'].min(), 
                                max_value=dataframe['Tanggal'].max(),
                                key=f"date_filter_{key_suffix}")
    
    if isinstance(tanggal_awal, tuple):
        start_date = pd.to_datetime(tanggal_awal[0])
        end_date = pd.to_datetime(tanggal_awal[1])
    else:
        start_date = pd.to_datetime(tanggal_awal)
        end_date = pd.to_datetime(tanggal_awal)
        
    return start_date, end_date


# Membuat dashboard
if data_loaded:
    # Head dashboard
    st.title("Dashboard Analisis Penyewaan Sepeda 🚲")
    st.markdown("""
    Dashboard ini menampilkan analisis Penyewaan sepeda berdasarkan data harian dan per jam.
    Gunakan filter di sidebar untuk menyesuaikan visualisasi.
    """)

    st.header("Informasi Penyewaan")
    col1, col2, col3, col4, col5 = st.columns(5)

    # Metric
    # Total Penyewaan tahun 2011
    total_Penyewaan_2011 = day_df[day_df['Tahun'] == 2011]['Total'].sum()
    rerata_Penyewaan_harian_2011 = day_df[day_df['Tahun'] == 2011]['Total'].mean()
    nilai_Penyewaan_harian_tertinggi_2011 = day_df[day_df['Tahun'] == 2011]['Total'].max()
    total_non_member_2011 = day_df[day_df['Tahun'] == 2011]['Non_member'].sum()
    total_member_2011 = day_df[day_df['Tahun'] == 2011]['Member'].sum()
    
    # Total Penyewaan tahun 2012
    total_Penyewaan_2012 = day_df[day_df['Tahun'] == 2012]['Total'].sum()
    rerata_Penyewaan_harian_2012 = day_df[day_df['Tahun'] == 2012]['Total'].mean()
    nilai_Penyewaan_harian_tertinggi_2012 = day_df[day_df['Tahun'] == 2012]['Total'].max()
    total_non_member_2012 = day_df[day_df['Tahun'] == 2012]['Non_member'].sum()
    total_member_2012 = day_df[day_df['Tahun'] == 2012]['Member'].sum()

    # Membuat metric
    col1.metric(label="Total Penyewaan (2012)", value=format_number(total_Penyewaan_2012), delta=f"{format_number(total_Penyewaan_2011)} (2011)", border=True)
    col2.metric(label="Rerata Penyewaan Harian (2012)", value=format_number(rerata_Penyewaan_harian_2012), delta=f"{format_number(rerata_Penyewaan_harian_2011)} (2011)", border=True)
    col3.metric(label="Nilai Sewa Harian Tertinggi (2012)", value=format_number(nilai_Penyewaan_harian_tertinggi_2012), delta=f"{format_number(nilai_Penyewaan_harian_tertinggi_2011)} (2011)", border=True)
    col4.metric(label="Total Non-Member (2012)", value=format_number(total_non_member_2012), delta=f"{format_number(total_non_member_2011)} (2011)", border=True)
    col5.metric(label="Total Member (2012)", value=format_number(total_member_2012), delta=f"{format_number(total_member_2011)} (2011)", border=True)

    # Detail Data
    with st.expander("Detail Data"):
        col_day, col_hour = st.columns(2)
        with col_day:
            st.subheader("Data Harian")
            st.dataframe(day_df)
        with col_hour:
            st.subheader("Data Per Jam")
            st.dataframe(hour_df)
            
    # Spasi
    st.markdown("""
    <style>
    .stApp {
        padding-top: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "Perbandingan Penyewaan Sepeda", 
        "Pengaruh Cuaca", 
        "Pola Pengguna", 
        "Tren Musiman"
    ])
    
    with tab1:
        st.subheader("Total Penyewaan Sepeda")
        
        # Tipe Filter
        col_tgl, col_select_box_null, col_perbandingan = st.columns([2, 3, 1])
        
        # Filter Tanggal
        start_date, end_date = create_date_filter(col_tgl, day_df, key_suffix="tab1")
        
        # Filter data berdasarkan tanggal
        filtered_df_day = day_df[(day_df['Tanggal'] >= start_date) & (day_df['Tanggal'] <= end_date)]
        filtered_df_hour = hour_df[(hour_df['Tanggal'] >= start_date) & (hour_df['Tanggal'] <= end_date)]
        
        # Filter perbandingan
        perbandingan = col_perbandingan.selectbox('Filter Berdasarkan:', ['Tahun', 'Bulan', 'Hari', 'Jam', 'Musim'])
        
        # Filter data berdasarkan pilihan
        perbandingan_tahun = filtered_df_day.groupby(by='Tahun', observed=False)['Total'].sum().reset_index()
        perbandingan_bulan = filtered_df_day.groupby(by='Bulan', observed=False)['Total'].sum().reset_index()
        perbandingan_hari = filtered_df_day.groupby(by='Hari', observed=False)['Total'].sum().reset_index()
        perbandingan_jam = filtered_df_hour.groupby(['Tahun', 'Jam'], observed=False)['Total'].sum().reset_index()
        perbandingan_musim = filtered_df_day.groupby(['Musim', 'Tahun'], observed=False)['Total'].sum().reset_index()
        
        if perbandingan == 'Tahun':
            # perbandingan_tahun["  Tahun"] = perbandingan_tahun["Tahun"].astype(str)
            fig = px.bar(perbandingan_tahun, x=perbandingan_tahun["Tahun"], y='Total', category_orders={"Tahun": ["2011", "2012"]}, title='Perbandingan Total Penyewaan Sepeda (2011 - 2012)')
            fig.update_layout(
                xaxis_title="Tahun",
                xaxis_type="category",
                yaxis_title="Total Penyewaan Sepeda"
            )
            st.plotly_chart(fig, use_container_width=True)

            # st.write(perbandingan_tahun.dtypes)
            
            with st.expander("Insight Perbandingan Berdasarkan Tahun"):
                st.info(f"""
                        ### Kesimpulan:
                        - **Tahun 2012** adalah tahun terbaik untuk **Total Penyewaan Sepeda** di **Capital Bike Share** karena:
                        - Keberhasilan **Ekspansi** besar-besaran dengan penambahan **32 stasiun** baru dan perluasan **18 stasiun** existing, hingga total mencapai **50 stasiun** pada akhir tahun. Strategi ini terbukti efektif meningkatkan **Total Penyewaan** ([Capital Bike Share System](https://capitalbikeshare.com/system-data)).
                        - Faktor **Cuaca** sangat mendukung, dengan **Tahun 2012** tercatat sebagai tahun terhangat di Washington, D.C., termasuk Maret yang sangat hangat dan musim panas yang masuk dalam tiga terhangat sepanjang sejarah ([The Washington Post](https://www.washingtonpost.com/blogs/capital-weather-gang/post/top-5-dc-weather-events-of-2012/2012/12/28/d384311c-4f0e-11e2-950a-7863a013264b_blog.html)).
                        - Meskipun ada bencana seperti **Hurricane Sandy**, **Tahun 2012** tetap menjadi tahun dengan **Total Penyewaan** terbanyak, dan ini valid 100%.
                        """)
                st.success("""
                        ### Saran:
                        Untuk meningkatkan Penyewaan di tahun mendatang, **Capital Bike Share** disarankan:
                        - Melanjutkan **Ekspansi** stasiun di lokasi strategis.
                        - Mengoptimalkan distribusi sepeda berdasarkan data penggunaan.
                        - Menawarkan insentif seperti diskon atau paket keanggotaan fleksibel untuk menarik lebih banyak pengguna.
                        - Meningkatkan keamanan, kenyamanan, dan manfaat bagi anggota agar loyalitas pengguna terjaga.
                        """)
            
        elif perbandingan == 'Bulan':
            # Urutkan bulan
            bulan_order = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember']
            
            fig = px.bar(perbandingan_bulan, 
                         x='Bulan', 
                         y='Total', 
                         title='Perbandingan Total Penyewaan Sepeda Bulanan (2011 - 2012)',
                         category_orders={"Bulan": bulan_order})
            
            fig.update_layout(
                xaxis_title="Bulan",
                xaxis_type="category",
                yaxis_title="Total Penyewaan Sepeda"
            )
            st.plotly_chart(fig, use_container_width=True)
            
        elif perbandingan == 'Hari':
            # Urutkan hari
            hari_order = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']
            
            fig = px.bar(perbandingan_hari, 
                         x='Hari', 
                         y='Total', 
                         title='Perbandingan Total Penyewaan Sepeda Harian (2011 - 2012)',
                         category_orders={"Hari": hari_order})
            
            fig.update_layout(
                xaxis_title="Hari",
                xaxis_type="category",
                yaxis_title="Total Penyewaan Sepeda"
            )
            st.plotly_chart(fig, use_container_width=True)
            
        elif perbandingan == 'Jam':
            fig = px.histogram(perbandingan_jam, 
                               x='Jam', 
                               y='Total', 
                               color='Tahun', 
                               barmode='group', 
                               title='Perbandingan Total Penyewaan Sepeda per Jam (2011 - 2012)')
            
            fig.update_xaxes(type='category', categoryorder='array', categoryarray=sorted(perbandingan_musim['Musim'].unique()))
            
            fig.update_layout(
                xaxis_title="Jam",
                yaxis_title="Total Penyewaan Sepeda"
            )
    
            st.plotly_chart(fig, use_container_width=True)
            
            with st.expander("Insight Perbandingan Berdasarkan Jam"):
                st.info("""
                        ### Kesimpulan:
                        Data menunjukkan bahwa meskipun **Tahun 2011** dan **Tahun 2012** memiliki lonjakan Penyewaan yang signifikan dengan pola serupa, **Tahun 2012** selalu menempati posisi tertinggi.
                        - **Morning Rush** dan **Evening Rush** sangat memengaruhi Penyewaan sepeda di kedua tahun, tetapi **Tahun 2012** mencatat lonjakan luar biasa pada **Evening Rush**, mencapai **2.000.000 Penyewaan**.
                        - Pola penggunaan di pagi dan sore hari pada kedua tahun sangat mirip, menunjukkan bahwa sepeda telah menjadi pilihan utama untuk **mobilitas sehari-hari**, bukan sekadar rekreasi.
                        - Lonjakan pada **Evening Rush** jauh lebih tajam dibandingkan **Morning Rush**, kemungkinan karena lebih banyak orang menggunakan sepeda untuk pulang kerja atau sekolah.
                        - **Tahun 2012** adalah tahun terbaik berkat strategi matang dari **Capital Bike Share**.
                        """)
                st.success("""
                           ### Saran:
                           - Optimalkan ketersediaan sepeda pada jam **Evening Rush** untuk mendukung lonjakan permintaan, misalnya dengan menambah stok sepeda di stasiun strategis.
                           - Promosikan penggunaan sepeda sebagai moda transportasi harian dengan kampanye yang menargetkan pengguna saat **Morning Rush** dan **Evening Rush**.
                           """)
                
            
        elif perbandingan == 'Musim':
            fig = px.histogram(perbandingan_musim, 
                               x='Musim',
                               y='Total', 
                               color='Tahun', 
                               barmode='group', 
                               title='Perbandingan Total Penyewaan Sepeda Musiman (2011 - 2012)')
            
            fig.update_layout(
                xaxis_title="Musim",
                yaxis_title="Total Penyewaan Sepeda"
            )
            
            st.plotly_chart(fig, use_container_width=True)
              
            
                
    # -------------------------- Tab 2 (Pengaruh Cuaca) ------------------------------ #
    
    with tab2:
        st.subheader("Pengaruh Cuaca")
        
        # Tipe Filter
        col_tgl, col_select_box_null, col_perbandingan = st.columns([2, 3, 1])
        
        # Filter Tanggal
        start_date, end_date = create_date_filter(col_tgl, hour_df, key_suffix="tab2")
        
        # Filter perbandingan
        perbandingan = col_perbandingan.selectbox('Filter Berdasarkan:', ['Cuaca', 'Suhu'])
        
        # Filter data berdasarkan tanggal
        filtered_df_day = day_df[(day_df['Tanggal'] >= start_date) & (day_df['Tanggal'] <= end_date)]
        filtered_df_hour = hour_df[(hour_df['Tanggal'] >= start_date) & (hour_df['Tanggal'] <= end_date)]
        
        # Filter data berdasarkan pilihan
        impact_cuaca = filtered_df_day.groupby(by=['Tahun', 'Cuaca'], observed=False)['Total'].sum().reset_index()
        atemp_impact = hour_df.groupby(by='Kategori_Suhu_Terasa', observed=False)['Total'].sum().sort_values(ascending=False).reset_index()
        
        if perbandingan == 'Cuaca':
            fig = px.histogram(impact_cuaca, 
                     x='Cuaca', 
                     y='Total', 
                     color='Tahun', 
                     barmode='group', 
                     title='Pengaruh Cuaca terhadap Total Penyewaan Sepeda (2011 - 2012)')
        
            fig.update_layout(
                yaxis_title="Total Penyewaan Sepeda",
                xaxis_title="Jenis Cuaca"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            with st.expander("Insight Pengaruh Cuaca"):
                st.info("""
                        ### Kesimpulan:
                        Berdasarkan grafik di atas, terlihat bahwa kondisi cuaca memiliki pengaruh besar terhadap jumlah Penyewaan sepeda di **Capital Bike Share**.
                        - Pada **Tahun 2011** dan **Tahun 2012**, **Cuaca Cerah/Berawan** selalu mencatat **Penyewaan tertinggi**, sementara **Hujan/Salju Ringan** memiliki **Penyewaan terendah**.
                        - **Tahun 2012** menunjukkan peningkatan drastis di semua kondisi **Cuaca** dibandingkan **Tahun 2011**, terutama pada **Cerah/Berawan** yang melonjak tajam. Ini dipengaruhi oleh pola **Cuaca** yang mendukung serta faktor eksternal seperti ekspansi stasiun pada tahun tersebut.
                        - Untuk memverifikasi apakah cuaca di **Tahun 2012** lebih mendukung dibanding **Tahun 2011**, perlu analisis tambahan terhadap variabel seperti suhu rata-rata dan curah hujan bulanan.
                        """)
                st.success("""
                           ### Saran:
                           Tingkatkan Penyewaan saat **Hujan/Salju Ringan** dengan menyediakan jas hujan gratis di setiap stasiun dan memasang kanopi di jalur sepeda. Langkah ini dapat menjaga kenyamanan pengguna meskipun **Cuaca** kurang mendukung, sehingga mencegah penurunan drastis **Penyewaan** di **Musim Hujan**.
                           """)
        
        elif perbandingan == 'Suhu':
            fig = px.scatter(
                day_df,
                x='Suhu_Terasa',
                y='Total',
                color='Kategori_Suhu_Terasa',
                color_continuous_scale='coolwarm',
                title='Pengaruh Kategori Suhu Terasa terhadap Penyewaan Sepeda Per Jam',
                labels={
                    'Suhu_Terasa': 'Suhu Terasa (°C)',
                    'Total': 'Jumlah Penyewaan Sepeda',
                    'Kategori_Suhu_Terasa': 'Kategori Suhu Terasa'
                },
                opacity=0.8,
            )

            fig.update_traces(marker=dict(size=10, line=dict(width=1, color='black')))
            fig.update_layout(legend_title_text='Kategori Suhu Terasa')
            
            st.plotly_chart(fig, use_container_width=True)
            
            with st.expander("Insight Pengaruh Suhu"):
                st.info("""
                        ### Kesimpulan:
                        Berdasarkan analisis menggunakan data **hour_df**, saya menemukan bahwa **Cuaca Cerah/Berawan** memberikan kontribusi tertinggi terhadap **Total Penyewaan**. Saya memilih **Suhu_Terasa** sebagai indikator karena mencerminkan kombinasi **Suhu Asli** dan **Kelembapan**, sehingga memberikan gambaran yang lebih akurat tentang kondisi nyata yang dirasakan penyewa sepeda.
                        - Kondisi **Hangat** dan **Nyaman** (ketika **Suhu_Terasa** berada di rentang 15°C hingga 35°C) menunjukkan peningkatan **Jumlah Penyewaan** yang stabil dan signifikan, seperti terlihat pada **scatterplot** di atas.
                        - **Cuaca Cerah/Berawan** terbukti secara faktual sebagai faktor utama yang paling berkontribusi pada **Total Penyewaan** di **Capital Bike Share**.
                        """)
                st.success("""
                           ### Saran:
                           Promosikan sewa sepeda saat **Cuaca Cerah/Berawan** dan suhu 15°C-35°C untuk maksimalkan **Total Penyewaan**.
                           """)
        
    
    # -------------------------- Tab 3 (Pola Pengguna) ------------------------------ #
    
    with tab3:
        st.subheader("Pola Pengguna")
        
        # Tipe Filter
        col_tgl, col_select_box_null, col_kondisi = st.columns([2, 3, 1])
        
        # Filter Tanggal
        start_date, end_date = create_date_filter(col_tgl, day_df, key_suffix="tab3")
        
        # Filter berdasarkan kondisi
        kondisi = col_kondisi.selectbox('Filter Berdasarkan:', ['Membership', 'Jenis Hari'])
        
        # Filter data berdasarkan tanggal
        filtered_df_day = day_df[(day_df['Tanggal'] >= start_date) & (day_df['Tanggal'] <= end_date)]
        filtered_df_hour = hour_df[(hour_df['Tanggal'] >= start_date) & (hour_df['Tanggal'] <= end_date)]
        
        # Kelompokkan data langsung tanpa buat kolom baru
        kategori_totals = filtered_df_day.groupby(
            day_df['Hari'].apply(lambda x: 'Libur' if x in ['Sabtu', 'Minggu'] else 'Kerja')
        )[['Member', 'Non_member']].sum().reset_index()
        
        if kondisi == 'Membership':
            # Buat plot dengan Plotly
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=kategori_totals['Hari'],
                y=kategori_totals['Member'],
                name='Member',
                marker_color='skyblue'
            ))
            fig.add_trace(go.Bar(
                x=kategori_totals['Hari'],
                y=kategori_totals['Non_member'],
                name='Non-Member',
                marker_color='lightcoral'
            ))
            
            st.plotly_chart(fig, use_container_width=True)

            # Tambahkan judul dan label
            fig.update_layout(
                title='Perbandingan Penyewaan Sepeda oleh Member vs Non-Member\nPada Hari Kerja dan Akhir Pekan',
                xaxis_title='Kategori Hari',
                yaxis_title='Total Penyewaan',
                barmode='group',
                legend_title='Tipe Pengguna'
            )
            
            with st.expander("Insight Berdasarkan Membership"):
                st.info("""
                        ### Kesimpulan:
                        Perbedaan yang bisa kita simpulkan dan kita ambil antara **Non_member** dan **Member** adalah:
                        - **Member**: Pengguna berlangganan lebih dominan menggunakan sepeda pada **hari kerja**, yang menunjukkan bahwa mereka memanfaatkannya sebagai sarana transportasi utama untuk aktivitas rutin seperti perjalanan ke **tempat kerja atau sekolah**.
                        - Jumlah Penyewaan mereka turun cukup signifikan pada **akhir pekan**, menandakan bahwa mereka lebih jarang menggunakan sepeda untuk liburan, karena mungkin lebih memilih istirahat dan meluangkan waktu bersama keluarganya. Dia liburannya pake mobil ye.
                        - **Non Member**: Berbeda dengan Pengguna kasual yang memiliki pola Penyewaan lebih merata antara **hari kerja** dan **akhir pekan**, meskipun total Penyewaannya tetap lebih kecil dibandingkan member.
                        - Hal ini mengindikasikan bahwa **Non member** kemungkinan besar adalah wisatawan atau pengguna rekreasi, yang menggunakan sepeda secara fleksibel tanpa bergantung pada jadwal kerja.
                        - **Member** lebih mengandalkan sepeda sebagai alat transportasi fungsional, sedangkan **Non member** lebih cenderung menggunakannya untuk keperluan rekreasi. 
                        """)
                st.success("""
                           ### Saran:
                           Dengan **insight** ini, kita bisa menyusun strategi yang lebih tepat untuk meningkatkan jumlah pengguna. Misalnya, menawarkan paket langganan fleksibel untuk Non member agar mereka tertarik menjadi member, atau meningkatkan promosi dan fasilitas bagi wisatawan pada akhir pekan.
                           Tapi untuk membuktikan data ini benar aku akan menghadirkan support nya.
                           """)
            
        elif kondisi == 'Jenis Hari':
            # Filtering data berdasarkan hari
            df_kerja = filtered_df_hour[filtered_df_hour['Hari'].isin(['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat'])]
            df_libur = filtered_df_hour[filtered_df_hour['Hari'].isin(['Sabtu', 'Minggu'])]

            # Grouping berdasarkan jam dan total
            jam_kerja = df_kerja.groupby('Jam', observed=False)['Total'].sum().reset_index()
            jam_libur = df_libur.groupby('Jam', observed=False)['Total'].sum().reset_index()

            # Buat plot dengan Plotly
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=jam_kerja['Jam'],
                y=jam_kerja['Total'],
                name='Hari Kerja',
                marker_color='blue',
                opacity=0.7
            ))
            fig.add_trace(go.Bar(
                x=jam_libur['Jam'],
                y=jam_libur['Total'],
                name='Akhir Pekan',
                marker_color='orange',
                opacity=0.7
            ))

            # Tambahkan judul dan label
            fig.update_layout(
                title='Perbandingan Pola Penyewaan Sepeda Berdasarkan Jam dalam Hari Kerja vs Akhir Pekan',
                xaxis_title='Jam',
                yaxis_title='Total Penyewaan',
                barmode='group',
                legend_title='Kategori Hari',
                xaxis=dict(tickmode='linear', dtick=1)
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            with st.expander("Insight Berdasarkan Jam"):
                st.info("""
                        ### Kesimpulan:
                        Dari insight yang sudah kita dapatkan sebelumnya di tambah dengan barplot yang lebih spesifik dengan melihat perbedaan perjamnya aku menemmukan bahwa:
                        - **Hari Kerja** sangat mendominasi sekali dan tadi insight sebelumnya mengatakan bahwa **Hari Kerja** di dominasi oleh **Member**. dan terbukti karena:
                        - Aktivitas di **Pagi Hari** (Jam 6 - 8) dan **Sore menjelang Malam** (Jam 16 - 19) terlihat bahwa lonjakan besar yang sangat signifikan terjadi, ini menunjukan bukti bahwa **Member** lebih memanfaatkan sepedanya dengan menjadikan sepeda nya alat **transportasi umum** atau **commuter**.
                        - Sedangkan untuk **Akhir Pekan** grafik menunjukan ke stabilan dan tidak ada lonjakan yang terlalu signifikan, ini membuktikan bahwa **Non Member** menggunakan sepedanya tanpa ada variable lain yang mendukung nya, mungkin ada, yaitu saat liburan dan hanya iseng saja.
                        """)
                st.success("""
                           ### Saran:
                           Perusahaan harus lebih memfokuskan diri kepada **Member** tanpa mengurangi kepedulian terhadap **Non-member**. Misalkan, mungkin saja di **Non-member** bukan hanya sekedar orang orang yang berlibur tapi ada juga pekerja yang belum mau berlangganan menjadi **Member**. Nah perusahaan harus memfokuskan diri kepada hal itu juga.
                           """)
    
    # -------------------------- Tab 4 (Tren Musiman) ------------------------------ #

    with tab4:
        st.subheader("Tren Musiman")
        
        # Tipe Filter
        col_tgl, _ = st.columns([2, 3])
        
        # Filter Tanggal
        start_date, end_date = create_date_filter(col_tgl, day_df, key_suffix="tab4")
        
        # Filter data berdasarkan tanggal
        filtered_df_day = day_df[(day_df['Tanggal'] >= start_date) & (day_df['Tanggal'] <= end_date)]
        
        # Urutan musim
        urutan_musim = ['Musim Dingin', 'Musim Semi', 'Musim Panas', 'Musim Gugur']

        # Hitung total Penyewaan per musim untuk setiap tahun
        total_Penyewaan = filtered_df_day.groupby(['Tahun', 'Musim'], observed=False)['Total'].sum().reset_index()

        # Buat plot dengan Plotly
        fig = px.histogram(
            total_Penyewaan,
            x='Musim',
            y='Total',
            color='Tahun',
            barmode='group',
            title='Tren Penyewaan Sepeda Berdasarkan Musim dan Tahun',
            labels={'Musim': 'Musim', 'Total': 'Total Penyewaan', 'Tahun': 'Tahun'},
            category_orders={'Musim': urutan_musim},
            color_discrete_sequence=['palegoldenrod', 'royalblue']
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        with st.expander("Insight Tren Musiman"):
            st.info("""
                    ### Kesimpulan:
                    Analisis data Penyewaan sepeda menunjukkan pola musiman yang konsisten dengan beberapa temuan menarik antara **Tahun 2011** dan **Tahun 2012**.
                    - **Peningkatan di Semua Musim:** Jumlah Penyewaan pada **Tahun 2012** lebih tinggi dibandingkan **Tahun 2011** di semua musim, mengindikasikan pertumbuhan penggunaan sepeda secara keseluruhan, kemungkinan akibat **ekspansi layanan** atau peningkatan kesadaran pengguna.
                    - **Musim Panas Puncak Tertinggi:** Baik di **Tahun 2011** maupun **Tahun 2012**, **Musim Panas** mencatat Penyewaan tertinggi karena cuaca yang nyaman dan mendukung aktivitas luar ruangan.
                    - **Musim Dingin Terendah:** Penyewaan turun drastis pada **Musim Dingin**, terutama di **Tahun 2011**, kemungkinan dipengaruhi oleh suhu rendah, hujan, atau salju.
                    - **Lonjakan di Musim Semi dan Gugur:** Dari **Tahun 2011** ke **Tahun 2012**, Penyewaan meningkat signifikan pada **Musim Semi** dan **Musim Gugur**, menunjukkan kenyamanan pengguna bertambah di luar **Musim Panas**, mungkin karena infrastruktur atau strategi pemasaran yang lebih baik.
                    """)
            st.success("""
                    ### Saran:
                    - Manfaatkan **Musim Panas** dengan promosi intensif untuk memaksimalkan Penyewaan.
                    - Tingkatkan Penyewaan di **Musim Dingin** dengan menyediakan fasilitas pendukung seperti jas hujan atau pemanas di stasiun sepeda.
                    - Perkuat infrastruktur dan kampanye di **Musim Semi** dan **Musim Gugur** untuk mempertahankan tren peningkatan penggunaan sepeda.
                    """)