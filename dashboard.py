import streamlit as st
import os
import pandas as pd

# 1. KONFIGURASI HALAMAN WAJIB PALING ATAS
st.set_page_config(page_title="Pencari PO", page_icon="📦")

# 2. FUNGSI UNTUK MEMUAT CSS
def local_css(file_name):
    # Cek apakah file style.css ada supaya tidak error di cloud
    if os.path.exists(file_name):
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Panggil fungsi CSS
local_css("style.css")

st.title("📦 Pencarian Cepat PO")

# 3. PATH DINAMIS (Bisa jalan di Lokal dan Streamlit Cloud)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FOLDER_PO = os.path.join(BASE_DIR, "data_po")

# Pengecekan apakah folder data_po sudah ada
if not os.path.exists(FOLDER_PO):
    st.error("⚠️ Folder 'data_po' belum ditemukan. Jika di Streamlit Cloud, pastikan foldernya sudah berhasil di-push ke GitHub!")
else:
    # --- BAGIAN PENCARIAN ---
    st.subheader("Cari PO")
    no_po = st.text_input("Masukkan nomor PO:")

    if st.button("Cari"):
        if no_po:
            file_ditemukan = None
            for nama_file in os.listdir(FOLDER_PO):
                if no_po in nama_file:
                    file_ditemukan = nama_file
                    break 
            
            if file_ditemukan:
                st.success(f"Ditemukan: {file_ditemukan}")
                with open(os.path.join(FOLDER_PO, file_ditemukan), "rb") as f:
                    st.download_button(
                        label=f"📥 Download {file_ditemukan}", 
                        data=f, 
                        file_name=file_ditemukan, 
                        mime="application/pdf"
                    )
            else:
                st.error(f"PO '{no_po}' tidak ditemukan.")
        else:
            st.warning("Masukkan nomor PO dulu!")

    st.divider() # Garis pemisah

    # --- BAGIAN LIST / SCROLLABLE TABLE ---
    st.subheader("Daftar Semua PO")

    # Ambil semua file PDF di folder
    semua_file = [f for f in os.listdir(FOLDER_PO) if f.endswith(".pdf")]

    # Buat DataFrame agar tampil jadi tabel
    if len(semua_file) > 0:
        df = pd.DataFrame(semua_file, columns=["Nama File PO"])
        # Tampilkan tabel yang bisa di-scroll
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Belum ada file PDF di dalam folder data_po.")