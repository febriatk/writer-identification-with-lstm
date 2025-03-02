# -*- coding: utf-8 -*-
"""2. Perancangan Data

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1BfB9Y5xDKJ4oahUUXg3JWQhGi4fAGa3n
"""

import os
import pandas as pd
import numpy as np
from google.colab import drive
drive.mount('/content/drive')

# Menyatukan File Matriks Biner dari Seluruh Citra ke dalam Satu File
def matriks_to_vektor(folder_matriks, folder_data):
    # Membuat folder untuk menyimpan file data
    if not os.path.exists(folder_data):
        os.makedirs(folder_data)

    # Membuat list untuk menyimpan semua matriks citra biner
    data_vektor_baris = []

    # Mendapatkan daftar file dari folder matriks biner
    files = os.listdir(folder_matriks)

    # Memastikan semua matriks memiliki dimensi yang sama
    dimensi = None

    for file_name in files:
        # Memeriksa apakah file adalah file excel
        if file_name.endswith('.xlsx'):
            # Membaca matriks citra biner dari file excel
            excel_path = os.path.join(folder_matriks, file_name)
            matriks_biner = pd.read_excel(excel_path, header=None).values

            # Memeriksa dimensi matriks
            if dimensi is None:
                dimensi = matriks_biner.shape
            elif matriks_biner.shape != dimensi:
                print(f"Error: Dimensi matriks pada file {file_name} tidak cocok dengan matriks lainnya")
                continue

            # Mengonversi matriks menjadi vektor baris dan menyimpannya
            vektor_baris = matriks_biner.flatten()
            data_vektor_baris.append(vektor_baris)

    # Menggabungkan semua vektor baris menjadi satu dataframe
    if data_vektor_baris:
        excel_filename = "data vektor.xlsx"
        excel_path = os.path.join(folder_data, excel_filename)
        pd.DataFrame(data_vektor_baris).to_excel(excel_path, index=False, header=False)
    else:
        print("Tidak ada file excel yang valid ditemukan dalam folder matriks biner.")

# Menambahkan Label Penulis pada File Data
def add_label(folder_data, data_file):
    # Membaca folder data
    file_name = "data vektor.xlsx"
    excel_path = os.path.join(folder_data, file_name)
    df = pd.read_excel(excel_path, header=None)

    # Mendapatkan jumlah baris dan kolom
    baris, kolom = df.shape

    # Menentukan jumlah kata per penulis dan jumlah penulis
    jml_kata = 25
    jml_penulis = baris // jml_kata

    # Membuat kolom label
    labels = []
    for penulis in range(1, jml_penulis + 1):
        labels.extend([penulis] * jml_kata)

    df['Label'] = labels

    # Menambahkan kolom label
    for i in range(1, jml_penulis + 1):
        label_column = f'L{i}'
        df[label_column] = (df['Label'] == i).astype(int)

    # Menyimpan DataFrame ke file excel
    df.to_excel(data_file, index=False)

# Membagi Data menjadi Data Pelatihan dan Data Pengujian
def bagi_train_test_data(data_file, train_data_file, test_data_file):
    # Membaca file data label
    df = pd.read_excel(data_file)

    # Mendapatkan jumlah penulis dan total data
    jml_penulis = df['Label'].nunique()
    jml_kata = df.groupby('Label').size().max()

    # Mendapatkan jumlah data untuk pelatihan dengan pembulatan ke atas
    train_data_size = int(0.8 * jml_kata) # Mengambil 70% dari jumlah kata per penulis dengan pembulatan ke atas
    # Inisialisasi DataFrame untuk data pelatihan dan pengujian
    train_data = []
    test_data = []

    # Memisahkan data untuk setiap penulis
    for i in range(1, jml_penulis + 1):
        data_penulis = df[df['Label'] == i]
        for j in range(train_data_size):
            train_data.append(data_penulis.iloc[j])
        for k in range(train_data_size, jml_kata):
            test_data.append(data_penulis.iloc[k])

    # Menambahkan data penulis ke DataFrame data pelatihan dan pengujian
    train_df = pd.DataFrame(train_data)
    test_df = pd.DataFrame(test_data)

    # Menyimpan data pelatihan dan pengujian ke file excel
    train_df.to_excel(train_data_file, index=False)
    test_df.to_excel(test_data_file, index=False)

    print("Data Pelatihan")
    print(train_df)

    print("Data Pengujian")
    print(test_df)


if __name__ == "__main__":
    folder_matriks = '/content/drive/My Drive/Skripsi/Output/MatriksBiner'
    folder_data = '/content/drive/My Drive/Skripsi/Output/Data'
    data_file = '/content/drive/My Drive/Skripsi/Output/Data/data.xlsx'
    train_data_file = '/content/drive/My Drive/Skripsi/Output/Data/datapelatihan.xlsx'
    test_data_file = '/content/drive/My Drive/Skripsi/Output/Data/datapengujian.xlsx'

    matriks_to_vektor(folder_matriks, folder_data)
    add_label(folder_data, data_file)
    bagi_train_test_data(data_file, train_data_file, test_data_file)