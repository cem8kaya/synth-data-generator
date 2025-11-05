# Telecom Synthetic Data Generator - Web UI

Flask tabanlı, interaktif web arayüzü ile telekom sentetik veri üretim aracı.

## 🎯 Özellikler

- **İstatistiksel Dağılımlar**: Gamma, Lognormal, Beta, Poisson
- **Zaman Serisi Özellikleri**: Mevsimsellik ve ARIMA
- **Anomali Enjeksiyonu**: Degradation, Spike, Outage, Congestion, Oscillation
- **İnteraktif UI**: Bootstrap 5 tabanlı responsive tasarım
- **Görselleştirme**: Chart.js ile zaman serisi ve histogram grafikleri
- **Çoklu Format**: CSV, Parquet, JSON export
- **Kalite Kontrolü**: Kapsamlı validasyon ve istatistiksel kontroller

## 📋 Gereksinimler

- Python 3.8 veya üzeri
- pip package manager

## 🚀 Kurulum

### 1. Repository'yi klonlayın veya dosyaları indirin

```bash
cd telecom-web-generator
```

### 2. Virtual environment oluşturun (önerilen)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Bağımlılıkları yükleyin

```bash
pip install -r requirements.txt
```

## 🎮 Kullanım

### 1. Uygulamayı başlatın

```bash
python app.py
```

Uygulama `http://localhost:5000` adresinde çalışmaya başlayacaktır.

### 2. Web arayüzünü açın

Tarayıcınızda `http://localhost:5000` adresine gidin.

### 3. Veri üretin

1. **Zaman penceresi**: Başlangıç, bitiş zamanı ve granülarite ayarlayın
2. **Metrikler**: "Add Metric" ile metrik ekleyin, dağılım tipini ve parametrelerini belirleyin
3. **Temporal Features**: Mevsimsellik ve ARIMA özelliklerini aktifleştirin
4. **Anomaliler** (opsiyonel): "Add Anomaly" ile anomali ekleyin
5. **Generate**: "Generate Data" butonuna basın
6. **İndir**: Sonuç sayfasında CSV, Parquet veya JSON formatında indirin

### 4. Hızlı başlangıç presetleri

- **Simple**: 24 saatlik basit örnek (4 metrik)
- **Advanced**: 7 günlük gelişmiş örnek (anomalilerle)

## 📁 Proje Yapısı

```
telecom-web-generator/
├── app.py                          # Flask ana uygulama
├── config.py                       # Konfigürasyon
├── requirements.txt                # Python bağımlılıkları
│
├── generator/                      # Core generator modülü
│   ├── __init__.py
│   ├── core.py                    # Ana orchestrator
│   ├── distributions.py           # İstatistiksel dağılımlar
│   ├── temporal.py                # Zaman serisi logic
│   ├── anomaly.py                 # Anomali enjeksiyonu
│   └── validation.py              # Validasyon
│
├── routes/                         # Flask routes
│   ├── __init__.py
│   ├── main.py                    # Sayfa routes
│   └── api.py                     # API endpoints
│
├── static/                         # Frontend assets
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
│
└── templates/                      # Jinja2 templates
    ├── base.html
    ├── index.html
    ├── results.html
    └── about.html
```

## 🔌 API Endpoints

### POST `/api/generate`
Veri üretimi başlatır.

**Request body:**
```json
{
  "start_time": "2024-01-01T00:00:00",
  "end_time": "2024-01-02T00:00:00",
  "granularity_minutes": 5,
  "seed": 42,
  "metrics": [...],
  "enable_seasonality": true,
  "enable_arima": false,
  "anomalies": [...]
}
```

**Response:**
```json
{
  "success": true,
  "session_id": "uuid",
  "total_rows": 288,
  "statistics": {...},
  "quality": {...}
}
```

### GET `/api/download/<session_id>/<format>`
Üretilen veriyi indirir. Format: `csv`, `parquet`, `json`

### GET `/api/visualize/<session_id>/<metric_name>`
Belirli bir metrik için görselleştirme verisi döner.

### GET `/api/presets`
Hazır konfigürasyon presetlerini döner.

## 📊 Dağılım Tipleri

| Dağılım | Kullanım Alanı | Parametreler |
|---------|----------------|--------------|
| **Gamma** | Latency, delay metrikleri | mean, cv |
| **Lognormal** | Throughput, bandwidth | median, cv |
| **Beta** | Success rate (0-1) | mean, cv |
| **Poisson** | Count metrikleri | rate |

## ⚠️ Anomali Tipleri

- **Degradation**: Kademeli performans düşüşü
- **Spike**: Ani artış
- **Outage**: Kesinti
- **Congestion**: Network yoğunluğu
- **Oscillation**: Salınım

## 🔧 Konfigürasyon

`config.py` dosyasından ayarlanabilir:

- `OUTPUT_FOLDER`: Üretilen dosyaların saklanacağı klasör
- `MAX_CONTENT_LENGTH`: Maksimum dosya boyutu
- `DEFAULT_SEED`: Varsayılan random seed
- `ALLOWED_FORMATS`: İzin verilen export formatları

## 🐛 Hata Ayıklama

Loglar şu konumlarda saklanır:
- Console output
- `logs/app.log`
- `telecom_generator.log`

## 📝 Lisans

Bu proje Anthropic'in Claude AI yardımıyla geliştirilmiştir.

## 🤝 Katkıda Bulunma

1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit yapın (`git commit -m 'Add amazing feature'`)
4. Push edin (`git push origin feature/amazing-feature`)
5. Pull Request açın

## 📧 İletişim

Sorularınız için issue açabilirsiniz.

---

**Not**: Bu proje orijinal `telecom_synthetic_generator_notebook.py` dosyasının Flask web arayüzüne uyarlanmış halidir. Tüm core fonksiyonalite korunmuştur.
