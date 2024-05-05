import streamlit as st
from app.home import home
from app.pilih_rekomendasi import pilih_rekomendasi
from app.daftar_rekomendasi import daftar_rekomendasi
from app.riwayat_rekomendasi import riwayat_rekomendasi

def main():
    st.title("Aplikasi dengan Sidebar Navigasi")
    st.sidebar.title('Navigation')
    # Pilihan sidebar
    option = st.sidebar.radio("Go to", ['Home', 'Pilih Rekomendasi', 'Daftar Rekomendasi', 'Riwayat Rekomendasi'])

    # Konten utama
    if option == "Home":
        home()
    elif option == "Pilih Rekomendasi":
        pilih_rekomendasi()
    elif option == 'Daftar Rekomendasi':
        daftar_rekomendasi()

    elif option == 'Riwayat Rekomendasi':
        riwayat_rekomendasi()
        

if __name__ == "__main__":
    main()
