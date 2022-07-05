User Table
|id|username|password|email|pin|phone|salt|secret|activate|

user dibuat dengan table spt ini
id username password email pin phone salt secret activate

history dibuat dengan table spt ini
id datetime judul jenis nominal pengirim penerima

Cara Kerja Aplikasi
1. Menu Awal Pertama kali ada 
    >>> Login
        Di Login Disuruh Memasukkan Username dan Password 
        Bila Database User tidak ada akan diberikan Error Message
        Bila Username tidak terdaftar akan diberikan Error Message
        Bila Password salah akan diberikan Error Message
        Bila sudah mengaktifkan Google Authenticator maka akan ditanya berapa kombinasi angka di Google Authenticator tersebut
        Bila sudah 5 kali salah nomor Google Authenticator maka akan otomatis keluar dari aplikasi
        
        Ketika Sudah Bisa Login Terdapat 5 Menu
        
        ▐▐ TOP UP ▐▐
            Top Up akan menanyakan dari Bank apa ingin Top Up dan Nominal yang ingin di transfer 
        
        ▐▐ TRANSFER▐▐
            Transfer akan menanyakan nomor telefon yang ingin di transfer, jumlah nominal, deskripsi, dan PIN
            *NOTES*
                Tidak dapat mengirim ke nomor telefon sendiri, ada pengecekan dan Error Message yang diberikan bila memasukkan nomor telefon sendiri
                Tidak dapat mengirim uang yang tidak dimiliki, ada pengecekan dan Error Message yang diberikan bila memasukkan nominal yang lebih besar daripada saldo 
                Bila PIN Salah maka tidak dapat transfer
                Bila Deskripsi terlalu panjang tidak dapat melanjutkan menu transfer
        
        ▐▐ HISTORY ▐▐
            Menu History akan memberikan History Transaksi dari awal buka account hingga terakhir kalo dilengkapi dengan warna.
             warna hijau menunjukkan uang masuk, dan warna merah menunjukkan uang keluar 

        ▐▐ DOWNLOAD HISTORY ▐▐
            Menu Download History memberikan option untuk mendownload history account ke dalam bentuk Excel maupun CSV

        ▐▐ SECURITY ▐▐
            Menu Security memberikan option untuk ENABLE dan DISABLE Google Authenticator yang terhubung ke dalam aplikasi asli GA di HP yang bisa di download di Play Store
            Ketika memilih untuk ENABLE maka akan diberikan QR Code yang bisa di masukkan ke dalam GA. Kemudian Ketika Masuk ke Aplikasi akan ditanya berapa kombinasi angka yang ada di GA tersebut

        ▐▐ LOG OFF ▐▐
            Keluar Dari Aplikasi

    >>> Sign Up
        Mengambil info username password email pin phone dan memasukkan ke dalam Database

    >>> Log Off
        Keluar dari aplikasi

▐▐ SISTEM KEAMANAN ▐▐

1. Menggunakan SHA-256 di dalam mengenkripsi password. password juga diberi salt terlebih dahulu agar tidak mudah dibobol
2. Menggunakan LSFR sebagai metode untuk RNG yang digunakan untuk generate Secret GA, userid, dan juga Secret Key
3. Menggunakan AES-128 untuk mengenkripsi Database setiap kali menggunakan aplikasi dan secret key nya berubah setiap kali keluar dari aplikasi
4. Ketika Membuat Password user dipaksa untuk membuat password yang panjangnya minimal 8 huruf, terdapat minimal 1 huruf besar, dan 1 special character
5. Sudah dilengkapi dengan minimal user input length di dalam setiap kali input data dari user menggunakan regex
6. email dan nomor telefon yang digunakan sudah benar - benar valid ketika dimasukkan
