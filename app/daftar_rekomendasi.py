import streamlit as st
import pandas as pd
import mysql.connector
from mysql.connector import Error

def daftar_rekomendasi():
    st.title('Daftar Rekomendasi Warna')

    conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='db_rekomendasi'
        )
    
    st.subheader('Data Asli')
    # Tampilkan data dari tabel database
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM data_asli")
    result = cursor.fetchall()
    
    columns = [i[0] for i in cursor.description]
    db_df = pd.DataFrame(result, columns=columns)
    st.markdown(db_df.to_html(index=False), unsafe_allow_html=True)
    
    cursor.close()
    conn.close()

    st.subheader('Data Kombinasi')
    file_path = "data/kombinasi_warna.csv"
    try:
        # Membaca file CSV menjadi DataFrame
        df = pd.read_csv(file_path)

        # Menampilkan isi DataFrame
        st.markdown(df.to_html(index=False), unsafe_allow_html=True)
    except FileNotFoundError:
        st.error("File tidak ditemukan.")
    except Exception as e:
        st.error("Terjadi kesalahan dalam membaca file CSV: {}".format(e))
