# Enhanced CNN-Based WiFi Intrusion Detection System for WSN

## Abstract
This project addresses the critical challenge of detecting rare network attacks in 
WiFi environments using Convolutional Neural Networks (CNNs). Using the Aegean 
WiFi Intrusion Dataset (AWID), which contains 575,643 network samples with 
severe class imbalance (92% normal traffic vs 8% attacks), we implement and 
compare multiple strategies to improve detection of minority attack classes 
(flooding, impersonation, and injection). Our approach demonstrates how 
class weighting, SMOTE oversampling, and focal loss can significantly improve 
attack detection rates while maintaining high accuracy for normal traffic.

## Problem Statement
Network intrusion detection systems face a fundamental challenge: attacks are 
rare by nature, creating severely imbalanced datasets. Traditional machine 
learning models trained on such data achieve high accuracy by simply predicting 
the majority class (normal), failing to detect critical security threats. 
This project tackles the problem of detecting rare WiFi attacks despite 
massive class imbalance.

## **1. CLASS IMBALANCE PROBLEM IN INTRUSION DETECTION**

### **1.1 The Problem**
In network intrusion detection, attack traffic is naturally rare compared to normal traffic:
- **Normal traffic**: 530,785 samples (92.2%)
- **Flooding**: 8,097 samples (1.4%)
- **Impersonation**: 20,079 samples (3.5%)
- **Injection**: 16,682 samples (2.9%)

**The Challenge**: When a model is trained on imbalanced data, it becomes biased toward the majority class because:
- The loss function is dominated by majority class samples
- The model achieves high accuracy by simply predicting "normal" for everything
- Minority class patterns are treated as noise

### **1.2 Why This Happens**
```
Standard Loss Function (Cross-Entropy):
L = -Σ y_true * log(y_pred)

For imbalanced data:
Total Loss = (530,785 × Loss_normal + 8,097 × Loss_flooding) / Total_samples
           ≈ 0.922 × Loss_normal + 0.078 × Loss_attacks

The model optimizes for normal class because it contributes 92% of the loss!
```

## **2. STRATEGY 1: CLASS WEIGHTS**

### **2.1 Mathematical Foundation**

Class weights are calculated as:
```
Weight_i = Total_samples / (n_classes × samples_i)

For flooding:   575,643 / (4 × 8,097)    = 17.77
For normal:     575,643 / (4 × 530,785)  = 0.27
```

### **2.2 How It Works**
The weighted loss function becomes:
```
L_weighted = -Σ w_i × y_true × log(y_pred)

Where w_i is the weight for class i
```

This amplifies the error for minority classes:
- Misclassifying flooding (weight=17.77) costs 17.77× more than normal
- The model is forced to pay attention to attack patterns

### **2.3 Limitations**
- Doesn't create new data, just reweights existing samples
- Can lead to overfitting on few attack samples
- Sensitive to weight calculation method

## **3. STRATEGY 2: SMOTE (Synthetic Minority Over-sampling Technique)**

### **3.1 Mathematical Principle**

SMOTE creates synthetic samples by interpolating between existing minority class samples:

```
For a minority sample x_i, find k nearest neighbors
Select random neighbor x_j
Create synthetic sample: x_new = x_i + λ × (x_j - x_i)
where λ ∈ [0, 1] is random
```

### **3.2 Visual Explanation**
```
Original minority samples:    ●    ●    ●
                              │    │    │
Synthetic samples:           ○─○─○ ○─○─○ ○─○─○

Each original sample generates multiple synthetic samples along lines to its neighbors
```

### **3.3 Algorithm Steps**
1. For each minority class sample, find k nearest neighbors (k=3)
2. Randomly select one neighbor
3. Create synthetic sample at random point on the line between them
4. Repeat until classes are balanced

### **3.4 Advantages**
- Creates realistic samples in feature space
- Expands the decision region of minority classes
- Reduces overfitting compared to simple duplication

### **3.5 Limitations**
- Can create overlapping samples between classes
- Not suitable for very high-dimensional data
- May amplify noise in the data

## **4. STRATEGY 3: FOCAL LOSS**

### **4.1 Theoretical Background**

Focal Loss was introduced by Lin et al. (2017) for object detection, but it's perfect for imbalanced classification.

### **4.2 Mathematical Formulation**

**Standard Cross-Entropy:**
```
CE(p, y) = -log(p)  where p is predicted probability for true class
```

**Focal Loss:**
```
FL(p, y) = -α × (1-p)^γ × log(p)

Where:
- p = predicted probability
- α = balancing factor (typically 0.25)
- γ = focusing parameter (typically 2.0)
```

### **4.3 Why It Works**

The key is the modulating factor `(1-p)^γ`:

| Scenario | p | (1-p)^γ | Effect |
|----------|---|---------|--------|
| Easy example (normal traffic) | 0.9 | 0.01 | Loss reduced 100× |
| Hard example (attack traffic) | 0.3 | 0.49 | Loss reduced only 2× |

**Example Calculation:**
```
For easy sample (p=0.9):
CE loss = -log(0.9) = 0.105
FL loss = -0.25 × (0.1)^2 × log(0.9) = 0.00026 (405× smaller!)

For hard sample (p=0.3):
CE loss = -log(0.3) = 1.204
FL loss = -0.25 × (0.7)^2 × log(0.3) = 0.206 (5.8× smaller)
```

### **4.4 Visual Representation**
```
Loss Value
    ↑
    |                                    CE (γ=0)
    |                             ╱
    |                         ╱
    |                     ╱
    |                 ╱
    |             ╱
    |         ╱
    |     ╱
    | ╱
    └────────────────────────────→ Probability
    0                           1
    
Focal Loss (γ=2) reduces loss for high-probability (easy) samples
```

## **5. ENHANCED CNN ARCHITECTURE THEORY**

### **5.1 Batch Normalization**

**Purpose**: Normalize layer inputs to accelerate training and provide regularization

**Mathematics**:
```
μ_B = (1/m) Σ x_i              # Batch mean
σ²_B = (1/m) Σ (x_i - μ_B)²    # Batch variance
x̂_i = (x_i - μ_B) / √(σ²_B + ε) # Normalize
y_i = γx̂_i + β                   # Scale and shift
```

### **5.2 Attention Mechanism (Squeeze-and-Excitation)**

**Squeeze**: Global information embedding
```
z_c = (1/H×W) Σ_h Σ_w x_c(h,w)  # Global average pooling
```

**Excitation**: Channel-wise attention weights
```
s = σ(W₂ × δ(W₁ × z))  # Two-layer bottleneck
where:
- σ = sigmoid activation
- δ = ReLU activation
- W₁, W₂ = learnable weights
```

**Scale**: Apply attention
```
x̃_c = s_c × x_c  # Channel-wise multiplication
```

### **5.3 Why This Architecture for Imbalanced Data**

1. **Multiple Conv Layers**: Extract hierarchical features at different scales
2. **BatchNorm**: Stabilizes training when using class weights
3. **Attention**: Focuses on discriminative features for attacks
4. **Dropout**: Prevents overfitting on few attack samples
5. **Global Pooling**: Reduces parameters, prevents overfitting

## **6. EVALUATION METRICS THEORY**

### **6.1 Why Accuracy is Misleading**
```
Accuracy = (TP + TN) / Total
For our data: 
- Always predicting "normal" gives 92.2% accuracy
- But detects 0% of attacks!
```

### **6.2 Important Metrics for Imbalanced Data**

**Precision** (Positive Predictive Value):
```
Precision = TP / (TP + FP)
Meaning: When we predict an attack, how often are we correct?
```

**Recall** (Sensitivity/True Positive Rate):
```
Recall = TP / (TP + FN)
Meaning: What proportion of actual attacks did we catch?
```

**F1-Score** (Harmonic Mean):
```
F1 = 2 × (Precision × Recall) / (Precision + Recall)
Meaning: Balances precision and recall
```

**Macro vs Weighted Average**:
```
Macro F1 = (F1₁ + F1₂ + F1₃ + F1₄) / 4
         = Gives equal weight to all classes

Weighted F1 = Σ (support_i × F1_i) / Total
            = Weighted by class size (biased toward majority)
```

## **7. WHY CURRENT APPROACH FAILS**

Your current model achieves:
- **Normal**: 98% recall ✅
- **Flooding**: 0% recall ❌
- **Impersonation**: 0% recall ❌

**Reasons**:
1. Loss dominated by normal samples
2. Attack patterns treated as outliers
3. Decision boundary pushed toward majority class
4. Insufficient examples to learn attack patterns

## **8. THEORETICAL SOLUTION**

The three strategies address different aspects:

```
Problem: Decision boundary biased toward normal class

Solution 1 (Class Weights): Lift the minority classes
├─ Before: ○○○○○○○○○○○○○○○○○○○○○● (normal dominates)
└─ After:  ○○○○○○○○○○○○○○○○○○○○○● (equal importance)

Solution 2 (SMOTE): Create more minority samples
├─ Before: ●● (few attacks)
└─ After:  ●●●●●●●●●● (balanced with normal)

Solution 3 (Focal Loss): Focus on hard examples
├─ Before: Easy samples dominate learning
└─ After:  Hard samples get more attention
```

## **9. MATHEMATICAL GUARANTEES**

### **9.1 Convergence with Class Weights**
The weighted loss ensures that the gradient contributions from each class are proportional:
```
∇L_weighted = Σ_i w_i × ∇L_i
where Σ_i w_i × n_i ≈ constant for all i
```

### **9.2 SMOTE Interpolation Safety**
Synthetic samples lie in convex hull of existing samples:
```
x_new ∈ convex_hull({x_i, x_j})
```
This ensures generated samples are realistic.

### **9.3 Focal Loss Property**
As γ increases, the loss function approaches:
```
lim(γ→∞) FL(p,y) = α × I(p<0.5)
```
Only misclassified samples contribute to loss!

## **10. PRACTICAL RECOMMENDATIONS**

Based on theory, the best approach would be:

1. **Start with Focal Loss** (γ=2, α=0.25)
2. **Add moderate class weights** if needed
3. **Use SMOTE only if** Focal Loss insufficient
4. **Monitor macro F1-score**, not accuracy
5. **Validate on temporal data** to ensure generalization

This theoretical framework explains why the enhanced solution should improve detection of minority attack classes!
