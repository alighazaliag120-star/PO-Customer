@echo off
echo Memulai proses auto-update ke GitHub...

:: Tambahkan semua file
git add .

:: Commit dengan pesan otomatis berisi tanggal dan jam
git commit -m "Auto-update: %date% %time%"

:: Kirim ke GitHub
git push origin main

echo.
echo Selesai! Data PO sudah terupdate di cloud.
pause