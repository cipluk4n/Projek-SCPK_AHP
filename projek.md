**Data dari dataset csv dari internet (tema bebas)**
Minimal: 250 baris data dan 5 kriteria

**Untuk AHP visualisasi data analitik (grafik) cukup minimal 1 saja (grafik hasil akhir), >1 lebih bagus**
Boleh pakai matplotlib, seaborn, dll   

**Fitur yang harus ada:**
1. Navigasi Layout: Sidebar/Tabs untuk Memisahkan Halaman
   - Ex: hal_data, hal_hitungSPK, hal_profilKelompok
2. Dataset mentah dalam bentuk tabel interaktif (st.dataframe)
3. Input Bobot Dinamis: Input widget interaktif  (Slider, Number Input, atau Selectbox) 
   - agar user bisa mengubah bobot kriteria atau memilih alternatif.
4. Tombol eksekusi: memulai proses perhitungan SPK (st.button)
   - menampilkan keseluruhan proses perhitungan
5. Menampilkan tabel hasil akhir di-sorting dari yang tertinggi (1st) ke terendah

# Hard Filter
Brand, Model, Fuel Type, Engine Type, Transmission, Exterior Color, Interior Color

# AHP
- Model Year (benefit): more big number = more new
- Milage (cost): more big number = more used
- Accident History (benefit): if 1 is None Reporter, else 0.01 is others  -> not using 0 because dont want to break alternatif calculation 
- Clean Title (benefit): if 1 is Yes, else 0.01 is No
- Price (cost): more price = more money