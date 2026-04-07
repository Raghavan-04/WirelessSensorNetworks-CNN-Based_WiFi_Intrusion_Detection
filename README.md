

# Intrusion Detection System for Wireless Sensor Networks using XGBoost + SMOTE


---

## 📌 Overview

This project presents a **machine learning-based Intrusion Detection System (IDS)** for securing Wireless Sensor Networks (WSNs). The system addresses class imbalance, high dimensionality, and real-time detection requirements using:

- **Feature reduction** (154 → 13 behavioral features)
- **SMOTE** for class balancing
- **XGBoost classifier** for multiclass intrusion detection

---

## 🎯 Problem Statement

WSNs are vulnerable to flooding, impersonation, and injection attacks. Existing IDS suffer from:
- Low detection accuracy for rare attacks
- High false alarm rates
- Poor handling of imbalanced data (91% normal traffic)

---

## 📊 Dataset

**AWID (Aegean Wi-Fi Intrusion Detection) Dataset**
- 1.7 million real-world Wi-Fi packets
- 4 classes: Normal (86%), Flooding (2.7%), Injection (3.6%), Impersonation (2.7%)
- 80/20 stratified split

---

## ⚙️ Methodology

| Step | Description |
|------|-------------|
| 1. Feature Selection | 154 → 13 features (frame length, QoS, Wi-Fi control, etc.) |
| 2. Preprocessing | One-hot encoding, Z-score normalization |
| 3. Class Balancing | SMOTE (k=1) |
| 4. Classification | XGBoost (150 trees, depth=10, GPU-accelerated) |

---

## 📈 Results

| Metric | Value |
|--------|-------|
| Overall Accuracy | **98.4%** |
| Macro F1-Score | **0.934** |
| Injection Recall | **100%** |
| Flooding Recall | 99.96% |
| Impersonation Recall | 99.79% |

✅ Outperforms CNN, DNN, and RNN-LSTM benchmarks

---

## 🧰 Tech Stack

- Python 3.8+
- XGBoost
- scikit-learn (SMOTE, StandardScaler)
- Pandas, NumPy
- Matplotlib, Seaborn (visualizations)

---

## 🚀 How to Run

```bash
# Clone repository
git clone https://github.com/yourusername/wsn-ids-xgboost.git
cd wsn-ids-xgboost

# Install dependencies
pip install -r requirements.txt

# Run training
python train.py --dataset awid.csv --smote --model xgboost

# Evaluate
python evaluate.py --test data/test.csv
```

---

## 📁 Repository Structure

```
├── data/               # AWID dataset (not included, download separately)
├── notebooks/          # Jupyter notebooks for EDA and experiments
├── src/
│   ├── preprocess.py   # Feature selection & normalization
│   ├── balance.py      # SMOTE implementation
│   ├── train.py        # XGBoost training
│   └── evaluate.py     # Metrics & confusion matrix
├── results/            # Plots, heatmaps, confusion matrix
├── requirements.txt
└── README.md
```

---

## 🔮 Future Work

- Real-time edge deployment (Raspberry Pi / Arduino)
- Federated learning for privacy-preserving IDS
- Explainable AI (SHAP/LIME) for feature importance

---

## 📚 References

1. Sadia et al. (2024) – Deep Learning for WSN IDS  
2. Kolias et al. (2016) – AWID dataset  
3. Chawla et al. (2002) – SMOTE  
4. Chen & Guestrin (2016) – XGBoost  

---


