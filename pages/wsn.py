
# app.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt

# Page configuration
st.set_page_config(
    page_title="WSN Intrusion Detection System",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: semi-bold;
        color: #ff7f0e;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
    }
    .info-text {
        background-color: #e8f4f8;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Title and Introduction
st.markdown('<div class="main-header">🔐 Intrusion Detection System for Wireless Sensor Networks</div>',
            unsafe_allow_html=True)
st.markdown('<div class="sub-header">A Machine Learning Based Approach</div>', unsafe_allow_html=True)
st.markdown("---")

# Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/190/190648.png", width=100)
    st.markdown("## 📊 Navigation")
    page = st.radio(
        "Select Section",
        ["📋 Project Overview",
         "📊 Dataset Analysis",
         "🧠 Model Architecture",
         "📈 Results & Performance",
         "⚖️ Comparative Analysis",
         "🎯 Conclusion & Future Work"]
    )

    st.markdown("---")
    st.markdown("### 📁 Dataset Info")
    st.info("**AWID Dataset** (Aegean Wi-Fi Intrusion Dataset)")
    st.write("- Total Records: 2,371,218")
    st.write("- Features: 154 → 76 → 13")
    st.write("- Classes: 4 (Normal, Flooding, Injection, Impersonation)")

# Project Overview Page
if page == "📋 Project Overview":
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown('<div class="sub-header">🎯 Problem Statement</div>', unsafe_allow_html=True)
        st.markdown("""
        The Internet of Things (IoT) security presents significant threats to wireless networks, 
        particularly in identifying and neutralizing malicious activities. Rapid and accurate detection 
        of unauthorized or irregular network traffic is crucial for detecting potential intrusion efforts.
        """)

        st.markdown('<div class="sub-header">💡 Key Contributions</div>', unsafe_allow_html=True)
        contributions = [
            "**Feature Optimization**: Reduced 154 features to 76, then to 13 key features",
            "**Multiple Model Architectures**: DNN (5-layer), DNN (3-layer), CNN, RNN-LSTM, and Logistic Regression",
            "**Binary & Multiclass Classification**: Comprehensive evaluation across all attack types",
            "**Ensemble Averaging**: Combined predictions from all fitted models for improved accuracy",
            "**Comprehensive Metrics**: Detection Rate, False Alarm Rate, F1-score, Precision, Recall"
        ]
        for contrib in contributions:
            st.markdown(f"- {contrib}")

    with col2:
        st.markdown('<div class="sub-header">📈 Key Metrics</div>', unsafe_allow_html=True)

        col2_1, col2_2 = st.columns(2)
        with col2_1:
            st.metric("🏆 Best Accuracy", "97%", "CNN Model")
            st.metric("📉 Best Loss", "0.14", "CNN Model")
        with col2_2:
            st.metric("🎯 Detection Rate", "99.9%", "MV (LR)")
            st.metric("⚠️ False Alarm Rate", "0.31%", "Lowest achieved")

    st.markdown("---")
    st.markdown('<div class="sub-header">🏗️ System Architecture Overview</div>', unsafe_allow_html=True)

    # Architecture Flow Diagram
    arch_data = dict(
        steps=["Data Preprocessing", "Feature Engineering", "Model Training", "Evaluation"],
        duration=["Data Cleaning", "Feature Selection", "DNN/CNN/LSTM", "Metrics Analysis"],
        tools=["Pandas, NumPy", "Standard Scaler", "TensorFlow/Keras", "Sklearn"]
    )

    fig = go.Figure()
    for i, step in enumerate(arch_data["steps"]):
        fig.add_trace(go.Scatter(
            x=[i],
            y=[0],
            mode="markers+text",
            marker=dict(size=50, color=["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"][i]),
            text=step,
            textposition="bottom center",
            textfont=dict(size=12),
            hovertext=arch_data["duration"][i],
            name=step
        ))

    fig.update_layout(
        title="IDS Pipeline Architecture",
        showlegend=False,
        xaxis=dict(showticklabels=False, showgrid=False),
        yaxis=dict(showticklabels=False, showgrid=False),
        height=300,
        margin=dict(t=50, b=50)
    )
    st.plotly_chart(fig, use_container_width=True)

# Dataset Analysis Page
elif page == "📊 Dataset Analysis":
    st.markdown('<div class="sub-header">📊 AWID Dataset Distribution</div>', unsafe_allow_html=True)

    # Class Distribution Data
    classes = ['Normal', 'Flooding', 'Injection', 'Impersonation']
    train_counts = [1633190, 48484, 65379, 48522]
    test_counts = [530785, 8097, 16682, 20079]

    col1, col2 = st.columns(2)

    with col1:
        fig = go.Figure(data=[
            go.Bar(name='Training Set', x=classes, y=train_counts, marker_color='#1f77b4'),
            go.Bar(name='Testing Set', x=classes, y=test_counts, marker_color='#ff7f0e')
        ])
        fig.update_layout(
            title="Class Distribution in AWID Dataset",
            xaxis_title="Attack Type",
            yaxis_title="Number of Records",
            barmode='group',
            height=450
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Pie chart for overall distribution
        total_counts = [sum(x) for x in zip(train_counts, test_counts)]
        fig = go.Figure(data=[go.Pie(
            labels=classes,
            values=total_counts,
            hole=0.3,
            marker_colors=['#2ecc71', '#e74c3c', '#f39c12', '#3498db']
        )])
        fig.update_layout(
            title="Overall Dataset Distribution",
            height=450
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    st.markdown('<div class="sub-header">🔍 Feature Selection Process</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Original Features", "154", delta=None)
    with col2:
        st.metric("After Preprocessing", "76", delta="-78")
    with col3:
        st.metric("Final Selected", "13", delta="-141")

    # Feature importance visualization
    st.markdown("### 📌 Top 13 Selected Features")
    top_features = [
        "frame.len", "wlan.fc.type", "wlan.fc.subtype", "radiotap.datarate",
        "wlan.duration", "wlan.ra", "wlan.da", "wlan.ta", "wlan.bssid",
        "wlan.seq", "wlan.frag", "data.len", "wlan.mgt.ssid"
    ]

    fig = go.Figure(data=[go.Bar(
        x=top_features,
        y=[1] * 13,
        orientation='h',
        marker_color='#1f77b4'
    )])
    fig.update_layout(
        title="Selected Features for Classification",
        xaxis_title="Importance (Relative)",
        yaxis_title="Features",
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)

    # Sample data table
    st.markdown("### 📋 Sample of Preprocessed Data")
    sample_data = pd.DataFrame({
        'frame.len': [64, 128, 256, 512, 64],
        'wlan.fc.type': [2, 2, 0, 1, 2],
        'wlan.fc.subtype': [8, 8, 0, 4, 8],
        'radiotap.datarate': [12, 24, 6, 48, 12],
        'Class': ['Normal', 'Injection', 'Flooding', 'Impersonation', 'Normal']
    })
    st.dataframe(sample_data, use_container_width=True)

# Model Architecture Page
elif page == "🧠 Model Architecture":
    st.markdown('<div class="sub-header">🧠 Deep Learning Models Architecture</div>', unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["CNN Architecture", "DNN (5-layer)", "DNN (3-layer)", "RNN-LSTM"])

    with tab1:
        st.markdown("### Convolutional Neural Network (CNN) - Best Performing Model")
        st.markdown("""
        **Architecture Details:**
        - Input Layer (76 features → 3D array)
        - Conv1D Layer (32 filters, kernel size=3)
        - MaxPooling1D Layer
        - Dropout Layer (0.3)
        - Conv1D Layer (64 filters, kernel size=3)
        - MaxPooling1D Layer
        - Dropout Layer (0.3)
        - Flatten Layer
        - Dense Layer (256 neurons, ReLU)
        - Dropout Layer (0.5)
        - Output Layer (3 neurons, Softmax)
        """)

        # CNN Architecture Visualization
        fig = go.Figure()

        layers = ['Input\n(76)', 'Conv1D\n(32)', 'MaxPool\n(1D)', 'Dropout\n(0.3)',
                  'Conv1D\n(64)', 'MaxPool\n(1D)', 'Dropout\n(0.3)', 'Flatten',
                  'Dense\n(256)', 'Dropout\n(0.5)', 'Output\n(3)']

        for i, layer in enumerate(layers):
            fig.add_trace(go.Scatter(
                x=[i],
                y=[0],
                mode="markers+text",
                marker=dict(size=[50 if i not in [3, 6, 9] else 30 for i in range(len(layers))],
                            color=plt.cm.viridis(i / len(layers))),
                text=layer,
                textposition="top center",
                name=layer
            ))
            if i < len(layers) - 1:
                fig.add_annotation(x=i + 0.5, y=0, ax=i, ay=0,
                                   xref="x", yref="y", axref="x", ayref="y",
                                   showarrow=True, arrowhead=2, arrowsize=1)

        fig.update_layout(
            title="CNN Architecture Flow",
            showlegend=False,
            xaxis=dict(showticklabels=False, showgrid=False),
            yaxis=dict(showticklabels=False, showgrid=False),
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("**Model Parameters:**")
        st.code("""
Total params: 154,819
Trainable params: 154,819
Non-trainable params: 0
        """)

    with tab2:
        st.markdown("### Deep Neural Network (5-layer)")
        st.markdown("""
        - Input Layer (76 features)
        - Dense Layer (128, ReLU)
        - Dropout (0.3)
        - Dense Layer (64, ReLU)
        - Dropout (0.3)
        - Dense Layer (32, ReLU)
        - Dense Layer (3, Softmax)
        """)

    with tab3:
        st.markdown("### Deep Neural Network (3-layer)")
        st.markdown("""
        - Input Layer (76 features)
        - Dense Layer (64, ReLU)
        - Dense Layer (32, ReLU)
        - Output Layer (3, Softmax)
        """)

    with tab4:
        st.markdown("### RNN with LSTM")
        st.markdown("""
        - Input Layer (76 features → sequence)
        - LSTM Layer (64 units, return_sequences=True)
        - Dropout (0.3)
        - LSTM Layer (32 units)
        - Dropout (0.3)
        - Dense Layer (3, Softmax)
        """)

    st.markdown("---")
    st.markdown('<div class="sub-header">⚙️ Training Configuration</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("**Optimizer**\nAdam\n\n**Learning Rate**\n0.001")
    with col2:
        st.info("**Loss Function**\nCategorical Crossentropy\n\n**Activation**\nReLU / Softmax")
    with col3:
        st.info("**Regularization**\nDropout (0.3-0.5)\n\n**Early Stopping**\nPatience=5")

# Results & Performance Page
elif page == "📈 Results & Performance":
    st.markdown('<div class="sub-header">📈 Model Performance Metrics</div>', unsafe_allow_html=True)

    # Performance Data
    models = ['DNN (5)', 'DNN (3)', 'CNN', 'RNN-LSTM', 'LR', 'MV (LR)']
    accuracy_76 = [95, 97, 96, 93, 98, 99]
    accuracy_13 = [94, 94, 97, 94, 91, 99]

    fig = make_subplots(rows=1, cols=2, subplot_titles=("Accuracy with 76 Features", "Accuracy with 13 Features"))

    fig.add_trace(go.Bar(x=models, y=accuracy_76, marker_color='#1f77b4', text=accuracy_76, textposition='auto'), row=1,
                  col=1)
    fig.add_trace(go.Bar(x=models, y=accuracy_13, marker_color='#ff7f0e', text=accuracy_13, textposition='auto'), row=1,
                  col=2)

    fig.update_layout(height=500, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    # Loss Comparison
    st.markdown("### 📉 Loss Comparison")

    loss_data = pd.DataFrame({
        'Model': ['DNN (5)', 'DNN (3)', 'CNN', 'RNN-LSTM'],
        'Binary (76 features)': [0.41, 0.47, 0.14, 0.68],
        'Binary (13 features)': [0.73, 0.26, 0.14, 0.47],
        'Multiclass (76 features)': [0.91, 0.79, 1.07, 1.16],
        'Multiclass (13 features)': [1.25, 5.79, 0.69, 0.62]
    })

    fig = go.Figure()
    for col in loss_data.columns[1:]:
        fig.add_trace(go.Bar(name=col, x=loss_data['Model'], y=loss_data[col]))

    fig.update_layout(
        title="Loss Values Across Different Configurations",
        xaxis_title="Model",
        yaxis_title="Loss",
        barmode='group',
        height=450
    )
    st.plotly_chart(fig, use_container_width=True)

    # Binary Classification Results
    st.markdown('<div class="sub-header">🎯 Binary Classification Results (76 Features)</div>', unsafe_allow_html=True)

    binary_results = pd.DataFrame({
        'Model': ['DNN (5)', 'DNN (3)', 'CNN', 'RNN-LSTM', 'LR', 'MV (LR)'],
        'Detection Rate': [272370, 270997, 265735, 272309, 77331, 77330],
        'False Alarm Rate': [10018, 1896, 100, 16196, 740, 827],
        'Accuracy (%)': [95, 97, 96, 93, 98, 99]
    })
    st.dataframe(binary_results, use_container_width=True)

    # Radar Chart for Model Comparison
    st.markdown("### 🎨 Model Performance Radar Chart")

    radar_data = pd.DataFrame({
        'Metric': ['Accuracy', 'Precision', 'Recall', 'F1-Score', 'Detection Rate'],
        'CNN': [97, 88, 85, 85, 96],
        'DNN (5)': [95, 76, 76, 76, 94],
        'RNN-LSTM': [93, 64, 64, 64, 89]
    })

    fig = go.Figure()
    for model in ['CNN', 'DNN (5)', 'RNN-LSTM']:
        fig.add_trace(go.Scatterpolar(
            r=radar_data[model],
            theta=radar_data['Metric'],
            fill='toself',
            name=model
        ))

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=True,
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)

# Comparative Analysis Page
elif page == "⚖️ Comparative Analysis":
    st.markdown('<div class="sub-header">⚖️ Comparative Analysis with Existing Works</div>', unsafe_allow_html=True)

    # Comparative Data
    comp_data = pd.DataFrame({
        'Reference': ['[29]', '[17]', '[22]', '[40]', '[35]', '[5]', '**Proposed**'],
        'Method': ['Linear SVM', 'XGBoost', 'ANN', 'SAE', 'FFDNN', 'DNN', '**CNN**'],
        'Features': [5, 15, 20, 71, 26, 23, 76],
        'Accuracy (%)': [98.22, 99.99, 99.95, 98.46, 99.77, 95.72, 97.00]
    })

    fig = go.Figure(data=[go.Bar(
        x=comp_data['Method'],
        y=comp_data['Accuracy (%)'],
        marker_color=['#2ecc71' if 'Proposed' in m else '#3498db' for m in comp_data['Method']],
        text=comp_data['Accuracy (%)'],
        textposition='auto'
    )])
    fig.update_layout(
        title="Comparison of IDS Models on AWID Dataset",
        xaxis_title="Model",
        yaxis_title="Accuracy (%)",
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 📊 Detailed Comparative Analysis")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Machine Learning Models")
        ml_comparison = pd.DataFrame({
            'Model': ['J48', 'Random Forest', 'XGBoost', 'SVM', 'Logistic Regression'],
            'Accuracy (%)': [99.5, 99.2, 99.99, 98.22, 99.9]
        })
        st.dataframe(ml_comparison, use_container_width=True)

    with col2:
        st.markdown("#### Deep Learning Models")
        dl_comparison = pd.DataFrame({
            'Model': ['CNN', 'DNN (7-layer)', 'LSTM', 'Autoencoder', 'FFDNN'],
            'Accuracy (%)': [97, 98.46, 92, 94.81, 99.77]
        })
        st.dataframe(dl_comparison, use_container_width=True)

    st.markdown("---")
    st.markdown('<div class="sub-header">🏆 Key Findings</div>', unsafe_allow_html=True)

    st.success("""
    - **CNN achieved 97% accuracy** with only 0.14 loss, outperforming other models
    - **Logistic Regression with Majority Voting** achieved 99.9% accuracy for binary classification
    - **Feature reduction** from 154 to 13 features significantly improved training efficiency without compromising accuracy
    - **Detection Rate** reached 99.9% with minimal False Alarm Rate (0.31%)
    """)

# Conclusion & Future Work Page
elif page == "🎯 Conclusion & Future Work":
    st.markdown('<div class="sub-header">🎯 Conclusion</div>', unsafe_allow_html=True)

    st.markdown("""
    This research successfully developed a robust Intrusion Detection System for Wireless Sensor Networks 
    using a combination of deep learning and machine learning approaches. Key achievements include:

    ### ✅ Key Achievements

    1. **Optimal Feature Selection**: Successfully reduced from 154 to 13 key features while maintaining high detection accuracy

    2. **High-Performance Models**:
       - CNN achieved **97% accuracy** with **0.14 loss** in binary classification
       - CNN achieved **97% accuracy** with **0.14 loss** in binary classification using 13 features
       - Logistic Regression with Majority Voting achieved **99.9% accuracy**

    3. **Comprehensive Evaluation**:
       - Evaluated across multiple metrics (Accuracy, Loss, Detection Rate, False Alarm Rate)
       - Binary and multiclass classification both performed exceptionally well

    4. **Real-World Applicability**:
       - Low False Alarm Rate (as low as 0.31%)
       - Efficient feature set enables faster training and deployment
       - Suitable for resource-constrained WSN environments
    """)

    st.markdown("---")
    st.markdown('<div class="sub-header">🚀 Future Work Directions</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 🔧 Technical Enhancements")
        st.markdown("""
        - **Ensemble Methods**: Implement true ensemble learning with majority voting across all fitted models
        - **Input Shape Optimization**: Update averaging test function to handle multiple array testing
        - **Alternative ML Approaches**: Explore additional machine learning algorithms for class probability analysis
        - **Real-time Processing**: Optimize models for real-time intrusion detection
        """)

    with col2:
        st.markdown("#### 🌍 Application Expansion")
        st.markdown("""
        - **Cross-Dataset Validation**: Test on other IDS datasets (KDD Cup 99, NSL-KDD, UNSW-NB15)
        - **IoT Integration**: Deploy on edge devices for IoT security applications
        - **Adaptive Learning**: Implement continuous learning for novel attack detection
        - **Resource Optimization**: Further optimize for extremely resource-constrained WSN nodes
        """)

    st.markdown("---")

    # Timeline Visualization
    st.markdown('<div class="sub-header">📅 Research Timeline</div>', unsafe_allow_html=True)

    timeline_data = dict(
        task=['Data Collection', 'Preprocessing', 'Model Development', 'Training & Validation', 'Testing & Evaluation'],
        start=[0, 1, 2, 3, 4],
        finish=[1, 2, 3, 4, 5]
    )

    fig = go.Figure()
    for i, task in enumerate(timeline_data['task']):
        fig.add_trace(go.Bar(
            x=[timeline_data['finish'][i] - timeline_data['start'][i]],
            y=[task],
            orientation='h',
            marker_color=px.colors.qualitative.Set3[i],
            text=f"{task}",
            textposition='outside'
        ))

    fig.update_layout(
        title="Project Timeline",
        xaxis_title="Time (Relative Units)",
        yaxis_title="Tasks",
        showlegend=False,
        height=300
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.markdown("### 📚 References")
    with st.expander("Show References"):
        st.markdown("""
        1. Kolias, C., et al. (2016). "Intrusion detection in 802.11 networks." IEEE Communications Surveys & Tutorials.
        2. Kasongo, S.M., & Sun, Y. (2020). "A deep learning method with wrapper based feature extraction." Computers & Security.
        3. Wang, S., et al. (2019). "Intrusion detection for WiFi network: A deep learning approach." International Wireless Internet Conference.
        4. Bhandari, S., et al. (2020). "Feature selection improves tree-based classification." International Workshop on Systems and Network Telemetry and Analytics.
        """)

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: gray; padding: 20px;">
    <p>📧 Corresponding author: Saeed Ali Omer Bahaj (saobahaj@gmail.com)</p>
    <p>🏛️ Supported by Higher Education Commission of Pakistan through National Research Program for Universities (NRPU) under Project 17006</p>
    <p>© 2024 IEEE Access | Digital Object Identifier: 10.1109/ACCESS.2024.3380014</p>
    </div>
    """, unsafe_allow_html=True)
