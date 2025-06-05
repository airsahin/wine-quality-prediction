import streamlit as st
import pandas as pd
import plotly.express as px

from utils.predict import predict_wine_quality_hybrid
from utils.data import load_example_wines


# ---- Page Configuration ----
st.set_page_config(
    page_title='Wine Quality Predictor',
    page_icon='🥂',
    layout='centered',
    initial_sidebar_state='expanded'
)

# ---- Helper Functions ----
def get_color_hex(emoji):
    return {
        '🟢': '#2ecc71',
        '🟠': '#f1c40f',
        '🔴': '#e74c3c'
    }.get(emoji, '#cccccc')

def get_quality_analysis(input_data):
    analysis = []
    
    # Alcohol Content Analysis
    alc = input_data['Alc']
    IDEAL_MIN = 11.7  
    IDEAL_MAX = 12.7  

    if IDEAL_MIN <= alc <= IDEAL_MAX:
        analysis.append((
            '🟢 Alcohol', 
            f'{alc}% (Ideal) -  Tune between 11.7% - 12.7% to optimize quality'
        ))
    elif 10.5 <= alc < IDEAL_MIN:
        analysis.append((
            '🟠 Alcohol', 
            f'{alc}% (Slightly Low) - Actions:'
            '• Extend fermentation time '
        ))
    elif alc < 10.5:
        analysis.append((
            '🔴 Alcohol', 
            f'{alc}% (Low) - Actions:'
            '• Check sugar levels pre-fermentation '
            '• Verify yeast alcohol tolerance '
        ))
    elif IDEAL_MAX < alc <= 14.1:
        analysis.append((
            '🟠 Alcohol', 
            f'{alc}% (Slightly High) - Actions:'
            '• Reduce sugar concentration in must '
            '• Adjust fermentation temperature '
        ))
    else:
        analysis.append((
            '🔴 Alcohol', 
            f'{alc}% (Excessive) - Actions:'
            '• Verify measurement accuracy '
            '• Consider reverse osmosis reduction '
        ))

        # Volatile Acidity Analysis
    va = input_data['VA']
    IDEAL_MIN = 0.25
    IDEAL_MAX = 0.29

    if IDEAL_MIN <= va <= IDEAL_MAX:
        analysis.append((
            '🟢 Volatile Acidity', 
            f'{va:.2f}g/L (Ideal) - Ideal for complexity.'
        ))
    elif 0.22 <= va < IDEAL_MIN:
        analysis.append((
            '🟠 Volatile Acidity', 
            f'{va:.2f}g/L (Slightly Low) - Actions: '
            '• Extend malolactic fermentation '
        ))
    elif va < 0.22:
        analysis.append((
            '🔴 Volatile Acidity', 
            f'{va:.2f}g/L (Low) - Actions: '
            '• Allow slightly warmer fermentation '
        ))
    elif IDEAL_MAX < va <= 0.55:
        analysis.append((
            '🟠 Volatile Acidity', 
            f'{va:.2f}g/L (High) - Actions: '
            '• More frequent topping up '
            '• Lower storage temperatures '
        ))
    else:
        analysis.append((
            '🔴 Volatile Acidity', 
            f'{va:.2f}g/L (Excessive) - Actions: '
            '• Test for microbial spoilage '
            '• Evaluate barrel sanitation procedures '
        ))

    # Chlorides Analysis
    cl = input_data['Cl']
    IDEAL_MIN = 0.030
    IDEAL_MAX = 0.042

    if IDEAL_MIN <= cl <= IDEAL_MAX:
        analysis.append((
            '🟢 Chlorides',
            f'{cl:.4f}g/L (Ideal) - Ideal salinity for balanced mouthfeel.'
        ))
    elif 0.020 <= cl < IDEAL_MIN:
        analysis.append((
            '🟠 Chlorides',
            f'{cl:.4f}g/L (Slightly Low) - Actions: '
            '• Check water sources for low minerals '
            '• Evaluate filtration systems '
        ))
    elif cl < 0.020:
        analysis.append((
            '🟠 Chlorides',
            f'{cl:.4f}g/L (Low) - Actions: '
            '• Verify lab measurement accuracy '
            '• Assess if over-dilution occurred '
        ))
    elif 0.042 < cl <= 0.062:
        analysis.append((
        '🟠 Chlorides',
        f'{cl:.4f}g/L (Slightly High) - Actions: '
        '• Check vineyard irrigation water for salt levels '
        '• Review cleaning protocols '
        ))
    elif cl > 0.062:
        analysis.append((
        '🔴 Chlorides',
        f'{cl:.4f}g/L (Excessive) - Actions: '
        '• Investigate contamination sources '
        '• Assess impact on wine sensory profile '
        ))



    # Free SO2 Analysis
    so2_free = input_data['FSO2']
    IDEAL_MIN = 36
    IDEAL_MAX = 39

    if IDEAL_MIN <= so2_free <= IDEAL_MAX:
        analysis.append((
            '🟢 Free SO₂',
            f'{so2_free} mg/L (Ideal) - Optimal antimicrobial and antioxidant protection. '
        ))
    elif 26 <= so2_free < IDEAL_MIN:
        analysis.append((
            '🟠 Free SO₂',
            f'{so2_free} mg/L (Slightly Low) - Actions: '
            '• Monitor free SO₂ levels regularly to prevent quality loss'
        ))
    elif so2_free < 26:
        analysis.append((
            '🔴 Free SO₂',
            f'{so2_free} mg/L (Low) - Actions: '
            '• Verify pH and adjust SO₂ usage '
            '• Reassess storage conditions '
        ))
    elif IDEAL_MAX < so2_free <= 41:
        analysis.append((
            '🟠 Free SO₂',
            f'{so2_free} mg/L (Slightly High) - Actions: '
            '• Potential harsh aroma '
            '• Monitor closely to avoid exceeding sensory threshold'
        ))
    else:
        analysis.append((
            '🔴 Free SO₂',
            f'{so2_free} mg/L (Excessive) - Actions: '
            '• Risk of strong SO₂ off-odors and flavors '
        ))


    # Total SO2 Analysis
    so2_total = input_data['TSO2']
    IDEAL_MIN = 120
    IDEAL_MAX = 180

    if IDEAL_MIN <= so2_total <= IDEAL_MAX:
        analysis.append((
            '🟢 Total SO₂',
            f'{so2_total} mg/L (Ideal) - Balanced antioxidant efficacy. Tune between 120–180 mg/L to optimize quality'
        ))
    elif 100 <= so2_total < IDEAL_MIN:
        analysis.append((
            '🟠 Total SO₂',
            f'{so2_total} mg/L (Slightly Low) - Actions: '
            '• Store in cooler conditions to preserve free SO₂ '
        ))
    elif so2_total < 100:
        analysis.append((
            '🔴 Total SO₂',
            f'{so2_total} mg/L (Low) - Actions: '
            '• Increase SO₂ dosage '
            '• Monitor closely during aging and distribution '
        ))
    elif IDEAL_MAX < so2_total <= 200:
        analysis.append((
            '🟠 Total SO₂',
            f'{so2_total} mg/L (Slightly High) - Actions: '
            '• Aerate to reduce free SO₂ levels '
        ))
    else:
        analysis.append((
            '🔴 Total SO₂',
            f'{so2_total} mg/L (Excessive) - Actions: '
            '• Halt SO₂ additions immediately '
        ))


    # Fixed Acidity Analysis
    fa = input_data['FA']
    IDEAL_MIN = 7.1
    IDEAL_MAX = 7.4

    if IDEAL_MIN <= fa <= IDEAL_MAX:
        analysis.append((
            '🟢 Fixed Acidity',
            f'{fa:.1f} g/L (Ideal) - Optimal crispness and freshness. '
        ))
    elif 6.2 <= fa < IDEAL_MIN:
        analysis.append((
            '🟠 Fixed Acidity',
            f'{fa:.1f} g/L (Slightly Low) - Actions: '
            '• Consider acid adjustments to improve vibrancy '
        ))
    elif fa < 6.2:
        analysis.append((
            '🔴 Fixed Acidity',
            f'{fa:.1f} g/L (Low) - Actions: '
            '• Risk of oxidation and short shelf life '
            '• Review acid management'
        ))
    elif IDEAL_MAX < fa <= 9.1:
        analysis.append((
            '🟠 Fixed Acidity',
            f'{fa:.1f} g/L (High) - Actions: '
            '• Consider balancing with sugar '
            '• Watch for potential influence on fermentation and yeast health'
        ))
    else:
        analysis.append((
            '🔴 Fixed Acidity',
            f'{fa:.1f} g/L (Excessive) - Actions: '
            '• Excess acidity may overpower delicate aromas and flavors '
            '• Immediate correction recommended'
        ))



    return analysis

# ---- Title Section ----
st.title('🥂 Wine Quality Classifier')

with st.expander("ℹ️ About this app"):
    st.markdown('''
    - This tool uses a **hybrid model**: Random Forest for medium-quality detection and Decision Tree for identifying low/high quality wines.
    - Input chemical measurements and get **instant predictions with quality breakdowns**.
    - [🔗 View source on GitHub](https://github.com/your-username/wine-quality-predictor)
    ''')


# ---- Sample Data Section ----
with st.expander('📊 Database Examples', expanded=False):
    samples = load_example_wines()
    formatted_samples = samples.round({
        'FSO2': 1,
        'VA': 2,
        'Cl': 4,
        'Alc': 1
    })
    st.dataframe(formatted_samples, use_container_width=True)

# ---- Input Section ----
st.header('🔧 Input Parameters')


col1, col2 = st.columns(2)
with col1:
    Alc = st.slider('Alcohol (% vol)', 8.0, 15.0, 11.5, 0.1,format="%.1f",
                        help='Alcohol is a key byproduct of fermentation that adds body, warmth, and sweetness to wine. Higher alcohol levels are often linked to better perceived quality.')
    Cl = st.slider('Chlorides (g/L)',  0.010, 0.170, 0.050, 0.001,format="%.3f",
                        help='Chlorides represent salt content, affecting the wines salinity and stability. High concentrations can lead to harshness or spoilage.')
    TSO2 = st.slider('Total SO₂ (mg/L)', 20, 350, 140, 1,
                        help='Total SO₂ acts as a key preservative for wines shelf life. Excessive levels can cause harsh flavors, while moderate levels support stability and freshness.')

with col2:
    VA = st.slider('Volatile Acidity (g/L)', 0.10, 0.70, 0.3, 0.01,
                                 help='Volatile acidity refers mainly to acetic acid (vinegar) that can arise from microbial spoilage. Lower levels are ideal, as higher values negatively impact aroma and taste.')
    FSO2 = st.slider('Free SO₂ (mg/L)', 5, 90, 40, 1,
                                    help='Free SO₂ is an active preservative that protects wine from oxidation and microbial spoilage. In optimal ranges it helps to preserve freshness without causing off-flavors.')
    FA = st.slider('Fixed Acidity (g/L)', 3.0, 15.0, 7.4, 0.1,format="%.1f",
                              help='Fixed acidity consists mainly of tartaric acid, contributing to the wine’s crispness and structure. Moderate levels enhance freshness, while too much can make wine taste overly sharp.')

    
    

input_data = {
    'Alc': Alc,
    'Cl': Cl,
    'TSO2': TSO2,
    'VA': VA,
    'FSO2': FSO2,
    'FA': FA
}


# ---- Prediction Section ----
st.markdown('---')

if st.button('Analyze Wine Quality', use_container_width=True):
    with st.spinner('Analyzing chemical composition...'):
        pred_label, rf_conf, dt_conf = predict_wine_quality_hybrid(input_data)
        quality_analysis = get_quality_analysis(input_data)

    st.header('🎯 Prediction Results')
    
    # Create columns for side-by-side layout
    col1, col2 = st.columns([3, 2])
    
    with col1:
        # Prediction Card
        quality_map = {
            0: ('Low Quality', '❌', '#ff4b4b'),
            1: ('Medium Quality', '⚠️', '#ffd700'),
            2: ('High Quality', '✅', '#2ecc71')
        }
        label_text, icon, color = quality_map[pred_label]
        
        st.markdown(f'''
        <div style="
            text-align: center;
            padding: 2.7rem;
            margin: 0.5rem 0;
            border-radius: 0.5rem;
            background: {color}10;
        ">
            <h2 style="color: {color}; margin: 0;">{icon} {label_text}</h2>
        </div>
        ''', unsafe_allow_html=True)

    with col2:
        # Model Confidence
        model_name = 'Decision Tree' if pred_label in [0, 2] else 'Random Forest'
        confidence = (dt_conf if pred_label in [0, 2] else rf_conf) * 100
        
        st.markdown('''
        <div style="
            text-align: center;
            padding: 0.0rem 0;
            margin: 0.0rem 0;
        ">
        ''', unsafe_allow_html=True)
        st.metric("Model Used", model_name)
        st.metric("Confidence", f"{confidence:.1f}%")
        st.markdown('</div>', unsafe_allow_html=True)

    # Quality Factors
    st.header('✅ Improvement Suggestions')
    
    cols = st.columns(2)
    for i, (factor, message) in enumerate(quality_analysis):
        with cols[i % 2]:
            st.markdown(f'''
            <div style="
                padding: 1rem;
                margin: 0.5rem 0;
                border-radius: 0.25rem;
                background: #0E1117,
                color: white;
            ">
                <strong>{factor}</strong><br>
                {message}
            </div>
            ''', unsafe_allow_html=True)


# ---- Footer ----
st.markdown('---')
st.markdown("""
<div style="text-align: center; font-size: 0.85em; color: gray; padding: 1rem 0;">
    🍇 Powered by <strong>UCI Wine Dataset</strong> · Hybrid Model: <strong>Random Forest + Decision Tree</strong>
</div>
""", unsafe_allow_html=True)