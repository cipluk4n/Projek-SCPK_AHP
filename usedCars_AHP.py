import streamlit as st
import pandas as pd
import numpy as np
import re
import time

st.set_page_config(page_title="SPK Mobil Bekas | AHP", layout="wide")

# SEED & FUNCTION PEMROSESAN DATA (pakai session_state)
# -----------------------------------------------------------
def clean_price(price_val):
    if pd.isna(price_val): return 0.0
    val = str(price_val).replace('$', '').replace(',', '')
    try: return float(val)
    except: return 0.0

def clean_milage(milage_val):
    if pd.isna(milage_val): return 0.0
    val = str(milage_val).replace(' mi.', '').replace(',', '')
    try: return float(val)
    except: return 0.0

def clean_tx(tx):
    tx = str(tx).lower()
    if 'm/t' in tx or 'manual' in tx: return 'Manual'
    elif 'cvt' in tx: return 'CVT'
    elif 'fixed' in tx or 'single' in tx: return 'Fixed Gear (EV)'
    return 'Automatic'

# inisialisasi data ke st.session_state agar perubahan (tambah/edit/hapus) tersimpan selama aplikasi berjalan
if 'df_mobil' not in st.session_state:
    try:
        df_init = pd.read_csv('used_cars.csv')
    except FileNotFoundError:
        df_init = pd.DataFrame(columns=['brand', 'model', 'model_year', 'milage', 'fuel_type', 'engine', 'transmission', 'ext_col', 'int_col', 'accident', 'clean_title', 'price'])
    
    # preprocessing kolom kalkulasi bersih
    df_init['price_clean'] = df_init['price'].apply(clean_price)
    df_init['milage_clean'] = df_init['milage'].apply(clean_milage)
    df_init['tx_clean'] = df_init['transmission'].apply(clean_tx)
    # df_init['engine_liters'] = df_init['engine'].apply(clean_eng)
    st.session_state['df_mobil'] = df_init

# ambil data aktif dari session state
df_mobil = st.session_state['df_mobil']

st.title("Sistem Cerdas & Pendukung Keputusan Mobil Bekas dengan Metode AHP", text_alignment='center')
st.markdown("---")

# SIDEBAR
# ----------------------------------------
menu = st.sidebar.selectbox("Pilih Menu Aplikasi:", ["Data Mobil Bekas", "Perhitungan Rekomendasi | AHP", "Profil Kelompok"])

# MENU 1: DATA MOBIL BEKAS
if menu == "Data Mobil Bekas":
    st.header("Database Mobil Bekas")
    # st.write(f"Total data di database: **{len(df_mobil)}** baris.")
    st.info(f"- Total data: {len(df_mobil)} baris. \n" \
    "- Dataset by: Taeef Najib \n" \
    "- Link: https://www.kaggle.com/datasets/taeefnajib/used-car-price-prediction-dataset")
    
    st.dataframe(df_mobil[['brand', 'model', 'model_year', 'price', 'milage', 'fuel_type', 'transmission', 'engine', 'accident', 'clean_title', 'ext_col', 'int_col']], use_container_width=True)
    # st.dataframe(df_mobil)
    tab_tambah, tab_edit, tab_hapus = st.tabs(["Tambah Data", "Edit Data", "Hapus Data"])
    
    # --- TAMBAH DATA ---
    with tab_tambah:
        st.subheader("Form Tambah Mobil Bekas Baru")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            brand = st.text_input("Brand/Merk") #contoh: Mercedes
            model = st.text_input("Model Mobil") #contoh: Formula 1
            year = st.number_input("Tahun Pembuatan", min_value=1950, max_value=2026, value=2026) #contoh: 1954
        with c2:
            price_input = st.text_input("Harga (contoh: $20,000)", "$") #contoh: $30,000,000
            milage_input = st.text_input("Milage (contoh: 15,000 mi.)", "mi.")
            fuel_type = st.text_input("Jenis Bahan Bakar") #contoh: Gasoline
        with c3:
            engine = st.text_input("Spesifikasi Mesin") #contoh: W196 
            transmission = st.text_input("Transmisi") #contoh: manual-4 speed
            accident = st.selectbox("Riwayat Kecelakaan", ["None reported", "At least 1 accident or damage reported"])
        with c4:
            ext_col = st.text_input("Warna Eksterior") #contoh: silver
            int_col = st.text_input("Warna Interior") #contoh: black
            clean_title = st.selectbox("Clean Title (Surat Lengkap)", ["Yes", "No"])
            
        if st.button("Simpan"):
            new_row = {
                'brand': brand, 'model': model, 'model_year': int(year),
                'price': price_input, 'milage': milage_input, 'fuel_type': fuel_type,
                'engine': engine, 'transmission': transmission, 'ext_col': ext_col, 'int_col': int_col,
                'accident': accident, 'clean_title': clean_title,
                'price_clean': clean_price(price_input), 'milage_clean': clean_milage(milage_input),
                # 'tx_clean': clean_tx(transmission), 'engine_liters': clean_eng(engine)
                'tx_clean': clean_tx(transmission)
            }
            # masukkan ke session state
            st.session_state['df_mobil'] = pd.concat([st.session_state['df_mobil'], pd.DataFrame([new_row])], ignore_index=True)
            st.toast("Data berhasil ditambahkan!")
            st.success("Data mobil baru berhasil ditambahkan!")
            time.sleep(2.0)
            st.rerun()

    # --- TAB EDIT DATA ---
    with tab_edit:
        st.subheader("Form Edit Data Mobil")
        if len(df_mobil) > 0:
            pilihan_indeks = st.selectbox("Pilih Mobil yang Akan Diedit (Berdasarkan Indeks & Nama):", 
                                         options=df_mobil.index, 
                                         format_func=lambda x: f"Indeks {x} - {df_mobil.loc[x, 'brand']} {df_mobil.loc[x, 'model']} ({df_mobil.loc[x, 'model_year']})")
            
            mobil_terpilih = df_mobil.loc[pilihan_indeks]
            
            # form edit isi otomatis sesuai data lama
            ce1, ce2, ce3 = st.columns(3)
            with ce1:
                edit_brand = st.text_input("Edit Brand", mobil_terpilih['brand'])
                edit_model = st.text_input("Edit Model", mobil_terpilih['model'])
                edit_year = st.number_input("Edit Tahun Model", mobil_terpilih['model_year'])
            with ce2:
                edit_price = st.text_input("Edit Harga", mobil_terpilih['price'])
                edit_milage = st.text_input("Edit Milage", mobil_terpilih['milage'])
            with ce3:
                edit_accident = st.selectbox("Edit Status Kecelakaan", ["None reported", "At least 1 accident or damage reported"], index=0 if "none" in str(mobil_terpilih['accident']).lower() else 1)
                edit_title = st.selectbox("Edit Status Surat", ["Yes", "No"], index=0 if str(mobil_terpilih['clean_title']).lower() == 'yes' else 1)
            
            if st.button("Update"):
                st.session_state['df_mobil'].loc[pilihan_indeks, 'brand'] = edit_brand
                st.session_state['df_mobil'].loc[pilihan_indeks, 'model'] = edit_model
                st.session_state['df_mobil'].loc[pilihan_indeks, 'price'] = edit_price
                st.session_state['df_mobil'].loc[pilihan_indeks, 'milage'] = edit_milage
                st.session_state['df_mobil'].loc[pilihan_indeks, 'accident'] = edit_accident
                st.session_state['df_mobil'].loc[pilihan_indeks, 'clean_title'] = edit_title
                st.session_state['df_mobil'].loc[pilihan_indeks, 'model_year'] = edit_year
                # re-clean data numeriknya (price, milage)
                st.session_state['df_mobil'].loc[pilihan_indeks, 'price_clean'] = clean_price(edit_price)
                st.session_state['df_mobil'].loc[pilihan_indeks, 'milage_clean'] = clean_milage(edit_milage)
                
                st.toast(f"Data mobil pada Indeks {pilihan_indeks} berhasil di-update!")
                st.success(f"Data mobil pada Indeks {pilihan_indeks} berhasil di-update!")
                time.sleep(2.0)
                st.rerun()
        else:
            st.warning("Database kosong.")

    # --- TAB HAPUS DATA ---
    with tab_hapus:
        st.subheader("Hapus Data Mobil dari Database")
        if len(df_mobil) > 0:
            hapus_indeks = st.selectbox("Pilih Mobil yang Akan Dihapus:", 
                                         options=df_mobil.index, 
                                         format_func=lambda x: f"Indeks {x} - {df_mobil.loc[x, 'brand']} {df_mobil.loc[x, 'model']}")
            
            if st.button("Hapus Permanen", type="secondary"):
                st.session_state['df_mobil'] = st.session_state['df_mobil'].drop(hapus_indeks).reset_index(drop=True)
                st.toast("Data berhasil dihapus dari database!")
                st.success("Data berhasil dihapus dari database sistem!")
                time.sleep(2.0)
                st.rerun()
        else:
            st.warning("Database kosong.")


# MENU 2: ANALISIS REKOMENDASI (AHP)
# ----------------------------------------------------
elif menu == "Perhitungan Rekomendasi | AHP":
    st.header("Pengaturan Kriteria & Proses Pengambilan Keputusan Menggunakan AHP)")
    
    # 1. Hard Filter (fuel_type, transmisi, warna eksterior, warna interior)
    st.subheader("1. Pilih Preferensi Utama (Filter)")
    cf1, cf2, cf3 = st.columns(3)
    with cf1:
        f_options = df_mobil['brand'].dropna().unique().tolist()
        s_fuel = st.multiselect("Brand:", f_options, default=f_options[:1] if len(f_options)>1 else f_options)
        f_options = df_mobil['fuel_type'].dropna().unique().tolist()
        s_fuel = st.multiselect("Bahan Bakar:", f_options, default=f_options[:2] if len(f_options)>1 else f_options)
    with cf2:
        t_options = df_mobil['engine'].unique().tolist()
        s_tx = st.multiselect("Spesifikasi Mesin:", t_options, default=t_options[:1])
        t_options = df_mobil['tx_clean'].unique().tolist()
        s_tx = st.multiselect("Transmisi:", t_options, default=t_options[:1])
    with cf3:
        ext_options = df_mobil['ext_col'].dropna().unique().tolist()
        s_ext = st.multiselect("Warna Eksterior:", ext_options, default=ext_options[:1] if len(ext_options)>3 else ext_options)
        int_options = df_mobil['int_col'].dropna().unique().tolist()
        s_int = st.multiselect("Warna Interior:", int_options, default=int_options[:2] if len(int_options)>3 else int_options)
    
    # filter mobil berdasarkan hard filter
    df_filtered = df_mobil[
        (df_mobil['fuel_type'].isin(s_fuel)) &
        (df_mobil['tx_clean'].isin(s_tx)) &
        (df_mobil['ext_col'].isin(s_ext)) &
        (df_mobil['int_col'].isin(s_int))
    ]
    st.info(f"Jumlah mobil terkualifikasi berdasarkan filter Anda: **{len(df_filtered)}** unit.")
    
    default_rules = {
        ('Price', 'Milage'): ('Price', 3),
        ('Price', 'Model Year'): ('Price', 3),
        # ('Price', 'Engine'): ('Price', 3),
        ('Price', 'Accident'): ('Price', 2),
        ('Price', 'Clean Title'): ('Price', 1),
        ('Milage', 'Model Year'): ('Milage', 6),
        # ('Milage', 'Engine'): ('Milage', 2),
        ('Milage', 'Accident'): ('Milage', 2),
        ('Milage', 'Clean Title'): ('Clean Title', 3),
        # ('Model Year', 'Engine'): ('Engine', 3),
        ('Model Year', 'Accident'): ('Accident', 3),
        ('Model Year', 'Clean Title'): ('Clean Title', 3),
        # ('Engine', 'Accident'): ('Engine', 2),
        # ('Engine', 'Clean Title'): ('Clean Title', 2),
        ('Accident', 'Clean Title'): ('Clean Title', 2)
    }

    # 2. Input Kriteria
    st.write("---")
    st.subheader("2. Kuesioner Perbandingan Berpasangan Kriteria (Skala Saaty 1-9)")
    
    kriteria = ['Price', 'Milage', 'Model Year', 'Accident', 'Clean Title']
    n = len(kriteria)
    inputs = {}
    idx = 0
    
    col_k1, col_k2 = st.columns(2)
    for i in range(n):
        for j in range(i + 1, n):
            k1 = kriteria[i]
            k2 = kriteria[j]
            
            def_pilihan, def_nilai = default_rules.get((k1, k2), (k1, 1))
            
            default_radio_index = 0 if def_pilihan == k1 else 1 # 0: k1, 1: k2
            
            with col_k1 if idx % 2 == 0 else col_k2:
                st.write(f"**Perbandingan {idx+1}:** {k1} vs {k2}")
                
                pilihan = st.radio(
                    f"Mana yang lebih diprioritaskan?", 
                    [k1, k2], 
                    index=default_radio_index, 
                    key=f"r2_{i}_{j}", 
                    horizontal=True
                )
                
                nilai = st.slider(
                    "Skor Kepentingan", 
                    1, 9, 
                    value=int(def_nilai), 
                    key=f"s2_{i}_{j}"
                )
                
                if pilihan == k1:
                    inputs[(i, j)] = float(nilai)
                else:
                    inputs[(i, j)] = 1.0 / float(nilai)
                    
                st.markdown("<br>", unsafe_allow_html=True)
                idx += 1

    if st.button("Confirm", type="primary"):
        if len(df_filtered) == 0:
            st.error("Gagal menghitung: Tidak ada mobil yang lolos filter awal di atas!")
        else:
            st.toast("Proses Perhitungan AHP Berhasil Dijalankan!")
            st.success("Perhitungan Sukses Dijalankan!")
            
            # --- MATRIKS BERPASANGAN ---
            st.subheader("Tabel Matriks Berpasangan Kriteria")
            A = np.eye(n)
            for (i, j), val in inputs.items():
                A[i, j] = val
                A[j, i] = 1.0 / val
            df_matriks = pd.DataFrame(A, columns=kriteria, index=kriteria)
            st.dataframe(df_matriks.style.format("{:.2f}"))
            
            # --- NORMALISASI & BOBOT PRIORITAS ---
            st.subheader("Normalisasi Matriks Kriteria & Perhitungan Bobot Prioritas")
            A_norm = A / A.sum(axis=0)
            bobot_prioritas = A_norm.mean(axis=1)
            
            df_bobot = pd.DataFrame({'Kriteria': kriteria, 'Bobot Prioritas': bobot_prioritas})
            st.dataframe(df_bobot.style.format({'Bobot Prioritas': '{:.4f}'}), use_container_width=True)
            
            # --- UJI CONSISTENCY RATIO (CR) ---
            st.subheader("Uji Consistency Ratio (CR)")
            lambda_max = np.mean(np.dot(A, bobot_prioritas) / bobot_prioritas)
            CI = (lambda_max - n) / (n - 1)
            RI = 1.24  # RI untuk matriks 6x6
            CR = CI / RI
            
            st.write(f"• Lambda Max ($\lambda_{{max}}$): `{lambda_max:.4f}`")
            st.write(f"• Consistency Index (CI): `{CI:.4f}`")
            st.write(f"• **Consistency Ratio (CR): {CR:.4f}**")
            
            if CR <= 0.1:
                st.success(f"Konfirmasi: Hasil Konsisten! (CR = {CR:.4f} ≤ 0.1), melangkah ke tahap perangkingan.")
                
                # --- TABEL NORMALISASI NILAI ALTERNATIF (ABSOLUTE MEASUREMENT) ---
                st.subheader("Tabel Normalisasi Nilai Alternatif (Skala 0 - 1)")
                st.caption("[BENEFIT] diukur absolut dengan: $x / max(x)$")
                st.caption("[[COST] diukur absolut dengan: $min(x) / x$")
                df_scoring = df_filtered.copy()
                
                # Menggunakan Min-Max Scaling (Aturan Utility Cost/Benefit)
                min_p, max_p = df_mobil['price_clean'].min(), df_mobil['price_clean'].max()
                min_m, max_m = df_mobil['milage_clean'].min(), df_mobil['milage_clean'].max()
                min_y, max_y = df_mobil['model_year'].min(), df_mobil['model_year'].max()

                # Sifat Safety Net: Menghindari pembagian dengan angka 0 jika ada data kosong/nol
                if min_p == 0: min_p = 1.0 
                if min_m == 0: min_m = 1.0
                
                # price(cost), milage(cost), model_year(benefit), accident(benefit), clean_title(benefit)
                df_scoring['s_price'] = df_scoring['price_clean'].apply(lambda x: min_p / x if x > 0 else 0.0)
                df_scoring['s_mile'] = df_scoring['milage_clean'].apply(lambda x: min_m / x if x > 0 else 0.0)

                # Kriteria BENEFIT: x / max(x)
                df_scoring['s_year'] = df_scoring['model_year'] / max_y

                # Kriteria Kategorikal (Disamakan skalanya menjadi 0 sampai 1)
                # df_scoring['s_engine'] = df_scoring['engine_liters'].apply(lambda l: 1.0 if 1.5 < l <= 2.5 else (0.66 if l <= 1.5 else 0.33))
                df_scoring['s_accident'] = df_scoring['accident'].apply(lambda x: 1.0 if 'none' in str(x).lower() else 0.11)
                df_scoring['s_title'] = df_scoring['clean_title'].apply(lambda x: 1.0 if str(x).lower() == 'yes' else 0.11)

                # Tampilkan ke DataFrame Streamlit
                df_alt_norm = df_scoring[['brand', 'model', 's_price', 's_mile', 's_year', 's_accident', 's_title']]
                df_alt_norm.columns = ['Brand', 'Model', 'Price_N (Cost)', 'Milage_N(Cost)', 'Year_N (Ben)', 'Accident_N (Ben)', 'Title_N (Ben)']
                st.dataframe(df_alt_norm.style.format({c: '{:.4f}' for c in df_alt_norm.columns if 'Norm' in c}))
                
                # --- TABEL HASIL AKHIR REKOMENDASI ---
                st.subheader("Hasil Akhir Rekomendasi Mobil Bekas Terbaik")
                score_matrix = df_scoring[['s_price', 's_mile', 's_year', 's_accident', 's_title']].values
                df_scoring['Skor_Akhir_AHP'] = np.dot(score_matrix, bobot_prioritas)
                
                hasil_akhir = df_scoring.sort_values(by='Skor_Akhir_AHP', ascending=False)
                kolom_akhir = ['brand', 'model', 'model_year', 'price', 'milage', 'Skor_Akhir_AHP']
                st.dataframe(hasil_akhir[kolom_akhir].style.format({'Skor_Akhir_AHP': '{:.4f}'}), use_container_width=True)

                # --- TOMBOL DOWNLOAD HASIL AKHIR ---
                csv_data = hasil_akhir[kolom_akhir].to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download Rekomendasi",
                    data=csv_data,
                    file_name="Rekomendasi_Mobil_Bekas_AHP.csv",
                    mime="text/csv"
                )
                
                # --- GRAFIK REKOMENDASI ---
                st.subheader("Grafik Top 30 Rekomendasi Mobil Terbaik")
                df_chart = hasil_akhir.copy()
                df_chart['Mobil'] = df_chart['brand'] + " " + df_chart['model'] + " (" + df_chart['model_year'].astype(str) + ")"
                df_chart_sorted = df_chart.sort_values(by='Skor_Akhir_AHP', ascending=False).head(30)
                # ngurutin sumbu x berdasarkan kategori skor akhir ahp
                df_chart_sorted['Mobil'] = pd.Categorical(
                    df_chart_sorted['Mobil'], 
                    categories=df_chart_sorted['Mobil'].tolist(), 
                    ordered=True
                )
                st.bar_chart(df_chart_sorted.set_index('Mobil')['Skor_Akhir_AHP'])

            else:
                st.error("Konfirmasi: Hasil TIDAK Konsisten! (CR > 0.1). Mohon isi kembali slider di atas dengan logika yang lebih sinkron.")

# MENU 2: Profil Kelompok
# ----------------------------------------------------
elif menu == "Profil Kelompok":
    st.write("## Profil Kelompok")
    col1, col2 = st.columns(2)
    with col1:
        st.info('- Desta Fondria \n - IF-A \n - 123240028')
    with col2:
        st.info('- Rabbani \n - IF-A \n - 123240099')