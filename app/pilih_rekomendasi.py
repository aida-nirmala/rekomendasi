import streamlit as st
import pandas as pd

def pilih_rekomendasi():
    st.title('Pilih Rekomendasi Warna')
    # st.write('Pilih Sesuai Preferensi')

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
        
        # Menghilangkan rekomendasi warna yang hanya memiliki satu warna dasar
        recommendations = [rec for rec in recommendations if len(rec[0]) > 1]
        
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

    # st.header("Rekomendasi Warna")
    st.subheader("Masukkan Preferensi")

    # Membaca data dari file CSV
    color_data = pd.read_csv("data/kombinasi_warna.csv")

    # Konversi data menjadi list of tuples
    color_database = color_data.values.tolist()

    # Meminta input dari pengguna untuk preferensi mereka
    style_desain_preference = st.multiselect("Pilih preferensi style desain:", ["American Classic", "Tradisional", "Modern", "Industrial", "Alam"])
    makna_warna_preference = st.multiselect("Pilih preferensi makna warna:", ["Suci", "Kekuatan", "Keceriaan", "Keberanian", "Keagungan", "Santai", "Ketenangan", "Kenyamanan", "Kerendahan hati", "Kewanitaan", "Kejantanan", "Kehangatan"])
    sifat_preference = st.multiselect("Pilih preferensi sifat:", ["Panas", "Hangat", "Dingin"])
    usia_pengguna_preference = st.multiselect("Pilih preferensi usia pengguna:", ["Anak-anak (5-11 tahun)", "Remaja (12-25 tahun)", "Dewasa (26-45 tahun)", "Lansia (<45 tahun)"])
    warna_dasar_preference = st.multiselect("Pilih preferensi warna dasar:", ["Putih", "Hitam", "Merah", "Kuning", "Biru"])

    if st.button('Cari Rekomendasi'):   
        # Mendapatkan rekomendasi
        recommendations = recommend_color(color_database, style_desain_preference, makna_warna_preference, sifat_preference, usia_pengguna_preference, warna_dasar_preference)

        # Memilih lima rekomendasi tertinggi
        top_recommendations = recommendations[:5]

        # Menampilkan rekomendasi
        st.text("Top 5 Rekomendasi Pemilihan Rekomendasi Warna:")
        for i, (nama_warna, score) in enumerate(top_recommendations, start=1):
            st.text(f"Rekomendasi {i}: {nama_warna} (Skor: {score})")
            # path_to_color_image = ("data", "warna", f"{nama_warna}.png")
            # st.image(path_to_color_image, caption=nama_warna, use_column_width=True)

pilih_rekomendasi()
