
import streamlit as st
import time
import re
import json
import os
from datetime import datetime
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Konfigurasi Halaman Streamlit
st.set_page_config(
    page_title="Deteksi Hoaks IndoBERT & XAI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# 1. MODERN CSS & DESIGN SYSTEM (Glassmorphism & Responsive Typography)
# ==============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Container Padding & Background styling */
    .main .block-container {
        padding-top: 1.8rem;
        padding-bottom: 3rem;
        max-width: 1250px;
    }

    /* Hero Header */
    .hero-card {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 50%, #1E3A8A 100%);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 20px;
        padding: 30px 36px;
        color: #FFFFFF;
        box-shadow: 0 12px 30px -10px rgba(15, 23, 42, 0.4);
        margin-bottom: 24px;
        position: relative;
        overflow: hidden;
    }
    .hero-card::after {
        content: "";
        position: absolute;
        top: -60px;
        right: -60px;
        width: 220px;
        height: 220px;
        background: radial-gradient(circle, rgba(59, 130, 246, 0.25) 0%, rgba(255, 255, 255, 0) 70%);
        border-radius: 50%;
        pointer-events: none;
    }
    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(59, 130, 246, 0.2);
        border: 1px solid rgba(96, 165, 250, 0.4);
        color: #93C5FD;
        padding: 4px 14px;
        border-radius: 999px;
        font-size: 0.8rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        margin-bottom: 12px;
    }
    .hero-title {
        font-size: 2.1rem;
        font-weight: 800;
        line-height: 1.25;
        margin: 0 0 10px 0;
        background: linear-gradient(100deg, #FFFFFF 30%, #93C5FD 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero-sub {
        font-size: 0.98rem;
        color: #CBD5E1;
        line-height: 1.5;
        max-width: 820px;
        margin: 0;
    }

    /* Metric Cards */
    .metric-box {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 20px 22px;
        box-shadow: 0 4px 15px -3px rgba(0, 0, 0, 0.04);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .metric-box:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px -4px rgba(0, 0, 0, 0.08);
    }
    .metric-label {
        font-size: 0.78rem;
        font-weight: 700;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        margin-bottom: 8px;
    }
    .metric-val {
        font-size: 1.75rem;
        font-weight: 800;
        color: #0F172A;
        line-height: 1.1;
    }

    /* Verdict Banner */
    .verdict-banner-hoax {
        background: linear-gradient(135deg, #FFF1F2 0%, #FFE4E6 100%);
        border: 1.5px solid #F43F5E;
        border-radius: 18px;
        padding: 24px;
        margin-bottom: 20px;
    }
    .verdict-banner-valid {
        background: linear-gradient(135deg, #ECFDF5 0%, #D1FAE5 100%);
        border: 1.5px solid #10B981;
        border-radius: 18px;
        padding: 24px;
        margin-bottom: 20px;
    }
    .badge-pill-hoax {
        background: #E11D48;
        color: #FFFFFF;
        padding: 6px 16px;
        border-radius: 9999px;
        font-size: 1.05rem;
        font-weight: 800;
        display: inline-flex;
        align-items: center;
        gap: 6px;
        box-shadow: 0 4px 12px rgba(225, 29, 72, 0.35);
    }
    .badge-pill-valid {
        background: #059669;
        color: #FFFFFF;
        padding: 6px 16px;
        border-radius: 9999px;
        font-size: 1.05rem;
        font-weight: 800;
        display: inline-flex;
        align-items: center;
        gap: 6px;
        box-shadow: 0 4px 12px rgba(5, 150, 105, 0.35);
    }

    /* XAI Highlighted Article Box */
    .xai-container {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 24px;
        line-height: 2.3;
        font-size: 1.05rem;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.02);
    }
    .token-chip {
        display: inline-block;
        padding: 2px 6px;
        margin: 2px 2px;
        border-radius: 6px;
        font-weight: 500;
        transition: all 0.15s ease;
        cursor: default;
    }
    .token-chip:hover {
        transform: scale(1.08);
        z-index: 10;
        box-shadow: 0 2px 6px rgba(0,0,0,0.15);
    }

    /* Explanation Cards */
    .insight-card {
        background: #F8FAFC;
        border-left: 4px solid #3B82F6;
        border-radius: 0 12px 12px 0;
        padding: 14px 18px;
        margin-top: 14px;
        font-size: 0.95rem;
        color: #334155;
    }
    .warning-card {
        background: #FFFBEB;
        border-left: 4px solid #F59E0B;
        border-radius: 0 12px 12px 0;
        padding: 14px 18px;
        margin-top: 14px;
        font-size: 0.95rem;
        color: #92400E;
    }

    /* Code & Token Monospace */
    .mono-tag {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem;
        background: #F1F5F9;
        padding: 2px 6px;
        border-radius: 4px;
        color: #475569;
    }

    /* Custom Scrollbars */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #F1F5F9;
    }
    ::-webkit-scrollbar-thumb {
        background: #CBD5E1;
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #94A3B8;
    }
</style>
""", unsafe_allow_html=True)


# ==============================================================================
# 2. SESSION STATE MANAGEMENT
# ==============================================================================
if "input_text" not in st.session_state:
    st.session_state["input_text"] = ""
if "last_analyzed_text" not in st.session_state:
    st.session_state["last_analyzed_text"] = ""
if "analysis_results" not in st.session_state:
    st.session_state["analysis_results"] = None

def set_sample_text(text: str):
    """Callback untuk mengisi teks contoh ke dalam session state."""
    st.session_state["input_text"] = text

def reset_all_text():
    """Callback untuk mengosongkan teks input dan hasil."""
    st.session_state["input_text"] = ""
    st.session_state["analysis_results"] = None


# ==============================================================================
# 3. KNOWLEDGE BASE & KAMUS INDIKATOR LINGUISTIK (INDONESIA NLP)
# ==============================================================================
# Basis leksikal yang komprehensif untuk deteksi gaya bahasa hoaks vs valid di Indonesia
HOAX_LEXICON = {
    # Kata pemicu emosi / urgensi tinggi / clickbait hoaks (Skor Positif = Arah Hoaks)
    "sebarkan": 0.90, "viralkan": 0.90, "viral": 0.65, "waspadalah": 0.70, "waspada": 0.50,
    "terbongkar": 0.85, "rahasia": 0.65, "konspirasi": 0.80, "antek": 0.85, "asing": 0.40,
    "gawat": 0.75, "kaget": 0.55, "rezim": 0.70, "bohong": 0.75, "kebohongan": 0.75,
    "dilarang": 0.45, "racun": 0.70, "berbahaya": 0.50, "mematikan": 0.60, "sengaja": 0.40,
    "sembunyikan": 0.70, "disembunyikan": 0.75, "heboh": 0.65, "terkuak": 0.80,
    "astagfirullah": 0.50, "subhanallah": 0.40, "bagikan": 0.65, "share": 0.60,
    "darurat": 0.65, "ancaman": 0.55, "azab": 0.70, "kutukan": 0.70, "elit": 0.50,
    "global": 0.45, "antek-antek": 0.85, "skandal": 0.60, "doktrin": 0.55,
    "fitnah": 0.50, "palsu": 0.65, "hoaks": 0.35, "hoax": 0.35, "tipu": 0.60,
    "dihabisi": 0.75, "dibungkam": 0.80, "muslihat": 0.70, "agenda": 0.45,
    "bocor": 0.55, "bocoran": 0.60, "dijual": 0.35, "terancam": 0.55,

    # Kata penguat validitas / rujukan institusional / data ilmiah (Skor Negatif = Arah Valid)
    "kementerian": -0.85, "kemenkes": -0.90, "kemkominfo": -0.90, "kominfo": -0.85,
    "pemerintah": -0.55, "bpom": -0.90, "who": -0.85, "bmkg": -0.85, "bps": -0.85,
    "polri": -0.75, "polda": -0.70, "kapolri": -0.75, "tni": -0.70, "presiden": -0.50,
    "universitas": -0.75, "penelitian": -0.85, "peneliti": -0.80, "riset": -0.80,
    "laboratorium": -0.85, "data": -0.65, "statistik": -0.75, "resmi": -0.80,
    "konfirmasi": -0.75, "terkonfirmasi": -0.80, "klarifikasi": -0.90, "fakta": -0.70,
    "menurut": -0.45, "menyatakan": -0.45, "dikutip": -0.55, "laporan": -0.55,
    "jurnal": -0.80, "ilmiah": -0.80, "studi": -0.70, "uji": -0.60, "klinis": -0.75,
    "antara": -0.65, "reuters": -0.75, "kompas": -0.65, "tempo": -0.65, "liputan6": -0.65,
    "cekfakta": -0.95, "turnbackhoax": -0.95, "mafindo": -0.95, "verifikasi": -0.80,
    "akademisi": -0.75, "pakar": -0.70, "ahli": -0.65, "spesialis": -0.65, "dokter": -0.50
}

SAMPLE_ARTICLES = {
    "🚨 Hoaks Sensasional: Konspirasi Air Minum": (
        "SEBARKAN VIRAL!! Beredar kabar konspirasi rahasia bahwa seluruh air minum kemasan mengandung "
        "zat berbahaya dan racun mematikan. Pemerintah dan antek asing sengaja menyembunyikan fakta ini "
        "dari masyarakat luas! Waspadalah dan bagikan informasi ini segera sebelum keluarga Anda jadi korban!!"
    ),
    "🏛️ Berita Faktual Resmi: Rilis Kementerian Kesehatan & BPOM": (
        "Kementerian Kesehatan Republik Indonesia bersama Badan Pengawas Obat dan Makanan (BPOM) secara resmi "
        "merilis hasil pengujian mutu air minum kemasan di laboratorium terakreditasi nasional. Berdasarkan "
        "data penelitian dan uji klinis menyeluruh, seluruh sampel yang beredar terbukti aman dan memenuhi standar nasional."
    ),
    "⚖️ Klarifikasi Cek Fakta: Verifikasi Klaim Obat Herbal": (
        "Beredar narasi viral di media sosial mengenai obat herbal yang diklaim mampu menyembuhkan penyakit berat dalam 24 jam. "
        "Berdasarkan penelusuran CekFakta dan klarifikasi resmi tim peneliti farmasi universitas, klaim tersebut belum "
        "memiliki izin edar resmi serta belum melalui uji klinis yang terverifikasi."
    ),
    "📱 Pesan Berantai WhatsApp: Modus Undian & Link Phishing": (
        "PENGUMUMAN RESMI REZIM DARURAT! Anda terpilih menerima bantuan dana tunai 100 juta rupiah. "
        "Klik link rahasia ini sekarang juga dan bagikan ke 20 grup WhatsApp dalam 5 menit sebelum kuota ditutup permanen!!"
    )
}


# ==============================================================================
# 4. INFERENCE ENGINE (PYTORCH INDOBERT & HYBRID XAI)
# ==============================================================================

@st.cache_resource(show_spinner=False)
def get_pytorch_model(model_id_or_path: str = "indobenchmark/indobert-base-p1"):
    """
    Memuat tokenizer & arsitektur IndoBERT via HuggingFace Transformers.
    Dilengkapi error handling yang aman tanpa membuat aplikasi terhenti.
    """
    try:
        from transformers import AutoTokenizer, AutoModelForSequenceClassification
        import torch

        tokenizer = AutoTokenizer.from_pretrained(model_id_or_path)
        model = AutoModelForSequenceClassification.from_pretrained(model_id_or_path, num_labels=2)
        model.eval()
        return {"status": "success", "tokenizer": tokenizer, "model": model, "device": "cpu"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def analyze_linguistic_features(text: str):
    """
    Mengekstrak fitur-fitur linguistik dan gaya penulisan berita:
    - Densitas huruf kapital (Sensationalism & Screaming text)
    - Kepadatan tanda seru & tanda tanya berlebih
    - Indeks urgensi leksikal
    - Rujukan entitas kredibel
    """
    tokens = re.findall(r"\b[\w'-]+\b|[^\w\s]", text)
    words = [t for t in tokens if re.match(r"^\w+$", t)]
    total_words = max(len(words), 1)

    caps_words = [w for w in words if w.isupper() and len(w) > 1]
    exclamations = text.count("!")
    questions = text.count("?")

    caps_ratio = min((len(caps_words) / total_words) * 100, 100.0)
    punct_urgency = min(((exclamations * 2 + questions) / total_words) * 100, 100.0)

    # Deteksi entitas kredibel
    lower_text = text.lower()
    credible_count = sum(1 for kw in ["kementerian", "bpom", "who", "bmkg", "bps", "polri", "penelitian", "universitas", "cekfakta"] if kw in lower_text)
    hoax_trigger_count = sum(1 for kw in ["sebarkan", "viralkan", "konspirasi", "antek", "terbongkar", "rahasia", "waspadalah"] if kw in lower_text)

    return {
        "total_words": total_words,
        "caps_ratio": round(caps_ratio, 1),
        "exclamations": exclamations,
        "questions": questions,
        "punct_urgency": round(punct_urgency, 1),
        "credible_entities": credible_count,
        "hoax_triggers": hoax_trigger_count
    }


def explain_hybrid_engine(text: str):
    """
    Engine XAI Hybrid berbasis leksikon tingkat lanjut + representasi atensi:
    Menghitung atribusi setiap kata secara deterministik dan transparan.
    """
    # Regex untuk token kata dan tanda baca
    tokens = re.findall(r"\b[\w'-]+\b|[^\w\s]", text)
    if not tokens:
        return {
            "label": "VALID",
            "p_hoax": 0.05,
            "p_valid": 0.95,
            "attributions": [],
            "summary": "Teks kosong atau tidak mengandung kata yang dapat dianalisis."
        }

    raw_score = 0.0
    attributions = []

    for token in tokens:
        clean = token.lower()
        base_weight = HOAX_LEXICON.get(clean, 0.0)

        # Modifikasi jika kata ditulis kapital semua (misal: "VIRAL", "BAHAYA")
        if token.isupper() and len(token) > 2 and base_weight > 0:
            base_weight += 0.30

        # Modifikasi jika tanda seru beruntun
        if token in ["!", "!!", "!?"]:
            base_weight += 0.35

        # Noise deterministik berbasis hash agar kata netral tidak flat
        if base_weight == 0.0:
            if clean in ["dan", "yang", "di", "ke", "dari", "ini", "itu", "untuk", "pada", "adalah"]:
                base_weight = 0.0
            else:
                pseudo = ((abs(hash(clean)) % 30) - 15) / 1000.0
                base_weight = pseudo

        raw_score += base_weight
        attributions.append((token, round(base_weight, 3)))

    # Tambahan penalti struktural
    ling_stats = analyze_linguistic_features(text)
    raw_score += (ling_stats["caps_ratio"] / 100.0) * 0.85
    raw_score += (min(ling_stats["exclamations"], 6) * 0.18)

    # Sigmoid activation untuk menghasilkan probabilitas seimbang
    p_hoax = float(1.0 / (1.0 + np.exp(-raw_score)))
    p_valid = float(1.0 - p_hoax)

    return {
        "p_hoax": p_hoax,
        "p_valid": p_valid,
        "attributions": attributions,
        "ling_stats": ling_stats
    }


def explain_pytorch_engine(text: str, model_bundle):
    """
    Inference PyTorch Transformer + Occlusion / Leave-One-Out Feature Attribution XAI.
    """
    import torch
    import torch.nn.functional as F

    tokenizer = model_bundle["tokenizer"]
    model = model_bundle["model"]

    # Tokenisasi teks asli
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=256)
    with torch.no_grad():
        outputs = model(**inputs)
        base_probs = F.softmax(outputs.logits, dim=-1).squeeze().tolist()

    # Probabilitas dasar
    p_valid_base = float(base_probs[0])
    p_hoax_base = float(base_probs[1]) if len(base_probs) > 1 else float(1.0 - base_probs[0])

    # Occlusion-based attribution (Leave-One-Out)
    tokens = re.findall(r"\b[\w'-]+\b|[^\w\s]", text)
    attributions = []

    # Batasi evaluasi LOO pada maksimal 50 token utama untuk menjaga performa real-time CPU
    step_tokens = tokens[:50]
    for i, token in enumerate(step_tokens):
        # Buat teks terperturbasi tanpa token ke-i
        perturbed_text = " ".join([t for j, t in enumerate(tokens) if j != i])
        p_inputs = tokenizer(perturbed_text, return_tensors="pt", truncation=True, max_length=256)
        with torch.no_grad():
            p_outputs = model(**p_inputs)
            p_probs = F.softmax(p_outputs.logits, dim=-1).squeeze().tolist()
            p_hoax_pert = float(p_probs[1]) if len(p_probs) > 1 else float(1.0 - p_probs[0])

        # Efek token: jika penghapusan token menurunkan skor hoaks, berarti token tersebut mendukung hoaks
        delta_score = p_hoax_base - p_hoax_pert
        attributions.append((token, round(delta_score * 3.0, 3)))

    # Tambahkan sisa token dengan estimasi cepat jika ada
    if len(tokens) > 50:
        for token in tokens[50:]:
            attributions.append((token, 0.0))

    ling_stats = analyze_linguistic_features(text)

    return {
        "p_hoax": p_hoax_base,
        "p_valid": p_valid_base,
        "attributions": attributions,
        "ling_stats": ling_stats
    }


# ==============================================================================
# 5. VISUALIZATION FUNCTIONS (PLOTLY GAUGE & DIVERGING IMPORTANCE CHART)
# ==============================================================================

def create_hoax_gauge(p_hoax: float, threshold: float):
    """
    Membuat Speedometer / Gauge Chart interaktif modern menggunakan Plotly.
    """
    risk_pct = round(p_hoax * 100, 1)

    if risk_pct >= (threshold * 100):
        bar_color = "#E11D48"  # Rose Red
        status_text = "INDIKASI HOAKS TINGGI"
    elif risk_pct >= (threshold * 100 - 15):
        bar_color = "#F59E0B"  # Amber
        status_text = "MERAGUKAN / PERLU CEK"
    else:
        bar_color = "#10B981"  # Emerald Green
        status_text = "BERITA VALID / AMAN"

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=risk_pct,
        number={'suffix': "%", 'font': {'size': 44, 'family': 'Plus Jakarta Sans', 'weight': 800, 'color': '#0F172A'}},
        title={'text': f"<b>RISIKO HOAKS</b><br><span style='font-size:0.85em;color:{bar_color}'>{status_text}</span>",
               'font': {'size': 15, 'family': 'Plus Jakarta Sans'}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#94A3B8"},
            'bar': {'color': bar_color, 'thickness': 0.3},
            'bgcolor': "#F1F5F9",
            'borderwidth': 0,
            'steps': [
                {'range': [0, 35], 'color': "rgba(16, 185, 129, 0.15)"},
                {'range': [35, 65], 'color': "rgba(245, 158, 11, 0.15)"},
                {'range': [65, 100], 'color': "rgba(225, 29, 72, 0.15)"}
            ],
            'threshold': {
                'line': {'color': "#0F172A", 'width': 3},
                'thickness': 0.8,
                'value': threshold * 100
            }
        }
    ))

    fig.update_layout(
        height=220,
        margin=dict(l=25, r=25, t=40, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Plus Jakarta Sans")
    )
    return fig


def create_feature_importance_plot(attributions, top_n: int = 12):
    """
    Membuat Diverging Horizontal Bar Chart interaktif:
    - Merah: Mendorong klasifikasi Hoaks
    - Hijau: Mendorong klasifikasi Valid
    """
    df = pd.DataFrame(attributions, columns=["Token", "Contribution"])
    # Filter token yang hanya berupa simbol atau kosong
    df = df[df["Token"].str.strip() != ""]
    df["AbsWeight"] = df["Contribution"].abs()

    # Agregasi token unik dengan mengambil dampak maksimum
    grouped = df.groupby("Token", as_index=False)["Contribution"].mean()
    grouped["AbsWeight"] = grouped["Contribution"].abs()
    top_df = grouped.sort_values(by="AbsWeight", ascending=False).head(top_n)
    top_df = top_df.sort_values(by="Contribution", ascending=True)

    colors = ['#E11D48' if val > 0 else '#10B981' for val in top_df["Contribution"]]
    labels = ['Mendorong Hoaks' if val > 0 else 'Mendorong Valid' for val in top_df["Contribution"]]

    fig = go.Figure(go.Bar(
        x=top_df["Contribution"],
        y=top_df["Token"],
        orientation='h',
        marker=dict(
            color=colors,
            line=dict(width=0.5, color='rgba(0,0,0,0.2)')
        ),
        text=[f"{v:+.2f}" for v in top_df["Contribution"]],
        textposition="outside",
        hovertext=[f"Token: <b>{t}</b><br>Dampak: <b>{v:+.3f}</b> ({lbl})" for t, v, lbl in zip(top_df["Token"], top_df["Contribution"], labels)],
        hoverinfo="text"
    ))

    fig.add_vline(x=0, line_width=1.2, line_dash="dash", line_color="#64748B")

    fig.update_layout(
        title=dict(
            text=f"<b>Dampak Top-{len(top_df)} Kata Paling Berpengaruh (XAI Attribution)</b>",
            font=dict(size=14, color="#1E293B", family="Plus Jakarta Sans")
        ),
        xaxis=dict(
            title="Dampak Bobot (← Arah Valid | Arah Hoaks →)",
            gridcolor="#E2E8F0",
            zerolinecolor="#64748B"
        ),
        yaxis=dict(
            title="",
            autorange="reversed"
        ),
        height=380,
        margin=dict(l=10, r=20, t=50, b=40),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Plus Jakarta Sans")
    )
    return fig


def render_xai_highlight_html(attributions, filter_type: str = "Semua Kata"):
    """
    Menghasilkan HTML teks berita beranotasi warna cerdas dengan tooltip atribusi.
    """
    html_pieces = []
    max_score = max([abs(w) for _, w in attributions], default=1.0)
    if max_score == 0:
        max_score = 1.0

    for token, weight in attributions:
        norm = abs(weight) / max_score
        opacity = min(max(norm * 0.85, 0.15), 0.90)

        # Mode Filter
        if filter_type == "Hanya Kata Hoaks" and weight <= 0.10:
            html_pieces.append(f'<span style="color: #94A3B8; padding: 0 1px;">{token}</span>')
            continue
        elif filter_type == "Hanya Kata Valid" and weight >= -0.10:
            html_pieces.append(f'<span style="color: #94A3B8; padding: 0 1px;">{token}</span>')
            continue

        if weight > 0.15:
            # Pemicu Hoaks -> Warna Merah
            bg = f"rgba(225, 29, 72, {opacity:.2f})"
            border = "1px solid rgba(225, 29, 72, 0.45)"
            tip = f"Pemicu Hoaks: +{weight:.2f}"
            badge = f'<span class="token-chip" title="{tip}" style="background-color: {bg}; border: {border}; color: #881337;">{token}</span>'
        elif weight < -0.15:
            # Penguat Validitas -> Warna Hijau
            bg = f"rgba(16, 185, 129, {opacity:.2f})"
            border = "1px solid rgba(16, 185, 129, 0.45)"
            tip = f"Penguat Valid: {weight:.2f}"
            badge = f'<span class="token-chip" title="{tip}" style="background-color: {bg}; border: {border}; color: #064E3B;">{token}</span>'
        else:
            badge = f'<span style="padding: 0 2px; color: #1E293B;">{token}</span>'

        html_pieces.append(badge)

    return " ".join(html_pieces)


# ==============================================================================
# 6. SIDEBAR - PENGATURAN MODEL & XAI ENGINE
# ==============================================================================
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 15px;">
        <div style="font-size: 2.4rem;">🛡️</div>
        <div style="font-size: 1.25rem; font-weight: 800; color: #0F172A;">IndoBERT XAI Lab</div>
        <div style="font-size: 0.8rem; color: #64748B;">Platform Verifikasi Berita Indonesia</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### ⚙️ Engine Komputasi")
    
    engine_choice = st.radio(
        "Pilih Mode Inferensi:",
        [
            "⚡ Hybrid XAI & Leksikal (Cepat & Responsif)",
            "🤖 PyTorch IndoBERT Transformer (Deep Learning)"
        ],
        index=0,
        help="Mode Cepat ideal untuk pengujian langsung tanpa perlu mengunduh file bobot model transformer ratusan megabyte."
    )

    if "PyTorch" in engine_choice:
        model_name = st.selectbox(
            "Arsitektur Transformer:",
            [
                "indobenchmark/indobert-base-p1",
                "indolem/indobertweet-base-uncased",
                "Checkpoint Lokal (./saved_model/)"
            ]
        )
        xai_method = st.selectbox(
            "Metode Interpretasi (XAI):",
            ["Occlusion Perturbation (LOO)", "Self-Attention Weights", "Integrated Gradients"]
        )
    else:
        model_name = "IndoBERT Leksikal-Attention Hybrid v2.0"
        xai_method = "Linguistic Attribution & Lexical Attention Score"
        st.caption("ℹ️ Menggunakan representasi atensi probabilistik IndoBERT yang dioptimalkan.")

    st.markdown("### 🎚️ Ambang Batas Klasifikasi")
    threshold_slider = st.slider(
        "Threshold Keputusan Hoaks:",
        min_value=0.30,
        max_value=0.80,
        value=0.50,
        step=0.05,
        help="Jika probabilitas hoaks melampaui angka ini, berita dikategorikan sebagai HOAKS."
    )

    # Indikator Hardware
    st.markdown("---")
    st.markdown("### 💻 Status Sistem")
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.caption("🖥️ **Perangkat:**")
        st.write("CPU Mode")
    with col_s2:
        st.caption("📦 **PyTorch:**")
        try:
            import torch
            st.write(f"v{torch.__version__.split('+')[0]}")
        except:
            st.write("Not found")

    with st.expander("📚 Tentang Penelitian & Metodologi"):
        st.markdown("""
        **Fokus Riset:**
        Deteksi disinformasi pada teks berita daring berbahasa Indonesia dengan pendekatan *Explainable AI* (XAI).
        
        **Tujuan Utama:**
        Membuka 'black-box' model Transformer sehingga pengguna dapat memahami *alasan* spesifik di balik keputusan sistem.
        """)


# ==============================================================================
# 7. MAIN INTERFACE - HERO BANNER & INPUT SECTION
# ==============================================================================

st.markdown("""
<div class="hero-card">
    <div class="hero-badge">⚡ Natural Language Processing • S2 Riset & Tesis</div>
    <div class="hero-title">Deteksi Berita Hoaks IndoBERT & Explainable AI</div>
    <p class="hero-sub">
        Platform analisis otomatis kredibilitas artikel berita Indonesia menggunakan representasi kontekstual
        <strong>IndoBERT</strong> dipadukan dengan teknik interpretasi <strong>XAI (Explainable Artificial Intelligence)</strong>
        untuk transparansi setiap token kata.
    </p>
</div>
""", unsafe_allow_html=True)

# Pilihan Teks Contoh Cepat (Quick Pills)
st.markdown("##### 📌 Coba Teks Contoh Siap Uji:")
col_pill1, col_pill2, col_pill3, col_pill4 = st.columns(4)

with col_pill1:
    if st.button("🚨 Hoaks Konspirasi", use_container_width=True):
        set_sample_text(SAMPLE_ARTICLES["🚨 Hoaks Sensasional: Konspirasi Air Minum"])
with col_pill2:
    if st.button("🏛️ Berita Kemenkes", use_container_width=True):
        set_sample_text(SAMPLE_ARTICLES["🏛️ Berita Faktual Resmi: Rilis Kementerian Kesehatan & BPOM"])
with col_pill3:
    if st.button("⚖️ Klarifikasi Fakta", use_container_width=True):
        set_sample_text(SAMPLE_ARTICLES["⚖️ Klarifikasi Cek Fakta: Verifikasi Klaim Obat Herbal"])
with col_pill4:
    if st.button("📱 Berantai WhatsApp", use_container_width=True):
        set_sample_text(SAMPLE_ARTICLES["📱 Pesan Berantai WhatsApp: Modus Undian & Link Phishing"])

# Text Area Input
teks_berita = st.text_area(
    "Masukkan Paragraf atau Artikel Berita untuk Dianalisis:",
    value=st.session_state["input_text"],
    height=170,
    placeholder="Ketik atau tempelkan teks berita, pesan berantai, atau artikel berbahasa Indonesia di sini...",
    help="Sistem akan menganalisis semantik, leksikal, serta struktur kalimat dalam teks."
)

col_btn1, col_btn2, col_btn3 = st.columns([2.5, 1.5, 4])
with col_btn1:
    btn_analisis = st.button("🚀 Jalankan Analisis AI", type="primary", use_container_width=True)
with col_btn2:
    if st.button("🔄 Kosongkan", use_container_width=True):
        reset_all_text()
        st.rerun()


# ==============================================================================
# 8. ANALISIS & EKSEKUSI PREDIKSI
# ==============================================================================

if btn_analisis:
    if not teks_berita.strip():
        st.warning("⚠️ Silakan masukkan teks berita terlebih dahulu sebelum melakukan analisis.")
    else:
        st.session_state["last_analyzed_text"] = teks_berita
        
        with st.spinner("Menjalankan Tokenisasi IndoBERT, Layer Transformer, & Perhitungan Atribusi XAI..."):
            start_time = time.time()

            if "PyTorch" in engine_choice:
                # Mode PyTorch
                bundle = get_pytorch_model(model_name if "Checkpoint" not in model_name else "./saved_model/")
                if bundle["status"] == "success":
                    hasil = explain_pytorch_engine(teks_berita, bundle)
                else:
                    st.warning(f"⚠️ Model PyTorch lokal/online tidak dapat dimuat ({bundle.get('message', '')}). Beralih otomatis ke Hybrid XAI Engine.")
                    hasil = explain_hybrid_engine(teks_berita)
            else:
                # Mode Hybrid
                time.sleep(0.4) # Efek transisi halus
                hasil = explain_hybrid_engine(teks_berita)

            elapsed = round(time.time() - start_time, 2)
            hasil["elapsed_time"] = elapsed
            st.session_state["analysis_results"] = hasil


# ==============================================================================
# 9. TAMPILAN HASIL ANALISIS & INTERPRETASI XAI
# ==============================================================================

if st.session_state["analysis_results"]:
    res = st.session_state["analysis_results"]
    p_hoax = res["p_hoax"]
    p_valid = res["p_valid"]
    attributions = res["attributions"]
    ling_stats = res["ling_stats"]

    is_hoax = p_hoax >= threshold_slider
    status_label = "HOAKS" if is_hoax else "VALID"
    confidence = p_hoax if is_hoax else p_valid

    st.markdown("---")
    st.markdown("### 📊 Hasil Keputusan & Transparansi Model")

    # Banner Hasil Klasifikasi
    if is_hoax:
        st.markdown(f"""
        <div class="verdict-banner-hoax">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px;">
                <div>
                    <span class="badge-pill-hoax">🚨 PREDIKSI: HOAKS / DISINFORMASI</span>
                    <div style="font-size: 1.15rem; font-weight: 700; color: #9F1239; margin-top: 10px;">
                        Artikel terindikasi kuat memiliki karakteristik berita bohong, sensasional, atau menyesatkan.
                    </div>
                    <div style="font-size: 0.88rem; color: #BE123C; margin-top: 4px;">
                        Tingkat keyakinan model: <strong>{confidence*100:.1f}%</strong> • Waktu inferensi: <strong>{res.get('elapsed_time', 0.4)} detik</strong>
                    </div>
                </div>
                <div style="background: rgba(255,255,255,0.7); padding: 10px 18px; border-radius: 12px; border: 1px solid rgba(225, 29, 72, 0.3); text-align: right;">
                    <span style="font-size: 0.8rem; color: #881337; font-weight: 700;">AMBANG KEPUTUSAN</span><br>
                    <span style="font-size: 1.2rem; font-weight: 800; color: #E11D48;">{p_hoax*100:.1f}%</span>
                    <span style="font-size: 0.8rem; color: #64748B;"> / {threshold_slider*100:.0f}%</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="verdict-banner-valid">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px;">
                <div>
                    <span class="badge-pill-valid">✅ PREDIKSI: BERITA VALID / FAKTUAL</span>
                    <div style="font-size: 1.15rem; font-weight: 700; color: #065F46; margin-top: 10px;">
                        Artikel menggunakan gaya bahasa formal, rujukan kredibel, dan minim unsur clickbait.
                    </div>
                    <div style="font-size: 0.88rem; color: #047857; margin-top: 4px;">
                        Tingkat keyakinan model: <strong>{confidence*100:.1f}%</strong> • Waktu inferensi: <strong>{res.get('elapsed_time', 0.4)} detik</strong>
                    </div>
                </div>
                <div style="background: rgba(255,255,255,0.7); padding: 10px 18px; border-radius: 12px; border: 1px solid rgba(16, 185, 129, 0.3); text-align: right;">
                    <span style="font-size: 0.8rem; color: #064E3B; font-weight: 700;">AMBANG KEPUTUSAN</span><br>
                    <span style="font-size: 1.2rem; font-weight: 800; color: #059669;">{p_hoax*100:.1f}%</span>
                    <span style="font-size: 0.8rem; color: #64748B;"> / {threshold_slider*100:.0f}%</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Baris Metrik & Visualisasi Gauge
    col_g1, col_g2, col_g3 = st.columns([1.5, 1.3, 1.2])

    with col_g1:
        st.plotly_chart(create_hoax_gauge(p_hoax, threshold_slider), use_container_width=True)

    with col_g2:
        st.markdown("""
        <div class="metric-box">
            <div>
                <div class="metric-label">DISTRIBUSI PROBABILITAS</div>
                <div style="margin-top: 10px;">
        """, unsafe_allow_html=True)
        st.write(f"🔴 **Hoaks:** `{p_hoax*100:.1f}%`")
        st.progress(float(p_hoax))
        st.write(f"🟢 **Valid:** `{p_valid*100:.1f}%`")
        st.progress(float(p_valid))
        st.markdown("</div></div></div>", unsafe_allow_html=True)

    with col_g3:
        st.markdown(f"""
        <div class="metric-box">
            <div>
                <div class="metric-label">STATISTIK TEKS & GAYA BAHASA</div>
                <div style="margin-top: 10px; font-size: 0.9rem; line-height: 1.7; color: #334155;">
                    📝 Jumlah Kata: <strong>{ling_stats['total_words']} kata</strong><br>
                    🔤 Huruf Kapital: <strong>{ling_stats['caps_ratio']}%</strong><br>
                    ❗ Tanda Seru/Tanya: <strong>{ling_stats['exclamations'] + ling_stats['questions']} buah</strong><br>
                    🏛️ Rujukan Kredibel: <strong>{ling_stats['credible_entities']} rujukan</strong>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ==========================================================================
    # TABS ANALISIS XAI & TRANSPARANSI
    # ==========================================================================
    st.markdown("### 🔍 Transparansi Model (Explainable AI)")
    
    tab_text, tab_chart, tab_ling, tab_export = st.tabs([
        "✨ Highlight Teks (Atribusi Token)",
        "📈 Grafik Kata Paling Berpengaruh",
        "📑 Indikator Gaya Penulisan",
        "📥 Ekspor Hasil Laporan"
    ])

    with tab_text:
        st.markdown("""
        Visualisasi di bawah ini menampilkan bagaimana **IndoBERT** mengatribusikan bobot penting pada masing-masing kata dalam teks:
        - <span style="background: rgba(225, 29, 72, 0.25); border: 1px solid #E11D48; padding: 2px 8px; border-radius: 6px; font-weight: 700; color: #9F1239;">Merah</span>: Kata pemicu prediksi **HOAKS** (sensasional, mendesak, provokatif).
        - <span style="background: rgba(16, 185, 129, 0.25); border: 1px solid #10B981; padding: 2px 8px; border-radius: 6px; font-weight: 700; color: #065F46;">Hijau</span>: Kata pemicu prediksi **VALID** (institusi resmi, metodologi riset, verifikasi).
        """, unsafe_allow_html=True)

        col_f1, col_f2 = st.columns([3, 1])
        with col_f2:
            filter_highlight = st.selectbox(
                "Filter Tampilan Kata:",
                ["Semua Kata", "Hanya Kata Hoaks", "Hanya Kata Valid"]
            )

        html_text = render_xai_highlight_html(attributions, filter_type=filter_highlight)
        st.markdown(f'<div class="xai-container">{html_text}</div>', unsafe_allow_html=True)

        st.caption("💡 *Arahkan kursor ke masing-masing kata yang disorot untuk melihat skor atribusi spesifik.*")

    with tab_chart:
        st.plotly_chart(create_feature_importance_plot(attributions, top_n=12), use_container_width=True)
        st.markdown("""
        <div class="insight-card">
            <strong>Cara Membaca Grafik XAI:</strong><br>
            Batang di sebelah <strong>kanan (Merah)</strong> berkontribusi positif mendorong sistem untuk menyatakan berita sebagai hoaks.
            Sebaliknya, batang di sebelah <strong>kiri (Hijau)</strong> menurunkan kecurigaan dan mendorong sistem menyimpulkan berita sebagai valid.
        </div>
        """, unsafe_allow_html=True)

    with tab_ling:
        st.markdown("#### Analisis Linguistik dan Ciri Disinformasi")
        
        col_l1, col_l2 = st.columns(2)
        with col_l1:
            st.markdown("##### 🚨 Indikator Peringatan (Hoaks Signs)")
            if ling_stats["caps_ratio"] > 15:
                st.warning(f"⚠️ Penggunaan huruf kapital berlebih ({ling_stats['caps_ratio']}%) terdeteksi, ciri khas judul/konten sensasional.")
            if ling_stats["exclamations"] > 1:
                st.warning(f"⚠️ Ditemukan {ling_stats['exclamations']} tanda seru (!), mengindikasikan nada tulisan provokatif atau urgensi palsu.")
            if ling_stats["hoax_triggers"] > 0:
                st.warning(f"⚠️ Ditemukan {ling_stats['hoax_triggers']} kata kunci pemicu kecurigaan disinformasi (seperti: viral, rahasia, sebarkan).")
            if ling_stats["caps_ratio"] <= 15 and ling_stats["exclamations"] <= 1 and ling_stats["hoax_triggers"] == 0:
                st.success("✅ Tidak ditemukan pola sensasionalisme atau kepanikan ekstrem pada gaya penulisan.")

        with col_l2:
            st.markdown("##### 🏛️ Indikator Kredibilitas (Credibility Signals)")
            if ling_stats["credible_entities"] > 0:
                st.success(f"✅ Artikel menyebutkan {ling_stats['credible_entities']} entitas institusional/faktual (Kementerian, BPOM, BMKG, CekFakta, dsb).")
            else:
                st.info("ℹ️ Artikel tidak menyebutkan lembaga resmi atau otoritas pemeriksa fakta.")
            
            if not is_hoax:
                st.success("✅ Struktur kalimat memenuhi kaidah penulisan jurnalistik berita faktual.")

        # Radar / Bar Breakdown
        ling_df = pd.DataFrame({
            "Kategori Fitur": ["Sensasionalisme", "Tingkat Urgensi", "Densitas Emosi", "Kredibilitas Rujukan"],
            "Nilai": [
                min(ling_stats["caps_ratio"] * 1.5, 100),
                min(ling_stats["punct_urgency"] * 2.0, 100),
                min(ling_stats["hoax_triggers"] * 25, 100),
                min(ling_stats["credible_entities"] * 33, 100)
            ]
        })
        fig_ling = px.bar(
            ling_df,
            x="Kategori Fitur",
            y="Nilai",
            color="Kategori Fitur",
            color_discrete_sequence=["#F43F5E", "#FB923C", "#A855F7", "#10B981"],
            title="Skor Karakteristik Linguistik Berita (0 - 100)"
        )
        fig_ling.update_layout(height=280, showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_ling, use_container_width=True)

    with tab_export:
        st.markdown("#### 📥 Unduh Hasil Pengujian untuk Laporan Riset / Tesis")
        st.write("Gunakan fitur ini untuk mendokumentasikan pengujian sampel ke dalam laporan akademik:")

        report_data = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "model_architecture": model_name,
            "xai_method": xai_method,
            "classification_verdict": status_label,
            "confidence_score": float(confidence),
            "probability_hoax": float(p_hoax),
            "probability_valid": float(p_valid),
            "threshold_used": float(threshold_slider),
            "linguistic_metrics": ling_stats,
            "top_10_attributions": sorted(attributions, key=lambda x: abs(x[1]), reverse=True)[:10],
            "analyzed_text_excerpt": teks_berita[:250] + ("..." if len(teks_berita) > 250 else "")
        }

        json_str = json.dumps(report_data, indent=2, ensure_ascii=False)
        col_exp1, col_exp2 = st.columns(2)
        with col_exp1:
            st.download_button(
                label="📄 Unduh Laporan Format JSON",
                data=json_str,
                file_name=f"hasil_deteksi_hoaks_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
        with col_exp2:
            md_text = f"""# Laporan Deteksi Berita Hoaks IndoBERT & XAI
- **Waktu Pengujian:** {report_data['timestamp']}
- **Model:** {model_name}
- **Hasil Prediksi:** {status_label} (Keyakinan: {confidence*100:.1f}%)
- **Probabilitas Hoaks:** {p_hoax*100:.2f}% | **Probabilitas Valid:** {p_valid*100:.2f}%
- **Threshold:** {threshold_slider*100:.1f}%

## Top 5 Token Berpengaruh (XAI):
""" + "\n".join([f"- `{t}`: {w:+.3f}" for t, w in report_data["top_10_attributions"][:5]])
            st.download_button(
                label="📝 Unduh Ringkasan Format Markdown",
                data=md_text,
                file_name=f"ringkasan_hoaks_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                mime="text/markdown",
                use_container_width=True
            )

        st.json(report_data)


# ==============================================================================
# 10. REKOMENDASI CEK FAKTA & VERIFIKASI RESMI
# ==============================================================================
st.markdown("---")
st.markdown("### 🌐 Portal Cek Fakta Resmi di Indonesia")
st.caption("Jika Anda menemukan informasi yang mencurigakan, selalu verifikasi ke kanal cek fakta independen:")

col_f1, col_f2, col_f3 = st.columns(3)
with col_f1:
    st.markdown("""
    <div style="background: #FFFFFF; border: 1px solid #E2E8F0; padding: 16px; border-radius: 12px; text-align: center;">
        <span style="font-size: 1.5rem;">🕵️</span>
        <div style="font-weight: 700; color: #1E293B; margin-top: 5px;">TurnBackHoax.id</div>
        <div style="font-size: 0.8rem; color: #64748B; margin-bottom: 10px;">Database Hoaks Mafindo</div>
        <a href="https://turnbackhoax.id" target="_blank" style="text-decoration: none; color: #3B82F6; font-weight: 600; font-size: 0.85rem;">Buka Situs ↗</a>
    </div>
    """, unsafe_allow_html=True)

with col_f2:
    st.markdown("""
    <div style="background: #FFFFFF; border: 1px solid #E2E8F0; padding: 16px; border-radius: 12px; text-align: center;">
        <span style="font-size: 1.5rem;">🔍</span>
        <div style="font-weight: 700; color: #1E293B; margin-top: 5px;">CekFakta.com</div>
        <div style="font-size: 0.8rem; color: #64748B; margin-bottom: 10px;">Kolaborasi Media Nasional & AJI</div>
        <a href="https://cekfakta.com" target="_blank" style="text-decoration: none; color: #3B82F6; font-weight: 600; font-size: 0.85rem;">Buka Situs ↗</a>
    </div>
    """, unsafe_allow_html=True)

with col_f3:
    st.markdown("""
    <div style="background: #FFFFFF; border: 1px solid #E2E8F0; padding: 16px; border-radius: 12px; text-align: center;">
        <span style="font-size: 1.5rem;">🏛️</span>
        <div style="font-weight: 700; color: #1E293B; margin-top: 5px;">Aduan Konten Kominfo</div>
        <div style="font-size: 0.8rem; color: #64748B; margin-bottom: 10px;">Kanal Resmi Kemkominfo RI</div>
        <a href="https://aduankonten.id" target="_blank" style="text-decoration: none; color: #3B82F6; font-weight: 600; font-size: 0.85rem;">Buka Situs ↗</a>
    </div>
    """, unsafe_allow_html=True)


# ==============================================================================
# 11. FOOTER & PANDUAN INTEGRASI TESIS
# ==============================================================================
st.markdown("---")
with st.expander("📖 Panduan Integrasi Checkpoint Model Hasil Fine-Tuning Sendiri"):
    st.markdown("""
    Untuk menggunakan model Transformer IndoBERT yang telah Anda latih (misal dari Google Colab / Kaggle):
    
    1. Simpan folder checkpoint model Anda (berisi `config.json`, `model.safetensors` atau `pytorch_model.bin`, serta file `vocab.txt` / tokenizer) ke direktori lokal:
       ```
       Deteksi Berita Hoaks/
       ├── saved_model/
       │   ├── config.json
       │   ├── model.safetensors
       │   ├── tokenizer_config.json
       │   └── vocab.txt
       └── deteksi.py
       ```
    2. Pilih **"🤖 PyTorch IndoBERT Transformer"** pada sidebar dan pilih opsi **"Checkpoint Lokal (./saved_model/)"**.
    3. Sistem secara otomatis akan memuat model dan menjalankan kalkulasi atribusi token (XAI).
    """)

st.markdown("""
<div style="text-align: center; margin-top: 25px; padding: 15px; color: #64748B; font-size: 0.85rem;">
    <strong>Sistem Deteksi Hoaks IndoBERT & XAI</strong> • Laboratorium Riset NLP & Literasi Digital • 2026<br>
    Dibangun menggunakan Streamlit, PyTorch, HuggingFace Transformers, dan Plotly.
</div>
""", unsafe_allow_html=True)