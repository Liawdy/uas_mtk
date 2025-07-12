import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog

# ============================
# Konfigurasi Halaman
# ============================
st.set_page_config(page_title="Optimasi Produksi", layout="centered")
st.title("📈 Optimasi Produksi Sepatu & Tas (Linear Programming)")

# ============================
# Studi Kasus dan Rumus
# ============================
st.markdown("## 📚 Studi Kasus")
st.markdown("""
PT **Prima Citra Indonesia** memproduksi **Sepatu (X)** dan **Tas (Y)** untuk memperoleh keuntungan maksimum.  
Perusahaan memiliki keterbatasan dalam:
- ⏱ Waktu produksi
- 🧱 Bahan baku
- 👷 Tenaga kerja

### 🎯 Fungsi Tujuan
""")
st.latex(r"Z = c_1 X + c_2 Y")

st.markdown("### ⛓️ Kendala Produksi")
st.latex(r"""
\begin{cases}
a_1 X + a_2 Y \leq \text{Waktu Maks} \\
b_1 X + b_2 Y \leq \text{Bahan Baku Maks} \\
t_1 X + t_2 Y \leq \text{Tenaga Kerja Maks} \\
X \geq 0,\quad Y \geq 0
\end{cases}
""")

st.markdown("### 📘 Keterangan:")
st.markdown("""
- \( X \), \( Y \) = Jumlah sepatu & tas yang diproduksi  
- \( c_1 \), \( c_2 \) = Keuntungan per unit  
- \( a, b, t \) = Koefisien waktu, bahan, tenaga kerja  
""")

# ============================
# Input Data Interaktif
# ============================
st.markdown("## 📥 Masukkan Parameter Produksi")

col1, col2 = st.columns(2)
with col1:
    c1 = st.number_input("Keuntungan per Sepatu (Rp)", value=40000)
    a1 = st.number_input("Waktu per Sepatu (jam)", value=2)
    b1 = st.number_input("Bahan Baku per Sepatu (unit)", value=1)
    t1 = st.number_input("Tenaga Kerja per Sepatu (jam)", value=1)
with col2:
    c2 = st.number_input("Keuntungan per Tas (Rp)", value=30000)
    a2 = st.number_input("Waktu per Tas (jam)", value=1)
    b2 = st.number_input("Bahan Baku per Tas (unit)", value=1)
    t2 = st.number_input("Tenaga Kerja per Tas (jam)", value=2)

st.markdown("### 🔒 Kapasitas Maksimum:")
waktu_maks = st.number_input("Total Waktu Tersedia (jam)", value=100)
bahan_maks = st.number_input("Total Bahan Baku Tersedia (unit)", value=80)
tenaga_maks = st.number_input("Total Tenaga Kerja Tersedia (jam)", value=90)

# ============================
# Linear Programming
# ============================
st.markdown("## 🧮 Solusi Linear Programming")

c = [-c1, -c2]  # karena linprog = minimisasi
A = [
    [a1, a2],  # waktu
    [b1, b2],  # bahan
    [t1, t2]   # tenaga
]
b = [waktu_maks, bahan_maks, tenaga_maks]

res = linprog(c, A_ub=A, b_ub=b, bounds=[(0, None), (0, None)], method='highs')

if res.success:
    x_opt, y_opt = res.x
    z_opt = -res.fun

    st.success("✅ Solusi Optimal Ditemukan:")
    st.write(f"Jumlah Sepatu (X): {x_opt:.2f} unit")
    st.write(f"Jumlah Tas (Y): {y_opt:.2f} unit")
    st.write(f"Total Keuntungan Maksimum: Rp {z_opt:,.0f}")

    # ============================
    # Visualisasi Grafik
    # ============================
    st.markdown("## 📊 Visualisasi Area Feasible")

    x_vals = np.linspace(0, max(x_opt * 1.5, 100), 200)
    y1 = (waktu_maks - a1 * x_vals) / a2
    y2 = (bahan_maks - b1 * x_vals) / b2
    y3 = (tenaga_maks - t1 * x_vals) / t2

    fig, ax = plt.subplots()
    ax.plot(x_vals, y1, label="Waktu", color="blue")
    ax.plot(x_vals, y2, label="Bahan Baku", color="green")
    ax.plot(x_vals, y3, label="Tenaga Kerja", color="orange")

    y_min = np.minimum.reduce([y1, y2, y3])
    ax.fill_between(x_vals, y_min, 0, where=(y_min >= 0), color='lightblue', alpha=0.3)

    ax.scatter(x_opt, y_opt, color='red', label="Solusi Optimal", zorder=5)
    ax.set_xlabel("Jumlah Sepatu (X)")
    ax.set_ylabel("Jumlah Tas (Y)")
    ax.set_title("Area Feasible Produksi")
    ax.legend()
    ax.set_xlim(left=0)
    ax.set_ylim(bottom=0)
    ax.grid(True)

    st.pyplot(fig)
else:
    st.error("❌ Solusi tidak ditemukan. Periksa kembali input kendala.")

