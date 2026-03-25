


## **1. WHAT IS THIS DATASET?**

This is the **AWID (Aegean WiFi Intrusion Dataset)** - a collection of WiFi network traffic containing both normal communications and various types of cyber attacks.

Think of it like:
- **Normal traffic**: Regular WiFi communications from phones, laptops, IoT devices
- **Attack traffic**: Malicious activities trying to hack or disrupt the network

## **2. DATASET STRUCTURE**

### **2.1 Column Categories**

The columns can be grouped into several logical categories:

```python
# Grouping features by their purpose
feature_groups = {
    'Frame Information': [
        'frame.interface_id', 'frame.dlt', 'frame.offset_shift',
        'frame.time_epoch', 'frame.time_delta', 'frame.time_relative',
        'frame.len', 'frame.cap_len'
    ],
    
    'Radiotap Header (Hardware Info)': [
        'radiotap.version', 'radiotap.length', 'radiotap.present.tsft',
        'radiotap.present.flags', 'radiotap.present.rate',
        'radiotap.present.channel', 'radiotap.datarate',
        'radiotap.channel.freq', 'radiotap.dbm_antsignal',
        'radiotap.antenna', 'radiotap.rxflags.badplcp'
    ],
    
    'MAC Layer (WiFi Management)': [
        'wlan.fc.type_subtype', 'wlan.fc.type', 'wlan.fc.subtype',
        'wlan.fc.ds', 'wlan.fc.retry', 'wlan.fc.pwrmgt',
        'wlan.ra', 'wlan.da', 'wlan.sa', 'wlan.bssid',
        'wlan.seq', 'wlan.frag'
    ],
    
    'WiFi Management Frames': [
        'wlan_mgt.fixed.capabilities.ess', 'wlan_mgt.fixed.capabilities.privacy',
        'wlan_mgt.fixed.listen_ival', 'wlan_mgt.fixed.beacon',
        'wlan_mgt.ssid', 'wlan_mgt.ds.current_channel'
    ],
    
    'Security Related': [
        'wlan.wep.iv', 'wlan.wep.key', 'wlan.wep.icv',
        'wlan.tkip.extiv', 'wlan.ccmp.extiv',
        'wlan_mgt.rsn.version', 'wlan_mgt.rsn.akms.type',
        'wlan.fc.protected'
    ],
    
    'QoS (Quality of Service)': [
        'wlan.qos.tid', 'wlan.qos.priority', 'wlan.qos.eosp',
        'wlan.qos.ack', 'wlan.qos.amsdupresent'
    ],
    
    'Data Fields': [
        'data.len', 'frame.len'
    ]
}
```

## **3. UNDERSTANDING EACH FEATURE**

### **3.1 Timestamp Features**
```python
timestamp_features = {
    'frame.time_epoch': 'Absolute time in seconds since 1970',
    'frame.time_delta': 'Time since previous frame (seconds)',
    'frame.time_relative': 'Time since first frame in capture'
}
```

### **3.2 Frame Size Features**
```python
size_features = {
    'frame.len': 'Total frame length on wire (including headers)',
    'frame.cap_len': 'Captured length (may be truncated)',
    'data.len': 'Length of payload data only'
}
```

**Why important?**
- Attack frames often have unusual sizes
- Flooding attacks may have many small frames
- Normal data tends to have typical size patterns

### **3.3 Radio Information (Radiotap)**
```python
radio_features = {
    'radiotap.datarate': 'Transmission rate (Mbps)',
    'radiotap.channel.freq': 'Channel frequency (MHz) - 2437 = channel 6',
    'radiotap.dbm_antsignal': 'Signal strength in dBm (e.g., -47 dBm)',
    'radiotap.antenna': 'Which antenna received the frame'
}
```

**Signal strength interpretation:**
- `-30 dBm`: Excellent signal (right next to AP)
- `-50 to -67 dBm`: Good signal
- `-67 to -80 dBm`: Fair signal
- `-80 to -90 dBm`: Poor signal

### **3.4 WiFi Frame Control (wlan.fc)**
```python
frame_control = {
    'wlan.fc.type': '0=Management, 1=Control, 2=Data',
    'wlan.fc.subtype': 'Specific frame subtype',
    'wlan.fc.retry': '1 if this is a retransmission',
    'wlan.fc.protected': '1 if frame is encrypted'
}
```

**Frame Types:**
```
Type 0 (Management):
  Subtype 8 = Beacon (AP advertising itself)
  Subtype 4 = Probe Request (device scanning)
  Subtype 5 = Probe Response
  
Type 1 (Control):
  Subtype 11 = RTS (Request to Send)
  Subtype 12 = CTS (Clear to Send)
  Subtype 13 = ACK (Acknowledgment)
  
Type 2 (Data):
  Subtype 0 = Data frame
  Subtype 4 = Null function (power save)
```

### **3.5 MAC Addresses**
```python
mac_addresses = {
    'wlan.ra': 'Receiver Address (who should get this)',
    'wlan.da': 'Destination Address (final destination)',
    'wlan.sa': 'Source Address (who sent this)',
    'wlan.bssid': 'BSSID (AP identifier)'
}
```

**Special addresses:**
- `ff:ff:ff:ff:ff:ff` = Broadcast (everyone)
- `33:33:00:00:00:01` = IPv6 multicast

### **3.6 SSID (Network Name)**
The `wlan_mgt.ssid` field contains the WiFi network name:
- In beacon frames: The AP announces its name
- In probe requests: Devices ask for specific networks
- `pnet`, `CYTA C565`, `OTE29224e` are actual network names

## **4. ATTACK TYPES IN THIS DATASET**

### **4.1 Flooding Attacks**
```python
flooding_characteristics = {
    'what': 'Overwhelming the network with too many frames',
    'detection': [
        'Very high frame rate',
        'Many frames from same source',
        'Unusual frame types repeated rapidly'
    ],
    'examples': [
        'Deauth flood: Sending many deauthentication frames',
        'Probe flood: Many probe requests in short time',
        'Beacon flood: Fake AP beacons overwhelming clients'
    ]
}
```

### **4.2 Impersonation Attacks**
```python
impersonation_characteristics = {
    'what': 'Pretending to be a legitimate device',
    'detection': [
        'MAC address spoofing',
        'Using legitimate SSIDs from fake APs',
        'Unusual sequence numbers',
        'Inconsistent frame types'
    ],
    'examples': [
        'Evil twin AP: Fake AP with legitimate SSID',
        'MAC spoofing: Using stolen MAC address',
        'Identity theft: Impersonating legitimate client'
    ]
}
```

### **4.3 Injection Attacks**
```python
injection_characteristics = {
    'what': 'Inserting malicious frames into the network',
    'detection': [
        'Malformed frames',
        'Invalid frame combinations',
        'Unexpected encryption patterns',
        'Corrupted frame check sequences'
    ],
    'examples': [
        'ARP injection: Fake ARP responses',
        'Data injection: Malicious payloads',
        'Encrypted frame injection'
    ]
}
```

## **5. UNDERSTANDING THE DATA ROW**

Let's analyze the first row in detail:

```python
row_0 = {
    'frame.len': 261,  # Normal-sized frame
    'radiotap.datarate': 1,  # 1 Mbps (slow, likely management frame)
    'radiotap.channel.freq': 2437,  # Channel 6 (2.4 GHz)
    'radiotap.dbm_antsignal': -47,  # Good signal strength
    'wlan.fc.type_subtype': 0x08,  # Type 0, Subtype 8 = Beacon
    'wlan.fc.type': 0,  # Management frame
    'wlan.fc.subtype': 8,  # Beacon
    'wlan.fc.retry': 0,  # First transmission
    'wlan.ra': 'ff:ff:ff:ff:ff:ff',  # Broadcast (everyone)
    'wlan.da': 'ff:ff:ff:ff:ff:ff',  # Broadcast
    'wlan.sa': 'b0:48:7a:e2:62:23',  # Source AP
    'wlan.bssid': 'b0:48:7a:e2:62:23',  # AP's BSSID
    'wlan_mgt.ssid': 'pnet',  # Network name
    'wlan_mgt.ds.current_channel': 6,  # Channel 6
    'class': 'normal'  # Normal traffic
}
```

**Interpretation:**
- This is a **normal beacon frame** from AP `pnet`
- It's broadcasting network information on channel 6
- Good signal strength (-47 dBm)
- All devices in range receive this to know about the network

## **6. PATTERNS IN ATTACKS VS NORMAL**

### **6.1 Normal Traffic Patterns**
```python
normal_patterns = {
    'beacon_regularity': 'Beacons every ~102.4 ms',
    'data_frames': 'Normal size distribution (mostly 1500 bytes or less)',
    'retry_rate': 'Low (<5%)',
    'signal_strength': 'Consistent for each device',
    'sequence_numbers': 'Continuous, increasing by 1-2 each frame'
}
```

### **6.2 Attack Patterns**
```python
attack_patterns = {
    'flooding': {
        'frame_rate': 'Extremely high (>1000 fps)',
        'source_variety': 'Many different source MACs',
        'frame_types': 'Repetitive (same type over and over)',
        'retry_rate': 'Very low (no waiting for ACK)'
    },
    
    'impersonation': {
        'mac_addresses': 'Same MAC with different BSSIDs',
        'sequence_anomalies': 'Sequence numbers jumping',
        'signal_inconsistency': 'Same MAC, very different signal strength',
        'timing': 'Unusual timing patterns'
    },
    
    'injection': {
        'frame_errors': 'Bad FCS (Frame Check Sequence)',
        'encryption': 'Invalid encryption headers',
        'payload': 'Malformed data',
        'fragmentation': 'Unusual fragmentation patterns'
    }
}
```

## **7. KEY FEATURES FOR DETECTION**

Based on research, these are the most discriminative features:

```python
critical_features = {
    # Time-based features
    'frame.time_delta': 'Inter-arrival time (shows flooding)',
    'frame.time_relative': 'Time since start (helps detect patterns)',
    
    # Frame characteristics
    'frame.len': 'Size anomalies',
    'data.len': 'Payload anomalies',
    
    # Radio layer
    'radiotap.datarate': 'Unusual rates for frame type',
    'radiotap.dbm_antsignal': 'Signal strength inconsistencies',
    
    # MAC layer
    'wlan.fc.type': 'Frame type distribution',
    'wlan.fc.subtype': 'Specific frame types',
    'wlan.fc.retry': 'Retransmission patterns',
    
    # Sequence analysis
    'wlan.seq': 'Sequence number gaps or duplicates',
    
    # Address patterns
    'wlan.ra': 'Receiver patterns',
    'wlan.sa': 'Source patterns (spoofing detection)',
    'wlan.bssid': 'AP patterns',
    
    # Network info
    'wlan_mgt.ssid': 'Network name (fake AP detection)',
    'wlan_mgt.ds.current_channel': 'Channel hopping detection'
}
```

## **8. VISUALIZING THE DATA**

```python
def visualize_feature_distributions(df, feature, attack_types):
    """
    Show how this feature differs between normal and attacks
    """
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    for idx, attack in enumerate(attack_types):
        ax = axes[idx // 2, idx % 2]
        
        # Plot distribution for normal
        normal_data = df[df['class'] == 'normal'][feature]
        ax.hist(normal_data, bins=50, alpha=0.5, label='Normal', density=True)
        
        # Plot for attack
        attack_data = df[df['class'] == attack][feature]
        ax.hist(attack_data, bins=50, alpha=0.5, label=attack, density=True)
        
        ax.set_title(f'{feature} - {attack} vs Normal')
        ax.set_xlabel(feature)
        ax.set_ylabel('Density')
        ax.legend()
    
    plt.tight_layout()
    plt.show()
```

## **9. WHY 13 FEATURES WERE SELECTED**

The code selected these 13 pivotal features:

```python
selected_features = {
    7: 'frame.len',  # Frame size (flooding creates many small frames)
    13: 'radiotap.length',  # Header length (some attacks malform this)
    14: 'radiotap.present.tsft',  # Timing sync (flooding breaks timing)
    15: 'radiotap.present.flags',  # Radio flags (some attacks spoof these)
    125: 'wlan.fc.type',  # Frame type distribution
    126: 'wlan.fc.subtype',  # Specific frame types
    128: 'wlan.fc.retry',  # Retry patterns
    139: 'wlan.seq',  # Sequence numbers (key for detecting injection)
    140: 'data.len',  # Payload size
    63: 'wlan_mgt.fixed.capabilities.privacy',  # Encryption flags
    68: 'wlan_mgt.fixed.beacon',  # Beacon interval (fake APs)
    37: 'wlan.qos.tid',  # QoS traffic ID
    38: 'wlan.qos.priority',  # QoS priority
    154: 'class'  # The label
}
```

## **10. SUMMARY**

The AWID dataset captures:
- **Normal WiFi traffic**: Regular network communications
- **Attack traffic**: Various intrusion attempts
- **Rich metadata**: Everything from signal strength to encryption details

**Why it's challenging:**
1. **Massive imbalance**: 530,785 normal vs 8,097 flooding
2. **Complex relationships**: Attacks hide in normal traffic patterns
3. **Temporal dependencies**: Patterns over time matter
4. **Feature interactions**: Multiple features combine to indicate attacks

This is why sophisticated ML models and class balancing techniques are needed to detect the rare but important attack patterns!

---
## **Selection process** 

Based on the paper, the reduction from 154 features down to 13 was achieved through a **multi-stage feature engineering and selection process**, rather than a single automated method. Here is how they did it:

### 1. Initial Reduction: Data Preprocessing (154 → 76)
The first major reduction happened during data cleaning and preprocessing. The AWID dataset originally contains 154 input features (labeled f1 to f154 in Table 3). The authors applied several filtering steps to get down to 76 features:
- **Dropping Null Values:** They identified columns with a high percentage of null values (specifically setting a threshold of 50%) and removed those columns entirely.
- **Removing Redundant Rows:** Rows containing null values were also dropped.
- **Data Type Conversion:** They converted certain features from float and hexadecimal datatypes to integers, which helps in identifying valid data versus placeholders.
- **Replacing Placeholders:** Unknown entries ("?") were replaced with "NaN" and subsequently dropped or converted.

These preprocessing steps automatically eliminated a significant portion of the 154 features because many columns in the AWID dataset contain sparse or incomplete data.

### 2. Secondary Reduction: Embedded Feature Selection (76 → 13)
Once the dataset was cleaned down to 76 relevant features, the authors used a method referred to as **"embedded feature selection."**

Unlike filter methods (which look at statistics) or wrapper methods (which test combinations), embedded methods perform feature selection during the model training process. The paper states:
> *"We employ an embedded feature selection method integrated into the model training process, identifying the prediction variable's most contributive features."*

While the paper does not explicitly name a specific algorithm (e.g., LASSO or Tree-based importance) for this step, the context suggests that the **Convolutional Neural Network (CNN)** itself played a role in the reduction. CNNs are adept at identifying and extracting the most salient features from high-dimensional data. By analyzing feature weights and contribution to the prediction accuracy during training, the model helped isolate the 13 "pivotal features" that were most relevant for distinguishing between Normal, Flooding, Injection, and Impersonation classes.

### Summary of the Logic
1.  **154:** Raw dataset attributes.
2.  **76:** Features that survived the preprocessing phase (removal of nulls/irrelevant columns).
3.  **13:** A highly refined subset derived from the 76 via embedded feature selection during deep learning training, representing the most critical indicators of security breaches.

