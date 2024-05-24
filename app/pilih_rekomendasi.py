import streamlit as st
import pandas as pd
import os

def pilih_rekomendasi():
    st.title('Pilih Rekomendasi Warna')

    # Fungsi untuk merekomendasikan warna
    def recommend_color(color_database, style_desain_preference, makna_warna_preference, sifat_preference, usia_pengguna_preference, warna_dasar_preference):
        recommendations = []
        for item in color_database:
            style_desain_score = calculate_score(style_desain_preference, item[1])
            makna_warna_score = calculate_score(makna_warna_preference, item[2])
            sifat_score = calculate_score(sifat_preference, item[3])
            usia_pengguna_score = calculate_score(usia_pengguna_preference, item[4])
            warna_dasar_score = calculate_score(warna_dasar_preference, item[5])
            
            total_score = (0.35 * style_desain_score +
                        0.25 * makna_warna_score +
                        0.25 * sifat_score +
                        0.1 * usia_pengguna_score +
                        0.05 * warna_dasar_score)
            
            recommendations.append((item[0], total_score))
        
        recommendations.sort(key=lambda x: x[1], reverse=True)
        
        return recommendations

    # Fungsi untuk menghitung skor preferensi
    def calculate_score(user_preference, item_attribute):
        if isinstance(item_attribute, list):
            num_values = len(item_attribute)
            match_count = sum(1 for value in item_attribute if value in user_preference)
            return match_count / num_values if num_values > 0 else 0
        else:
            return 1 if item_attribute in user_preference else 0


    # Membaca data dari file CSV
    color_data = pd.read_csv("data/kombinasi_warna.csv")

    # Konversi data menjadi list of tuples
    color_database = color_data.values.tolist()

    # Membuat dua kolom dengan lebar yang sama
    col1, col2 = st.columns(2)
    # Menambahkan konten ke dalam kolom pertama
    col1.subheader("Masukkan Preferensi")
    
    # Meminta input dari pengguna untuk preferensi mereka
    style_desain_preference = col1.multiselect("Pilih preferensi style desain:", ["American Classic", "Tradisional", "Modern", "Industrial", "Alam"])
    makna_warna_preference = col1.multiselect("Pilih preferensi makna warna:", ["Suci", "Kekuatan", "Keceriaan", "Keberanian", "Keagungan", "Santai", "Ketenangan", "Kenyamanan", "Kerendahan hati", "Kewanitaan", "Kejantanan", "Kehangatan"])
    sifat_preference = col1.multiselect("Pilih preferensi sifat:", ["Panas", "Hangat", "Dingin"])
    usia_pengguna_preference = col1.multiselect("Pilih preferensi usia pengguna:", ["Anak-anak (5-11 tahun)", "Remaja (12-25 tahun)", "Dewasa (26-45 tahun)", "Lansia (<45 tahun)"])
    warna_dasar_preference = col1.multiselect("Pilih preferensi warna dasar:", ["Putih", "Hitam", "Merah", "Kuning", "Biru"])

    # Initialize session state
    if 'has_cari_rekomendasi' not in st.session_state:
        st.session_state.has_cari_rekomendasi = False
    if 'daftar_rekomendasi' not in st.session_state:
        st.session_state.daftar_rekomendasi = []

    if col1.button('Cari Rekomendasi'):
        # Set state has_cari_rekomendasi menjadi True
        st.session_state.has_cari_rekomendasi = True

    if st.session_state.has_cari_rekomendasi:   
        # Menambahkan konten ke dalam kolom kedua
        col2.subheader("Hasil Rekomendasi")
        # Mendapatkan rekomendasi
        recommendations = recommend_color(color_database, style_desain_preference, makna_warna_preference, sifat_preference, usia_pengguna_preference, warna_dasar_preference)

        # Memilih lima rekomendasi tertinggi
        top_recommendations = recommendations[:5]

        # Menampilkan rekomendasi
        col2.text("Top 5 Rekomendasi Pemilihan Rekomendasi Warna:")

        # Tampilkan rekomendasi
        for i, (nama_warna, score) in enumerate(top_recommendations, start=1):
            col2.text(f"Rekomendasi {i}: {nama_warna} (Skor: {score})")

            # Memisahkan kombinasi warna dengan tanda '&'
            warna_terpisah = [warna.strip() for warna in nama_warna.split('&')]
            
            # Membuat dua kolom untuk menampilkan gambar bersebelahan
            cols = col2.columns(2)
            
            # Menambahkan gambar ke dalam kolom
            for col, warna in zip(cols, warna_terpisah):
                path_to_color_image = os.path.join("data", "warna", f"{warna}.jpg")
                if os.path.exists(path_to_color_image):
                    col.image(path_to_color_image, caption=warna, use_column_width=True)
                else:
                    col.warning(f"Image for {warna} not found!")

        # Tampilkan opsi untuk memilih satu pilihan
        pilihan = ['Pilihan 1', 'Pilihan 2', 'Pilihan 3', 'Pilihan 4', 'Pilihan 5']
        index_rekomendasi = col1.radio("Pilih satu opsi:", pilihan, key="options")  # Beri key untuk widget ini
        if col1.button('Simpan Rekomendasi'):
            selected_rekomendasi = st.session_state.daftar_rekomendasi[int(index_rekomendasi[-1])-1]
            col1.text(selected_rekomendasi)  # Menampilkan rekomendasi yang dipilih

        # Tampilkan daftar rekomendasi setelah rekomendasi selesai ditampilkan
        col2.text("Daftar Rekomendasi:")
        col2.text(st.session_state.daftar_rekomendasi)
