import streamlit as st
import pandas as pd

def daftar_rekomendasi():
    st.title('Daftar Rekomendasi Page')
    st.write('Welcome to the Daftar Rekomendasi Page!')

    st.write('Data Asli')
    file_path = "data/data_warna.csv"
    try:
        # Membaca file CSV menjadi DataFrame
        df = pd.read_csv(file_path)

        # Menampilkan header
        st.write("Header:", list(df.columns))

        # Menampilkan isi DataFrame
        st.write(df)
    except FileNotFoundError:
        st.error("File tidak ditemukan.")
    except Exception as e:
        st.error("Terjadi kesalahan dalam membaca file CSV: {}".format(e))

    st.write('Data Kombinasi')
    file_path = "data/kombinasi_warna.csv"
    try:
        # Membaca file CSV menjadi DataFrame
        df = pd.read_csv(file_path)

        # Menampilkan header
        st.write("Header:", list(df.columns))

        # Menampilkan isi DataFrame
        st.write(df)
    except FileNotFoundError:
        st.error("File tidak ditemukan.")
    except Exception as e:
        st.error("Terjadi kesalahan dalam membaca file CSV: {}".format(e))
