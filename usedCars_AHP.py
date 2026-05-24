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
        st.write("123240099 - fas")
        st.write("123240099 - fas")
        st.write("123240099 - fas")
with tab2:
    st.write("Pengertian Singkkat Metode AHP")
with tab3:
    # st.header("Data Mobil Bekas")
    df = pd.read_csv('used_cars.csv')
    st.dataframe(df)
with tab4:
    st.write("")
    if st.button("Mulai Perhitungan"):
        st.write("nanti hasilnya ditaruh di tab hasil")    
with tab5:
    st.write("diisi hasilnya")

