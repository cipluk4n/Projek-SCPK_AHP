import matplotlib as plt
import numpy as np
import pandas as pd
import streamlit as st

st.header("Pemilihan Mobil Bekas Menggunakan Metode AHP (Analytical Hierarchy Process)", text_alignment="center")
# st.divider()
tab1, tab2, tab3, tab4, tab5 = st.tabs(['Profil Kelompok', 'Pengertian', 'Data Mobil Bekas', 'Perhitungan', 'Hasil'])
with tab1:
    st.subheader("Kelompok 15 ~ AHP", text_alignment="center")
    # st.subheader("Pemilihan Mobil Bekas Menggunakan AHP")
    with st.container(border=True):  
        st.text("123240099 - Rabbani")
        st.text("123240099 - Desta")
        st.text("123240099 - Dimas")
with tab2:
    st.text("Pengertian Singkkat Metode AHP")
with tab3:
    # st.header("Data Mobil Bekas")
    df = pd.read_csv('used_cars.csv')
    st.dataframe(df)
with tab4:
    
    #TODO: buat matriks perbandingan antar kriteria  
    #TODO: normalisasi matriks perbandigan
    #TODO: mencari bobot baris kriteria (rata-rata dari setiap baris matriks)
    #TODO: mencari CV (perkalian matriks antara matriks perbandingan awal dengan matriks bobot baris kriteria)
    #TODO: menghitung nilai eigen (rata-rata CV)
    #TODO: menghitung nilai CI: (nilai eigen-jumlahKriteria)/(jumlahKriteria-1)
    #TODO: menghitung nilai CR: CI/RI, RI(random index) didapat dari standar ketetapan nilai RI
    #TODO: decision (apakah nilai CR <=0.1) jika iya berarti konsisten dan valid dipakai
    #TODO: rekap bobot alternatif
    #TODO: perhitungan bobot akhir (perkalian matriks rekap bobot alternatif dengan bobot baris kriteria)
    #TODO: perangkingan (dari yang paling baik)

    with st.expander("Evaluasi Bobot Kriteria"):
        st.text("Matriks Perbandingan Berpasangan Kriteria")
        st.text("Normalisasi dan Perhitungan Bobot")
        st.text("Matriks Perbandingan Setelah Normalisasi")
        st.text("Bobot Kriteria")
        st.text("Uji Validitas Bobot")
    with st.expander("Evaluasi Alternatif Tiap Kriteria"):
        st.text("Kriteria Satu")
        st.text("Kriteria Dua")
        st.text("Kriteria ...")
    with st.expander("Perangkingan Akhir"):
        st.text("Matriks Rekap Bobot ALternatif (W_total)")
        st.text("Bobot Akhir Tiap Alternatif")
    if st.button("Mulai Perhitungan"):
        st.write("nanti hasilnya ditaruh di tab hasil")    
with tab5:
    st.write("diisi hasilnya")
    st.text("Alternatif terbaik")

