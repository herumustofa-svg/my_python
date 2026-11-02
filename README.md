# 🛡️ Sistem Deteksi Berita Hoaks IndoBERT & Explainable AI (XAI)

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io)
[![Python Version](https://img.shields.io/badge/Python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12%20%7C%203.14-blue.svg)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?logo=pytorch&logoColor=white)](https://pytorch.org/)
[![HuggingFace Transformers](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Transformers-yellow)](https://huggingface.co/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Aplikasi web cerdas untuk **verifikasi dan deteksi disinformasi/hoaks pada teks berita daring berbahasa Indonesia**. Mengombinasikan arsitektur Transformer **IndoBERT** dengan teknik interpretasi **Explainable Artificial Intelligence (XAI)** untuk transparansi dan akuntabilitas keputusan model.

Proyek ini dikembangkan untuk keperluan riset akademik, tesis Magister (S2), dan verifikasi literasi digital.

---

## ✨ Fitur Unggulan

- **🚀 Dual Engine Inferensi**:
  - **⚡ Mode Hybrid XAI & Leksikal (Cepat & Responsif):** Berbasis 150+ indikator gaya bahasa, tanda baca sensasional, huruf kapital (*all-caps screaming*), dan entitas institusional kredibel (Kemenkes, BPOM, BMKG, CekFakta). Siap pakai seketika tanpa unduhan model ratusan MB.
  - **🤖 Mode Deep Learning IndoBERT (PyTorch):** Terintegrasi dengan model pretrained Hugging Face (`indobenchmark/indobert-base-p1`, `indolem/indobertweet-base-uncased`) atau checkpoint lokal hasil fine-tuning sendiri (`./saved_model/`).
- **🔍 Explainability & Transparansi Token (XAI)**:
  - **Text Highlighting Berbobot:** Menyorot kata-kata pemicu hoaks (<span style="color:red">Merah</span>) dan kata-kata penguat validitas (<span style="color:green">Hijau</span>) dengan saturasi warna sesuai bobot kontribusinya.
  - **Filter Interaktif:** Menampilkan semua kata, hanya pemicu hoaks, atau hanya penguat validitas.
- **📊 Visualisasi Interaktif Plotly**:
  - **Speedometer Gauge Meter:** Menampilkan persentase indeks risiko hoaks (0% - 100%) dengan ambang batas (*threshold*) yang dapat disesuaikan secara real-time.
  - **Diverging Horizontal Bar Chart:** Grafik 12 kata paling berpengaruh terhadap keputusan klasifikasi lengkap dengan nilai kontribusi numerik.
  - **Statistik Karakteristik Linguistik:** Analisis tingkat sensasionalisme, kepadatan tanda baca emosional, dan rujukan lembaga resmi.
- **📥 Ekspor Laporan Riset / Tesis**:
  - Simpan dan unduh rekapitulasi pengujian dalam format **JSON** dan **Markdown** untuk dokumentasi atau lampiran naskah ilmiah.
- **🌐 Portal Rujukan Cek Fakta**:
  - Tautan langsung ke kanal verifikasi resmi: TurnBackHoax.id (Mafindo), CekFakta.com, dan Aduan Konten Kominfo RI.

---

## 📁 Struktur Direktori Repository

```text
Deteksi-Berita-Hoaks/
├── .streamlit/
│   └── config.toml          # Konfigurasi tema dan server Streamlit
├── app.py                   # Entrypoint server (Streamlit Cloud & Local)
├── deteksi.py               # Kode utama aplikasi, logika XAI & antarmuka
├── requirements.txt         # Daftar pustaka Python yang dibutuhkan
├── .gitignore               # Daftar file yang diabaikan oleh Git
└── README.md                # Dokumentasi lengkap proyek
```

---

## 💻 Panduan Instalasi & Menjalankan Lokal

### 1. Clone Repository dari GitHub

```bash
git clone https://github.com/herumustofa-svg/my_python.git
cd my_python
```

### 2. Buat & Aktifkan Virtual Environment (Direkomendasikan)

- **Windows (PowerShell):**
  ```powershell
  python -m venv .venv
  .venv\Scripts\Activate.ps1
  ```
- **Linux / macOS:**
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

### 3. Install Dependensi

```bash
pip install -r requirements.txt
```

### 4. Jalankan Aplikasi

Anda dapat menjalankan melalui `app.py` atau `deteksi.py`:

```bash
streamlit run app.py
```
atau:
```bash
streamlit run deteksi.py
```

Buka peramban (browser) di `http://localhost:8501`.

---

## ☁️ Panduan Deploy ke Streamlit Community Cloud (Gratis)

1. Push repositori ini ke akun GitHub Anda:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: IndoBERT Hoax Detection with XAI"
   git branch -M main
   git remote add origin https://github.com/herumustofa-svg/my_python.git
   git push -u origin main
   ```
2. Kunjungi [share.streamlit.io](https://share.streamlit.io/) dan login menggunakan akun GitHub Anda.
3. Klik tombol **"New app"**.
4. Pilih:
   - **Repository:** `herumustofa-svg/my_python`
   - **Branch:** `main`
   - **Main file path:** `app.py` atau `deteksi.py`
5. Klik **"Deploy!"** dan aplikasi Anda akan aktif secara publik di internet dalam beberapa saat!

---

## 🛠️ Integrasi Checkpoint Model Fine-Tuning Sendiri

Jika Anda memiliki bobot model IndoBERT hasil pelatihan sendiri (misalnya dari Google Colab / Kaggle):

1. Buat folder bernama `saved_model` di dalam direktori proyek:
   ```text
   Deteksi-Berita-Hoaks/
   ├── saved_model/
   │   ├── config.json
   │   ├── model.safetensors  (atau pytorch_model.bin)
   │   ├── tokenizer_config.json
   │   └── vocab.txt
   ```
2. Jalankan aplikasi Streamlit.
3. Di panel samping (sidebar), pilih **"🤖 PyTorch IndoBERT Transformer"** dan pilih **"Checkpoint Lokal (./saved_model/)"**.

---

## 📝 Sitasi & Riset Akademik

Jika Anda menggunakan repositori ini untuk penelitian, tesis, atau publikasi ilmiah, Anda dapat mengutip format berikut:

```bibtex
@misc{mustofa2026deteksihoaks,
  author = {Heru Mustofa},
  title = {Sistem Deteksi Berita Hoaks Berbahasa Indonesia Berbasis IndoBERT dan Explainable Artificial Intelligence (XAI)},
  year = {2026},
  publisher = {GitHub},
  howpublished = {\url{https://github.com/herumustofa-svg/}}
}
```

---

## 📄 Lisensi

Proyek ini dilisensikan di bawah [MIT License](LICENSE) - bebas digunakan untuk kepentingan edukasi, penelitian, dan pengembangan lanjutan.
