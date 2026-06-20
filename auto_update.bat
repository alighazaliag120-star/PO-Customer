@echo off
echo [1/2] Menarik PO dari email...
python fetch_po.py

echo [2/2] Mengupload ke GitHub...
git add .
git commit -m "Auto-update: %date% %time%"
git push origin main

echo.
echo Selesai! Email sudah ditarik dan data sudah update di web.
pause