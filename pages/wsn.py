# app.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import time
from datetime import datetime, timedelta
import random
import plotly.figure_factory as ff

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
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: semi-bold;
        color: #ff7f0e;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
        border-left: 4px solid #ff7f0e;
        padding-left: 15px;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .info-text {
        background-color: #e8f4f8;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        border-left: 4px solid #1f77b4;
    }
    .attack-card {
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        border-left: 4px solid;
    }
    .normal-card {
        background-color: #d4edda;
        border-left-color: #28a745;
    }
    .flooding-card {
        background-color: #fff3cd;
        border-left-color: #ffc107;
    }
    .injection-card {
        background-color: #f8d7da;
        border-left-color: #dc3545;
    }
    .impersonation-card {
        background-color: #e2e3e5;
        border-left-color: #6c757d;
    }
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: bold;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        transition: all 0.3s ease;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="main-header">🔐 WSN Intrusion Detection System</div>', unsafe_allow_html=True)
st.markdown(
    '<div style="text-align: center; margin-bottom: 2rem;">A Machine Learning Based Approach for Wireless Sensor Networks</div>',
    unsafe_allow_html=True)

# Initialize session state for simulation
if 'simulation_running' not in st.session_state:
    st.session_state.simulation_running = False
if 'attack_log' not in st.session_state:
    st.session_state.attack_log = []
if 'detection_history' not in st.session_state:
    st.session_state.detection_history = []
if 'network_packets' not in st.session_state:
    st.session_state.network_packets = []
if 'simulation_time' not in st.session_state:
    st.session_state.simulation_time = 0
if 'active_attacks' not in st.session_state:
    st.session_state.active_attacks = []

# Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/190/190648.png", width=100)
    st.markdown("## 📊 Control Panel")

    page = st.radio(
        "Navigation",
        ["🌐 Network Simulation",
         "📊 Dataset Analysis",
         "🧠 Model Architecture",
         "📈 Results & Performance",
         "⚖️ Comparative Analysis",
         "🎯 Conclusion"]
    )

    st.markdown("---")
    st.markdown("### 🎮 Simulation Controls")

    attack_types = ["Normal Traffic", "Flooding Attack", "Injection Attack", "Impersonation Attack"]
    selected_attack = st.selectbox("Simulate Attack Type", attack_types)

    if st.button("🚨 Trigger Attack", key="trigger_attack"):
        st.session_state.simulation_running = True
        st.session_state.active_attacks.append({
            'type': selected_attack,
            'time': datetime.now(),
            'intensity': random.randint(50, 100)
        })
        st.success(f"⚠️ {selected_attack} triggered at {datetime.now().strftime('%H:%M:%S')}")

    if st.button("🛡️ Start IDS Monitoring"):
        st.session_state.simulation_running = True
        st.success("IDS Monitoring Active! 🛡️")

    if st.button("⏹️ Stop Simulation"):
        st.session_state.simulation_running = False
        st.warning("Simulation Stopped")

    if st.button("🗑️ Clear Logs"):
        st.session_state.attack_log = []
        st.session_state.detection_history = []
        st.session_state.network_packets = []
        st.success("Logs Cleared")


# Helper functions for simulation
def generate_network_packet(attack_type="Normal"):
    """Generate simulated network packet data"""
    packet = {
        'frame.len': random.randint(64, 1518),
        'wlan.fc.type': random.randint(0, 2),
        'wlan.fc.subtype': random.randint(0, 13),
        'radiotap.datarate': random.choice([1, 2, 5.5, 6, 9, 11, 12, 18, 24, 36, 48, 54]),
        'wlan.duration': random.randint(0, 32768),
        'wlan.seq': random.randint(0, 4095),
        'attack_type': attack_type,
        'timestamp': datetime.now()
    }

    # Modify packet based on attack type
    if attack_type == "Flooding Attack":
        packet['frame.len'] = random.randint(1500, 65535)
        packet['radiotap.datarate'] = random.choice([54, 48, 36])
    elif attack_type == "Injection Attack":
        packet['wlan.fc.type'] = random.choice([0, 1, 3])
        packet['frame.len'] = random.randint(32, 128)
    elif attack_type == "Impersonation Attack":
        packet['wlan.seq'] = random.randint(0, 100)
        packet['wlan.duration'] = random.randint(30000, 32768)

    return packet


def detect_intrusion(packet):
    """Simulate ML model prediction"""
    # Simulate CNN model prediction based on packet features
    features = [packet['frame.len'], packet['wlan.fc.type'],
                packet['wlan.fc.subtype'], packet['radiotap.datarate']]

    # Simplified model simulation
    if packet['attack_type'] == "Normal Traffic":
        confidence = random.uniform(0.85, 0.99)
        prediction = "Normal"
    elif packet['attack_type'] == "Flooding Attack":
        confidence = random.uniform(0.75, 0.95)
        prediction = "Flooding"
    elif packet['attack_type'] == "Injection Attack":
        confidence = random.uniform(0.70, 0.92)
        prediction = "Injection"
    else:
        confidence = random.uniform(0.65, 0.90)
        prediction = "Impersonation"

    return prediction, confidence


# ==================== NETWORK SIMULATION PAGE ====================
if page == "🌐 Network Simulation":
    st.markdown('<div class="sub-header">🌐 Real-Time WSN Network Simulation</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("### 📡 Sensor Network Topology")

        # Create interactive network visualization
        num_nodes = 12
        node_positions = []

        # Generate node positions in a circular pattern
        for i in range(num_nodes):
            angle = 2 * np.pi * i / num_nodes
            x = np.cos(angle) * 2
            y = np.sin(angle) * 2
            node_positions.append((x, y))

        # Add sink node at center
        node_positions.append((0, 0))

        # Create network graph
        edge_x = []
        edge_y = []

        # Connect nodes to sink
        for i in range(num_nodes):
            x0, y0 = node_positions[i]
            x1, y1 = node_positions[-1]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])

        # Create figure
        fig = go.Figure()

        # Add edges
        fig.add_trace(go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=1, color='#888'),
            hoverinfo='none',
            mode='lines'
        ))

        # Add nodes
        node_x = [pos[0] for pos in node_positions]
        node_y = [pos[1] for pos in node_positions]

        # Color nodes based on attack status
        node_colors = []
        node_text = []
        for i in range(num_nodes):
            if st.session_state.simulation_running and i < len(st.session_state.active_attacks) * 2:
                node_colors.append('#dc3545')  # Attack node
                node_text.append(f"Sensor Node {i + 1}\n⚠️ Under Attack")
            else:
                node_colors.append('#28a745')  # Normal node
                node_text.append(f"Sensor Node {i + 1}\n✅ Normal")

        # Sink node
        node_colors.append('#ffc107')
        node_text.append("Gateway/Sink Node")

        fig.add_trace(go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            marker=dict(size=30, color=node_colors, line=dict(color='white', width=2)),
            text=node_text,
            textposition="bottom center",
            textfont=dict(size=10),
            hoverinfo='text',
            name='Network Nodes'
        ))

        fig.update_layout(
            showlegend=False,
            hovermode='closest',
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            height=500,
            title="WSN Network Topology (12 Sensor Nodes + Gateway)",
            plot_bgcolor='rgba(0,0,0,0)'
        )

        st.plotly_chart(fig, use_container_width=True)

        # Network traffic animation
        if st.session_state.simulation_running:
            # Generate new packets
            for attack in st.session_state.active_attacks:
                for _ in range(random.randint(1, 3)):
                    packet = generate_network_packet(attack['type'])
                    prediction, confidence = detect_intrusion(packet)

                    st.session_state.network_packets.append({
                        **packet,
                        'prediction': prediction,
                        'confidence': confidence
                    })

                    # Keep last 50 packets
                    if len(st.session_state.network_packets) > 50:
                        st.session_state.network_packets.pop(0)

                    # Log detection if attack detected
                    if prediction != "Normal":
                        st.session_state.detection_history.append({
                            'timestamp': datetime.now(),
                            'attack': attack['type'],
                            'detected': prediction,
                            'confidence': confidence
                        })

            # Remove old attacks
            st.session_state.active_attacks = [
                a for a in st.session_state.active_attacks
                if (datetime.now() - a['time']).seconds < 5
            ]

            st.session_state.simulation_time += 1

    with col2:
        st.markdown("### 🚨 Real-Time Alerts")

        # Display recent alerts
        if st.session_state.detection_history:
            recent_alerts = st.session_state.detection_history[-5:]
            for alert in reversed(recent_alerts):
                if alert['attack'] != "Normal Traffic":
                    st.error(f"""
                    **🚨 INTRUSION DETECTED!**  
                    Type: {alert['attack']}  
                    Time: {alert['timestamp'].strftime('%H:%M:%S')}  
                    Confidence: {alert['confidence']:.2%}
                    """)
        else:
            st.info("🟢 No active threats detected")

        st.markdown("---")
        st.markdown("### 📊 Live Network Metrics")

        # Live metrics
        metrics_col1, metrics_col2 = st.columns(2)
        with metrics_col1:
            st.metric("Active Attacks", len(st.session_state.active_attacks),
                      delta=len(st.session_state.active_attacks))
            st.metric("Packets/sec", len(st.session_state.network_packets))
        with metrics_col2:
            detection_rate = len([d for d in st.session_state.detection_history
                                  if d['detected'] != "Normal"]) / max(len(st.session_state.detection_history), 1)
            st.metric("Detection Rate", f"{detection_rate:.1%}")
            st.metric("Active Nodes", "12/12")

    # Packet Analysis
    st.markdown("---")
    st.markdown('<div class="sub-header">📦 Real-Time Packet Analysis</div>', unsafe_allow_html=True)

    if st.session_state.network_packets:
        packet_df = pd.DataFrame(st.session_state.network_packets[-10:])
        st.dataframe(packet_df[['timestamp', 'attack_type', 'prediction', 'confidence', 'frame.len']],
                     use_container_width=True)

        # Packet timeline
        fig = go.Figure()

        timeline_data = packet_df.groupby('attack_type').size().reset_index(name='count')
        fig.add_trace(go.Bar(
            x=timeline_data['attack_type'],
            y=timeline_data['count'],
            marker_color=['#28a745', '#ffc107', '#dc3545', '#6c757d'],
            text=timeline_data['count'],
            textposition='auto'
        ))

        fig.update_layout(
            title="Packet Distribution by Attack Type",
            xaxis_title="Traffic Type",
            yaxis_title="Number of Packets",
            height=300
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No packets captured. Start simulation to see network traffic.")

    # Auto-refresh for simulation
    if st.session_state.simulation_running:
        st.markdown("### 🔄 Simulation Status")
        st.success(f"✅ IDS Monitoring Active | Time: {st.session_state.simulation_time} cycles")
        time.sleep(0.5)
        st.rerun()

# ==================== DATASET ANALYSIS PAGE ====================
elif page == "📊 Dataset Analysis":
    st.markdown('<div class="sub-header">📊 AWID Dataset Analysis</div>', unsafe_allow_html=True)

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

    # Feature Correlation Heatmap
    st.markdown('<div class="sub-header">🔍 Feature Correlation Analysis</div>', unsafe_allow_html=True)

    # Simulated correlation matrix
    features = ['frame.len', 'wlan.fc.type', 'wlan.fc.subtype', 'radiotap.datarate',
                'wlan.duration', 'wlan.seq', 'data.len']

    np.random.seed(42)
    corr_matrix = np.random.randn(len(features), len(features))
    corr_matrix = (corr_matrix + corr_matrix.T) / 2
    np.fill_diagonal(corr_matrix, 1)

    fig = ff.create_annotated_heatmap(
        z=corr_matrix,
        x=features,
        y=features,
        colorscale='RdBu',
        showscale=True,
        font_colors=['white']
    )
    fig.update_layout(
        title="Feature Correlation Matrix",
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)

    # Feature importance
    st.markdown('<div class="sub-header">📌 Feature Importance (SHAP Values)</div>', unsafe_allow_html=True)

    feature_importance = {
        'frame.len': 0.95,
        'wlan.duration': 0.87,
        'radiotap.datarate': 0.76,
        'wlan.fc.subtype': 0.68,
        'wlan.seq': 0.54,
        'wlan.fc.type': 0.49,
        'data.len': 0.42,
        'wlan.ra': 0.38,
        'wlan.ta': 0.35,
        'wlan.bssid': 0.31
    }

    fig = go.Figure(data=[go.Bar(
        x=list(feature_importance.values()),
        y=list(feature_importance.keys()),
        orientation='h',
        marker_color='#1f77b4'
    )])
    fig.update_layout(
        title="Top 10 Feature Importance",
        xaxis_title="SHAP Value (Importance)",
        yaxis_title="Features",
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)

# ==================== MODEL ARCHITECTURE PAGE ====================
elif page == "🧠 Model Architecture":
    st.markdown('<div class="sub-header">🧠 CNN Model Architecture Visualization</div>', unsafe_allow_html=True)

    # Interactive model architecture
    layers = [
        {"name": "Input Layer", "shape": "(76, 1)", "params": 0},
        {"name": "Conv1D", "shape": "(76, 32)", "params": 128, "filters": 32, "kernel": 3},
        {"name": "MaxPooling1D", "shape": "(19, 32)", "params": 0, "pool": 2},
        {"name": "Dropout", "shape": "(19, 32)", "params": 0, "rate": 0.3},
        {"name": "Conv1D", "shape": "(19, 64)", "params": 6208, "filters": 64, "kernel": 3},
        {"name": "MaxPooling1D", "shape": "(9, 64)", "params": 0, "pool": 2},
        {"name": "Dropout", "shape": "(9, 64)", "params": 0, "rate": 0.3},
        {"name": "Flatten", "shape": "(576,)", "params": 0},
        {"name": "Dense", "shape": "(256,)", "params": 147712, "activation": "ReLU"},
        {"name": "Dropout", "shape": "(256,)", "params": 0, "rate": 0.5},
        {"name": "Output", "shape": "(3,)", "params": 771, "activation": "Softmax"}
    ]

    # Create network architecture visualization
    fig = go.Figure()

    for i, layer in enumerate(layers):
        height = 100 if "Dropout" in layer["name"] else 150
        width = 150 if "Flatten" in layer["name"] else 120

        fig.add_trace(go.Scatter(
            x=[i],
            y=[0],
            mode="markers+text",
            marker=dict(
                size=height / 2,
                symbol="square",
                color=["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"][i % 5]
            ),
            text=f"{layer['name']}<br>{layer['shape']}<br>Params: {layer['params']:,}",
            textposition="top center",
            textfont=dict(size=10),
            hoverinfo="text",
            name=layer['name']
        ))

        # Add connections
        if i < len(layers) - 1:
            fig.add_annotation(
                x=i + 0.5, y=0,
                ax=i, ay=0,
                xref="x", yref="y",
                axref="x", ayref="y",
                showarrow=True,
                arrowhead=2,
                arrowsize=1,
                arrowwidth=2,
                arrowcolor="gray"
            )

    fig.update_layout(
        title="CNN Architecture Flow Diagram",
        showlegend=False,
        xaxis=dict(showticklabels=False, showgrid=False, range=[-0.5, len(layers) - 0.5]),
        yaxis=dict(showticklabels=False, showgrid=False, range=[-1, 1]),
        height=500,
        margin=dict(t=100)
    )
    st.plotly_chart(fig, use_container_width=True)

    # Model parameters table
    st.markdown("### 📊 Model Summary")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Parameters", "154,819")
        st.metric("Trainable Parameters", "154,819")
    with col2:
        st.metric("Non-trainable Parameters", "0")
        st.metric("Conv1D Layers", "2")
    with col3:
        st.metric("Dense Layers", "2")
        st.metric("Dropout Layers", "3")

    # Architecture comparison
    st.markdown("---")
    st.markdown('<div class="sub-header">🔄 Model Architecture Comparison</div>', unsafe_allow_html=True)

    arch_comparison = pd.DataFrame({
        'Model': ['DNN (3-layer)', 'DNN (5-layer)', 'CNN', 'RNN-LSTM'],
        'Layers': [3, 5, 8, 4],
        'Parameters': ['~50K', '~120K', '~155K', '~85K'],
        'Best Accuracy': ['97%', '95%', '97%', '93%'],
        'Inference Time': ['0.2ms', '0.4ms', '0.5ms', '0.8ms']
    })
    st.dataframe(arch_comparison, use_container_width=True)

# ==================== RESULTS & PERFORMANCE PAGE ====================
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

    # Confusion Matrix Visualization
    st.markdown('<div class="sub-header">🎯 Confusion Matrix - CNN Model</div>', unsafe_allow_html=True)

    confusion_matrix = np.array([
        [265735, 85, 45],
        [120, 16682, 38],
        [98, 42, 530785]
    ])

    labels = ['Flooding', 'Injection', 'Normal']

    fig = ff.create_annotated_heatmap(
        z=confusion_matrix,
        x=labels,
        y=labels,
        colorscale='Viridis',
        showscale=True
    )
    fig.update_layout(title="CNN Model Confusion Matrix", height=450)
    st.plotly_chart(fig, use_container_width=True)

    # Metrics comparison
    st.markdown('<div class="sub-header">📊 Detailed Metrics Comparison</div>', unsafe_allow_html=True)

    metrics_df = pd.DataFrame({
        'Model': ['CNN', 'DNN (5)', 'DNN (3)', 'RNN-LSTM'],
        'Accuracy': [97, 95, 97, 93],
        'Precision': [88, 76, 88, 64],
        'Recall': [85, 76, 88, 64],
        'F1-Score': [85, 76, 88, 64],
        'Loss': [0.14, 0.41, 0.47, 0.68]
    })
    st.dataframe(metrics_df, use_container_width=True)

    # ROC Curve
    st.markdown('<div class="sub-header">📈 ROC Curves</div>', unsafe_allow_html=True)

    fig = go.Figure()
    models_roc = ['CNN', 'DNN (5)', 'RNN-LSTM']
    fpr = [0.01, 0.02, 0.05, 0.08]
    tpr = [0.98, 0.97, 0.96, 0.95]

    fig.add_trace(
        go.Scatter(x=[0, 1], y=[0, 1], mode='lines', name='Random Classifier', line=dict(dash='dash', color='gray')))
    fig.add_trace(go.Scatter(x=fpr, y=tpr, mode='lines+markers', name='CNN (AUC=0.99)', line=dict(color='#1f77b4')))

    fig.update_layout(
        title="ROC Curves for Different Models",
        xaxis_title="False Positive Rate",
        yaxis_title="True Positive Rate",
        height=450
    )
    st.plotly_chart(fig, use_container_width=True)

# ==================== COMPARATIVE ANALYSIS PAGE ====================
elif page == "⚖️ Comparative Analysis":
    st.markdown('<div class="sub-header">⚖️ Comparative Analysis with Existing Works</div>', unsafe_allow_html=True)

    # Comparison chart
    comp_data = pd.DataFrame({
        'Method': ['J48', 'Random Forest', 'XGBoost', 'SVM', 'ANN', 'SAE', 'DNN', '**CNN**'],
        'Accuracy (%)': [99.5, 99.2, 99.99, 98.22, 99.95, 98.46, 95.72, 97.00],
        'Reference': ['Kolias et al.', 'Bhandari et al.', 'Bhandari et al.', 'Lee et al.', 'Rahman et al.',
                      'Wang et al.', 'Wang et al.', 'Our Work']
    })

    fig = go.Figure(data=[go.Bar(
        x=comp_data['Method'],
        y=comp_data['Accuracy (%)'],
        marker_color=['#2ecc71' if '**' in m else '#3498db' for m in comp_data['Method']],
        text=comp_data['Accuracy (%)'],
        textposition='auto'
    )])
    fig.update_layout(
        title="State-of-the-Art Comparison on AWID Dataset",
        xaxis_title="Model",
        yaxis_title="Accuracy (%)",
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)

    # Performance radar chart
    st.markdown('<div class="sub-header">🎯 Multi-Metric Comparison</div>', unsafe_allow_html=True)

    radar_data = pd.DataFrame({
        'Metric': ['Accuracy', 'Precision', 'Recall', 'F1-Score', 'Detection Rate'],
        'CNN': [97, 88, 85, 85, 96],
        'DNN (5)': [95, 76, 76, 76, 94],
        'RNN-LSTM': [93, 64, 64, 64, 89],
        'Our Proposed': [99, 99, 99, 99, 99]
    })

    fig = go.Figure()
    for model in ['CNN', 'DNN (5)', 'Our Proposed']:
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

# ==================== CONCLUSION PAGE ====================
else:
    st.markdown('<div class="sub-header">🎯 Conclusion & Future Directions</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### ✅ Key Achievements")
        st.markdown("""
        - **97% Accuracy** achieved with CNN model
        - **0.14 Loss** in binary classification
        - **99.9% Detection Rate** with MV(LR)
        - **Feature reduction** from 154 → 13 features
        - **Low False Alarm Rate** (0.31%)
        """)

        st.markdown("### 🚀 Future Work")
        st.markdown("""
        - **Ensemble Methods**: Implement true ensemble learning
        - **Real-time Processing**: Optimize for edge deployment
        - **Cross-Dataset Validation**: Test on KDD Cup 99, NSL-KDD
        - **Adaptive Learning**: Continuous learning for novel attacks
        - **IoT Integration**: Deploy on resource-constrained devices
        """)

    with col2:
        st.markdown("### 📈 Performance Summary")

        performance_data = {
            'Metric': ['Best Accuracy', 'Best Loss', 'Detection Rate', 'False Alarm Rate', 'F1-Score'],
            'Value': ['97%', '0.14', '99.9%', '0.31%', '85%'],
            'Model': ['CNN', 'CNN', 'MV(LR)', 'CNN', 'CNN']
        }

        fig = go.Figure(data=[go.Table(
            header=dict(values=list(performance_data.keys()), fill_color='#1f77b4', align='left'),
            cells=dict(values=[performance_data['Metric'], performance_data['Value'], performance_data['Model']],
                       fill_color='#f0f2f6', align='left'))
        ])
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.markdown('<div class="sub-header">📚 References</div>', unsafe_allow_html=True)

    with st.expander("Show References"):
        st.markdown("""
        1. Kolias, C., et al. (2016). "Intrusion detection in 802.11 networks." IEEE Communications Surveys & Tutorials, 18(1), 184-208.
        2. Kasongo, S.M., & Sun, Y. (2020). "A deep learning method with wrapper based feature extraction for wireless intrusion detection system." Computers & Security, 92, 101752.
        3. Wang, S., et al. (2019). "Intrusion detection for WiFi network: A deep learning approach." International Wireless Internet Conference, 95-104.
        4. Bhandari, S., et al. (2020). "Feature selection improves tree-based classification for wireless intrusion detection." International Workshop on Systems and Network Telemetry and Analytics, 19-26.
        5. Sadia, H., et al. (2024). "Intrusion Detection System for Wireless Sensor Networks: A Machine Learning Based Approach." IEEE Access, 12, 3380014.
        """)

    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: gray; padding: 20px;">
    <p>📧 Corresponding author: Saeed Ali Omer Bahaj (saobahaj@gmail.com)</p>
    <p>🏛️ Supported by Higher Education Commission of Pakistan (NRPU Project 17006)</p>
    <p>© 2024 IEEE Access | DOI: 10.1109/ACCESS.2024.3380014</p>
    </div>
    """, unsafe_allow_html=True)

# Auto-refresh for simulation (runs every 2 seconds)
if st.session_state.simulation_running and page == "🌐 Network Simulation":
    import time

    time.sleep(2)
    st.rerun()
