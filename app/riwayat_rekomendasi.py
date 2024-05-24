import streamlit as st
import mysql.connector
import pandas as pd
from mysql.connector import Error

def riwayat_rekomendasi():
    st.title('Riwayat Rekomendasi Page')
    st.write('Welcome to the Riwayat Rekomendasi Page!')
    
    # Koneksi ke database MySQL
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="db_rekomendasi"
    )
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM riwayat_rekomendasi")
    result = mycursor.fetchall()

    columns = [i[0] for i in mycursor.description]
    df = pd.DataFrame(result, columns=columns)
    st.write(df)
    st.markdown(df.to_html(index=False), unsafe_allow_html=True)
    
    # Variabel Streamlit untuk mendapatkan input dari pengguna
    style_desain_preference = st.multiselect(
        "Pilih preferensi style desain:", 
        ["American Classic", "Tradisional", "Modern", "Industrial", "Alam"], 
        key='style_desain'
    )
    makna_warna_preference = st.multiselect(
        "Pilih preferensi makna warna:", 
        ["Suci", "Kekuatan", "Keceriaan", "Keberanian", "Keagungan", "Santai", "Ketenangan", "Kenyamanan", "Kerendahan hati", "Kewanitaan", "Kejantanan", "Kehangatan"], 
        key='makna_warna'
    )
    sifat_preference = st.multiselect(
        "Pilih preferensi sifat:", 
        ["Panas", "Hangat", "Dingin"], 
        key='sifat'
    )
    usia_pengguna_preference = st.multiselect(
        "Pilih preferensi usia pengguna:", 
        ["Anak-anak (5-11 tahun)", "Remaja (12-25 tahun)", "Dewasa (26-45 tahun)", "Lansia (<45 tahun)"], 
        key='usia_pengguna'
    )
    warna_dasar_preference = st.multiselect(
        "Pilih preferensi warna dasar:", 
        ["Putih", "Hitam", "Merah", "Kuning", "Biru"], 
        key='warna_dasar'
    )

    # Fungsi untuk menyimpan data ke dalam database MySQL
    def save_to_db(style_desain, makna_warna, sifat, usia_pengguna, warna_dasar):
        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='db_rekomendasi'
            )
            if conn.is_connected():
                cursor = conn.cursor()
                
                # Membuat tabel jika belum ada
                cursor.execute('''
                CREATE TABLE IF NOT EXISTS riwayat_baru (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    style_desain TEXT,
                    makna_warna TEXT,
                    sifat TEXT,
                    usia_pengguna TEXT,
                    warna_dasar TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                    
                )
                ''')
                
                # Memasukkan data ke dalam tabel
                cursor.execute('''
                INSERT INTO riwayat_baru (style_desain, makna_warna, sifat, usia_pengguna, warna_dasar)
                VALUES (%s, %s, %s, %s, %s)
                ''', (', '.join(style_desain), ', '.join(makna_warna), ', '.join(sifat), ', '.join(usia_pengguna), ', '.join(warna_dasar)))
                
                conn.commit()
        except Error as e:
            st.error(f"Error: {e}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    # Tombol untuk menyimpan data
    if st.button('Simpan Preferensi'):
        save_to_db(style_desain_preference, makna_warna_preference, sifat_preference, usia_pengguna_preference, warna_dasar_preference)
        st.success('Preferensi berhasil disimpan ke dalam database.')
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM riwayat_baru")
    result = mycursor.fetchall()

    columns = [i[0] for i in mycursor.description]
    df = pd.DataFrame(result, columns=columns)
    st.write(df)
    st.markdown(df.to_html(index=False), unsafe_allow_html=True)
