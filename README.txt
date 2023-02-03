SEBELUM PENGGUNAAN PROGRAM DETEKSI OSILASI
1. Pastikan telah menginstall aplikasi mosquitto untuk komunikasi data
2. Pastikan telah menginstall aplikasi MQTT Explorer
3. Pastikan telah menginstall bahasa  pemrograman  Python versi 3.8.10

CARA PENGGUNAAN PROGRAM DETEKSI OSILASI
1. Jalankan  program  TEP-mod-plant-mqtt.py  dengan menggunakan Visual 
   Studio Code, IDLE Python 3.8.10, atau environment yang lain.
2. Jalankan main.py  dan  ketikkan topic XMEAS yang ingin di-subscribe
   di terminal, sebagai contoh ketik XMEAS(9).
3. Buka Aplikasi MQTT Explorer, lalu kirim topic START_PAUSE = 1 untuk
   memulai program. 
4. Apabila ingin memberikan gangguan, lakukanlah  manipulasi  variabel 
   dengan mengubah-ubah variabel sebagai berikut:
   a. IDV(4)  = 1 atau 0
   b. IDV(14) = 1 atau 0
   c. gain_10 = -3.12 atau -1.56
   Catatan :a. Nilai 1 atau -3.12 adalah nilai untuk mengaktifkan gang-
               gUan.
            b. Nilai 0 atau -1,56 adalah nilai untuk meniadakan gangguan
5. Apabila ingin menyelesaikan program, ketik  topic  STOP  di  Aplikasi 
   MQTT  Explorer  untuk  menghentikan  simulasi  program  deteksi  dari
   TEP-mod-plant-mqtt.py
6. Tutup jendela main.py untuk menghentikan program deteksi online