## 📊 TELECOM SYNTHETIC DATA GENERATOR 

### 🎯 **UYGULAMA AMACI**

Bu uygulama, **telekom operatörleri için gerçekçi sentetik network KPI verisi üreten** profesyonel bir sistemdir. Asıl amacı:
- Machine learning modellerinin eğitimi
- Kapasite planlaması simülasyonu  
- Anomali tespit algoritmalarının geliştirilmesi
- Hassas operasyonel verilerin paylaşılmadan test ortamları oluşturulması

---

### 🏗️ **MİMARİ TASARIM - 6 KATMANLI MODEL**

Uygulama, **modüler katmanlı mimari** kullanarak çalışır:

```
LAYER 6: Validation & Quality Assurance
           ↓ (validates)
LAYER 5: Anomaly Modeling & Scenarios
           ↓ (injects anomalies)
LAYER 4: Procedure Simulation
           ↓ (simulates protocols)
LAYER 3: Temporal Engineering & Time Series
           ↓ (applies seasonality, ARIMA)
LAYER 2: Multivariate Dependency Modeling
           ↓ (applies correlations, dependencies)
LAYER 1: Statistical Foundation
           ↓ (generates base distributions)
Raw Random Numbers
```

---

### 🔬 **KULLANILAN METODLAR VE MODELLER**

#### **1. İstatistiksel Dağılımlar (Layer 1)**

| Dağılım | Kullanım Alanı | Parametreler |
|---------|---------------|--------------|
| **Poisson** | Event arrival rates, çağrı denemeleri | λ (mean) |
| **Gamma** | Latency, gecikme, işleme süreleri | shape (α), scale (θ), CV |
| **Log-Normal** | Throughput, bandwidth, data volume | μ, σ (log-scale) |
| **Beta** | Success rates, availability (0-1 arası) | α, β, stability level |
| **Exponential** | Inter-arrival times, failure times | rate (λ) |
| **Normal** | Genel metrikler | mean (μ), std (σ) |

**Parametre Hesaplama Örnekleri:**
```python
# Gamma için shape ve scale hesaplama
cv = std / mean  # Coefficient of Variation
shape = 1 / (cv ** 2)
scale = mean / shape

# Beta için alpha ve beta hesaplama
concentration = {HIGH: 50, MEDIUM: 10, LOW: 2}[stability]
alpha = target_rate * concentration
beta = (1 - target_rate) * concentration
```

#### **2. Çok Değişkenli Bağımlılık Modelleri (Layer 2)**

- **Gaussian Copula**: Farklı dağılımlara sahip metrikler arası korelasyon
  - Uniform değerleri standart normale transform eder (CDF → Normal PPF)
  - Korelasyon matrisini Cholesky decomposition ile uygular
  - Geri original dağılıma inverse transform eder

- **Bayesian Network**: Nedensel ilişkiler (örn: latency ↑ → success rate ↓)

- **Conditional Probability Chain**: Prosedür state machine'leri
  - SIP call flows
  - PDU session establishment
  - NAS procedures

#### **3. Zaman Serisi Mühendisliği (Layer 3)**

**Fourier Series ile Seasonality:**
```python
seasonal = Σ (amplitude/h) * sin(2πh*f*t + φ)
# h: harmonic order (1-10)
# f: base frequency (24h, 7d, 30d)
```

**ARIMA Modeli (AutoRegressive Integrated Moving Average):**
- **AR(p)**: Geçmiş değerlere bağlı (temporal smoothing)
- **MA(q)**: Geçmiş hatalara bağlı (noise cancellation)

```python
value[t] = 0.3*base[t] + 0.5*AR_component + 0.2*MA_component + noise[t]
AR_component = Σ ar_coef[i] * value[t-i-1]
MA_component = Σ ma_coef[i] * noise[t-i-1]
```

**Change Point Detection:**
- **STEP**: Anlık değişim (software upgrade)
- **RAMP**: Aşamalı değişim (capacity expansion)
- **SPIKE**: Geçici değişim (special event)

#### **4. Anomali Modelleme (Layer 5)**

| Anomali Tipi | Etki | Propagation |
|--------------|------|-------------|
| **SPIKE** | Ani artış | value *= (1 + severity) |
| **DROP** | Ani düşüş | value *= (1 - severity) |
| **OSCILLATION** | Salınım | sin-wave pattern |
| **CONGESTION** | Network tıkanıklığı | success↓, latency↑ |
| **DEGRADATION** | Kademeli bozulma | Zaman içinde artış |
| **OUTAGE** | Tam kesinti | value *= (1 - 0.8*severity) |

---

### ⚙️ **CONFIGURATION YAPISI**

#### **Ana Konfigürasyon Bileşenleri:**

```python
GeneratorConfig:
  ├─ seed: int                    # Reproducibility için
  ├─ start_time / end_time: str   # Zaman penceresi
  ├─ granularity_minutes: int     # Örnekleme aralığı (5, 15, 30 dk)
  ├─ nodes: List[NodeConfig]      # Network node'ları
  ├─ seasonality: SeasonalityConfig
  ├─ arima: ARIMAConfig
  ├─ correlations: List[CorrelationConfig]
  ├─ change_points: List[ChangePointConfig]
  ├─ anomalies: List[AnomalyConfig]
  └─ validation: ValidationConfig
```

#### **Node ve Metric Konfigürasyonu:**

```python
NodeConfig:
  ├─ node_id: str          # Unique identifier
  ├─ node_type: str        # IMS, 4G, 5G Core
  ├─ capacity: int         # Max users/sessions
  ├─ location: str
  └─ metrics: List[MetricConfig]
      ├─ name: str
      ├─ distribution: DistributionConfig
      ├─ dependencies: List[str]    # Bağımlı metrikler
      ├─ qos_min / qos_max: float  # QoS boundaries
```

#### **Korelasyon Tanımlama:**

```python
CorrelationConfig:
  ├─ source: str            # Kaynak metrik
  ├─ target: str            # Hedef metrik
  └─ coefficient: float     # -1 to +1 arası
  
# Örnek: latency ↑ → success_rate ↓
correlation = CorrelationConfig(
    source="latency",
    target="success_rate",
    coefficient=-0.7
)
```

---

### 🔄 **ÇALIŞMA AKIŞI (TEXT-BASED FLOW)**

```
┌─────────────────────────────────────────────────────────────┐
│ 1. BAŞLANGIÇ - CONFIGURATION PARSING                        │
│    User Input (JSON/YAML) → parse_config()                  │
│    └─> GeneratorConfig object oluşturulur                   │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. TIME WINDOW GENERATION                                   │
│    pd.date_range(start_time, end_time, freq=granularity)    │
│    └─> Zaman damgaları listesi oluşturulur                 │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. LAYER 1 - BASE DISTRIBUTION GENERATION                   │
│    For each node and metric:                                │
│      ├─> Select distribution type (Poisson, Gamma, etc.)    │
│      ├─> Calculate parameters (shape, scale, α, β)          │
│      └─> Generate random values: np.random.{dist}()         │
│    Result: raw_values[n_windows]                            │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. LAYER 3 - TEMPORAL PATTERNS APPLICATION                  │
│    A) Seasonality (Fourier Series):                         │
│       └─> Apply daily/weekly cycles                         │
│           values *= (1 + Σ sin(harmonics))                  │
│                                                              │
│    B) ARIMA Smoothing:                                      │
│       └─> Apply AR and MA components                        │
│           value[t] = f(value[t-1..t-p], noise[t-1..t-q])   │
│                                                              │
│    Result: temporal_values[n_windows]                       │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 5. CHANGE POINTS APPLICATION                                │
│    For each change_point in config:                         │
│      ├─> Find timestamp index in time_windows               │
│      ├─> Apply change based on type:                        │
│      │    • STEP: instant *= (1 + magnitude)               │
│      │    • RAMP: gradual over duration                     │
│      │    • SPIKE: Gaussian bump                            │
│      └─> Update values[idx:end]                             │
│    Result: changed_values[n_windows]                        │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 6. LAYER 5 - ANOMALY INJECTION                             │
│    For each anomaly in config:                              │
│      ├─> Find start/end indices                             │
│      ├─> Apply anomaly effect based on type:                │
│      │    • SPIKE: values *= (1 + severity)                 │
│      │    • CONGESTION: if 'latency' *= 2, 'success' /= 2  │
│      │    • OUTAGE: values *= (1 - 0.8*severity)           │
│      └─> Propagate if enabled (via dependency graph)        │
│    Result: anomalous_values[n_windows]                      │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 7. LAYER 2 - DEPENDENCIES & CORRELATIONS                   │
│    A) Apply Dependencies:                                    │
│       └─> If metric depends on others:                      │
│           value *= scale_factor(dependency_values)           │
│                                                              │
│    B) Apply Correlations (Gaussian Copula):                 │
│       └─> Normalize → Apply correlation matrix              │
│           → Transform back                                   │
│                                                              │
│    Result: correlated_values[n_windows]                     │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 8. QoS ENFORCEMENT                                          │
│    For each metric with qos_min/max:                        │
│      ├─> np.maximum(values, qos_min)                        │
│      └─> np.minimum(values, qos_max)                        │
│    Result: bounded_values[n_windows]                        │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 9. DATAFRAME CONSTRUCTION                                   │
│    df = pd.DataFrame({                                       │
│        'timestamp': time_windows,                            │
│        'node1_metric1': values1,                            │
│        'node1_metric2': values2,                            │
│        ...                                                   │
│    })                                                        │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 10. LAYER 6 - VALIDATION                                    │
│     Statistical Validation:                                  │
│       ├─> Check for NaN/Inf values                          │
│       ├─> Verify distribution moments match                 │
│       └─> KS test for distribution fit                      │
│                                                              │
│     Logical Validation:                                      │
│       ├─> QoS boundary compliance                           │
│       └─> Metric ordering (e.g., p50 < p95)                │
│                                                              │
│     Temporal Validation:                                     │
│       ├─> Autocorrelation structure                         │
│       ├─> Seasonality detection                             │
│       └─> Change point detection                            │
│                                                              │
│     Quality Score = Σ (weight_i * score_i)                  │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 11. OUTPUT GENERATION                                        │
│     Formats:                                                 │
│       • CSV  → df.to_csv()                                  │
│       • JSON → df.to_json(orient='records')                 │
│       • Parquet → df.to_parquet()                           │
│       • SAR Format → export_sar_format() (custom)           │
│                                                              │
│     Metadata:                                                │
│       • Generation time                                      │
│       • Quality score                                        │
│       • Configuration summary                                │
└─────────────────────────────────────────────────────────────┘
                            ↓
                    [COMPLETED]
```

---

### 🌐 **API ENDPOINTS**

#### **1. POST /api/generate**
- **Amaç**: Sentetik data üretimi
- **Input**: JSON configuration (nodes, metrics, anomalies, etc.)
- **Process**: Yukarıdaki flow'u çalıştırır
- **Output**: Generated DataFrame + metadata

#### **2. GET /api/download**
- **Amaç**: Üretilen veriyi indir
- **Params**: format (csv/json/parquet/sar)
- **Output**: File download

#### **3. GET /api/health**
- **Amaç**: Servis sağlık kontrolü
- **Output**: {"status": "healthy", "version": "2.1"}

---

### 🔧 **TEMEL SINIFLAR VE DATA YAPILARI**

```python
# Core Classes
DataGenerator(config: GeneratorConfig)
  └─ generate() → pd.DataFrame

# Configuration Classes
GeneratorConfig      # Ana konfigürasyon
NodeConfig          # Node tanımları
MetricConfig        # Metrik tanımları
DistributionConfig  # Dağılım parametreleri
SeasonalityConfig   # Mevsimsellik ayarları
ARIMAConfig         # ARIMA parametreleri
CorrelationConfig   # Korelasyon tanımları
ChangePointConfig   # Değişim noktaları
AnomalyConfig       # Anomali senaryoları
ValidationConfig    # Doğrulama kriterleri

# Enums
DistributionType    # normal, gamma, beta, etc.
AnomalyType        # spike, drop, congestion, etc.
ChangeType         # step, ramp
StabilityLevel     # high, medium, low
```

---

### 📈 **ÖZELLEŞME VE GENİŞLETME NOKTALARI**

1. **Yeni Dağılım Ekleme**: `_generate_base_distribution()` metoduna yeni case
2. **Yeni Anomali Tipi**: `_apply_anomalies()` metoduna yeni elif bloğu
3. **Custom Korelasyon**: `_apply_correlations()` metodunda Gaussian Copula yerine başka yöntem
4. **Prosedür Simulasyonu**: Layer 4'e state machine ekleyerek
5. **Yeni Validasyon**: `calculate_validation_score()` fonksiyonuna yeni metrik

---