import matplotlib as plt
import numpy as np
import pandas as pd
import streamlit as st

st.header("Pemilihan Mobil Bekas Menggunakan Metode AHP (Analytical Hierarchy Process)", text_alignment="center")
tab1, tab2, tab3, tab4, tab5 = st.tabs(['Profil Kelompok', 'Pengertian', 'Data Mobil Bekas', 'Perhitungan', 'Hasil'])
with tab1:
    st.subheader("Kelompok 15 ~ AHP", text_alignment="center")
    # st.subheader("Pemilihan Mobil Bekas Menggunakan AHP")
    with st.container(border=True):  
        st.write("123240099 - Rabbani")
        st.write("123240099 - Desta")
        st.write("123240099 - Dimas")
with tab2:
    st.write("Pengertian Singkkat Metode AHP")
with tab3:
    # st.header("Data Mobil Bekas")
    df = pd.read_csv('used_cars.csv')
    st.dataframe(df)
with tab4:
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

