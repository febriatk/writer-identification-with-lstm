# -*- coding: utf-8 -*-
"""4. Pengujian LSTM

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1CWQUEp2jmfg8L_jgZo4kk5bPEE6SnU9s
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from google.colab import drive
drive.mount('/content/drive')

# Membaca Data Pelatihan
def read_train_data(test_data_file):
    # Membaca file data pelatihan
    df = pd.read_excel(test_data_file)

    print("\nData Pengujian :")
    print(df)

    return df

def load_weights_biases(filename):
    data = np.load(filename)
    Wf = data['Wf']
    Uf = data['Uf']
    bf = data['bf']
    Wi = data['Wi']
    Ui = data['Ui']
    bi = data['bi']
    Wc = data['Wc']
    Uc = data['Uc']
    bc = data['bc']
    Wo = data['Wo']
    Uo = data['Uo']
    bo = data['bo']
    Wy = data['Wy']
    by = data['by']

    print("\n\nBobot dan Bias Optimal")
    print("\nWf : ")
    print(Wf)
    print("\nUf : ")
    print(Uf)
    print("\nbf : ")
    print(bf)
    print("\nWi : ")
    print(Wi)
    print("\nUi : ")
    print(Ui)
    print("\nbi : ")
    print(bi)
    print("\nWc : ")
    print(Wc)
    print("\nUc : ")
    print(Uc)
    print("\nbc : ")
    print(bc)
    print("\nWo : ")
    print(Wo)
    print("\nUo : ")
    print(Uo)
    print("\nbo : ")
    print(bo)
    print("\nWy : ")
    print(Wy)
    print("\nby : ")
    print(by)

    return Wf, Uf, bf, Wi, Ui, bi, Wc, Uc, bc, Wo, Uo, bo, Wy, by

# Fungsi Aktivasi Sigmoid Biner
def sigm(x):
    return 1 / (1 + np.exp(-x))

# Fungsi Aktivasi Tangent Hyperbolic
def tanh(x):
    return (np.exp(x) - np.exp(-x)) / (np.exp(x) + np.exp(-x))

# Fungsi Aktivasi Softmax
def softmax(x):
    exp_x = np.exp(x - np.max(x))
    sum_exp_x = np.sum(exp_x)
    softmax = exp_x / (sum_exp_x)

    return softmax

def ins_hidd_cell_awal(jml_hidden):
    h_prev = np.zeros((1, jml_hidden))
    C_prev = np.zeros((1, jml_hidden))

    print("\nNilai h(t-1) dan C(t-1) Awal Proses Pengujian : ")
    print("\nh(t-1) : ")
    print(h_prev)
    print("\nC(t-1) : ")
    print(C_prev)

    return h_prev, C_prev

def feedforward(df, Wf, Uf, bf, Wi, Ui, bi, Wc, Uc, bc, Wo, Uo, bo, Wy, by, h_prev, C_prev):
    f_list = []
    i_list = []
    kC_list = []
    C_list = []
    o_list = []
    h_list = []
    yin_list = []
    y_list = []
    h_prev_list = [h_prev]
    C_prev_list = [C_prev]

    data_uji = df.iloc[:, :2500].to_numpy()
    for t in range(len(data_uji)):
        print(f"\nProses Feedforward untuk Data ke-{t}")
        f = sigm(np.dot(data_uji[t], Wf) + np.dot(h_prev, Uf) + bf)
        f_list.append(f)
        print(f"\nNilai f{t} : ")
        print(f)
        i = sigm(np.dot(data_uji[t], Wi) + np.dot(h_prev, Ui) + bi)
        i_list.append(i)
        print(f"\nNilai i{t} : ")
        print(i)
        kC = np.tanh(np.dot(data_uji[t], Wc) + np.dot(h_prev, Uc) + bc)
        kC_list.append(kC)
        print(f"\nNilai kC{t} : ")
        print(kC)
        C = (C_prev * f) + (kC * i)
        C_list.append(C)
        print(f"\nNilai C{t} : ")
        print(C)
        o = sigm(np.dot(data_uji[t], Wo) + np.dot(h_prev, Uo) + bo)
        o_list.append(o)
        print(f"\nNilai o{t} : ")
        print(o)
        h = o * np.tanh(C)
        h_list.append(h)
        print(f"\nNilai h{t} : ")
        print(h)
        yin = np.dot(h, Wy) + by
        yin_list.append(yin)
        print(f"\nNilai yin{t} : ")
        print(yin)
        y = softmax(yin)
        y_list.append(y)
        print(f"\nNilai y{t} : ")
        print(y)

        h_prev = h
        h_prev_list.append(h_prev)
        C_prev = C
        C_prev_list.append(C_prev)

    return f_list, i_list, kC_list, C_list, o_list, h_list, yin_list, y_list, h_prev_list, C_prev_list

def error(df, y_list):
    target_uji = df.iloc[:, 2501:].to_numpy()
    print("\nTarget Sebenarnya : ")
    print(target_uji)
    y = np.array(y_list)
    print("\nTarget Prediksi : ")
    print(y)

    E = 0
    for t in range (len(target_uji)):
        diff = target_uji[t] - y[t]
        square_diff = np.square(diff)
        E += np.sum(square_diff)
    MSE = E / (len(target_uji))
    print("\nNilai Error MSE : ", MSE)

    return MSE

def evaluate_prediction(df, y_list):
    target_uji = df.iloc[:, 2501:].to_numpy()
    print("\nPerbandingan Label Prediksi dan Sebenarnya dalam bentuk tabel:")
    comparison_table = pd.DataFrame({
        "Label Prediksi": [np.argmax(pred) + 1 for pred in y_list],
        "Label Sebenarnya": [np.argmax(target) + 1 for target in target_uji]
    })
    comparison_table["Keterangan"] = ["Benar" if pred == actual else "Salah" for pred, actual in zip(comparison_table["Label Prediksi"], comparison_table["Label Sebenarnya"])]

    print(comparison_table)

    # Menghitung dan menampilkan tingkat akurasi
    jumlah_benar = sum(comparison_table["Keterangan"] == "Benar")
    akurasi = jumlah_benar / len(target_uji) * 100
    print(f"Tingkat Akurasi: {akurasi:.2f}%")
    return comparison_table, akurasi

# Fungsi untuk visualisasi akurasi prediksi
def visualize_accuracy(comparison_table):
    # Menghitung jumlah prediksi benar dan salah
    benar = comparison_table["Keterangan"].value_counts()["Benar"]
    salah = comparison_table["Keterangan"].value_counts()["Salah"]

    # Membuat bar chart
    plt.figure(figsize=(6, 4))
    sns.barplot(x=["Benar", "Salah"], y=[benar, salah], color="blue")
    plt.title("Jumlah Prediksi Benar dan Salah")
    plt.ylabel("Jumlah")
    plt.show()

# Fungsi untuk visualisasi distribusi output model
def visualize_output_distribution(y_list):
    y_np = np.array([np.argmax(y) for y in y_list])

    plt.figure(figsize=(6, 4))
    sns.histplot(y_np, bins=np.arange(1, y_np.max()+2) - 0.5, kde=False, color="blue")
    plt.title("Distribusi Prediksi Model")
    plt.xlabel("Label Prediksi")
    plt.ylabel("Frekuensi")
    plt.show()

# Fungsi untuk visualisasi proses feedforward (nilai dari f, i, o, h)
def visualize_feedforward(f_list, i_list, o_list, h_list):
    time_steps = range(len(f_list))

    plt.figure(figsize=(10, 6))

    # Plot nilai f
    plt.subplot(2, 2, 1)
    plt.plot(time_steps, [f.mean() for f in f_list], label="f(t)", color="green")
    plt.title("Nilai f(t)")
    plt.xlabel("Time Steps")
    plt.ylabel("Nilai Rata-rata f(t)")

    # Plot nilai i
    plt.subplot(2, 2, 2)
    plt.plot(time_steps, [i.mean() for i in i_list], label="i(t)", color="blue")
    plt.title("Nilai i(t)")
    plt.xlabel("Time Steps")
    plt.ylabel("Nilai Rata-rata i(t)")

    # Plot nilai o
    plt.subplot(2, 2, 3)
    plt.plot(time_steps, [o.mean() for o in o_list], label="o(t)", color="red")
    plt.title("Nilai o(t)")
    plt.xlabel("Time Steps")
    plt.ylabel("Nilai Rata-rata o(t)")

    # Plot nilai h
    plt.subplot(2, 2, 4)
    plt.plot(time_steps, [h.mean() for h in h_list], label="h(t)", color="purple")
    plt.title("Nilai h(t)")
    plt.xlabel("Time Steps")
    plt.ylabel("Nilai Rata-rata h(t)")

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    test_data_file = '/content/drive/My Drive/Skripsi/Output/Data/data pengujian.xlsx'
    filename = '/content/drive/My Drive/Skripsi/Output/Pelatihan/bobotbiasoptimal.npz'

df = read_train_data(test_data_file)

Wf, Uf, bf, Wi, Ui, bi, Wc, Uc, bc, Wo, Uo, bo, Wy, by = load_weights_biases(filename)

h_prev, C_prev = ins_hidd_cell_awal(2500)

f_list, i_list, kC_list, C_list, o_list, h_list, yin_list, y_list, h_prev_list, C_prev_list = feedforward(df, Wf, Uf, bf, Wi, Ui, bi, Wc, Uc, bc, Wo, Uo, bo, Wy, by, h_prev, C_prev)

MSE = error(df, y_list)

comparison_table, akurasi = evaluate_prediction(df, y_list)
    visualize_accuracy(comparison_table)
    visualize_output_distribution(y_list)
    visualize_feedforward(f_list, i_list, o_list, h_list)