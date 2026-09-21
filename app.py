import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="CDC Cardiovascular Health Risk Dashboard",
    page_icon="🫀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 0rem;
    }
    .sub-header {
        font-size: 1.0rem;
        color: #64748B;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. DATA LOADING & CACHING
# -----------------------------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("heart_2020_cleaned.csv")
    # Numerical indicator for calculation convenience
    df['HeartDisease_Num'] = (df['HeartDisease'] == 'Yes').astype(int)
    return df

try:
    df = load_data()
except Exception as e:
    st.error("⚠️ Could not load `heart_2020_cleaned.csv`. Please ensure the file is placed in the same directory as this script.")
    st.stop()

# Overall baseline calculations
baseline_prevalence = df['HeartDisease_Num'].mean() * 100

# -----------------------------------------------------------------------------
# 3. SIDEBAR CONTROLS & FILTERS
# -----------------------------------------------------------------------------
st.sidebar.header("🫀 Cohort Filter Panel")
st.sidebar.write("Customize patient demographics to analyze targeted sub-populations.")

# Age Category Filter
age_order = ['18-24', '25-29', '30-34', '35-39', '40-44', '45-49', 
             '50-54', '55-59', '60-64', '65-69', '70-74', '75-79', '80 or older']
selected_ages = st.sidebar.multiselect(
    "Age Categories",
    options=age_order,
    default=age_order
)

# Sex Filter
selected_sex = st.sidebar.multiselect(
    "Sex",
    options=sorted(df['Sex'].unique()),
    default=df['Sex'].unique()
)

# Smoking Status
selected_smoking = st.sidebar.multiselect(
    "Smoking Status",
    options=sorted(df['Smoking'].unique()),
    default=df['Smoking'].unique()
)

# Diabetic Status
selected_diabetic = st.sidebar.multiselect(
    "Diabetic Status",
    options=sorted(df['Diabetic'].unique()),
    default=df['Diabetic'].unique()
)

# BMI Range
min_bmi, max_bmi = int(df['BMI'].min()), int(df['BMI'].max())
selected_bmi = st.sidebar.slider(
    "BMI Range",
    min_value=min_bmi,
    max_value=max_bmi,
    value=(min_bmi, max_bmi)
)

# Filter Dataset based on sidebar selections
filtered_df = df[
    (df['AgeCategory'].isin(selected_ages)) &
    (df['Sex'].isin(selected_sex)) &
    (df['Smoking'].isin(selected_smoking)) &
    (df['Diabetic'].isin(selected_diabetic)) &
    (df['BMI'] >= selected_bmi[0]) &
    (df['BMI'] <= selected_bmi[1])
]

if filtered_df.empty:
    st.warning("No records match the selected filter criteria. Please adjust your filters.")
    st.stop()

# -----------------------------------------------------------------------------
# 4. MAIN HEADER & TOP KPI CARDS
# -----------------------------------------------------------------------------
st.markdown("<div class='main-header'>CDC Cardiovascular Health Risk Dashboard</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>Executive Analytics & Risk Factor Profiling (BRFSS 2020 Dataset)</div>", unsafe_allow_html=True)

total_count = len(filtered_df)
heart_disease_count = filtered_df['HeartDisease_Num'].sum()
cohort_prevalence = filtered_df['HeartDisease_Num'].mean() * 100
delta_prevalence = cohort_prevalence - baseline_prevalence

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Selected Population Size", value=f"{total_count:,}")

with col2:
    st.metric(label="Heart Disease Cases", value=f"{heart_disease_count:,}")

with col3:
    st.metric(
        label="Cohort Prevalence", 
        value=f"{cohort_prevalence:.2f}%", 
        delta=f"{delta_prevalence:+.2f}% vs CDC Baseline",
        delta_color="inverse"
    )

with col4:
    st.metric(label="CDC Baseline Prevalence", value=f"{baseline_prevalence:.2f}%")

st.markdown("---")

# -----------------------------------------------------------------------------
# 5. INTERACTIVE ANALYSIS TABS
# -----------------------------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Demographic Drivers", 
    "🚬 Lifestyle & Comorbidity Factors", 
    "🎯 Interactive Risk Profiler", 
    "📋 Data Explorer & Export"
])

# -----------------------------------------------------------------------------
# TAB 1: DEMOGRAPHIC DRIVERS
# -----------------------------------------------------------------------------
with tab1:
    st.subheader("Heart Disease Prevalence by Demographics")
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        # Prevalence by Age Category
        age_prev = (
            filtered_df.groupby('AgeCategory')['HeartDisease_Num']
            .mean()
            .reset_index()
        )
        age_prev['Prevalence (%)'] = age_prev['HeartDisease_Num'] * 100
        
        # Ensure age sorting
        age_prev['AgeCategory'] = pd.Categorical(age_prev['AgeCategory'], categories=age_order, ordered=True)
        age_prev = age_prev.sort_values('AgeCategory')
        
        fig_age = px.bar(
            age_prev, 
            x='AgeCategory', 
            y='Prevalence (%)',
            title='Prevalence Rate by Age Category (%)',
            text_auto='.1f',
            color='Prevalence (%)',
            color_continuous_scale='Reds'
        )
        fig_age.update_layout(xaxis_title="Age Category", yaxis_title="Prevalence (%)", showlegend=False)
        st.plotly_chart(fig_age, use_container_width=True)

    with col_right:
        # Prevalence by Sex & Race
        sex_race_prev = (
            filtered_df.groupby(['Race', 'Sex'])['HeartDisease_Num']
            .mean()
            .reset_index()
        )
        sex_race_prev['Prevalence (%)'] = sex_race_prev['HeartDisease_Num'] * 100
        
        fig_race = px.bar(
            sex_race_prev, 
            x='Race', 
            y='Prevalence (%)', 
            color='Sex',
            barmode='group',
            title='Prevalence Rate by Race and Sex (%)',
            text_auto='.1f',
            color_discrete_map={'Female': '#1f77b4', 'Male': '#d62728'}
        )
        fig_race.update_layout(xaxis_title="Race/Ethnicity", yaxis_title="Prevalence (%)")
        st.plotly_chart(fig_race, use_container_width=True)

# -----------------------------------------------------------------------------
# TAB 2: LIFESTYLE & COMORBIDITIES
# -----------------------------------------------------------------------------
with tab2:
    st.subheader("Behavioral & Clinical Risk Factors")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        # Stroke Impact
        stroke_prev = filtered_df.groupby('Stroke')['HeartDisease_Num'].mean().reset_index()
        stroke_prev['Prevalence (%)'] = stroke_prev['HeartDisease_Num'] * 100
        
        fig_stroke = px.bar(
            stroke_prev,
            x='Stroke',
            y='Prevalence (%)',
            color='Stroke',
            title='Impact of Prior Stroke History on Prevalence',
            text_auto='.1f',
            color_discrete_map={'No': '#7f7f7c', 'Yes': '#d62728'}
        )
        fig_stroke.update_layout(showlegend=False)
        st.plotly_chart(fig_stroke, use_container_width=True)

    with col_b:
        # Difficulty Walking Impact
        walk_prev = filtered_df.groupby('DiffWalking')['HeartDisease_Num'].mean().reset_index()
        walk_prev['Prevalence (%)'] = walk_prev['HeartDisease_Num'] * 100
        
        fig_walk = px.bar(
            walk_prev,
            x='DiffWalking',
            y='Prevalence (%)',
            color='DiffWalking',
            title='Impact of Difficulty Walking on Prevalence',
            text_auto='.1f',
            color_discrete_map={'No': '#7f7f7c', 'Yes': '#d62728'}
        )
        fig_walk.update_layout(showlegend=False)
        st.plotly_chart(fig_walk, use_container_width=True)

    # General Health Self-Assessment vs Prevalence
    gen_order = ['Poor', 'Fair', 'Good', 'Very good', 'Excellent']
    gen_prev = filtered_df.groupby('GenHealth')['HeartDisease_Num'].mean().reset_index()
    gen_prev['Prevalence (%)'] = gen_prev['HeartDisease_Num'] * 100
    gen_prev['GenHealth'] = pd.Categorical(gen_prev['GenHealth'], categories=gen_order, ordered=True)
    gen_prev = gen_prev.sort_values('GenHealth')
    
    fig_gen = px.line(
        gen_prev,
        x='GenHealth',
        y='Prevalence (%)',
        markers=True,
        title='Prevalence vs Self-Reported General Health Rating',
        line_shape='linear'
    )
    fig_gen.update_traces(line_color='#d62728', line_width=3, marker_size=10)
    st.plotly_chart(fig_gen, use_container_width=True)

# -----------------------------------------------------------------------------
# TAB 3: INTERACTIVE RISK PROFILER
# -----------------------------------------------------------------------------
with tab3:
    st.subheader("Individual Risk Assessment Calculator")
    st.write("Select patient parameters to calculate empirical cohort risk based on historical survey data.")
    
    p_col1, p_col2, p_col3 = st.columns(3)
    
    with p_col1:
        p_age = st.selectbox("Patient Age Category", options=age_order, index=8) # Default 60-64
        p_sex = st.selectbox("Patient Sex", options=['Male', 'Female'])
        p_smoking = st.selectbox("Smoker?", options=['Yes', 'No'])
        
    with p_col2:
        p_diabetic = st.selectbox("Diabetic?", options=['Yes', 'No'])
        p_stroke = st.selectbox("History of Stroke?", options=['No', 'Yes'])
        p_diffwalk = st.selectbox("Difficulty Walking?", options=['No', 'Yes'])
        
    with p_col3:
        p_genhealth = st.selectbox("General Health Assessment", options=gen_order, index=2)
        p_kidney = st.selectbox("Kidney Disease?", options=['No', 'Yes'])
        p_physical = st.selectbox("Physically Active?", options=['Yes', 'No'])

    # Find matching cohort in full dataset
    match = df[
        (df['AgeCategory'] == p_age) &
        (df['Sex'] == p_sex) &
        (df['Smoking'] == p_smoking) &
        (df['Diabetic'] == p_diabetic) &
        (df['Stroke'] == p_stroke) &
        (df['DiffWalking'] == p_diffwalk)
    ]
    
    st.markdown("---")
    
    if len(match) > 10:
        emp_risk = match['HeartDisease_Num'].mean() * 100
        st.success(f"**Calculated Cohort Risk Rate:** **{emp_risk:.1f}%** (Based on {len(match):,} matching CDC respondents)")
        
        # Risk gauge chart
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = emp_risk,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Estimated Heart Disease Risk (%)"},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "#d62728"},
                'steps': [
                    {'range': [0, 10], 'color': "lightgreen"},
                    {'range': [10, 25], 'color': "yellow"},
                    {'range': [25, 100], 'color': "pink"}
                ],
                'threshold': {
                    'line': {'color': "black", 'width': 4},
                    'thickness': 0.75,
                    'value': baseline_prevalence
                }
            }
        ))
        fig_gauge.update_layout(height=280)
        st.plotly_chart(fig_gauge, use_container_width=True)
    else:
        st.info("Insufficient matching records for this precise combination. Try broadening cohort criteria.")

# -----------------------------------------------------------------------------
# TAB 4: DATA EXPLORER & EXPORT
# -----------------------------------------------------------------------------
with tab4:
    st.subheader("Filtered Dataset View")
    st.write(f"Showing {len(filtered_df):,} records matching sidebar criteria.")
    
    st.dataframe(filtered_df.drop(columns=['HeartDisease_Num']).head(100), use_container_width=True)
    
    # Download CSV Button
    csv = filtered_df.drop(columns=['HeartDisease_Num']).to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Dataset as CSV",
        data=csv,
        file_name="filtered_heart_disease_data.csv",
        mime="text/csv"
    )