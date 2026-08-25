import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
import time

st.set_page_config(page_icon='🗿', page_title='SPK Mobil Bekas | AHP', layout='wide')
st.title('Pemilihan Mobil Bekas dengan Metode AHP', text_alignment='center')
st.divider()

#[ (Pembersihan Data ) ]
if 'df_raw' not in st.session_state:
    try:
        df = pd.read_csv('used_cars.csv')
    except FileNotFoundError:
        # kalau file CSV tidak ditemukan, tampilin data dummy
        data_dummy = {
            'brand': ['Ford', 'Hyundai', 'Lexus', 'BMW', 'Audi'],
            'model': ['Utility', 'Palisade', 'RX 350', '740 iL', 'Q3'],
            'model_year': [2013, 2021, 2022, 2001, 2021],
            'milage': ['51,000 mi', '34,742 mi', '22,372 mi', '242,000 mi', '9,835 mi'],
            'accident': ['At least 1 accident or damage reported', 'At least 1 accident or damage reported', 'None reported', 'None reported', 'None reported'],
            'clean_title': ['Yes', 'Yes', np.nan, 'Yes', np.nan],
            'price': ['$10,300', '$38,005', '$54,598', '$7,300', '$34,999']
        }
        df = pd.DataFrame(data_dummy)
    st.session_state.df_raw = df

# Fungsi buat bersihin data
def get_cleaned_data():
    cleaned_df = st.session_state.df_raw.copy()
    
    # price: menghilangkan '$' dan ','
    cleaned_df['c_price'] = cleaned_df['price'].astype(str).str.replace('$', '', regex=False).str.replace(',', '', regex=False).astype(float)
    # milage: menghilangkan ',' dan 'mi'
    cleaned_df['c_milage'] = cleaned_df['milage'].astype(str).str.replace(',', '', regex=False).str.replace('mi', '', regex=False).str.replace('.', '', regex=False).str.strip().astype(float)
    # accident: none reported = 1, ada accident = 0
    cleaned_df['c_accident'] = cleaned_df['accident'].apply(
        lambda x: 1 if str(x).strip() == 'None reported' else 0
    )
    # clean_title: yes = 1, lainnya = 0
    cleaned_df['c_clean_title'] = cleaned_df['clean_title'].apply(
        lambda x: 1 if str(x).strip() == 'Yes' else 0
    )
    # model_year: sesuai data
    cleaned_df['c_model_year'] = cleaned_df['model_year'].astype(float)
    
    return cleaned_df

# ambil data ter update
df_raw = st.session_state.df_raw
df_clean = get_cleaned_data()

#[ (SIDEBAR) ]
st.sidebar.title('Menu Utama')
# menu = st.sidebar.selectbox('Pilih halaman:', ['Data Mobil Bekas', 'CRUD','AHP | Pairwise Comparison', 'AHP | Absolute Measurement', 'Profil Kelompok'])
menu = st.sidebar.selectbox('Pilih halaman:', ['Data Mobil Bekas', 'CRUD', 'AHP | Absolute Measurement', 'Profil Kelompok'])

#[ (PAGE: Data Mboil Bekas) ]
if menu == 'Data Mobil Bekas':
    st.write('## Dataset Mentah Mobil Bekas')
    st.info("- Dataset by: Taeef Najib \n" \
    f"- Total data: {len(df_raw)} baris dan {len(df_raw.columns)} kolom. \n" \
    "- Link: https://www.kaggle.com/datasets/taeefnajib/used-car-price-prediction-dataset")
    with st.expander('raw'):
        st.dataframe(df_raw, use_container_width=True)
    with st.expander('clean'):
        df_cook = df_clean[['brand', 'model', 'c_model_year', 'c_milage', 'c_accident', 'c_clean_title', 'c_price']]
        st.dataframe(df_cook, use_container_width=True)
#[ (PAGE: CRUD) ]
#[ (PAGE: Kelola Data - CRUD) ]
elif menu == 'CRUD':
    st.write('## Kelola Data Mobil Bekas (CRUD)')
    st.caption("Gunakan halaman ini untuk Menambah (Create), Mengubah (Update), atau Menghapus (Delete) data mobil.")
    
    # Ambil referensi data agar modifikasi langsung berdampak ke session_state
    df_current = st.session_state.df_raw

    # Buat 3 tab agar tampilan rapi tidak menumpuk
    tab_create, tab_update, tab_delete = st.tabs(["➕ Tambah Data", "✏️ Ubah Data", "❌ Hapus Data"])

    # ------------------- CREATE (TAMBAH DATA) -------------------
    with tab_create:
        st.write("#### Tambah Mobil Baru")
        with st.form("form_tambah_mobil", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                brand = st.text_input("Brand (Contoh: Honda)")
                model = st.text_input("Model (Contoh: Civic)")
                model_year = st.number_input("Tahun Mobil", min_value=1980, max_value=2026, value=2020)
            with col2:
                milage = st.text_input("Milage (Contoh: 15,000 mi)", value="0 mi")
                accident = st.selectbox("Status Kecelakaan", ["None reported", "At least 1 accident or damage reported"])
                clean_title = st.selectbox("Clean Title", ["Yes", "No"])
                price = st.text_input("Harga (Contoh: $25,000)", value="$0")
            
            submit_create = st.form_submit_button("Simpan Mobil Baru")
            
            if submit_create:
                if brand and model:
                    new_row = {
                        'brand': brand, 'model': model, 'model_year': int(model_year),
                        'milage': milage, 'accident': accident, 'clean_title': clean_title, 'price': price
                    }
                    # Concat ke dataframe utama
                    st.session_state.df_raw = pd.concat([df_current, pd.DataFrame([new_row])], ignore_index=True)
                    st.toast(f"Berhasil menambahkan data: {brand} {model}")
                    time.sleep(1.5)
                    st.rerun() # Refresh halaman untuk melihat update data
                else:
                    st.error("Nama Brand dan Model tidak boleh kosong!")

    # ------------------- UPDATE (UBAH DATA) -------------------
    with tab_update:
        st.write("#### Ubah Data Mobil")
        if not df_current.empty:
            # Cari data berdasarkan indeks baris
            pilihan_indeks = df_current.index
            pilihan_label = [f"Baris {i} - {df_current.loc[i, 'brand']} {df_current.loc[i, 'model']}" for i in pilihan_indeks]
            
            pilih_edit = st.selectbox("Pilih mobil yang ingin diubah:", pilihan_indeks, format_func=lambda x: pilihan_label[x])
            
            # Form untuk edit data terpilih
            with st.form("form_edit_mobil"):
                col1, col2 = st.columns(2)
                with col1:
                    edit_brand = st.text_input("Brand", value=df_current.loc[pilih_edit, 'brand'])
                    edit_model = st.text_input("Model", value=df_current.loc[pilih_edit, 'model'])
                    edit_year = st.number_input("Tahun", min_value=1980, max_value=2026, value=int(df_current.loc[pilih_edit, 'model_year']))
                with col2:
                    edit_milage = st.text_input("Milage", value=df_current.loc[pilih_edit, 'milage'])
                    
                    # Cari indeks bawaan untuk selectbox agar sesuai data lama
                    idx_acc = 0 if df_current.loc[pilih_edit, 'accident'] == "None reported" else 1
                    edit_accident = st.selectbox("Status Kecelakaan", ["None reported", "At least 1 accident or damage reported"], index=idx_acc)
                    
                    idx_title = 0 if df_current.loc[pilih_edit, 'clean_title'] == "Yes" else 1
                    edit_clean = st.selectbox("Clean Title", ["Yes", "No"], index=idx_title)
                    
                    edit_price = st.text_input("Harga", value=df_current.loc[pilih_edit, 'price'])
                
                submit_update = st.form_submit_button("Simpan Perubahan")
                
                if submit_update:
                    st.session_state.df_raw.at[pilih_edit, 'brand'] = edit_brand
                    st.session_state.df_raw.at[pilih_edit, 'model'] = edit_model
                    st.session_state.df_raw.at[pilih_edit, 'model_year'] = edit_year
                    st.session_state.df_raw.at[pilih_edit, 'milage'] = edit_milage
                    st.session_state.df_raw.at[pilih_edit, 'accident'] = edit_accident
                    st.session_state.df_raw.at[pilih_edit, 'clean_title'] = edit_clean
                    st.session_state.df_raw.at[pilih_edit, 'price'] = edit_price
                    
                    st.toast("Data berhasil diperbarui!")
                    time.sleep(1.5)
                    st.rerun()
        else:
            st.info("Tidak ada data untuk diubah.")

    # ------------------- DELETE (HAPUS DATA) -------------------
    with tab_delete:
        st.write("#### Hapus Data Mobil")
        if not df_current.empty:
            pilihan_indeks_del = df_current.index
            pilihan_label_del = [f"Baris {i} - {df_current.loc[i, 'brand']} {df_current.loc[i, 'model']}" for i in pilihan_indeks_del]
            
            pilih_hapus = st.selectbox("Pilih mobil yang ingin dihapus:", pilihan_indeks_del, format_func=lambda x: pilihan_label_del[x], key="del_box")
            
            konfirmasi = st.checkbox(f"Saya yakin ingin menghapus data Baris {pilih_hapus}")
            submit_delete = st.button("Hapus Permanen", type="primary")
            
            if submit_delete:
                if konfirmasi:
                    # Hapus baris data dan reset indeksnya agar tidak error saat diakses kembali
                    st.session_state.df_raw = df_current.drop(pilih_hapus).reset_index(drop=True)
                    st.toast("Data berhasil dihapus!")
                    time.sleep(1.5)
                    st.rerun()
                else:
                    st.error("Silakan centang kotak konfirmasi terlebih dahulu!")
        else:
            st.info("Tidak ada data untuk dihapus.")

    # Tampilkan preview data saat ini di bagian paling bawah halaman CRUD
    st.write("---")
    st.write("### Data Saat Ini:")
    st.dataframe(st.session_state.df_raw, use_container_width=True)

#[ (PAGE: AHP Pairwise Comparison) ]
# elif menu == 'AHP | Pairwise Comparison':
#     st.write('## AHP Pairwise Comparison')
#     st.write("#### Atur Perbandingan Berpasangan Kriteria Anda:")
    
#     criteria_keys = ['c_model_year', 'c_milage', 'c_accident', 'c_clean_title', 'c_price']
#     criteria_labels = [
#         'Model Year (Benefit)', 
#         'Milage (Cost)', 
#         'Accident (Benefit)', 
#         'Clean Title (Benefit)', 
#         'Price (Cost)'
#     ]
#     key_to_idx = {k: i for i, k in enumerate(criteria_keys)}
#     pairs = [
#         ('c_model_year', 'c_milage', 'Model Year', 'Milage', 1, 2),        # Milage > Model Year (Skala 2)
#         ('c_model_year', 'c_accident', 'Model Year', 'Accident', 1, 4),    # Accident > Model Year (Skala 4)
#         ('c_model_year', 'c_clean_title', 'Model Year', 'Clean Title', 0, 2),# Model Year > Clean Title (Skala 2)
#         ('c_model_year', 'c_price', 'Model Year', 'Price', 1, 5),         # Price > Model Year (Skala 5)
#         ('c_milage', 'c_accident', 'Milage', 'Accident', 1, 2),            # Accident > Milage (Skala 2)
#         ('c_milage', 'c_clean_title', 'Milage', 'Clean Title', 0, 3),      # Milage > Clean Title (Skala 3)
#         ('c_milage', 'c_price', 'Milage', 'Price', 1, 3),                 # Price > Milage (Skala 3)
#         ('c_accident', 'c_clean_title', 'Accident', 'Clean Title', 0, 5),  # Accident > Clean Title (Skala 5)
#         ('c_accident', 'c_price', 'Accident', 'Price', 1, 2),             # Price > Accident (Skala 2)
#         ('c_clean_title', 'c_price', 'Clean Title', 'Price', 1, 6)         # Price > Clean Title (Skala 6)
#     ] 
#     with st.expander("Isi Nilai Perbandingan Berpasangan Kriteria", expanded=True):
#         col_left, col_right = st.columns(2)
#         for idx, (k1, k2, l1, l2, def_idx, def_skala) in enumerate(pairs):
#             target_col = col_left if idx < 5 else col_right
#             with target_col:
#                 st.markdown(f"**Perbandingan {idx+1}: {l1} vs {l2}**")
#                 c1, c2 = st.columns(2)
#                 with c1:
#                     lp = st.selectbox("Mana yang lebih penting?", [l1, l2], index=def_idx, key=f"lp_p_{k1}_{k2}")
#                 with c2:
#                     sk = st.slider("Skala Kepentingan (1-9):", 1, 9, value=def_skala, key=f"sk_p_{k1}_{k2}")
#                 st.write("---")
                
#     st.info("Catatan: Untuk AHP Pairwise Comparison, jumlah alternatif dibatasi (misal 5 sampel mobil teratas) " \
#     "agar matriks perbandingan alternatif dapat dihitung dan ditampilkan step-by-step.")
#     num_alternatif = st.slider('Jumlah sampel mobil untuk AHP Murni:', min_value=3, max_value=20, value=5)
    
#     if st.button('Mulai Perhitungan Pairwise Comparison Murni', key='btn_pairwise'):
#         st.success('Perhitungan berhasil dijalankan.')
        
#         # BAGIAN KRITERIA
#         # STEP 1: Matriks Perbandingan Kriteria
#         st.write("### [1. BAGIAN KRITERIA]")
#         st.write("#### Step 1.1: Matriks Perbandingan Berpasangan Kriteria")
#         n_crit = len(criteria_keys)
#         A_crit = np.ones((n_crit, n_crit))
        
#         for k1, k2, l1, l2, _, _ in pairs:
#             i = key_to_idx[k1]
#             j = key_to_idx[k2]
#             lp = st.session_state[f"lp_p_{k1}_{k2}"]
#             sk = st.session_state[f"sk_p_{k1}_{k2}"]
#             val = float(sk) if lp == l1 else 1.0 / float(sk)
#             A_crit[i, j] = val
#             A_crit[j, i] = 1.0 / val
            
#         df_crit_matrix = pd.DataFrame(A_crit, index=criteria_labels, columns=criteria_labels)
#         df_crit_matrix_show = df_crit_matrix.copy()
#         df_crit_matrix_show.loc['TOTAL KOLOM'] = df_crit_matrix_show.sum(axis=0)
#         st.table(df_crit_matrix_show)
        
#         # #### STEP 1.2: Normalisasi Kriteria & Bobot Kriteria
#         st.write("#### Step 1.2: Normalisasi Matriks Kriteria & Bobot Kriteria (Rata-rata Baris)")
#         crit_col_sums = A_crit.sum(axis=0)
#         A_crit_norm = A_crit / crit_col_sums
#         crit_weights = A_crit_norm.mean(axis=1)
        
#         df_crit_norm = pd.DataFrame(A_crit_norm, index=criteria_labels, columns=criteria_labels)
#         df_crit_norm['Bobot Kriteria (W)'] = crit_weights
#         st.table(df_crit_norm)
        
#         # #### STEP 1.3: Uji Konsistensi Rasio Kriteria
#         st.write("#### Step 1.3: Uji Konsistensi Kriteria")
#         lambda_max = np.sum(crit_col_sums * crit_weights)
#         CI = (lambda_max - n_crit) / (n_crit - 1)
#         # RI = 1.12 # Nilai RI untuk n=5
#         # CR = CI / RI if RI != 0 else 0
#         RI = {
#             2: 0.00, 3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45,
#             10: 1.51, 11: 1.53, 12: 1.54, 13: 1.56, 14: 1.57
#         }
#         CR = CI / RI[n_crit] if RI[n_crit] != 0 else 0
        
#         c1, c2, c3 = st.columns(3)
#         c1.metric("λ max", f"{lambda_max:.4f}")
#         c2.metric("CI", f"{CI:.4f}")
#         c3.metric("CR", f"{CR:.4f}")
#         if CR < 0.1:
#             st.success(f"Logika Kriteria KONSISTEN karena nilai $CR < 0.1$ ({CR:.4f} < 0.1). Hasil perhitungan valid.")
#         else:
#             st.warning(f"Logika Kriteria TIDAK KONSISTEN karena nilai $CR \ge 0.1$ ({CR:.4f} $\ge$ 0.1). Disarankan mengatur ulang skala perbandingan.")

#         # BAGIAN ALTERNATIF
#         st.write("### [2. BAGIAN ALTERNATIF]")
        
#         # ambil sampel data alternatif
#         df_sample = df_clean.head(num_alternatif).copy()
#         alt_names = [f"{row['brand']} {row['model']} ({idx})" for idx, row in df_sample.iterrows()]
#         n_alt = len(alt_names)
        
#         rekap_bobot_alt = np.zeros((n_alt, n_crit))
        
#         for c_idx, k_key in enumerate(criteria_keys):
#             st.write(f"#### Step 2.{c_idx+1}: Perbandingan Alternatif pada Kriteria **{criteria_labels[c_idx]}**")
            
#             A_alt = np.ones((n_alt, n_alt))
#             is_cost = 'Cost' in criteria_labels[c_idx]
            
#             for i in range(n_alt):
#                 for j in range(n_alt):
#                     val_i = df_sample.iloc[i][k_key]
#                     val_j = df_sample.iloc[j][k_key]
                    
#                     val_i = 0.001 if val_i == 0 else val_i
#                     val_j = 0.001 if val_j == 0 else val_j
                    
#                     if not is_cost:
#                         A_alt[i, j] = val_i / val_j
#                     else:
#                         A_alt[i, j] = val_j / val_i
            
#             df_a_alt = pd.DataFrame(A_alt, index=alt_names, columns=alt_names)
#             df_a_alt_show = df_a_alt.copy()
#             df_a_alt_show.loc['TOTAL KOLOM'] = df_a_alt_show.sum(axis=0)
#             st.caption(f"Matriks Perbandingan Berpasangan Alternatif - {criteria_labels[c_idx]}")
#             st.table(df_a_alt_show)
            
#             alt_col_sums = A_alt.sum(axis=0)
#             A_alt_norm = A_alt / alt_col_sums
#             alt_weights = A_alt_norm.mean(axis=1)
            
#             rekap_bobot_alt[:, c_idx] = alt_weights
            
#             df_a_alt_norm = pd.DataFrame(A_alt_norm, index=alt_names, columns=alt_names)
#             df_a_alt_norm['Bobot Lokal'] = alt_weights
#             st.caption(f"Matriks Normalisasi & Bobot Lokal Alternatif - {criteria_labels[c_idx]}")
#             st.table(df_a_alt_norm)
#             st.write("---")
            
#         # REKAP BOBOT & SKOR AKHIR
#         st.write("### [3. BAGIAN AKHIR: REKAP BOBOT & SKOR AKHIR]")
#         st.write("#### Step 3.1: Tabel Rekapitulasi Bobot Alternatif")
        
#         df_rekap = pd.DataFrame(rekap_bobot_alt, index=alt_names, columns=criteria_labels)
#         st.table(df_rekap)
        
#         st.write("#### Step 3.2: Hasil Perhitungan Skor Akhir (Rekap Bobot $\times$ Bobot Kriteria)")
#         skor_akhir = np.dot(rekap_bobot_alt, crit_weights)
        
#         df_final = pd.DataFrame({
#             'Alternatif Mobil': alt_names,
#             'Skor Akhir AHP': skor_akhir
#         })
#         # tabel hasil akhir
#         df_final_sorted = df_final.sort_values(by='Skor Akhir AHP', ascending=False).reset_index(drop=True)
#         df_final_sorted.index = df_final_sorted.index + 1
#         df_final_sorted.index.name = 'Rank'
#         st.dataframe(df_final_sorted, use_container_width=True)

#         # grafik hasil
#         fig, ax = plt.subplots(figsize=(8, 4))
#         bars = ax.barh(df_final_sorted['Alternatif Mobil'], df_final_sorted['Skor Akhir AHP'], color='lightgreen', edgecolor='black')
#         ax.invert_yaxis()
#         ax.set_xlabel('Skor Akhir')
#         ax.set_title('Rekomendasi Akhir AHP Murni')
#         ax.bar_label(bars, fmt='%.4f', padding=5)
#         st.pyplot(fig)

#          # download button
#         csv = df_final_sorted.to_csv(index=False).encode('utf-8')
#         st.download_button(label='Unduh Hasil Akhir', data=csv, file_name='hasil_ahp_pairwise_comparison.csv', mime="text/csv")

#[ (PAGE: AHP Absolute Measurement) ]
elif menu == 'AHP | Absolute Measurement':
    st.write('## AHP Absolute Measurement')
    st.write("#### Langkah 1: Input Perbandingan Berpasangan Antar Kriteria")
    st.caption("Tentukan tingkat kepentingan relatif antar kriteria menggunakan skala Saaty (1-9).")
    
    criteria_keys = ['c_model_year', 'c_milage', 'c_accident', 'c_clean_title', 'c_price']
    criteria_labels = [
        'Model Year (Benefit)', 
        'Milage (Cost)', 
        'Accident (Benefit)', 
        'Clean Title (Benefit)', 
        'Price (Cost)'
    ]
    key_to_idx = {k: i for i, k in enumerate(criteria_keys)}
    pairs = [
        ('c_model_year', 'c_milage', 'Model Year', 'Milage', 1, 2),        # Milage sedikit lebih penting (Skala 2)
        ('c_model_year', 'c_accident', 'Model Year', 'Accident', 1, 4),    # Accident lebih penting (Skala 4)
        ('c_model_year', 'c_clean_title', 'Model Year', 'Clean Title', 0, 2),# Model Year sedikit lebih penting (Skala 2)
        ('c_model_year', 'c_price', 'Model Year', 'Price', 1, 5),         # Price jauh lebih penting (Skala 5)
        ('c_milage', 'c_accident', 'Milage', 'Accident', 1, 2),            # Accident sedikit lebih penting (Skala 2)
        ('c_milage', 'c_clean_title', 'Milage', 'Clean Title', 0, 3),      # Milage lebih penting (Skala 3)
        ('c_milage', 'c_price', 'Milage', 'Price', 1, 3),                 # Price lebih penting (Skala 3)
        ('c_accident', 'c_clean_title', 'Accident', 'Clean Title', 0, 5),  # Accident jauh lebih penting (Skala 5)
        ('c_accident', 'c_price', 'Accident', 'Price', 1, 2),             # Price sedikit lebih penting (Skala 2)
        ('c_clean_title', 'c_price', 'Clean Title', 'Price', 1, 6)         # Price mutlak lebih penting (Skala 6)
    ]
    
    with st.expander("Isi Nilai Perbandingan Berpasangan Kriteria", expanded=True):
        col_left, col_right = st.columns(2)
        for idx, (k1, k2, l1, l2, def_idx, def_skala) in enumerate(pairs):
            target_col = col_left if idx < 5 else col_right
            with target_col:
                st.markdown(f"**Perbandingan {idx+1}: {l1} vs {l2}**")
                c1, c2 = st.columns(2)
                with c1:
                    # Menggunakan parameter 'index' untuk menentukan pilihan default [l1, l2]
                    lp = st.selectbox("Mana yang lebih penting?", [l1, l2], index=def_idx, key=f"lp_{k1}_{k2}")
                with c2:
                    # Menggunakan parameter 'value' untuk menentukan nilai default slider
                    sk = st.slider("Skala Kepentingan:", 1, 9, value=def_skala, key=f"sk_{k1}_{k2}")
                st.write("---")              
    max_baris = st.number_input('Batasi jumlah baris data yang dihitung: ', min_value=10, max_value=len(df_clean), value=500)
    if st.button('Mulai Perhitungan'):
        st.success('Perhitungan berhasil dijalankan.')

        # STEP 1: Matriks Perbandingan Berpasangan Kriteria
        st.write("#### Step 1: Matriks Perbandingan Berpasangan Kriteria ($A$)")
        n = len(criteria_keys) # banyak kriteria
        A = np.ones((n, n))
        
        for k1, k2, l1, l2, _, _ in pairs:
            i = key_to_idx[k1]
            j = key_to_idx[k2]
            lp = st.session_state[f"lp_{k1}_{k2}"]
            sk = st.session_state[f"sk_{k1}_{k2}"]
            
            val = float(sk) if lp == l1 else 1.0 / float(sk)
            A[i, j] = val
            A[j, i] = 1.0 / val
            
        df_matrix = pd.DataFrame(A, index=criteria_labels, columns=criteria_labels)
        df_matrix_show = df_matrix.copy()
        df_matrix_show.loc['TOTAL KOLOM'] = df_matrix_show.sum(axis=0)
        st.table(df_matrix_show)
        
        # STEP 2: Normalisasi Matriks & Mencari Bobot Kriteria
        st.write("#### Step 2: Normalisasi Matriks Kriteria & Perhitungan Bobot Prioritas ($wK$)")
        col_sums = A.sum(axis=0) # axis=0 -> kolom
        A_norm = A / col_sums
        # bobot prioritas
        weights = A_norm.mean(axis=1) # axis=1 -> baris
        
        df_norm = pd.DataFrame(A_norm, index=criteria_labels, columns=criteria_labels)
        df_norm['Bobot Prioritas (wK)'] = weights
        st.table(df_norm)
        
        # STEP 3: Uji Consistency Ratio (CR)
        st.write("#### Step 3: Uji Konsistensi Logika Kriteria (Consistency Ratio Check)")
        # menghitung CV
        CV = np.dot(A, weights)
        hasil_CV = CV /weights
        # nilai eigen
        lambda_max = np.mean(hasil_CV)
        CI = (lambda_max - n) / (n - 1)
        RI = {
            2: 0.00, 3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45,
            10: 1.51, 11: 1.53, 12: 1.54, 13: 1.56, 14: 1.57
        }
        CR = CI / RI[n] if RI[n] != 0 else 0
        
        c_m1, c_m2, c_m3 = st.columns(3)
        c_m1.metric("Eigenvalue Maksimum ($\lambda_{max}$)", f"{lambda_max:.4f}")
        c_m2.metric("Consistency Index (CI)", f"{CI:.4f}")
        c_m3.metric("Consistency Ratio (CR)", f"{CR:.4f}")
        
        if CR < 0.1:
            st.success(f"Logika Kriteria KONSISTEN karena nilai $CR < 0.1$ ({CR:.4f} < 0.1). Hasil perhitungan valid.")
        else:
            st.warning(f"Logika Kriteria TIDAK KONSISTEN karena nilai $CR \ge 0.1$ ({CR:.4f} $\ge$ 0.1). Disarankan mengatur ulang skala perbandingan.")
            
        # pisahkan bobot kriteria untuk perhitungan alternatif
        b_year, b_milage, b_accident, b_clean_title, b_price = weights
        
        # STEP 4: Normalisasi Nilai Absolut Alternatif
        st.write("#### Step 4: Normalisasi Nilai Alternatif (Absolute Measurement Scale)")
        st.caption("[BENEFIT] diukur absolut dengan: $x / max(x)$")
        st.caption("[[COST] diukur absolut dengan: $min(x) / x$")
        
        df_batas = df_clean.head(max_baris).copy()
        
        # proses rating/pengukuran absolut
        df_batas['n_year'] = df_batas['c_model_year'] / df_batas['c_model_year'].max()
        df_batas['n_milage'] = df_batas['c_milage'].min() / df_batas['c_milage']
        
        max_accident = df_batas['c_accident'].max() if df_batas['c_accident'].max() > 0 else 1
        df_batas['n_accident'] = df_batas['c_accident'] / max_accident
        
        max_clean_title = df_batas['c_clean_title'].max() if df_batas['c_clean_title'].max() > 0 else 1
        df_batas['n_clean_title'] = df_batas['c_clean_title'] / max_clean_title
        
        df_batas['n_price'] = df_batas['c_price'].min() / df_batas['c_price']
        
        st.dataframe(df_batas[['brand', 'model', 'n_year', 'n_milage', 'n_accident', 'n_clean_title', 'n_price']].head(max_baris), use_container_width=True)
        
        # STEP 5: Perhitungan Skor Akhir
        st.write("#### Step 5: Perhitungan Skor Akhir AHP")
        st.caption("Rumus: $\sum$ (Nilai Absolut Alternatif * Bobot Hasil Pairwise Kriteria)")
        
        df_batas['skor_AHP'] = (
            df_batas['n_year'] * b_year +
            df_batas['n_milage'] * b_milage +
            df_batas['n_accident'] * b_accident +
            df_batas['n_clean_title'] * b_clean_title +
            df_batas['n_price'] * b_price
        )
        # tabel hasil akhir
        st.write("#### Tabel Hasil Akhir Rekomendasi Mobil Bekas Terbaik")
        df_hasil = df_batas[['brand', 'model', 'model_year', 'milage', 'accident', 'clean_title', 'price', 'skor_AHP']]
        df_hasil_sorted = df_hasil.sort_values(by='skor_AHP', ascending=False).reset_index(drop=True)
        df_hasil_sorted.index = df_hasil_sorted.index + 1
        df_hasil_sorted.index.name = 'Rank'
        st.dataframe(df_hasil_sorted, use_container_width=True)
        
        # grafik hasil
        st.write("### Grafik Hasil Akhir Rekomendasi Mobil Bekas Terbaik")
        df_top10 = df_hasil_sorted.head(10).copy()
        df_top10['Label_X'] = [f"#{i} {b} {m}" for i, b, m in zip(range(1, 11), df_top10['brand'], df_top10['model'])]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        batang = ax.bar(df_top10['Label_X'], df_top10['skor_AHP'], color='skyblue', edgecolor='black')
        ax.set_ylim(df_top10['skor_AHP'].min() - 0.02, df_top10['skor_AHP'].max() + 0.01)
        ax.set(ylabel='Skor Akhir AHP', title='Top 10 Mobil Berdasarkan Skor AHP Absolute Terbaik')
        ax.set_xticklabels(df_top10['Label_X'], rotation=45, ha='right')        
        ax.bar_label(batang, fmt='%.3f', padding=3, fontsize=9)        
        plt.tight_layout()
        st.pyplot(fig)

        # download button
        csv = df_hasil_sorted.to_csv(index=False).encode('utf-8')
        st.download_button(label='Unduh Hasil Akhir', data=csv, file_name='hasil_ahp_absolute.csv', mime="text/csv")

#[ (PAGE: Profil Kelompok) ]
elif menu == 'Profil Kelompok':
    st.write('## Profil Kelompok')
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info('- Dimas Proboningrat \n - 123220211')
    with col2:
        st.info('- Desta Fondria \n - 123240028')
    with col3:
        st.info('- Rabbani \n - 123240099')
