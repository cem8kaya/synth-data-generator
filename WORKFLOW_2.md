# 📊 TELECOM SYNTHETIC DATA GENERATOR - DETAYLI TEKNİK ANALİZ

## 🎯 **UYGULAMA AMACI**

Bu uygulama, **telekom operatörleri için gerçekçi sentetik network KPI verisi üreten** profesyonel bir sistemdir. Asıl amacı:
- Machine learning modellerinin eğitimi
- Kapasite planlaması simülasyonu  
- Anomali tespit algoritmalarının geliştirilmesi
- Hassas operasyonel verilerin paylaşılmadan test ortamları oluşturulması

---

## 🏗️ **MİMARİ TASARIM - 6 KATMANLI MODEL**

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

## 🔬 **LAYER 1: İSTATİSTİKSEL TEMEL - DAĞILIM ÜRETME KATMANI**

Bu katman, tüm sistemin matematiksel temelini oluşturur ve üzerindeki tüm katmanların güvenle kullanabileceği istatistiksel olarak geçerli sayılar üretir. Her network metriğinin kendine özgü bir davranış karakteristiği vardır ve bu karakteristikler belirli olasılık dağılımlarıyla en iyi şekilde modellenebilir.

### **Neden Farklı Dağılımlar Kullanılır?**

Gerçek dünyada farklı fenomenler farklı istatistiksel davranışlar gösterir. Örneğin, bir santraldeki telefon çağrılarının gelme zamanlaması ile bu çağrıların süreleri tamamen farklı doğalara sahiptir. Çağrılar rastgele ve bağımsız olarak gelirken (Poisson), çağrı süreleri genellikle birkaç dakika etrafında yoğunlaşır ama bazen çok uzun olabilir (Log-Normal). İşte bu nedenle sistemimiz altı farklı dağılım tipi kullanır.

### **Kullanılan Dağılımlar ve Detaylı Açıklamaları**

| Dağılım | Kullanım Alanı | Parametreler | Matematiksel Özellik |
|---------|---------------|--------------|---------------------|
| **Poisson** | Event arrival rates, çağrı denemeleri | λ (mean) | Discrete, non-negative integers |
| **Gamma** | Latency, gecikme, işleme süreleri | shape (α), scale (θ), CV | Continuous, positive, right-skewed |
| **Log-Normal** | Throughput, bandwidth, data volume | μ, σ (log-scale) | Continuous, positive, heavy-tailed |
| **Beta** | Success rates, availability (0-1 arası) | α, β, stability level | Bounded [0,1], flexible shape |
| **Exponential** | Inter-arrival times, failure times | rate (λ) | Memoryless, decreasing probability |
| **Normal** | Genel metrikler | mean (μ), std (σ) | Symmetric, unbounded |

#### **Poisson Dağılımı - Event Arrival Modeling**

Poisson dağılımı, belirli bir zaman aralığında meydana gelen bağımsız olayların sayısını modellemek için kullanılır. Telekom networklerinde, SIP INVITE mesajlarının gelme sıklığı, PDU session kurulum istekleri veya handover olayları Poisson süreciyle mükemmel şekilde modellenir. 

Lambda parametresi ortalama olay sayısını temsil eder. Örneğin lambda yüz ise, dakikada ortalama yüz çağrı beklenir, ancak bazı dakikalarda doksan dokuz, bazılarında yüz bir olabilir. Dağılımın güzel yanı, bu varyasyonu matematiksel olarak tutarlı bir şekilde üretmesidir.

Gerçek dünya uygulamasında lambda sabit değildir. Gece yarısı lambda on olabilirken, öğlen saatlerinde beş yüze çıkabilir. Bu yüzden sistemimiz non-homogeneous Poisson process kullanır, yani lambda zamanın bir fonksiyonu olarak tanımlanır. Bu fonksiyon günlük döngüleri, yoğun saatleri ve haftalık pattern'leri içerir.

```python
# Poisson generation with time-varying lambda
base_lambda = 100  # Base rate
hour_of_day = timestamp.hour
time_factor = 1 + 0.3 * sin(2*pi * hour_of_day / 24)  # Daily cycle
busy_hour_boost = 1.5 if 8 <= hour_of_day <= 10 else 1.0
adjusted_lambda = base_lambda * time_factor * busy_hour_boost
event_count = np.random.poisson(adjusted_lambda)
```

#### **Gamma Dağılımı - Latency ve Timing Modeling**

Gamma dağılımı, network latency ve işleme süreleri için ideal bir modeldir. Latency değerleri hiçbir zaman negatif olamaz, genellikle belli bir değer etrafında yoğunlaşır ama bazen çok yüksek değerler alabilir, bu da sağa çarpık bir dağılım oluşturur.

Shape parametresi dağılımın şeklini, scale parametresi ise yayılımını kontrol eder. İlginç olan nokta, bu iki parametreyi doğrudan ayarlamak yerine, ortalama ve coefficient of variation üzerinden hesaplamamızdır. CV değeri standart sapmanın ortalamaya oranıdır ve network'ün ne kadar kararlı çalıştığını gösterir.

Düşük CV değerli bir network çok tutarlıdır, latency değerleri dar bir aralıkta kalır. Yüksek CV değerli network ise değişkendir, bazen hızlı bazen yavaş çalışır. Örneğin, yüksek kaliteli fiber optik network CV değeri sıfır nokta bir civarında olabilirken, congestion problemi yaşayan wireless network CV değeri sıfır nokta beş veya daha yüksek olabilir.

```python
# Gamma parameter calculation from mean and CV
mean_latency = 50  # milliseconds
cv = 0.3  # Coefficient of variation
shape = 1 / (cv ** 2)  # Inverse square relationship
scale = mean_latency / shape
latency_values = np.random.gamma(shape, scale, size=n_samples)
```

Shape parametresi on bir ise, dağılım neredeyse bell curve gibi simetriktir. Shape parametresi iki ise, belirgin sağa çarpıklık vardır. Shape parametresi bir ise, exponential dağılıma yaklaşır. Sistemimiz genellikle shape değerlerini beş ile yirmi arasında tutar, bu da gerçekçi latency profilleri üretir.

#### **Log-Normal Dağılımı - Throughput ve Bandwidth Modeling**

Log-Normal dağılım, throughput ve bandwidth gibi metrikler için kullanılır. Bu dağılımın özel özelliği, değerlerin logaritması normal dağılım gösterir, ancak değerlerin kendisi son derece sağa çarpık bir profil sergiler. Bu, gerçek network throughput davranışını mükemmel yansıtır.

Çoğu kullanıcı orta seviye throughput alır, bazı şanslı kullanıcılar yüksek throughput alır, ama birkaç kullanıcı çok yüksek throughput değerlerine ulaşabilir. Örneğin median throughput beş megabit olabilirken, doksan beşinci percentile yirmi megabit, maksimum değer elli megabit olabilir. Bu tip heavy-tailed distribution, log-normal ile doğal olarak modellenir.

Sistemimiz log-normal parametrelerini median ve doksan beşinci percentile değerlerinden türetir. Bu yaklaşım, kullanıcı için daha sezgiseldir çünkü doğrudan gözlemlenebilir metriklerle çalışır. Mu ve sigma parametreleri bu hedef değerlerden ters hesaplama ile bulunur.

```python
# Log-normal parameter calculation from median and p95
median_throughput = 10  # Mbps
p95_throughput = 30  # Mbps
# Solve equations: median = exp(mu), p95 = exp(mu + 1.645*sigma)
sigma = (log(p95_throughput) - log(median_throughput)) / 1.645
mu = log(median_throughput)
throughput_values = np.random.lognormal(mu, sigma, size=n_samples)
```

#### **Beta Dağılımı - Success Rate ve Availability Modeling**

Beta dağılımı, sıfır ile bir arasında sınırlı olan metrikler için özel olarak tasarlanmıştır. Success rate, availability percentage, packet delivery ratio gibi metrikler doğası gereği bu aralıktadır ve beta dağılımı bunları modellemek için matematiksel olarak mükemmel bir araçtır.

Beta dağılımının güzelliği, iki parametresiyle çok farklı şekiller alabilmesidir. Alpha ve beta parametreleri her ikisi de büyük olduğunda, dağılım dar ve peaked olur. Bu, çok kararlı bir network'ü temsil eder, success rate sürekli doksan beş ile doksan sekiz arasında salınır. Her iki parametre de küçük olduğunda, dağılım U-shape alır, yani değerler ya çok düşük ya çok yüksek olur, bu da problemli bir network'ü gösterir.

Sistemimiz alpha ve beta parametrelerini iki kavramdan türetir: target rate ve stability level. Target rate, istenen ortalama success rate'dir. Stability level ise bu target'ın etrafında ne kadar dar kalındığını belirler. High stability, çok az varyasyon demektir. Low stability, geniş bir değişkenlik aralığı demektir.

```python
# Beta parameter calculation from target and stability
target_rate = 0.95  # 95% success rate
stability = "HIGH"  # HIGH, MEDIUM, or LOW
concentration_map = {"HIGH": 50, "MEDIUM": 10, "LOW": 2}
concentration = concentration_map[stability]
alpha = target_rate * concentration  # = 0.95 * 50 = 47.5
beta = (1 - target_rate) * concentration  # = 0.05 * 50 = 2.5
success_rate_values = np.random.beta(alpha, beta, size=n_samples)
```

High stability ile target doksan beş percent kombinasyonu, alpha kırk yedi nokta beş ve beta iki nokta beş verir. Bu dağılım, success rate değerlerini doksan üç ile doksan yedi arasında sıkı bir şekilde tutar. Medium stability ise alpha dokuz nokta beş ve beta sıfır nokta beş verir, bu da doksan ile doksan sekiz arası daha geniş bir dağılım sağlar.

#### **Exponential Dağılımı - Inter-arrival Times**

Exponential dağılım, olaylar arası süreleri modellemek için kullanılır. Eğer olaylar Poisson süreciyle geliyorsa, olaylar arası süreler otomatik olarak exponential dağılım gösterir. Bu iki dağılım matematiksel olarak birbirinin ikilidir.

Exponential dağılımın önemli bir özelliği memoryless property'sidir. Yani bir sonraki olayın ne zaman geleceği, en son olayın ne zaman geldiğinden bağımsızdır. Bu, gerçek network trafiği için genellikle geçerli bir varsayımdır çünkü farklı kullanıcılar birbirinden bağımsız hareket eder.

Rate parametresi lambda, birim zamanda beklenen olay sayısıdır. Eğer lambda yüz ise, dakikada ortalama yüz olay olur, bu da olaylar arası ortalama sürenin sıfır nokta sıfır bir dakika yani altı yüz milisaniye olması demektir. Exponential dağılım, bu altı yüz milisaniye etrafında değerler üretir ama büyük varyasyonla, bazı olaylar hemen arkasından gelir, bazıları gecikmeli gelir.

---

## 🔗 **LAYER 2: ÇOK DEĞİŞKENLİ BAĞIMLILIKLAR - KORELASYON VE NEDENSELLIK KATMANI**

Bu katman, Layer 1'in ürettiği bağımsız değerleri alır ve aralarında gerçek dünyada gözlemlenen ilişkileri kurar. Gerçek telekom networklerinde metrikler izole değildir, karmaşık bir bağımlılık ağı içinde birbirleriyle etkileşir. Latency arttığında success rate düşer, throughput yükseldiğinde CPU kullanımı artar, packet loss olduğunda voice quality bozulur. Bu katman, bu ilişkileri matematiksel olarak modelleyerek sentetik verinin gerçekçiliğini dramatik şekilde artırır.

### **Gaussian Copula - Korelasyon Yapısını Koruma**

Gaussian Copula, farklı dağılımlara sahip değişkenler arasında korelasyon yaratmanın zarif bir yöntemidir. Temel fikir şudur: önce değişkenleri uniform dağılıma transform edersiniz, uniform değerleri correlated normal değişkenlere dönüştürürsünüz, sonra bu normal değişkenleri istediğiniz orijinal dağılımlara geri transform edersiniz.

Sürecin ilk adımında, her değişkenin kendi dağılımının cumulative distribution function'ı kullanılarak uniform değerlere dönüştürülür. Örneğin, gamma dağılımlı bir latency değeri elli milisaniye ise ve bu değer dağılımın yetmiş beşinci percentile'ında ise, bu değer sıfır nokta yetmiş beş uniform değerine map edilir. Bu işlem probability integral transform olarak bilinir ve her dağılımdan uniform'a geçişi garanti eder.

İkinci adımda, bu uniform değerler standard normal dağılıma transform edilir. Bu, inverse normal CDF kullanılarak yapılır. Sıfır nokta yetmiş beş uniform değeri, yaklaşık sıfır nokta altmış yedi standard normal değerine karşılık gelir. Bu noktada tüm değişkenlerimiz standard normal uzayında bulunur ve burada korelasyon matrisini uygulayabiliriz.

```python
# Gaussian Copula implementation
def apply_gaussian_copula(values_dict, correlation_matrix):
    # Step 1: Transform to uniform using empirical CDF
    uniform_values = {}
    for name, values in values_dict.items():
        ranks = stats.rankdata(values)
        uniform_values[name] = ranks / (len(values) + 1)
    
    # Step 2: Transform to standard normal
    normal_values = {}
    for name, u_vals in uniform_values.items():
        normal_values[name] = stats.norm.ppf(u_vals)
    
    # Step 3: Apply correlation via Cholesky decomposition
    L = np.linalg.cholesky(correlation_matrix)
    normal_matrix = np.column_stack([normal_values[name] for name in sorted(normal_values.keys())])
    correlated_normal = normal_matrix @ L.T
    
    # Step 4: Transform back to uniform
    correlated_uniform = stats.norm.cdf(correlated_normal)
    
    # Step 5: Transform back to original distributions
    result = {}
    for i, name in enumerate(sorted(values_dict.keys())):
        original_distribution = get_distribution_for_metric(name)
        result[name] = original_distribution.ppf(correlated_uniform[:, i])
    
    return result
```

Üçüncü adım kritiktir: Cholesky decomposition kullanarak korelasyon matrisini uygularız. Korelasyon matrisi mutlaka positive semi-definite olmalıdır, yani tüm eigenvalue'ları sıfır veya pozitif olmalıdır. Eğer kullanıcı tutarsız korelasyonlar tanımlarsa, örneğin A ile B arasında artı bir, B ile C arasında artı bir, ama A ile C arasında eksi bir korelasyon, bu matematiksel olarak imkansızdır. Sistemimiz bu durumda matrisi nearest valid matrix'e project eder veya kullanıcıyı uyarır.

Dördüncü adımda, correlated normal değerler tekrar uniform değerlere dönüştürülür, bu sefer normal CDF kullanılarak. Son adımda, her değişken kendi orijinal dağılımına geri transform edilir. Örneğin latency gamma dağılımından geliyordu, şimdi correlated uniform değer gamma'nın inverse CDF'i ile gamma değerine geri dönüştürülür.

Bu sürecin sonunda, her değişken kendi orijinal dağılımını korurken, aralarında istenen korelasyon yapısı oluşmuş olur. Bu, Gaussian Copula'nın en büyük avantajıdır: marginal dağılımları bozmadan korelasyon yaratır.

### **Dependency Modeling - Nedensel İlişkiler**

Korelasyonun ötesinde, bazı metrikler arasında doğrudan nedensel bağlar vardır. Örneğin, network congestion olduğunda hem latency artar hem de success rate düşer. Ama bu iki etki aynı anda ve bağımlı olarak gerçekleşir. Dependency modeling, bir metriğin değerinin diğer metriklerin değerlerine göre dinamik olarak ayarlanmasını sağlar.

Sistemimiz basit bir dependency mechanism kullanır. Her metrik, bağımlı olduğu metriklerin bir listesini içerir. Generation sırasında, önce tüm base değerler üretilir, sonra dependency pass'inde her metrik bağımlılıklarını kontrol eder. Eğer bir dependency metrik düşük değerler alıyorsa, bağımlı metrik de scale down edilir.

```python
# Dependency application example
def apply_dependencies(metric_values, metric_config, all_values_df):
    result = metric_values.copy()
    
    for dependency_name in metric_config.dependencies:
        if dependency_name in all_values_df.columns:
            dep_values = all_values_df[dependency_name].values
            
            # Normalize dependency to [0, 1]
            dep_normalized = (dep_values - dep_values.min()) / (dep_values.max() - dep_values.min())
            
            # Scale target metric: full value when dep=1, 70% value when dep=0
            scale_factor = 0.7 + 0.3 * dep_normalized
            result *= scale_factor
    
    return result
```

Örneğin, call success rate metriği network latency'ye bağımlı olarak tanımlanmışsa, latency değerleri yüksek olduğunda success rate otomatik olarak düşürülür. Bu, korelasyondan daha güçlü bir ilişkidir çünkü direction of causality'yi encode eder.

### **Bayesian Network - Nedensel Graf Yapısı**

Bayesian Network, değişkenler arası nedensel ilişkileri directed acyclic graph olarak modelleyen güçlü bir araçtır. Her node bir metriği temsil eder, her edge bir nedensel bağlantıyı gösterir. Örneğin, network load node'undan latency node'una bir edge varsa, bu "network load, latency'nin bir nedenidir" demektir.

Her node, parent node'larının değerlerine bağlı olarak conditional probability distribution içerir. Örneğin, latency node'u "eğer network load low ise latency distribution gamma with mean=30, eğer network load high ise latency distribution gamma with mean=80" şeklinde bir CPD içerebilir.

Bayesian Network'ün generation süreci topological sort ile yapılır. Önce parent'ı olmayan node'lar generate edilir, sonra parent'ları generate edilmiş node'lar, böylece her node generate edilirken parent değerleri hazırdır ve condition'lar doğru şekilde uygulanabilir.

```python
# Bayesian Network generation with topological ordering
def generate_with_bayesian_network(network_structure, n_samples):
    # Topological sort: nodes with no parents first
    sorted_nodes = topological_sort(network_structure)
    results = {}
    
    for node in sorted_nodes:
        parent_values = {p: results[p] for p in node.parents}
        
        # Generate values conditional on parent values
        node_values = np.zeros(n_samples)
        for i in range(n_samples):
            # Get conditional distribution based on parent values at this sample
            parent_state = {p: parent_values[p][i] for p in node.parents}
            conditional_dist = node.get_conditional_distribution(parent_state)
            node_values[i] = conditional_dist.sample()
        
        results[node.name] = node_values
    
    return results
```

Sistemimizde Bayesian Network tam implement edilmemiş, ancak dependency mechanism'i onun basit bir versiyonu olarak düşünülebilir. Gelecek versiyonlarda, full Bayesian Network inference ve learning capabilities eklenebilir.

---

## ⏰ **LAYER 3: TEMPORAL MÜHENDİSLİĞİ - ZAMAN SERİSİ KATMANI**

Bu katman, veriye zamansal tutarlılık kazandırır. Gerçek network metrikleri zaman içinde rastgele değildir, belirli pattern'ler ve smooth transitions gösterir. Sabahtan öğleye geçerken trafik aşamalı olarak artar, haftalık döngüler tekrar eder, ani sıçramalar olmaz. Temporal engineering olmadan, üretilen data anlamsız olur: bir dakika yüksek trafik, sonraki dakika çok düşük trafik, ardından tekrar yüksek. Bu gerçek network davranışını yansıtmaz ve machine learning modelleri bu tip data ile temporal pattern'leri öğrenemez.

### **Fourier Series - Seasonality Modelleme**

Fourier Series, periyodik pattern'leri matematiksel olarak temsil etmenin elegant bir yoludur. Fourier Teoremi der ki, herhangi bir periyodik fonksiyon, sinüs ve cosinüs fonksiyonlarının toplamı olarak ifade edilebilir. Her sinüs ve cosinüs terimi bir "harmonic" olarak adlandırılır.

Günlük seasonality için fundamental period yirmi dört saattir. İlk harmonic, yirmi dört saatlik tam bir sinüs dalgasıdır ve genel günlük ritmi verir. Gece yarısı minimum, öğlen maksimum, akşam tekrar yüksek, gece tekrar minimum şeklinde smooth bir döngü. İkinci harmonic, on iki saatlik bir döngüdür ve günde iki kez tekrar eden pattern'leri yakalar. Örneğin öğle ve akşam olmak üzere iki peak olabilir. Üçüncü harmonic sekiz saatlik döngüdür ve daha ince detayları yakalar.

```python
# Fourier Series seasonality implementation
def apply_fourier_seasonality(base_values, timestamps, period_hours=24, harmonics=3, amplitude=0.3):
    n = len(base_values)
    t = np.arange(n)
    
    # Base frequency: one complete cycle per period
    base_freq = 2 * np.pi / (period_hours * (60 / granularity_minutes))
    
    # Sum multiple harmonics with decreasing amplitude
    seasonal_component = np.zeros(n)
    for h in range(1, harmonics + 1):
        # Each harmonic has frequency h * base_freq
        harmonic_amplitude = amplitude / h  # Amplitude decreases with harmonic order
        phase = np.random.uniform(0, 2*np.pi)  # Random phase shift
        seasonal_component += harmonic_amplitude * np.sin(base_freq * h * t + phase)
    
    # Multiply base values by (1 + seasonal_component)
    # This gives percentage change relative to base
    result = base_values * (1 + seasonal_component)
    
    return result
```

Harmonik sayısı kritik bir parametredir. Çok fazla harmonik kullanmak overfitting'e yol açar, model noise'u da öğrenmeye çalışır. Çok az harmonik kullanmak underfitting'e yol açar, önemli pattern'ler kaçırılır. Pratikte üç ile beş arası harmonik, telecom network seasonality'si için yeterlidir. Basit daily pattern için iki harmonik yeter, kompleks pattern'ler için dört veya beş harmonik kullanılabilir.

Amplitude parametresi, seasonality'nin ne kadar güçlü olduğunu kontrol eder. Amplitude sıfır nokta üç ise, değerler base value'larının yüzde otuz üçüne kadar yukarı veya aşağı salınabilir. Residential network'ler yüksek amplitude gösterir çünkü kullanıcılar gündüz çok aktif, gece çok pasiftir. Enterprise network'ler düşük amplitude gösterir çünkü ofis saatleri boyunca trafik nispeten stabıldır.

### **ARIMA Modeli - Temporal Smoothing ve Autocorrelation**

ARIMA modeli, zaman serisinin smooth olmasını ve temporal coherence göstermesini sağlar. ARIMA üç component'ten oluşur: AutoRegressive, Integrated ve Moving Average. Sistemimizde sadece AR ve MA component'lerini kullanıyoruz, I component'i (differencing) kullanmıyoruz çünkü verilerimiz zaten stationary.

AutoRegressive component, bir değerin geçmiş değerlerine bağlı olduğunu söyler. AR order iki ise, current value son iki value'ya bağlıdır. AR coefficient'lar bu bağımlılığın gücünü kontrol eder. Tipik AR coefficient'lar sıfır nokta altı ve sıfır nokta üç gibi değerlerdir, birinci lag daha güçlü etki eder, ikinci lag daha zayıf.

```python
# ARIMA generation with AR and MA components
def apply_arima_smoothing(base_values, ar_order=2, ma_order=1, 
                          ar_coef=[0.6, 0.3], ma_coef=[0.4], noise_std=0.05):
    n = len(base_values)
    result = np.zeros(n)
    
    # Initialize first few values
    result[:ar_order] = base_values[:ar_order]
    
    # Generate noise sequence
    noise = np.random.normal(0, noise_std, n)
    
    for t in range(ar_order, n):
        # AR component: weighted sum of past values
        ar_component = sum(ar_coef[i] * result[t - i - 1] 
                          for i in range(ar_order))
        
        # MA component: weighted sum of past errors
        ma_component = sum(ma_coef[i] * noise[t - i - 1] 
                          for i in range(min(ma_order, t)))
        
        # Combine: weighted average of base value, AR, MA, and noise
        result[t] = (0.3 * base_values[t] + 
                     0.5 * ar_component + 
                     0.2 * ma_component + 
                     noise[t])
    
    return result
```

Moving Average component, geçmiş error'lara bağlıdır. Error, predicted value ile actual value arasındaki farktır. MA order bir ise, current value son bir error'a bağlıdır. MA component, systematic error'ları cancel etmeye yardımcı olur ve time series'i daha smooth yapar.

Weight'ler çok önemlidir. Sistemimiz tipik olarak base value'ya yüzde otuz, AR component'e yüzde elli, MA component'e yüzde yirmi ağırlık verir. Bu, temporal smoothing'i sağlarken base distribution'ın özelliklerini de korur. Eğer AR'a çok fazla ağırlık verirsek, time series çok smooth olur ama base distribution'dan uzaklaşır. Eğer base value'ya çok fazla ağırlık verirsek, temporal coherence kaybolur.

AR coefficient'lar eksi bir ile bir arasında olmalıdır, aksi halde time series diverge eder veya wild oscillation gösterir. Coefficient'ların toplamı birden küçük olmalıdır, bu stationarity'yi garanti eder. MA coefficient'lar daha esnek olabilir ama genellikle eksi bir ile bir arasında tutulur.

### **Change Point Detection and Injection**

Network'lerde structural change'ler vardır: software upgrade, hardware replacement, capacity expansion, configuration change. Bu change'ler KPI'larda ani veya aşamalı değişikliklere yol açar. Change Point Injection modülü, bu tip event'leri simüle eder.

Üç ana change type vardır. Step change, immediate ve permanent bir değişikliktir. Örneğin bir software patch anında uygulanır ve performance'ı immediately improve eder. Step change'de değer bir seviyeden başka bir seviyeye instant geçer. Implementation basittir: change timestamp'inden sonraki tüm değerler magnitude factor ile multiply edilir.

```python
# Step change application
def apply_step_change(values, change_time_idx, magnitude):
    result = values.copy()
    # magnitude = 0.2 means +20% increase
    result[change_time_idx:] *= (1 + magnitude)
    return result
```

Ramp change, gradual bir değişikliktir. Örneğin capacity expansion birkaç gün boyunca aşamalı olarak deploy edilir. Ramp change'de değer starting level'dan ending level'a linear veya smooth curve ile geçer. Duration parametresi transition'ın ne kadar sürdüğünü belirtir. Implementation lineer interpolation kullanır: her time step'te magnitude bir miktar artar, sonunda tam magnitude'a ulaşır.

```python
# Ramp change application
def apply_ramp_change(values, start_idx, duration_steps, magnitude):
    result = values.copy()
    end_idx = min(start_idx + duration_steps, len(result))
    
    # Linear ramp from 0 to magnitude
    ramp = np.linspace(0, magnitude, end_idx - start_idx)
    result[start_idx:end_idx] *= (1 + ramp)
    
    # Full magnitude after ramp completes
    result[end_idx:] *= (1 + magnitude)
    
    return result
```

Spike change, temporary bir değişikliktir. Örneğin bir special event, büyük spor maçı veya konser, geçici bir trafik artışına yol açar. Spike change'de değer hızla artar, bir peak'te tutar ve sonra hızla geri düşer. Shape Gaussian bell curve ile modellenir. Peak'e yaklaştıkça magnitude artar, peak'ten uzaklaştıkça azalır.

Spike implementation Gaussian function kullanır. Center point peak zamanıdır. Width parametresi spike'ın ne kadar geniş olduğunu kontrol eder. Her time step'te Gaussian function evaluate edilir ve magnitude buna göre uygulanır.

---

## 🔬 **LAYER 4: PROSEDÜR SİMÜLASYONU - PROTOKOL MODELLEME KATMANI**

Bu katman gerçek network protokollerinin davranışını taklit eder. SIP çağrı akışları, NAS kayıt prosedürleri, GTP session kurulumları gibi telecom spesifik işlemleri adım adım simüle eder. Her prosedür kendi state machine'ini takip eder ve network koşullarına göre başarı veya başarısızlık üretir.

### **State Machine Modeling - Durum Geçişleri**

Her prosedür bir state machine olarak tasarlanır. State machine, olası durumları ve durumlar arası geçişleri tanımlar. Örneğin bir SIP call flow şu state'leri içerir: IDLE, INVITE_SENT, TRYING, RINGING, PROGRESS, ESTABLISHED, BYE_SENT, TERMINATED.

Her transition bir olasılığa sahiptir. INVITE_SENT'den TRYING'e geçiş olasılığı çok yüksektir, neredeyse yüzde doksan dokuz nokta dokuz, çünkü bu neredeyse her zaman gerçekleşir. Ancak RINGING'den ESTABLISHED'e geçiş olasılığı daha düşüktür, belki yüzde doksan beş, çünkü kullanıcı aramayı reddetebilir veya timeout olabilir.

```python
# State machine implementation for SIP call
class SIPCallStateMachine:
    def __init__(self, network_condition):
        self.state = "IDLE"
        self.network_condition = network_condition
        self.timestamps = {}
        
    def execute_call(self):
        self.state = "INVITE_SENT"
        self.timestamps['invite'] = current_time()
        
        # Transition probabilities adjusted by network condition
        if self.network_condition == "GOOD":
            trying_prob = 0.999
            ringing_prob = 0.98
            established_prob = 0.95
        elif self.network_condition == "DEGRADED":
            trying_prob = 0.95
            ringing_prob = 0.90
            established_prob = 0.85
        else:  # POOR
            trying_prob = 0.85
            ringing_prob = 0.75
            established_prob = 0.70
        
        # Execute state transitions
        if random.random() < trying_prob:
            self.state = "TRYING"
            self.timestamps['trying'] = current_time()
        else:
            self.state = "FAILED"
            return self.get_metrics()
        
        if random.random() < ringing_prob:
            self.state = "RINGING"
            self.timestamps['ringing'] = current_time()
        else:
            self.state = "FAILED"
            return self.get_metrics()
        
        if random.random() < established_prob:
            self.state = "ESTABLISHED"
            self.timestamps['established'] = current_time()
            # Simulate call duration
            time.sleep(random.expovariate(1/120))  # Average 120 seconds
            self.state = "BYE_SENT"
            self.state = "TERMINATED"
        else:
            self.state = "FAILED"
        
        return self.get_metrics()
    
    def get_metrics(self):
        setup_latency = self.timestamps.get('established', 0) - self.timestamps['invite']
        success = (self.state == "TERMINATED")
        return {
            'setup_latency': setup_latency,
            'call_success': success,
            'failure_stage': self.state if not success else None
        }
```

Context-aware probability adjustment çok önemlidir. Transition olasılıkları statik değildir, network context'ine göre dinamik olarak ayarlanır. Network congestion varsa, her transition'da failure olasılığı artar. High latency varsa, timeout olasılığı artar. Bu yaklaşım, prosedürlerin gerçekçi bir şekilde fail etmesini sağlar.

### **Counter ve KPI Hesaplama**

Her prosedür execution counter'lara yansıtılır. Attempt counter, başlatılan prosedür sayısını sayar. Success counter, başarılı tamamlanan prosedür sayısını sayar. Failure counter, her failure reason için ayrı ayrı tutulur: timeout failure, reject failure, error failure.

Bu counter'lar periyodik olarak aggregate edilir ve KPI'lara dönüştürülür. Success rate, success counter'ın attempt counter'a oranıdır. Average setup latency, tüm setup latency değerlerinin ortalamasıdır. Percentile latency'ler, sorted latency array'inden hesaplanır.

```python
# Counter aggregation and KPI calculation
class MetricAggregator:
    def __init__(self, window_duration_minutes=15):
        self.window_duration = window_duration_minutes
        self.counters = defaultdict(int)
        self.latency_samples = []
        
    def record_procedure(self, metrics):
        self.counters['attempt'] += 1
        if metrics['call_success']:
            self.counters['success'] += 1
            self.latency_samples.append(metrics['setup_latency'])
        else:
            self.counters[f"failure_{metrics['failure_stage']}"] += 1
    
    def calculate_kpis(self):
        kpis = {}
        
        # Success rate
        if self.counters['attempt'] > 0:
            kpis['success_rate'] = self.counters['success'] / self.counters['attempt']
        else:
            kpis['success_rate'] = 0.0
        
        # Latency statistics
        if self.latency_samples:
            kpis['avg_latency'] = np.mean(self.latency_samples)
            kpis['p50_latency'] = np.percentile(self.latency_samples, 50)
            kpis['p95_latency'] = np.percentile(self.latency_samples, 95)
            kpis['p99_latency'] = np.percentile(self.latency_samples, 99)
        else:
            kpis['avg_latency'] = 0.0
            kpis['p50_latency'] = 0.0
            kpis['p95_latency'] = 0.0
            kpis['p99_latency'] = 0.0
        
        # Failure breakdown
        total_failures = self.counters['attempt'] - self.counters['success']
        if total_failures > 0:
            for key, value in self.counters.items():
                if key.startswith('failure_'):
                    failure_type = key.replace('failure_', '')
                    kpis[f'{failure_type}_rate'] = value / self.counters['attempt']
        
        return kpis
```

---

## 🚨 **LAYER 5: ANOMALİ MODELLEME - PROBLEM SİMÜLASYONU KATMANI**

Gerçek telecom network'lerinde her şey her zaman mükemmel çalışmaz. Hardware failure'lar, software bug'lar, capacity bottleneck'ler, external attack'ler ve konfigürasyon hataları anomalilere yol açar. Anomali Modelleme modülü bu exceptional durumları sistematik olarak simüle eder. Bu machine learning anomaly detection modellerinin eğitimi için kritiktir.

### **Anomali Tipleri ve Enjeksiyon Mekanizmaları**

| Anomali Tipi | Etki Mekanizması | Network Nedeni | Propagation Davranışı |
|--------------|------------------|----------------|----------------------|
| **SPIKE** | Ani artış: value *= (1 + severity) | Traffic burst, DDoS attack | Dependency graph üzerinden yayılır |
| **DROP** | Ani düşüş: value *= (1 - severity) | Service interruption, failover | İlgili metriklere cascade eder |
| **OSCILLATION** | Salınım: sin-wave pattern | Misconfiguration, feedback loop | Periodic pattern oluşturur |
| **CONGESTION** | Karma etki: success↓, latency↑ | Capacity exceeded, overload | Tüm performance metriklerini etkiler |
| **DEGRADATION** | Kademeli bozulma | Hardware aging, memory leak | Zamanla şiddetlenir |
| **OUTAGE** | Tam kesinti: value *= 0.2 | Complete failure, power loss | İlgili tüm servisleri etkiler |

### **Spike Anomaly - Traffic Burst**

Spike anomaly, kısa süreli ani artışları simüle eder. Bu bir flash crowd event, viral content, veya DDoS attack'den kaynaklanabilir. Spike'ın karakteristiği, hızlı yükseliş, peak'te durma ve hızlı düşüştür. Duration tipik olarak on beş dakika ile iki saat arasındadır.

Implementation straightforward'dır: anomaly'nin aktif olduğu zaman pencerelerinde, etkilenen metriklerin değerleri severity factor ile multiply edilir. Severity sıfır nokta beş ise, değerler yüzde elli artar. Severity bir ise değerler iki katına çıkar.

```python
# Spike anomaly injection
def inject_spike_anomaly(values, start_idx, duration_steps, severity):
    result = values.copy()
    end_idx = min(start_idx + duration_steps, len(result))
    
    # Simple approach: constant multiplier during spike period
    result[start_idx:end_idx] *= (1 + severity)
    
    return result
```

Daha sophisticated bir yaklaşım, spike'a Gaussian shape vermektir. Bu durumda magnitude peak'te maksimum, başlangıç ve bitişte sıfıra yakındır, smooth bir geçiş sağlar.

### **Congestion Anomaly - Network Overload**

Congestion anomaly en kompleks tiplerden biridir çünkü farklı metrikleri farklı şekilde etkiler. Network congestion olduğunda, latency artar çünkü paketler queue'larda bekler. Success rate düşer çünkü timeout'lar ve drop'lar artar. Throughput düşer çünkü TCP congestion control throttle yapar. Packet loss artar çünkü buffer'lar overflow olur.

Sistemimiz congestion'ı metric type'a göre farklı uygular. Eğer metric name'de "latency" veya "time" varsa, değerler artırılır. Eğer "success" veya "rate" varsa, değerler azaltılır. Eğer "loss" veya "error" varsa, değerler artırılır.

```python
# Congestion anomaly with metric-specific effects
def inject_congestion_anomaly(values, metric_name, start_idx, duration_steps, severity):
    result = values.copy()
    end_idx = min(start_idx + duration_steps, len(result))
    
    # Different effects based on metric type
    if any(keyword in metric_name.lower() for keyword in ['latency', 'time', 'delay']):
        # Latency increases during congestion
        result[start_idx:end_idx] *= (1 + severity * 2.0)  # Can double or triple
    
    elif any(keyword in metric_name.lower() for keyword in ['success', 'rate', 'availability']):
        # Success rate decreases during congestion
        result[start_idx:end_idx] *= (1 - severity * 0.5)  # Can drop by 50%
    
    elif any(keyword in metric_name.lower() for keyword in ['throughput', 'bandwidth']):
        # Throughput decreases during congestion
        result[start_idx:end_idx] *= (1 - severity * 0.6)  # Significant drop
    
    elif any(keyword in metric_name.lower() for keyword in ['loss', 'error', 'drop']):
        # Packet loss increases during congestion
        result[start_idx:end_idx] *= (1 + severity * 5.0)  # Can increase 5x
    
    return result
```

### **Anomaly Propagation - Cascade Effects**

Gerçek network'lerde anomaliler izole kalmaz, dependency graph üzerinden yayılır. Eğer congestion downstream etkiler yaratır. Eğer bir critical service fail ederse, ona bağlı tüm servisler etkilenir. Propagation flag true ise, anomaly sadece epicenter metriği etkilemez, dependency graph üzerinden reachable tüm metrikleri de etkiler.

Propagation implementation graph traversal algoritması kullanır. Epicenter'dan başlayarak breadth-first search yapar, her reachable node'u bulur. Her hop'ta severity bir miktar azalır, yani epicenter'dan uzaklaştıkça etki zayıflar. Bu realistic çünkü gerçek dünyada da anomaly effects distance ile decay eder.

---

## ✅ **LAYER 6: VALIDASYON VE KALİTE GÜVENCESİ KATMANI**

Bu katman üretilen verinin tüm kalite kriterlerini karşılayıp karşılamadığını kontrol eder. Validation multi-dimensional'dır: istatistiksel, mantıksal, nedensel, temporal ve domain-specific testler içerir. Her test dimension'ı bir score üretir ve weighted combination ile overall quality score hesaplanır.

### **Statistical Validation - Dağılım Uygunluğu**

İstatistiksel validation, generated değerlerin intended distribution'a uyup uymadığını kontrol eder. İlk check, NaN ve Inf değerlerinin olmamasıdır. Eğer herhangi bir NaN veya Inf varsa, bu ciddi bir implementation bug'ı işaret eder.

İkinci check, empirical moment'ların theoretical moment'lara yakınlığıdır. Mean, variance, skewness ve kurtosis hesaplanır ve hedef değerlerle karşılaştırılır. Örneğin gamma distribution için skewness iki bölü square root of shape olmalıdır, empirical skewness bu formüle yakın olmalıdır.

```python
# Statistical validation implementation
def validate_distribution_fit(values, expected_distribution):
    scores = {}
    
    # Check for invalid values
    has_nan = np.isnan(values).any()
    has_inf = np.isinf(values).any()
    scores['validity'] = 1.0 if not (has_nan or has_inf) else 0.0
    
    # Moment matching
    empirical_mean = np.mean(values)
    empirical_std = np.std(values)
    expected_mean = expected_distribution.mean
    expected_std = expected_distribution.std
    
    mean_error = abs(empirical_mean - expected_mean) / expected_mean
    std_error = abs(empirical_std - expected_std) / expected_std
    
    scores['mean_match'] = max(0, 1 - mean_error)
    scores['std_match'] = max(0, 1 - std_error)
    
    # Kolmogorov-Smirnov test for distribution fit
    ks_statistic, ks_pvalue = stats.kstest(values, expected_distribution.cdf)
    scores['ks_test'] = 1.0 if ks_pvalue > 0.05 else ks_pvalue / 0.05
    
    # Overall statistical score
    overall = np.mean([scores['validity'], scores['mean_match'], 
                       scores['std_match'], scores['ks_test']])
    
    return overall, scores
```

Kolmogorov-Smirnov test kritik bir testtir. Bu test, empirical CDF ile theoretical CDF arasındaki maximum distance'ı ölçer. Eğer distance küçükse ve p-value yüksekse, distribution fit iyidir. P-value sıfır nokta sıfır beşten büyükse, yüzde doksan beş confidence ile distribution'ın doğru olduğunu söyleyebiliriz.

### **Logical Validation - Constraint Checking**

Mantıksal validation, domain-specific constraint'lerin korunduğunu kontrol eder. QoS boundaries birinci constraint'tir. Her metrik için minimum ve maksimum değerler tanımlanmışsa, tüm generated değerler bu boundaries içinde olmalıdır. Tek bir violation bile logical validation'ı fail eder.

```python
# Logical validation with QoS boundaries
def validate_logical_constraints(df, metric_configs):
    scores = {}
    
    for config in metric_configs:
        col_name = config.full_name
        violations = 0
        total_samples = len(df)
        
        if config.qos_min is not None:
            violations += (df[col_name] < config.qos_min).sum()
        
        if config.qos_max is not None:
            violations += (df[col_name] > config.qos_max).sum()
        
        # Score based on violation percentage
        violation_rate = violations / total_samples
        scores[col_name] = max(0, 1 - violation_rate * 10)  # Penalize heavily
    
    overall = np.mean(list(scores.values()))
    return overall, scores
```

Ordering constraint'ler başka bir logical check'tir. Örneğin p50 latency her zaman p95 latency'den küçük olmalıdır. Minimum throughput her zaman maximum throughput'tan küçük olmalıdır. Bu ordering relations violated ise, data internally inconsistent'tir.

### **Temporal Validation - Zaman Serisi Özellikleri**

Temporal validation, time series'in expected temporal properties'i gösterip göstermediğini kontrol eder. Autocorrelation structure ilk check'tir. Sağlıklı bir time series, pozitif autocorrelation gösterir: bugünkü değer dünkü değere benzer. Lag bir autocorrelation tipik olarak sıfır nokta altı ile sıfır nokta sekiz arasındadır.

```python
# Temporal validation with autocorrelation
def validate_temporal_properties(time_series):
    scores = {}
    
    # Autocorrelation at lag 1
    acf_lag1 = pd.Series(time_series).autocorr(lag=1)
    # Should be positive and significant
    scores['autocorr'] = 1.0 if 0.3 < acf_lag1 < 0.9 else max(0, acf_lag1)
    
    # Stationarity test (Augmented Dickey-Fuller)
    from statsmodels.tsa.stattools import adfuller
    adf_result = adfuller(time_series)
    adf_pvalue = adf_result[1]
    # p-value < 0.05 means stationary (good)
    scores['stationarity'] = 1.0 if adf_pvalue < 0.05 else 1 - adf_pvalue
    
    # Smoothness check: ratio of consecutive differences
    diffs = np.diff(time_series)
    smoothness = 1 - (np.std(diffs) / np.std(time_series))
    scores['smoothness'] = max(0, smoothness)
    
    overall = np.mean(list(scores.values()))
    return overall, scores
```

Seasonality detection başka bir temporal check'tir. Eğer seasonality enabled ise, generated time series'te periyodik pattern görülmelidir. FFT kullanarak dominant frequency'leri buluruz ve expected seasonality period'una karşılık geldiklerini doğrularız.

### **Overall Quality Score Calculation**

Final quality score, tüm dimension score'larının weighted average'ıdır. Weight'ler configuration'da tanımlanır ve sistemin hangi aspect'lere daha çok önem verdiğini gösterir. Tipik weight distribution: statistical yüzde yirmi beş, logical yüzde yirmi beş, causal yüzde yirmi, temporal yüzde on beş, domain yüzde on beş.

```python
# Overall quality score calculation
def calculate_overall_quality(validation_results, weights):
    overall_score = (
        validation_results['statistical'] * weights.statistical_weight +
        validation_results['logical'] * weights.logical_weight +
        validation_results['causal'] * weights.causal_weight +
        validation_results['temporal'] * weights.temporal_weight +
        validation_results['domain'] * weights.domain_weight
    )
    
    quality_grade = 'EXCELLENT' if overall_score > 0.95 else \
                    'GOOD' if overall_score > 0.85 else \
                    'ACCEPTABLE' if overall_score > 0.75 else \
                    'POOR'
    
    return overall_score, quality_grade
```

Eğer quality score threshold'un altında ise, sistem uyarı verir. Kullanıcı generation parameters'ı adjust edebilir ve yeniden üretim yapabilir. Bu iterative quality improvement süreci, yüksek kaliteli sentetik data garantiler.

---

## 🔄 **ÇALIŞMA AKIŞI (TEXT-BASED FLOW)**

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

## 🌐 **API ENDPOINTS**

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

## 🔧 **TEMEL SINIFLAR VE DATA YAPILARI**

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

## 📈 **ÖZELLEŞME VE GENİŞLETME NOKTALARI**

1. **Yeni Dağılım Ekleme**: `_generate_base_distribution()` metoduna yeni case
2. **Yeni Anomali Tipi**: `_apply_anomalies()` metoduna yeni elif bloğu
3. **Custom Korelasyon**: `_apply_correlations()` metodunda Gaussian Copula yerine başka yöntem
4. **Prosedür Simulasyonu**: Layer 4'e state machine ekleyerek
5. **Yeni Validasyon**: `calculate_validation_score()` fonksiyonuna yeni metrik

---