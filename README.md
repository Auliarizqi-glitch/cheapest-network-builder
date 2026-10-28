Cheapest Network Builder

1. Deskripsi Proyek

Cheapest Network Builder merupakan aplikasi berbasis Python untuk menentukan jaringan koneksi dengan total panjang minimum menggunakan algoritma Kruskal. Proyek ini memodelkan permasalahan jaringan sebagai graf berbobot tak berarah.

Dataset yang digunakan adalah Surabaya_Edgelist.csv, yang memuat informasi titik awal, titik akhir, dan panjang koneksi dalam meter.

2. Tujuan Proyek

Tujuan proyek ini adalah:

Memodelkan jaringan koneksi menggunakan teori graf.

Menentukan Minimum Spanning Tree (MST) dengan algoritma Kruskal.

Menampilkan visualisasi jaringan sebelum dan sesudah perubahan panjang koneksi.

Mengamati perubahan koneksi yang terpilih dalam MST ketika bobot sisi diubah.

Memvalidasi hasil MST yang diperoleh.

3. Model Graf

Jaringan dimodelkan sebagai graf berbobot tak berarah dengan:

Simpul (vertex): titik atau lokasi dalam jaringan.

Sisi (edge): koneksi yang menghubungkan dua simpul.

Bobot (weight): panjang koneksi dalam meter.

Aplikasi menggunakan subgraf yang terdiri atas 15 simpul dan 27 kandidat koneksi. Karena graf terhubung, MST memiliki 14 sisi.

4. Algoritma Kruskal

Algoritma Kruskal digunakan untuk memperoleh Minimum Spanning Tree, yaitu pohon rentang yang menghubungkan seluruh simpul dengan total bobot minimum.

Langkah-langkah algoritma:

Mengurutkan seluruh sisi berdasarkan bobot dari yang terkecil.

Memilih sisi dengan bobot terkecil.

Menambahkan sisi jika tidak membentuk siklus.

Mengulangi proses hingga diperoleh sebanyak (n-1) sisi, dengan (n) merupakan jumlah simpul.

5. Teknologi yang Digunakan

Python

Streamlit

Pandas

NetworkX

Plotly

6. Struktur File

cheapest-network-builder/
├── main.py
├── main_backup.py
├── requirements.txt
├── Surabaya_Edgelist.csv
├── README.md
└── bukti_pengujian/
    ├── 01_ringkasan jaringan.png.png
    ├── 02_visualisasi_awal.png.png
    ├── 03_panjang koneksi awal.png.png
    ├── 04_panjang_koneksi_setelah_diubah.png.png
    ├── 05_visualisasi_setelah_diubah.png.png
    ├── 06_perbandingan_mst.png.png
    └── 07_daftar_koneksi_mst.png.png

7. Instalasi dan Cara Menjalankan

Pastikan Python telah terpasang. Buka terminal pada folder proyek, kemudian instal pustaka yang diperlukan:

python -m pip install -r requirements.txt

Jalankan aplikasi menggunakan perintah:

python -m streamlit run main.py

Aplikasi akan terbuka melalui browser lokal.

8. Fitur Aplikasi

Aplikasi Cheapest Network Builder memiliki fitur:

Menampilkan ringkasan jaringan.

Memvisualisasikan seluruh kandidat koneksi dan MST.

Menampilkan total panjang jaringan dan estimasi biaya.

Mengubah panjang koneksi melalui input yang tersedia.

Membandingkan MST sebelum dan sesudah perubahan.

Menampilkan daftar koneksi yang termasuk dalam MST.

Memeriksa validitas hasil MST.

9. Skenario Pengujian

9.1 Kondisi Awal

Hasil pengujian pada kondisi awal menunjukkan:

Jumlah simpul: 15.

Jumlah kandidat koneksi: 27.

Jumlah sisi MST: 14.

Total panjang MST: 11.002,94 meter.

Estimasi biaya: Rp550.146.925.

Estimasi biaya menggunakan tarif simulasi sebesar Rp50.000 per meter. Tarif tersebut merupakan asumsi untuk kebutuhan simulasi, bukan harga pemasangan aktual.

9.2 Perubahan Panjang Koneksi

Pengujian dilakukan dengan mengubah panjang koneksi antara simpul 100445 dan 100453 dari 1.869,49 meter menjadi 3.000 meter.

Setelah perubahan, koneksi 100445 — 100453 keluar dari MST dan koneksi 100453 — 100457 dengan panjang 1.869,49 meter masuk ke MST.

Total panjang MST tetap 11.002,94 meter karena panjang koneksi yang masuk sama dengan panjang koneksi yang sebelumnya terpilih. Oleh karena itu, estimasi biaya juga tetap Rp550.146.925.

Pengujian ini menunjukkan bahwa perubahan bobot sisi dapat mengubah susunan MST tanpa mengubah total panjang dan biaya akhirnya.

10. Validasi Hasil

Validasi dilakukan untuk memastikan bahwa hasil algoritma Kruskal memenuhi karakteristik Minimum Spanning Tree, yaitu:

Graf hasil MST terhubung.

Jumlah sisi MST sama dengan jumlah simpul dikurangi satu.

MST tidak mengandung siklus.

Total bobot MST sesuai dengan penjumlahan bobot seluruh sisi terpilih.

Berdasarkan hasil pengujian aplikasi, pemeriksaan validasi menunjukkan hasil yang sesuai dengan karakteristik MST.

11. Dokumentasi Pengujian

Dokumentasi pengujian disimpan pada folder bukti_pengujian. Folder tersebut berisi tangkapan layar ringkasan jaringan, visualisasi awal, perubahan panjang koneksi, visualisasi setelah perubahan, perbandingan MST, dan daftar koneksi MST.

12. Batasan Model

Aplikasi ini menggunakan panjang koneksi sebagai bobot untuk menentukan MST. Estimasi biaya dihitung berdasarkan tarif simulasi per meter.

Model belum memperhitungkan kondisi medan, hambatan fisik, kapasitas jaringan, perbedaan material, dan biaya pemasangan aktual. Oleh karena itu, hasil aplikasi merupakan simulasi matematis dan belum dapat dianggap sebagai rancangan pemasangan jaringan yang siap diterapkan.

13. Kesimpulan

Cheapest Network Builder berhasil memodelkan permasalahan jaringan sebagai graf berbobot tak berarah dan menentukan Minimum Spanning Tree menggunakan algoritma Kruskal. Aplikasi memungkinkan pengguna mengubah bobot koneksi dan mengamati perubahan sisi yang terpilih dalam MST.

Hasil pengujian menunjukkan bahwa perubahan bobot dapat mengubah susunan MST tanpa selalu mengubah total panjang jaringan. Aplikasi juga menyediakan visualisasi dan validasi untuk membantu memahami proses penentuan jaringan dengan total panjang minimum.
