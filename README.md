# **Physim: Platform Simulasi Fisika Interaktif**

Sebuah aplikasi desktop interaktif yang dirancang untuk membantu mahasiswa dan siswa memahami konsep-konsep fisika dasar melalui simulasi visual dan kuis adaptif. Aplikasi ini dibangun dengan Python menggunakan framework PyQt5 untuk antarmuka pengguna dan Pygame serta Pymunk untuk mesin simulasi fisika.

### **Daftar Isi**

1. [Tentang Proyek](#bookmark=id.5k7k27je5egw)  
2. [Fitur-Fitur Utama](#bookmark=id.l9wsmnbihyti)  
3. [Teknologi yang Digunakan](#bookmark=id.84pj3lu1c1yb)  
4. [Struktur Proyek](#bookmark=id.iw4w0w2op6g8)  
5. [Instalasi](#bookmark=id.ioitppqr3l5b)  
6. [Cara Menjalankan Aplikasi](#bookmark=id.8vax5ppwzuzi)  
7. [Pengembangan Lebih Lanjut](#bookmark=id.sr78uworghsx)  
8. [Lisensi](#bookmark=id.220co3wnn88g)  
9. [Kontak](#bookmark=id.ufjcuf7p26jz)

### **1\. Tentang Proyek**

Physim bertujuan untuk menjembatani kesenjangan antara teori fisika abstrak dan pemahaman visual. Dengan menyediakan simulasi interaktif untuk berbagai fenomena fisika, pengguna dapat memanipulasi parameter dan melihat dampaknya secara *real-time*. Selain itu, aplikasi ini dilengkapi dengan sistem kuis adaptif yang relevan dengan materi simulasi, mendukung proses pembelajaran yang lebih efektif.

Proyek ini dibangun dengan arsitektur modular, menjadikannya *scalable* dan mudah untuk ditambahkan materi simulasi atau fitur baru di masa mendatang.

### **2\. Fitur-Fitur Utama**

* **Sistem Akun (Login & Registrasi):** Pengguna dapat membuat akun baru atau masuk menggunakan NIM dan password. Data akun disimpan dalam file CSV (```Akun.csv```).  
* **Antarmuka Pengguna Responsif (Responsive UI):** Aplikasi dirancang untuk menyesuaikan diri dengan berbagai resolusi layar laptop, memastikan tampilan yang optimal dan proporsional.  
* **Basis Kode Modular:** Kode aplikasi dipecah menjadi beberapa modul (file Python) yang terpisah berdasarkan fungsinya, memudahkan pemeliharaan, *debugging*, dan pengembangan kolaboratif.  
* **Simulasi Fisika Interaktif:**  
  * **Gerak Lurus Berubah Beraturan (GLBB):** Simulasi objek bergerak dengan akselerasi yang dapat diatur.  
  * **Gerak Harmonik Sederhana (GHS):** Simulasi massa pada pegas dengan parameter amplitudo, konstanta pegas, dan massa yang dapat diubah.  
  * *Fitur simulasi lainnya dapat ditambahkan dengan mudah.*  
* **Kuis Adaptif:** Soal kuis secara otomatis dimuat berdasarkan materi simulasi yang sedang diakses pengguna. Soal-soal disimpan dalam file CSV terpisah per materi (misal: soal\_gl.csv, soal\_shm.csv).

### **3\. Teknologi yang Digunakan**

* **Python:** Bahasa pemrograman utama.  
* **PyQt5:** Framework GUI untuk membangun antarmuka pengguna yang kaya dan responsif.  
* **Pygame:** Library multimedia untuk menggambar dan mengelola inti simulasi visual.  
* **Pymunk:** Library fisika 2D berbasis Chipmunk, digunakan untuk simulasi fisika yang realistis dan interaktif.  
* **Modul csv (Python Standard Library):** Untuk operasi baca/tulis data dari file CSV (akun pengguna dan soal kuis).

### **4\. Struktur Proyek**

Struktur direktori proyek dirancang untuk kejelasan dan modularitas:

	your\_project\_root/  
	├── main.py                    \# Titik masuk aplikasi  
	├── config.py                  \# Konstanta konfigurasi global (warna, dll.)  
	├── widgets.py                 \# Widget GUI kustom yang dapat digunakan kembali  
	├── login\_screen.py            \# Logika dan UI untuk layar Login/Registrasi  
	├── menu\_screen.py             \# Logika dan UI untuk layar Menu Utama  
	├── material\_screens.py        \# Kelas dasar Materi dan implementasi layar simulasi (GL, SHM, dll.)  
	├── harmonic\_simulation.py     \# Logika simulasi Gerak Harmonik Sederhana (SHM)  
	├── glbb.py                    \# Logika simulasi Gerak Lurus Berubah Beraturan (GLBB)  
	├── quiz\_screen.py             \# Logika dan UI untuk layar Kuis Adaptif  
	├── source/                    \# Folder untuk file data  
	│   ├── Akun.csv               \# Data akun pengguna (NIM, Password)  
	│   ├── soal\_gl.csv            \# Soal kuis untuk Gerak Lurus  
	│   └── soal\_shm.csv           \# Soal kuis untuk Gerak Harmonik (perlu ditambahkan)  
	└── icons/                     \# Folder untuk aset ikon dan gambar  
		├── atom.png               \# Logo aplikasi  
		├── 1.png                  \# Ikon materi 1  
		└── ...                    \# Ikon materi lainnya (2.png, 3.png, dst.)

### **5\. Instalasi**

Untuk menjalankan aplikasi ini, ikuti langkah-langkah berikut:

1. **Kloning Repositori (jika ada):**  

	   git clone \[URL\_REPOSITORI\_ANDA\]  
	   cd \[NAMA\_FOLDER\_PROYEK\]

   *Jika Anda mengunduh file secara manual, pastikan struktur folder sesuai dengan yang dijelaskan di atas.*  
2. Instal Dependensi Python:  
   Buka terminal atau Command Prompt di root directory proyek Anda dan jalankan perintah:  
  
		pip install PyQt5 pygame pymunk

3. **Pastikan File Data Ada:**  
   * Pastikan ```Akun.csv```ada di folder ```source/.```.  
   * Pastikan ```soal\_gl.csv``` ada di folder ```source/.``` Jika belum ada, Anda bisa membuatnya dengan format:  
     
		 soal,a,b,c,d,correct  
		 Ini adalah soal pertama,Pilihan A,Pilihan B,Pilihan C,Pilihan D,Pilihan A

   * Untuk kuis Gerak Harmonik, buat soal\_shm.csv di folder source/ dengan format yang sama.  
4. **Pastikan Aset Ikon Ada:**  
   * Pastikan folder ```icons/``` ada di *root directory* proyek dan berisi ```atom.png serta``` ikon-ikon bernomor (```1.png``` hingga ```6.png```).

### **6\. Cara Menjalankan Aplikasi**

Setelah semua dependensi terinstal dan struktur proyek sudah benar:

1. Buka terminal atau Command Prompt.  
2. Navigasi ke *root directory* proyek Anda (misalnya, ```cd C:\\path\\to\\Physim```).  
3. Jalankan aplikasi dengan perintah:  
   python main.py

Aplikasi akan terbuka dengan layar Login.

### **7\. Pengembangan Lebih Lanjut**

Aplikasi ini dirancang untuk mudah diperluas:

* **Menambahkan Simulasi Baru:** Buat file simulasi baru (misal hukum\_newton\_sim.py), lalu buat kelas layar materi di material\_screens.py yang menggunakannya, dan tambahkan ke menu\_screen.py.  
* **Menambahkan Kuis Baru:** Cukup buat file CSV soal baru di source/ dengan format yang konsisten, lalu pastikan kelas materi memanggil quiz\_screen.Kuis dengan simulation\_type yang sesuai.

### **8\. Lisensi**

Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.

### **9\. Kontak**

Untuk pertanyaan atau kolaborasi, silakan hubungi:
* Talitha Ayunda Maritsa
	

* \[Nashr Ardy Wahyono\]  
* \[nashrardy@Gmail.com\]  
* [Linkedin](www.linkedin.com/in/nashr-ardy-wahyono)

