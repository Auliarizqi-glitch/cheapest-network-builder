# Cheapest Network Builder

## 1. Deskripsi Proyek

Cheapest Network Builder merupakan aplikasi berbasis web untuk membangun jaringan dengan total panjang minimum menggunakan algoritma Minimum Spanning Tree (MST). Aplikasi ini menerapkan algoritma Kruskal untuk memilih koneksi dengan bobot terkecil tanpa membentuk siklus sehingga seluruh simpul dapat terhubung dengan total panjang minimum.

Proyek ini menggunakan dataset jaringan jalan Surabaya. Graf dimodelkan sebagai graf tak berarah, dengan simpul merepresentasikan titik jaringan, sisi merepresentasikan koneksi yang dapat digunakan, dan bobot sisi berupa panjang koneksi dalam meter.

Aplikasi menyediakan visualisasi jaringan interaktif, perhitungan MST, fitur perubahan panjang koneksi, perbandingan hasil MST sebelum dan sesudah perubahan, validasi hasil, serta estimasi biaya berdasarkan tarif simulasi.

Estimasi biaya dihitung dengan mengalikan total panjang jaringan dengan tarif simulasi per meter. Tarif tersebut merupakan asumsi untuk keperluan simulasi dan bukan harga pemasangan aktual.

## 2. Tujuan Proyek

1. Memodelkan jaringan menggunakan teori graf.
2. Menentukan Minimum Spanning Tree menggunakan algoritma Kruskal.
3. Menampilkan jaringan dan hasil MST melalui visualisasi interaktif.
4. Mengamati pengaruh perubahan panjang koneksi terhadap struktur MST.
5. Membandingkan koneksi yang masuk dan keluar dari MST setelah perubahan.
6. Menghitung total panjang jaringan dan estimasi biaya berdasarkan tarif simulasi.
7. Memvalidasi hasil MST berdasarkan keterhubungan, jumlah sisi, ketiadaan siklus, dan konsistensi perhitungan total panjang.

## 3. Model Graf

Jaringan dimodelkan menggunakan graf tak berarah berbobot, yaitu \(G=(V,E)\), dengan:

- \(V\): himpunan simpul yang merepresentasikan titik jaringan.
- \(E\): himpunan sisi yang merepresentasikan koneksi kandidat.
- \(w(e)\): bobot sisi berupa panjang koneksi dalam meter.

Tujuan perhitungan adalah menentukan Minimum Spanning Tree yang menghubungkan seluruh simpul dengan total panjang minimum.

Total panjang MST dihitung dengan menjumlahkan panjang seluruh sisi terpilih:

\[
L_{\mathrm{MST}}=\sum_{e\in T}w(e)
\]

dengan \(T\) merupakan himpunan sisi yang terpilih dalam MST.

Estimasi biaya pemasangan dihitung menggunakan:

\[
C_{\mathrm{MST}}=L_{\mathrm{MST}}\times r
\]

dengan \(r\) merupakan tarif simulasi pemasangan per meter.

**Batas interpretasi:** hasil minimum hanya berlaku pada daftar koneksi kandidat yang digunakan dalam simulasi. Hambatan fisik, kapasitas kabel, kondisi lapangan, dan biaya pemeliharaan belum diperhitungkan.

## 4. Teknologi yang Digunakan

- **Python:** bahasa pemrograman untuk menjalankan logika aplikasi dan perhitungan.
- **Streamlit:** membangun antarmuka aplikasi web interaktif.
- **NetworkX:** memodelkan graf dan membantu perhitungan MST.
- **Pandas:** membaca dan mengolah dataset.
- **Plotly:** menampilkan visualisasi jaringan secara interaktif.

## 5. Struktur File

```text
cheapest-network-builder/
├── main.py
├── main_backup.py
├── Surabaya_Edgelist.csv
├── README.md
└── bukti_pengujian/
    ├── 01_tampilan_awal.png
    ├── 02_perubahan_bobot.png
    ├── 03_hasil_mst.png
    └── 04_validasi.png
```

Keterangan:

- `main.py`: kode utama aplikasi interaktif.
- `main_backup.py`: kode cadangan untuk pengolahan graf dan perhitungan MST.
- `Surabaya_Edgelist.csv`: dataset jaringan jalan Surabaya.
- `README.md`: dokumentasi proyek.
- `bukti_pengujian/`: folder dokumentasi berupa tangkapan layar hasil pengujian.

Nama file gambar pada struktur di atas merupakan contoh. Sesuaikan dengan nama screenshot yang benar-benar disimpan.

## 6. Instalasi dan Cara Menjalankan

### 6.1 Persyaratan

Pastikan Python sudah terpasang pada komputer dan seluruh file proyek berada dalam satu folder yang sesuai.

### 6.2 Instalasi pustaka

Buka terminal pada folder proyek, kemudian jalankan perintah:

```bash
pip install pandas networkx streamlit plotly
```

### 6.3 Menjalankan aplikasi

Jalankan perintah berikut:

```bash
python -m streamlit run main.py
```

Aplikasi akan terbuka melalui browser. Jika browser tidak terbuka secara otomatis, ikuti alamat lokal yang ditampilkan pada terminal oleh Streamlit.

Pastikan file `Surabaya_Edgelist.csv` tersedia pada lokasi yang digunakan oleh kode aplikasi.

## 7. Algoritma Kruskal

Algoritma Kruskal digunakan untuk menentukan Minimum Spanning Tree dengan memilih sisi berdasarkan bobot terkecil dan menghindari pembentukan siklus.

Tahapan algoritma:

1. Mengurutkan sisi berdasarkan bobot dari yang terkecil.
2. Memeriksa sisi satu per satu berdasarkan urutan bobot.
3. Memilih sisi apabila penambahannya tidak membentuk siklus.
4. Menolak sisi yang membentuk siklus.
5. Mengulangi proses hingga seluruh simpul terhubung dan MST memiliki tepat \(n-1\) sisi, dengan \(n\) merupakan jumlah simpul.
6. Menjumlahkan bobot seluruh sisi terpilih untuk memperoleh total panjang MST.

Pada aplikasi ini, perubahan panjang suatu koneksi akan digunakan sebagai bobot terbaru dalam perhitungan ulang MST. Hasilnya kemudian dibandingkan dengan MST awal untuk mengetahui perubahan koneksi yang terpilih.

## 8. Fitur Aplikasi

1. **Visualisasi jaringan:** menampilkan simpul, koneksi kandidat, dan koneksi terpilih dalam MST.
2. **Ringkasan jaringan:** menampilkan jumlah simpul, jumlah koneksi kandidat, jumlah sisi MST, total panjang MST, dan estimasi biaya.
3. **Ubah panjang koneksi:** memungkinkan pengguna mengubah panjang salah satu koneksi kandidat.
4. **Hitung ulang MST:** menjalankan kembali perhitungan Kruskal berdasarkan panjang koneksi terbaru.
5. **Perbandingan MST:** menampilkan koneksi yang masuk atau keluar dari MST dibandingkan kondisi awal.
6. **Reset bobot:** mengembalikan panjang koneksi ke kondisi awal.
7. **Legenda visualisasi:** membedakan simpul, sisi MST, dan koneksi kandidat lainnya.
8. **Validasi MST:** memeriksa keterhubungan graf, jumlah sisi, ketiadaan siklus, dan konsistensi total panjang.
9. **Estimasi biaya:** menghitung perkiraan biaya berdasarkan total panjang MST dan tarif simulasi per meter.

## 9. Skenario Pengujian

### 9.1 Uji Coba 1: Kondisi Awal Jaringan

**Tujuan:** Mengetahui hasil pembentukan MST sebelum dilakukan perubahan panjang koneksi.

**Langkah pengujian:**

1. Menjalankan aplikasi Cheapest Network Builder.
2. Mengamati visualisasi jaringan awal.
3. Memeriksa jumlah simpul dan koneksi kandidat.
4. Mencatat total panjang MST dan estimasi biaya.
5. Memeriksa hasil validasi MST.

**Hasil aktual:**

Berdasarkan tampilan awal aplikasi, jaringan yang diuji memiliki 15 simpul dan 27 koneksi kandidat. MST yang ditampilkan terdiri atas 14 sisi dengan total panjang 11.002,94 meter dan estimasi biaya Rp550.146.925.

Hasil validasi menunjukkan bahwa graf awal terhubung, MST terhubung, jumlah sisi MST sama dengan jumlah simpul dikurangi satu, MST tidak memiliki siklus, dan perhitungan total panjang dinyatakan konsisten.

### 9.2 Uji Coba 2: Perubahan Panjang Koneksi

**Tujuan:** Mengamati pengaruh perubahan panjang koneksi terhadap struktur MST dan estimasi biaya jaringan.

**Langkah pengujian:**

1. Memilih koneksi kandidat `100445 — 100453`.
2. Mencatat panjang awal koneksi sebesar 1.869,49 meter.
3. Mengubah panjang koneksi menjadi 3.000 meter.
4. Menerapkan perubahan untuk menghitung ulang MST.
5. Mengamati visualisasi jaringan dan panel perbandingan MST.
6. Memeriksa koneksi yang masuk dan keluar dari MST.
7. Memeriksa kembali hasil validasi.

**Hasil aktual:**

Setelah panjang koneksi `100445 — 100453` diubah dari 1.869,49 meter menjadi 3.000 meter, aplikasi menampilkan perubahan struktur MST.

Koneksi `100445 — 100453` keluar dari MST, sedangkan koneksi `100453 — 100457` dengan panjang 1.869,49 meter masuk ke MST. Perubahan tersebut ditampilkan pada panel perbandingan MST dan divisualisasikan melalui perubahan warna koneksi.

Pada tampilan setelah perubahan, total panjang MST masih tercatat sebesar 11.002,94 meter dan estimasi biaya sebesar Rp550.146.925. Nilai total tersebut perlu dipastikan kembali menggunakan hasil perhitungan terbaru karena koneksi yang masuk dan keluar memiliki panjang yang sama pada tampilan aplikasi.

Hasil validasi yang ditampilkan aplikasi tetap menunjukkan bahwa graf awal terhubung, MST terhubung, jumlah sisi MST sama dengan jumlah simpul dikurangi satu, MST tidak memiliki siklus, dan perhitungan total panjang konsisten.

### 9.3 Analisis Hasil Pengujian

Perubahan panjang koneksi dapat memengaruhi urutan pemilihan sisi dalam algoritma Kruskal. Ketika suatu koneksi menjadi lebih panjang, koneksi lain dapat menggantikannya apabila menghasilkan jaringan yang lebih pendek tanpa membentuk siklus.

Perubahan struktur MST tidak selalu menyebabkan perubahan total panjang. Apabila sisi yang masuk memiliki panjang yang sama dengan sisi yang keluar, total panjang dapat tetap sama. Namun, total panjang dan estimasi biaya perlu diperiksa berdasarkan seluruh sisi MST terbaru untuk memastikan konsistensi hasil perhitungan.

## 10. Validasi Hasil

Aplikasi menyediakan pemeriksaan untuk memastikan bahwa hasil MST memenuhi karakteristik pohon rentang minimum.

Validasi yang dilakukan meliputi:

1. **Graf awal terhubung:** memastikan jaringan kandidat yang digunakan dapat menghubungkan seluruh simpul.
2. **MST terhubung:** memastikan semua simpul tetap terhubung setelah pemilihan sisi.
3. **Jumlah sisi MST:** memastikan MST memiliki tepat \(n-1\) sisi.
4. **Tidak ada siklus:** memastikan sisi terpilih tidak membentuk siklus.
5. **Konsistensi total panjang:** memeriksa kesesuaian total panjang dengan penjumlahan bobot sisi terpilih.

Pada pengujian yang dilakukan, seluruh pemeriksaan tersebut ditampilkan dengan status berhasil oleh aplikasi.

## 11. Pertanyaan Presentasi

**Mengapa turunnya biaya satu sambungan belum tentu mengubah pohon terpilih?**

Penurunan biaya satu sambungan tidak selalu mengubah MST karena pemilihan sisi tetap bergantung pada keseluruhan struktur graf dan bobot sisi lainnya. Jika perubahan bobot tidak mengubah keputusan pemilihan sisi oleh algoritma Kruskal, MST dapat tetap sama. Sebaliknya, jika perubahan bobot mengubah urutan pemilihan atau membuat alternatif yang lebih menguntungkan, struktur MST dapat berubah.

## 12. Bukti Pengujian

Tangkapan layar hasil pengujian disimpan dalam folder `bukti_pengujian/` dan digunakan untuk mendokumentasikan:

1. Tampilan awal aplikasi dan jaringan kandidat.
2. Proses perubahan panjang koneksi.
3. Hasil perbandingan MST setelah perubahan.
4. Hasil validasi MST.

Bukti tersebut menunjukkan pelaksanaan pengujian terhadap fitur utama aplikasi Cheapest Network Builder.

## 13. Kesimpulan

Cheapest Network Builder merupakan aplikasi interaktif untuk memodelkan jaringan dan menentukan Minimum Spanning Tree menggunakan algoritma Kruskal. Aplikasi menyediakan visualisasi graf, perubahan panjang koneksi, perhitungan ulang MST, perbandingan koneksi yang masuk dan keluar, estimasi biaya, serta validasi hasil.

Melalui dua skenario pengujian, pengguna dapat mengamati bahwa perubahan panjang suatu koneksi dapat mengubah struktur MST. Hasil akhir perlu tetap diperiksa melalui validasi dan penjumlahan bobot seluruh sisi terpilih.

Estimasi biaya yang ditampilkan merupakan hasil simulasi berdasarkan tarif per meter yang ditentukan pengguna, bukan harga pemasangan aktual. Model juga belum memperhitungkan hambatan fisik, kapasitas kabel, kondisi lapangan, dan biaya pemeliharaan.