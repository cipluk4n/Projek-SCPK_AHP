import numpy as np
import pandas as pd
import streamlit as st

# Nama Tab
st.set_page_config(page_title="SPK Mobil Bekas AHP", layout="wide")
st.title("Sistem Pendukung Keputusan: Pemilihan Mobil Bekas dengan Metode AHP", text_alignment="center")
st.divider()

# [( -- Load Function & Pembersihan Data -- )]
@st.cache_data # nyimpen dataset ke cache memori
def load_n_clean():
    try:
        df = pd.read_csv('used_cars.csv')
    except FileNotFoundError: # error handling kalau file belum terupload di folder
        data_dummy = {
            'brand': ['Ford', 'Hyundai', 'Lexus', 'BMW', 'Audi'],
            'model': ['Utility', 'Palisade', 'RX 350', '740 iL', 'Q3'],
            'model_year': [2013, 2021, 2022, 2001, 2021],
            'milage': ['51,000 mi', '34,742 mi', '22,372 mi', '242,000 mi', '9,835 mi'],
            'accident': ['At least 1 accident or damage reported', 'At least 1 accident or damage reported', 'None reported', 'None reported', 'None reported'],
            'clean_title': ['Yes', 'Yes', np.nan, 'Yes', np.nan], # np.nan -> not a number
            'price': ['$10,300', '$38,005', '$54,598', '$7,300', '$34,999']
        }
        df = pd.DataFrame(data_dummy)
    
    # duplikat data untuk dibersihkan
    cleaned_df = df.copy()

    #price: menghilangkan '$'
    cleaned_df['price_clean'] = cleaned_df['price'].astype(str).str.replace('$', '').str.replace(',', ''). astype(float)
    #milage: menghilangkan ',' dan 'mi.'
    cleaned_df['milage_clean'] = cleaned_df['milage'].astype(str).str.replace(',', '').str.replace('mi.', '').astype(float)
    #accident: none reported = 1, ada accident = 0
    cleaned_df['accident_clean'] = cleaned_df['accident'].apply(
        lambda x: 1 if str(x).strip() == 'None reported' else 0)
    #clean_title: yes = 1, lainnya = 0
    cleaned_df['clean_title_clean'] = cleaned_df['clean_title'].apply(
        lambda x: 1 if str(x).strip() == 'Yes' else 0)
    #model_year: sesuai data
    cleaned_df['model_year_clean'] = cleaned_df['model_year'].astype(float)

    return df, cleaned_df

# Load Data Awal
df_raw, df_clean = load_n_clean()
# [( -- Sidebar -- )]
st.sidebar.title("Menu Utama:")
menu = st.sidebar.selectbox("Pilih halaman:", ["Data Mobil Bekas", "Perhitungan AHP", "Profil Kelompok"])

if menu == "Data Mobil Bekas":
    st.header("Dataset Mobil Bekas")
    st.text("Dataset mentah 'used_cars.csv:")
    st.info(f"Total data yang tersedia: {len(df_raw)} baris dan {len(df_raw.columns)} kolom.")
    st.dataframe(df_raw, use_container_width=True)

elif menu == "Perhitungan AHP":
    st.header("Perhitungan AHP")
    st.text("Atur tingkat kepentingan kriteria Anda.")
    col1, col2, col3 = st.columns(3)
    with col1: #w -> weight
        w_year = st.slider("Model Year (Tahun Model)- Benefit", 1, 9, value=7)
        w_milage = st.slider("Milage (Jarak Tempuh) - Cost", 1, 9, value=4)
    with col2:
        w_accident = st.slider("Accident (Riwayat Kecelakaan) - Benefit", 1, 9, value=7)
        w_price = st.slider("Harga Mobil (Price) - Cost", 1, 9, value=8)
    with col3:
        w_title = st.slider("Clean Title (Status Surat Kelengkapan)) - Benefit", 1, 9, value=6)

    st.divider()
    max_baris = st.number_input("Batasi jumlalh baris data yang dihitung: ", min_value=10, max_value=len(df_clean), value=500)

    if st.button("Mulai Perhitungan"):
        st.success("Perhitungan Berhasil Dijalankan")

        st.write("### Step 1: Normalisasi Bobot Kriteria")
        total_skala = w_year + w_milage + w_accident + w_title + w_price

        #b -> bobotPrioritas
        b_year = w_year / total_skala
        b_milage = w_milage / total_skala
        b_accident = w_accident / total_skala
        b_title = w_title / total_skala
        b_price = w_price / total_skala

        #Menampilkan tabel bobot
        df_bobot = pd.DataFrame({
            'Kriteria': ['Model Year (Benefit)', 'Milage (Cost)', 'Accident (Benefit)', 'Clean Title (Benefit)', 'Price (Cost)'],
            'Skala Pilihan': [w_year, w_milage, w_accident, w_title, w_price],
            'Bobot Hasil (W)': [b_year, b_milage, b_accident, b_title, b_price]
        })
        st.table(df_bobot)
        
        #Menampilkan data sesuai batas yang ditentukan user
        df_proses = df_clean.head(max_baris).copy()

        st.write("### Step 2: Normalisasi Nilai Alternatif (Skala Max/Min)")
        st.caption("[BENEFIT] dinormalisasi dengan: $x / max(x)$ | [COST] dinormalisasi dengan: $min(x) / x$")
        #Normalisasi setiap kriteria
        df_proses['n_year'] = df_proses['model_year_clean'] / df_proses['model_year_clean'].max()
        df_proses['n_milage'] = df_proses['milage_clean'].min() / df_proses['milage_clean']
        max_acc = df_proses['accident_clean'].max() if df_proses['accident_clean'].max() > 0 else 1
        df_proses['n_accident'] = df_proses['accident_clean'] / max_acc
        max_title = df_proses['clean_title_clean'].max() if df_proses['clean_title_clean'].max() > 0 else 1
        df_proses['n_title'] = df_proses['clean_title_clean'] / max_title
        df_proses['n_price'] = df_proses['price_clean'].min() / df_proses['price_clean']

        #Menampilkan sebagian tabel hasil normalisasi
        st.dataframe(df_proses[['brand', 'model', 'n_year', 'n_milage', 'n_accident', 'n_title', 'n_price']].head(), use_container_width=True)
        
        st.write("### Step 3: Perhitungan Skor Akhir (Perkalian Nilai dengan Bobot)")
        df_proses['Skor_AHP'] = (
            (df_proses['n_year'] * b_year) +
            (df_proses['n_milage'] * b_milage) +
            (df_proses['n_accident'] * b_accident) +
            (df_proses['n_title'] * b_title) +
            (df_proses['n_price'] * b_price)
        )

        #Menampilkan tabel hasil akhir yg di sorting (tertinggi - terendah)
        st.write("### Hasil Akhir Rekomendasi Mobil Bekas Terbaik")
        df_hasil = df_proses[['brand', 'model', 'model_year', 'milage', 'accident', 'clean_title', 'price', 'Skor_AHP']]
        df_hasil_sorted = df_hasil.sort_values(by='Skor_AHP', ascending=False).reset_index(drop=True)
        #Tambah kolom ranking
        df_hasil_sorted.index = df_hasil_sorted.index + 1
        df_hasil_sorted.index.name = 'Rank'

        st.dataframe(df_hasil_sorted, use_container_width=True)
     

elif menu == "Profil Kelompok":
    st.header("Profil Kelompok")

    with st.container(horizontal=True):
        with st.container(width="content", border=True):
            st.text("Dimas Proboningrat")
            st.text("Desta Fondria")
            st.text("Asiil NR")
        with st.container(width="content", border=True):
            st.write("123220211")
            st.text("123240028")
            st.text("123240099")

