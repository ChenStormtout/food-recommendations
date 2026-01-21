import pandas as pd
import random
import streamlit as st
import numpy as np
from datetime import datetime

# Default weights for WP calculation
default_weights = {
    'Rating': 0.25,
    'Harga': 0.20,
    'Waktu_Persiapan': 0.15,
    'Popularitas': 0.25,
    'Ketersediaan': 0.15
}

# Function to calculate Weighted Product Score
def calculate_wp_score(data, weights=None):
    if weights is None:
        weights = default_weights
    
    # Create a copy to avoid modifying original data
    df = data.copy()
    
    # Add missing columns with sample data if they don't exist
    if 'Waktu_Persiapan' not in df.columns:
        np.random.seed(42)
        df['Waktu_Persiapan'] = np.random.randint(15, 120, len(df))  # 15-120 minutes
    
    if 'Popularitas' not in df.columns:
        np.random.seed(43)
        df['Popularitas'] = np.random.randint(50, 1000, len(df))  # 50-1000 popularity score
    
    if 'Ketersediaan' not in df.columns:
        np.random.seed(44)
        df['Ketersediaan'] = np.random.randint(70, 100, len(df))  # 70-100% availability
    
    # Normalization for each criterion
    # Rating: Higher is better (benefit)
    normalized_rating = df['Rating'] / df['Rating'].max()
    
    # Harga: Lower is better (cost) - invert the values
    normalized_harga = df['Harga'].min() / df['Harga']
    
    # Waktu_Persiapan: Lower is better (cost) - invert the values
    normalized_waktu = df['Waktu_Persiapan'].min() / df['Waktu_Persiapan']
    
    # Popularitas: Higher is better (benefit)
    normalized_popularitas = df['Popularitas'] / df['Popularitas'].max()
    
    # Ketersediaan: Higher is better (benefit)
    normalized_ketersediaan = df['Ketersediaan'] / df['Ketersediaan'].max()
    
    # Calculate WP Score using the formula: ∏(xi^wi)
    wp_score = (
        (normalized_rating ** weights['Rating']) *
        (normalized_harga ** weights['Harga']) *
        (normalized_waktu ** weights['Waktu_Persiapan']) *
        (normalized_popularitas ** weights['Popularitas']) *
        (normalized_ketersediaan ** weights['Ketersediaan'])
    )
    
    # Scale to 0-100 for better readability
    df['WP_Score'] = (wp_score * 100).round(2)
    
    return df

# Function to generate the food dataset
def generate_food_dataset():
    # Data sample yang sudah ditentukan dengan lengkap (tidak random)
    sample_data = [
        # KATEGORI ASIN
        {
            "Nama": "Kerupuk Udang",
            "Kategori": "Asin",
            "Harga": 12000,
            "Waktu_Makan": "Camilan",
            "Lokasi": "Jakarta",
            "Deskripsi": "Kerupuk renyah dengan rasa udang yang gurih",
            "Rating": 4.2,
            "Waktu_Persiapan": 10,  # menit
            "Popularitas": 750,     # skor popularitas
            "Ketersediaan": 95      # persen
        },
        {
            "Nama": "Telur Asin",
            "Kategori": "Asin",
            "Harga": 6000,
            "Waktu_Makan": "Sarapan",
            "Lokasi": "Brebes",
            "Deskripsi": "Telur bebek yang diasinkan dengan cita rasa khas",
            "Rating": 4.0,
            "Waktu_Persiapan": 5,
            "Popularitas": 620,
            "Ketersediaan": 88
        },
        {
            "Nama": "Ikan Teri Medan",
            "Kategori": "Asin",
            "Harga": 28000,
            "Waktu_Makan": "Makan Siang",
            "Lokasi": "Medan",
            "Deskripsi": "Ikan teri kering khas Medan yang gurih",
            "Rating": 4.5,
            "Waktu_Persiapan": 15,
            "Popularitas": 480,
            "Ketersediaan": 75
        },
        
        # KATEGORI MANIS
        {
            "Nama": "Es Krim Vanila",
            "Kategori": "Manis",
            "Harga": 18000,
            "Waktu_Makan": "Camilan",
            "Lokasi": "Bandung",
            "Deskripsi": "Es krim lembut dengan rasa vanila klasik",
            "Rating": 4.3,
            "Waktu_Persiapan": 3,
            "Popularitas": 890,
            "Ketersediaan": 92
        },
        {
            "Nama": "Klepon",
            "Kategori": "Manis",
            "Harga": 12000,
            "Waktu_Makan": "Camilan",
            "Lokasi": "Yogyakarta",
            "Deskripsi": "Kue tradisional dengan isian gula merah",
            "Rating": 4.1,
            "Waktu_Persiapan": 30,
            "Popularitas": 560,
            "Ketersediaan": 80
        },
        {
            "Nama": "Martabak Manis",
            "Kategori": "Manis",
            "Harga": 35000,
            "Waktu_Makan": "Makan Malam",
            "Lokasi": "Jakarta",
            "Deskripsi": "Martabak tebal dengan berbagai topping manis",
            "Rating": 4.6,
            "Waktu_Persiapan": 20,
            "Popularitas": 950,
            "Ketersediaan": 85
        },
        
        # KATEGORI PEDAS
        {
            "Nama": "Ayam Geprek",
            "Kategori": "Pedas",
            "Harga": 25000,
            "Waktu_Makan": "Makan Siang",
            "Lokasi": "Surabaya",
            "Deskripsi": "Ayam crispy dengan sambal pedas yang menggigit",
            "Rating": 4.4,
            "Waktu_Persiapan": 25,
            "Popularitas": 820,
            "Ketersediaan": 90
        },
        {
            "Nama": "Seblak Kerupuk",
            "Kategori": "Pedas",
            "Harga": 18000,
            "Waktu_Makan": "Camilan",
            "Lokasi": "Bandung",
            "Deskripsi": "Makanan berkuah pedas dengan kerupuk",
            "Rating": 4.2,
            "Waktu_Persiapan": 15,
            "Popularitas": 670,
            "Ketersediaan": 85
        },
        {
            "Nama": "Nasi Padang",
            "Kategori": "Pedas",
            "Harga": 35000,
            "Waktu_Makan": "Makan Siang",
            "Lokasi": "Padang",
            "Deskripsi": "Nasi dengan lauk khas Padang yang pedas",
            "Rating": 4.7,
            "Waktu_Persiapan": 10,
            "Popularitas": 900,
            "Ketersediaan": 95
        },
        
        # KATEGORI ASAM
        {
            "Nama": "Rujak Buah",
            "Kategori": "Asam",
            "Harga": 15000,
            "Waktu_Makan": "Camilan",
            "Lokasi": "Jakarta",
            "Deskripsi": "Campuran buah segar dengan bumbu asam pedas",
            "Rating": 4.0,
            "Waktu_Persiapan": 10,
            "Popularitas": 720,
            "Ketersediaan": 85
        },
        {
            "Nama": "Es Jeruk",
            "Kategori": "Asam",
            "Harga": 12000,
            "Waktu_Makan": "Semua",
            "Lokasi": "Bali",
            "Deskripsi": "Minuman segar dengan rasa jeruk asam",
            "Rating": 3.9,
            "Waktu_Persiapan": 5,
            "Popularitas": 650,
            "Ketersediaan": 95
        },
        {
            "Nama": "Asinan Betawi",
            "Kategori": "Asam",
            "Harga": 17000,
            "Waktu_Makan": "Camilan",
            "Lokasi": "Jakarta",
            "Deskripsi": "Asinan khas Betawi dengan rasa asam segar",
            "Rating": 4.1,
            "Waktu_Persiapan": 8,
            "Popularitas": 580,
            "Ketersediaan": 80
        },
        
        # KATEGORI GURIH/UMAMI
        {
            "Nama": "Nasi Gudeg",
            "Kategori": "Gurih/Umami",
            "Harga": 30000,
            "Waktu_Makan": "Makan Siang",
            "Lokasi": "Yogyakarta",
            "Deskripsi": "Nasi dengan gudeg khas Yogyakarta",
            "Rating": 4.5,
            "Waktu_Persiapan": 15,
            "Popularitas": 780,
            "Ketersediaan": 90
        },
        {
            "Nama": "Sate Ayam",
            "Kategori": "Gurih/Umami",
            "Harga": 35000,
            "Waktu_Makan": "Makan Malam",
            "Lokasi": "Solo",
            "Deskripsi": "Sate ayam dengan bumbu kacang gurih",
            "Rating": 4.6,
            "Waktu_Persiapan": 30,
            "Popularitas": 860,
            "Ketersediaan": 88
        },
        {
            "Nama": "Rendang Daging",
            "Kategori": "Gurih/Umami",
            "Harga": 50000,
            "Waktu_Makan": "Makan Siang",
            "Lokasi": "Padang",
            "Deskripsi": "Daging sapi dengan bumbu rendang khas",
            "Rating": 4.8,
            "Waktu_Persiapan": 120,
            "Popularitas": 950,
            "Ketersediaan": 75
        }
    ]
    
    df = pd.DataFrame(sample_data)
    return df

# Generate the dataset
# Generate the dataset
try:
    data = pd.read_csv("MoodRasaDataFleksibel_cleaned.csv")
except:
    data = generate_food_dataset()

# Data sudah lengkap dengan Rating, Waktu_Persiapan, Popularitas, dan Ketersediaan
# Tidak perlu generate random lagi karena sudah didefinisikan di sample data

# Calculate WP Score for all data
data = calculate_wp_score(data, default_weights)

# Generate random ratings for each food
np.random.seed(42)
data['Rating'] = np.random.uniform(3.8, 5.0, len(data))
data['Rating'] = data['Rating'].round(1)

# Streamlit Page Configuration
st.set_page_config(
    page_title="🍽️ Mood Rasa - Premium Culinary Experience",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium Glassmorphism CSS with improved visibility
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Playfair+Display:wght@400;500;600;700&display=swap');
    
    :root {
        --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        --accent-gradient: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        --dark-gradient: linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 50%, #16213e 100%);
        --glass-bg: rgba(255, 255, 255, 0.12);
        --glass-border: rgba(255, 255, 255, 0.25);
        --text-primary: #999999;
        --text-secondary: rgba(255, 255, 255, 0.9);
        --text-muted: rgba(255, 255, 255, 0.8);
        --shadow-glass: 0 25px 45px rgba(0, 0, 0, 0.1);
        --shadow-hover: 0 35px 60px rgba(0, 0, 0, 0.15);
    }
    
    * {
        font-family: 'Inter', sans-serif;
        box-sizing: border-box;
    }
    
    .stApp {
        background: var(--dark-gradient);
        background-attachment: fixed;
        min-height: 100vh;
        color: var(--text-primary) !important;
    }
    
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Fix text visibility */
    .stMarkdown, .stText, p, div, span, h1, h2, h3, h4, h5, h6 {
        color: var(--text-primary) !important;
    }
    
    /* Premium Header Styling */
    .premium-header {
        text-align: center;
        margin-bottom: 4rem;
        padding: 3rem 2rem;
        background: var(--glass-bg);
        backdrop-filter: blur(25px);
        border-radius: 30px;
        border: 1px solid var(--glass-border);
        box-shadow: var(--shadow-glass);
        position: relative;
        overflow: hidden;
        animation: fadeInUp 0.8s ease-out;
    }
    
    .premium-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: var(--primary-gradient);
        opacity: 0.03;
        z-index: -1;
    }
    
    .main-title {
        font-family: 'Playfair Display', serif;
        font-size: 4.5rem;
        font-weight: 700;
        background: var(--accent-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1rem;
        letter-spacing: -2px;
        line-height: 1.1;
    }
    
    .subtitle {
        font-size: 1.3rem;
        color: var(--text-secondary) !important;
        font-weight: 400;
        margin-bottom: 1rem;
        letter-spacing: 0.5px;
    }
    
    .project-tag {
        display: inline-block;
        background: var(--glass-bg);
        backdrop-filter: blur(15px);
        border: 1px solid var(--glass-border);
        padding: 0.5rem 1.5rem;
        border-radius: 25px;
        font-size: 0.9rem;
        color: var(--text-muted) !important;
        margin-top: 1rem;
        transition: all 0.3s ease;
    }
    
    .project-tag:hover {
        background: rgba(255, 255, 255, 0.12);
        transform: translateY(-2px);
    }
    
    /* Stats Cards */
    .stats-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 2rem;
        margin-bottom: 4rem;
    }
    
    .stat-card {
        background: var(--glass-bg);
        backdrop-filter: blur(25px);
        border-radius: 25px;
        border: 1px solid var(--glass-border);
        padding: 2.5rem 2rem;
        text-align: center;
        box-shadow: var(--shadow-glass);
        transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
        position: relative;
        overflow: hidden;
    }
    
    .stat-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: var(--accent-gradient);
        transform: scaleX(0);
        transition: transform 0.3s ease;
    }
    
    .stat-card:hover {
        transform: translateY(-8px);
        box-shadow: var(--shadow-hover);
        background: rgba(255, 255, 255, 0.12);
    }
    
    .stat-card:hover::before {
        transform: scaleX(1);
    }
    
    .stat-number {
        display: block;
        font-size: 3rem;
        font-weight: 800;
        background: var(--primary-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        line-height: 1;
    }
    
    .stat-label {
        font-size: 1.1rem;
        color: var(--text-secondary) !important;
        font-weight: 500;
        letter-spacing: 0.5px;
    }
    
    /* Random Button Styling */
    .random-button {
        background: var(--secondary-gradient);
        border: none;
        border-radius: 25px;
        padding: 1rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        color: black;
        cursor: pointer;
        transition: all 0.3s ease;
        margin: 1rem 0;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
    }
    
    .random-button:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.3);
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: var(--glass-bg) !important;
        backdrop-filter: blur(25px) !important;
        border-right: 1px solid var(--glass-border) !important;
    }
    
    .sidebar-header {
        background: var(--glass-bg);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        border: 1px solid var(--glass-border);
        padding: 1.5rem;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .filter-header {
        color: var(--text-primary) !important;
        font-size: 1.4rem;
        font-weight: 600;
        margin: 0;
        letter-spacing: 0.5px;
    }
    
    /* Custom Selectbox and Input Styling */
    .stSelectbox > div > div {
        background: var(--glass-bg) !important;
        backdrop-filter: blur(15px) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: 15px !important;
        color: var(--text-primary) !important;
    }
    
    .stTextInput > div > div > input {
        background: var(--glass-bg) !important;
        backdrop-filter: blur(15px) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: 15px !important;
        color: var(--text-primary) !important;
    }
    
    /* Results Section */
    .results-header {
        background: var(--glass-bg);
        backdrop-filter: blur(25px);
        border-radius: 25px;
        border: 1px solid var(--glass-border);
        padding: 2rem;
        margin-bottom: 3rem;
        box-shadow: var(--shadow-glass);
    }
    
    .results-title {
        font-size: 2rem;
        font-weight: 700;
        color: var(--text-primary) !important;
        margin-bottom: 1rem;
    }
    
    .results-count {
        font-size: 1.1rem;
        color: var(--text-secondary) !important;
        font-weight: 500;
    }
    
    .count-highlight {
        background: var(--accent-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700;
        font-size: 1.2rem;
    }
    
    /* Premium Food Cards */
    .food-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
        gap: 2.5rem;
        margin-top: 2rem;
    }
    
    .food-card {
        background: var(--glass-bg);
        backdrop-filter: blur(25px);
        border-radius: 25px;
        border: 1px solid var(--glass-border);
        padding: 2.5rem;
        box-shadow: var(--shadow-glass);
        transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
        position: relative;
        overflow: hidden;
        margin-bottom: 2rem;
    }
    
    .food-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: var(--secondary-gradient);
        transform: scaleX(0);
        transition: transform 0.3s ease;
    }
    
    .food-card:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: var(--shadow-hover);
        background: rgba(255, 255, 255, 0.12);
    }
    
    .food-card:hover::before {
        transform: scaleX(1);
    }
    
    .food-name {
        font-size: 1.6rem;
        font-weight: 700;
        color: var(--text-primary) !important;
        margin-bottom: 1.5rem;
        font-family: 'Playfair Display', serif;
        line-height: 1.3;
    }
    
    .food-info {
        display: flex;
        flex-wrap: wrap;
        gap: 1rem;
        margin-bottom: 1.5rem;
    }
    
    .info-tag {
        background: var(--glass-bg);
        backdrop-filter: blur(15px);
        border: 1px solid var(--glass-border);
        padding: 0.6rem 1.2rem;
        border-radius: 20px;
        font-size: 0.9rem;
        color: var(--text-secondary) !important;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .info-tag:hover {
        background: rgba(255, 255, 255, 0.15);
        transform: translateY(-2px);
    }
    
    .food-description {
        color: var(--text-muted) !important;
        font-size: 1rem;
        line-height: 1.6;
        font-weight: 400;
        letter-spacing: 0.3px;
    }
    
    /* Progress Bar */
    .stProgress .st-bo {
        background: var(--glass-bg) !important;
        backdrop-filter: blur(15px) !important;
        border-radius: 10px !important;
        border: 1px solid var(--glass-border) !important;
    }
    
    .stProgress .st-bp {
        background: var(--accent-gradient) !important;
        border-radius: 8px !important;
    }
    
    /* Footer */
    .premium-footer {
        background: var(--glass-bg);
        backdrop-filter: blur(25px);
        border-radius: 25px;
        border: 1px solid var(--glass-border);
        padding: 2rem;
        text-align: center;
        margin-top: 4rem;
        box-shadow: var(--shadow-glass);
    }
    
    .footer-text {
        color: var(--text-muted) !important;
        font-size: 1rem;
        font-weight: 400;
        letter-spacing: 0.5px;
    }
    
    /* Special Random Pick Card */
    .random-pick-card {
        background: linear-gradient(135deg, rgba(240, 147, 251, 0.2) 0%, rgba(245, 87, 108, 0.2) 100%);
        backdrop-filter: blur(25px);
        border-radius: 25px;
        border: 2px solid rgba(245, 87, 108, 0.4);
        padding: 2.5rem;
        box-shadow: 0 25px 50px rgba(245, 87, 108, 0.2);
        margin-bottom: 3rem;
        position: relative;
        overflow: hidden;
    }
    
    .random-pick-card::before {
        content: '🎲';
        position: absolute;
        top: 20px;
        right: 20px;
        font-size: 2rem;
        animation: pulse 2s infinite;
    }
    
    /* Animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.8; transform: scale(1.1); }
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--glass-border);
        border-radius: 10px;
        backdrop-filter: blur(10px);
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(255, 255, 255, 0.3);
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main-title {
            font-size: 3rem;
        }
        
        .premium-header {
            padding: 2rem 1rem;
        }
        
        .food-grid {
            grid-template-columns: 1fr;
        }
        
        .stat-card {
            padding: 2rem 1.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Premium Header
st.markdown(f"""
<div class="premium-header">
    <h1 class="main-title">🍽️ Mood Rasa</h1>
    <p class="subtitle">Discover Premium Culinary Experiences Tailored to Your Mood</p>
    <div class="project-tag">✨ Project SCPK - Premium Food Discovery Platform</div>
</div>
""", unsafe_allow_html=True)

# Premium Statistics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="stat-card">
        <span class="stat-number">{len(data)}</span>
        <div class="stat-label">🍽️ Premium Dishes</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="stat-card">
        <span class="stat-number">{len(data['Kategori'].unique())}</span>
        <div class="stat-label">🎯 Flavor Categories</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="stat-card">
        <span class="stat-number">{len(data['Lokasi'].unique())}</span>
        <div class="stat-label">📍 Culinary Regions</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    avg_rating = data['Rating'].mean()
    st.markdown(f"""
    <div class="stat-card">
        <span class="stat-number">{avg_rating:.1f}</span>
        <div class="stat-label">⭐ Average Rating</div>
    </div>
    """, unsafe_allow_html=True)


    st.markdown("\n### ⚖️ **WP Score Configuration**")
st.markdown("Customize weights for decision criteria:")

# Weight sliders
col1, col2 = st.columns(2)
with col1:
    rating_weight = st.slider("Rating", 0.0, 1.0, default_weights['Rating'], 0.05)
    harga_weight = st.slider("Price", 0.0, 1.0, default_weights['Harga'], 0.05)
    waktu_weight = st.slider("Prep Time", 0.0, 1.0, default_weights['Waktu_Persiapan'], 0.05)

with col2:
    popularitas_weight = st.slider("Popularity", 0.0, 1.0, default_weights['Popularitas'], 0.05)
    ketersediaan_weight = st.slider("Availability", 0.0, 1.0, default_weights['Ketersediaan'], 0.05)

# Normalize weights to sum to 1
total_weight = rating_weight + harga_weight + waktu_weight + popularitas_weight + ketersediaan_weight
if total_weight > 0:
    custom_weights = {
        'Rating': rating_weight / total_weight,
        'Harga': harga_weight / total_weight,
        'Waktu_Persiapan': waktu_weight / total_weight,
        'Popularitas': popularitas_weight / total_weight,
        'Ketersediaan': ketersediaan_weight / total_weight
    }
else:
    custom_weights = default_weights

    st.markdown(f"**Total Weight:** {total_weight:.2f} (normalized to 1.0)")

# Premium Sidebar
with st.sidebar:
    st.markdown("""
    <div class="sidebar-header">
        <h3 class="filter-header">🔍 Discover Your Perfect Meal</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced filters with better UX
    st.markdown("### 🎯 **Mood & Taste**")
    categories = ["Semua"] + sorted(data["Kategori"].unique().tolist())
    selected_category = st.selectbox("Select your flavor mood:", categories, key="category")
    
    st.markdown("### 📍 **Culinary Region**")
    locations = ["Semua"] + sorted(data["Lokasi"].unique().tolist())
    selected_location = st.selectbox("Choose your preferred region:", locations, key="location")
    
    st.markdown("### 💰 **Budget Range**")
    price_ranges = {
        "All Budgets": (0, 100000),
        "Budget Friendly (< 25k)": (0, 25000),
        "Mid Range (25k - 40k)": (25000, 40000),
        "Premium (40k - 60k)": (40000, 60000),
        "Luxury (> 60k)": (60000, 100000)
    }
    selected_price_range = st.selectbox("Select your budget:", list(price_ranges.keys()))
    price_range = price_ranges[selected_price_range]
    
    st.markdown("### 🕒 **Dining Time**")
    meal_times = ["Semua"] + sorted(data["Waktu_Makan"].unique().tolist())
    selected_meal_time = st.selectbox("When do you want to dine:", meal_times, key="meal_time")
    
    st.markdown("### ⭐ **Quality Rating**")
    rating_options = {
        "All Ratings": 0.0,
        "Good (≥ 4.0)": 4.0,
        "Excellent (≥ 4.5)": 4.5,
        "Outstanding (≥ 4.8)": 4.8
    }
    selected_rating = st.selectbox("Minimum quality standard:", list(rating_options.keys()))
    min_rating = rating_options[selected_rating]
    
    st.markdown("### 🔍 **Search**")
    search_text = st.text_input("Search for specific dishes:", placeholder="Type dish name or ingredient...")
    
    st.markdown("### 📊 **Sort Options**")
    sort_options = ["🌟 Highest Rated", "💰 Lowest Price", "💎 Highest Price", "🔤 A-Z", "🎯 Best WP Score", "🎯 Best Match"]
    sort_by = st.selectbox("Sort results by:", sort_options)


    
    
    # Random Food Picker Button
    st.markdown("---")
    st.markdown("### 🎲 **Feeling Lucky?**")
    if st.button("🎯 Pick Random Food for Me!", key="random_pick", help="Get a random food suggestion based on your current filters"):
        st.session_state.show_random = True
    else:
        st.session_state.show_random = False

# Function to apply filters with enhanced logic
def apply_filters(data, custom_weights=None):
    # Recalculate WP Score with custom weights if provided
    if custom_weights and custom_weights != default_weights:
        filtered_data = calculate_wp_score(data, custom_weights)
    else:
        filtered_data = data.copy()
    
    if selected_category != "Semua":
        filtered_data = filtered_data[filtered_data["Kategori"] == selected_category]
    
    if selected_location != "Semua":
        filtered_data = filtered_data[filtered_data["Lokasi"] == selected_location]
    
    if selected_meal_time != "Semua":
        filtered_data = filtered_data[
            (filtered_data["Waktu_Makan"] == selected_meal_time) | 
            (filtered_data["Waktu_Makan"] == "Semua")
        ]
    
    # Apply price range
    filtered_data = filtered_data[
        (filtered_data["Harga"] >= price_range[0]) & 
        (filtered_data["Harga"] <= price_range[1])
    ]
    
    # Apply rating filter
    if min_rating > 0:
        filtered_data = filtered_data[filtered_data["Rating"] >= min_rating]
    
    # Apply search filter
    if search_text:
        filtered_data = filtered_data[
            filtered_data["Nama"].str.contains(search_text, case=False, na=False) | 
            filtered_data["Deskripsi"].str.contains(search_text, case=False, na=False)
        ]
    
    # Apply sorting
    if sort_by == "🌟 Highest Rated":
        filtered_data = filtered_data.sort_values("Rating", ascending=False)
    elif sort_by == "💰 Lowest Price":
        filtered_data = filtered_data.sort_values("Harga")
    elif sort_by == "💎 Highest Price":
        filtered_data = filtered_data.sort_values("Harga", ascending=False)
    elif sort_by == "🔤 A-Z":
        filtered_data = filtered_data.sort_values("Nama")
    elif sort_by == "🎯 Best WP Score":
        filtered_data = filtered_data.sort_values("WP_Score", ascending=False)
    else:  # Best Match
        filtered_data = filtered_data.sort_values(["WP_Score", "Rating"], ascending=[False, False])
    
    return filtered_data

# Apply filters
filtered_data = apply_filters(data, custom_weights)

# Show Random Pick if button was clicked
if hasattr(st.session_state, 'show_random') and st.session_state.show_random and len(filtered_data) > 0:
    random_pick = filtered_data.sample(1).iloc[0]
    formatted_price = f"Rp {random_pick['Harga']:,}"
    
    st.markdown(f"""
    <div class="random-pick-card">
        <div class="food-name">🎲 Random Pick: {random_pick['Nama']}</div>
        <div class="food-info">
            <span class="info-tag">📍 {random_pick['Lokasi']}</span>
            <span class="info-tag">⏰ {random_pick['Waktu_Makan']}</span>
            <span class="info-tag">💰 {formatted_price}</span>
            <span class="info-tag">🌟 {random_pick['Rating']}/5.0</span>
            <span class="info-tag">🏷️ {random_pick['Kategori']}</span>
            <span class="info-tag">⚖️ WP: {random_pick['WP_Score']}/100</span>
            <span class="info-tag">⏱️ {random_pick['Waktu_Persiapan']} min</span>
            <span class="info-tag">📊 Pop: {random_pick['Popularitas']}</span>
            <span class="info-tag">✅ {random_pick['Ketersediaan']}%</span>
        </div>
        <div class="food-description">✨ {random_pick['Deskripsi']}</div>
    </div>
    """, unsafe_allow_html=True)

# Enhanced Results Section
if len(filtered_data) > 0:
    progress_value = len(filtered_data) / len(data)
    
    st.markdown(f"""
    <div class="results-header">
        <h3 class="results-title">🎯 Curated Results</h3>
        <div class="results-count">
            Showing <span class="count-highlight">{len(filtered_data)}</span> exceptional dishes out of {len(data)} total options
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Progress indicator
    st.progress(progress_value)
    
    # Setelah apply_filters
    best_wp_score = filtered_data["WP_Score"].max()
    
    # Display ALL food cards (not limited to 20)
    for idx, row in filtered_data.iterrows():
    # Format price with proper currency
        formatted_price = f"Rp {row['Harga']:,}"
        
        st.markdown(f"""
    <div class="food-card">
        <div class="food-name">{row['Nama']}</div>
        <div class="food-info">
            <span class="info-tag">📍 {row['Lokasi']}</span>
            <span class="info-tag">⏰ {row['Waktu_Makan']}</span>
            <span class="info-tag">💰 {formatted_price}</span>
            <span class="info-tag">🌟 {row['Rating']}/5.0</span>
            <span class="info-tag">🏷️ {row['Kategori']}</span>
            <span class="info-tag">⚖️ WP: {row['WP_Score']}/100</span>
            <span class="info-tag">⏱️ {row['Waktu_Persiapan']} min</span>
            <span class="info-tag">📊 Pop: {row['Popularitas']}</span>
            <span class="info-tag">✅ {row['Ketersediaan']}%</span>
        </div>
        <div class="food-description">{row['Deskripsi']}</div>
    </div>
    """, unsafe_allow_html=True)
        
else:
    st.markdown("""
    <div class="results-header">
        <h3 class="results-title">🔍 No Results Found</h3>
        <div class="results-count">
            Try adjusting your filters to discover more culinary options
        </div>
    </div>
    """, unsafe_allow_html=True)

# Premium Footer
st.markdown(f"""
<div class="premium-footer">
    <div class="footer-text">
        ✨ Crafted with passion by SCPK Team | {datetime.now().year} | Premium Food Discovery Experience
    </div>
</div>
""", unsafe_allow_html=True)