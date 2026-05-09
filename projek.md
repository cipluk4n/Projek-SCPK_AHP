**Data dari dataset csv dari internet (tema bebas)**
    Minimal: 250 baris data dan 5 kriteria

**Untuk AHP visualisasi data analitik (grafik) cukup minimal 1 saja (grafik hasil akhir), >1 lebih bagus**
    boleh pakai matplotlib, seaborn, dll   

**Fitur yang harus ada:**
    1. Navigasi Layout: Sidebar/Tabs untuk Memisahkan Halaman
       - Ex: hal_data, hal_hitungSPK, hal_profilKelompok
    2. Dataset mentah dalam bentuk tabel interaktif (st.dataframe)
    3. Input Bobot Dinamis: Input widget interaktif  (Slider, Number Input, atau Selectbox) 
        - agar user bisa mengubah bobot kriteria atau memilih alternatif.
    4. Tombol eksekusi: memulai proses perhitungan SPK (st.button)
        - menampilkan keseluruhan proses perhitungan
    5. Menampilkan tabel hasil akhir di-sorting dari yang tertinggi (1st) ke terendah
