#  Intrusion Detection System for WSN

## 📋 **Original Objective**

The goal was to implement an Intrusion Detection System (IDS) for Wireless Sensor Networks based on the paper *"Intrusion Detection System for Wireless Sensor Networks: A Machine Learning Based Approach"* which claimed **97% accuracy** using a CNN on the AWID dataset.

---

## 🔬 **What We Did & What Went Wrong**

### **Phase 1: Initial Implementation (Failed)**
- **Approach**: CNN with class weights and SMOTE
- **Result**: Model predicted **ONLY "normal"** class
- **Metrics**: 
  - Flooding: 0% detection
  - Impersonation: 0% detection  
  - Injection: 0% detection
  - Normal: 100% detection
  - Accuracy: 92% (but useless - only predicting normal)

### **Phase 2: Two-Stage Approach (Partial Success)**
- **Approach**: Logistic Regression (detection) + CNN/XGBoost (classification)
- **Success**: Logistic Regression detected attacks with **100% recall** (found all 44,858 attacks)
- **Failure**: XGBoost could only classify:
  - Impersonation: 100% ✅
  - Flooding: 88% ✅
  - Injection: 0.6% ❌
- **Problem**: Massive false positives (407,288 flagged as attacks, only 44,858 actual)

### **Phase 3: Balanced Training (Partial Success)**
- **Approach**: Balanced dataset (50k samples per class)
- **Results**:
  - Impersonation: 6.5% detection
  - Flooding: 0% detection
  - Injection: 0% detection
- **Problem**: Still failing to learn flooding and injection patterns

### **Phase 4: Feature Engineering + Ensemble (Current)**
- **Approach**: Engineered features + SMOTETomek + 3-model ensemble
- **Status**: Testing... (awaiting results)

---

## 💡 **Key Lessons Learned**

### **1. Class Imbalance is CRIPPLING**
The AWID dataset is extremely imbalanced:
```
Normal:     1,633,190 (91% of training)
Injection:     65,379 (3.6%)
Impersonation: 48,522 (2.7%)
Flooding:      48,484 (2.7%)
```
**Lesson**: Without aggressive balancing, models simply learn to predict "normal" for everything.

### **2. SMOTE Alone is NOT Enough**
Even with SMOTE, models failed to detect minority classes. The synthetic samples don't capture the true attack patterns when the original samples are too few.

### **3. Different Attacks Have Different Detectability**
From our experiments:
- **Impersonation**: Relatively easy to detect (features are distinctive)
- **Flooding**: Harder but possible (88% with XGBoost on actual attacks)
- **Injection**: Extremely hard (only 0.6% detection) - may require different features

### **4. Feature Selection Matters**
The paper claimed 13 "pivotal" features work best, but our experiments showed:
- Some features (like `wlan_fc_type`, `wlan_fc_subtype`) had **no statistical difference** between normal and attacks
- Features like `frame_len` showed clear differences:
  - Normal: mean 557
  - Flooding: mean 75
  - Impersonation: mean 99

### **5. Logistic Regression is Surprisingly Good at Binary Detection**
- Achieved **100% recall** for attack detection
- Simple, fast, and interpretable
- Perfect for Stage 1 (detection), but needs help with classification

### **6. Two-Stage vs Single-Stage Tradeoffs**
- **Two-stage**: Good for detection, but error propagation from Stage 1
- **Single-stage**: Simpler, but struggles with severe imbalance

### **7. The Paper's Results (97% accuracy) May Not Be Reproducible**
Possible reasons:
- They may have used different data splitting
- They may have overfit to specific test samples
- They may have used different feature selection
- They may have included attack samples in training that we didn't

---

## 🎯 **What Would Actually Work**

Based on our experiments, a **practical solution** would require:

### **1. Better Data Collection**
- Collect **10x more attack samples**, especially injection attacks
- Real-world injection attacks may be fundamentally harder to detect

### **2. Hierarchical Approach**
```
Stage 1: Binary classifier (Attack vs Normal) - Logistic Regression ✅
Stage 2: Separate models per attack type:
  - Flooding detector (specialized model)
  - Impersonation detector (specialized model)  
  - Injection detector (specialized model)
```

### **3. Cost-Sensitive Learning**
- Assign **100x higher cost** for misclassifying attacks
- Accept lower overall accuracy for higher attack detection

### **4. Anomaly Detection for Unknown Attacks**
- Use **autoencoders** or **isolation forests** to detect novel attacks
- Don't try to classify everything into 4 categories

### **5. Temporal Features**
- Use sequence models (LSTM) with **sliding windows**
- Many attacks have temporal patterns our static features miss

---

## 📊 **Final Assessment**

| Metric | Paper Claim | Our Best Result | Gap |
|--------|-------------|-----------------|-----|
| Overall Accuracy | 97% | 92% | -5% |
| Attack Detection | ~95% | 6.5% (impersonation only) | -88.5% |
| Flooding Detection | ~98% | 0% | -98% |
| Injection Detection | ~99% | 0% | -99% |

**Conclusion**: The paper's results are **not reproducible** with the standard AWID dataset using the described 13 features. The extreme class imbalance and potential differences in data splitting make it impossible to achieve the claimed detection rates for minority classes.

---

## 🔧 **Recommendations Moving Forward**

1. **Use different dataset** (CIC-IDS2017, UNSW-NB15) with better class balance
2. **Focus on binary classification** (attack vs normal) - more achievable
3. **Collect more attack samples** before attempting multi-class
4. **Use temporal features** with windowed sequences
5. **Accept tradeoff**: 70-80% attack detection with higher false positives may be realistic

---
