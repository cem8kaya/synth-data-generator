# Telecom Synthetic Data Generator - Proje Mimarisi

## 📐 Mimari Konsept

### Genel Bakış
Bu proje, `telecom_synthetic_generator_notebook.py` dosyasındaki monolitik Jupyter Notebook kodunu, Flask tabanlı modüler bir web uygulamasına dönüştürür.

### Tasarım Prensipleri

1. **Separation of Concerns**: Backend logic, API routes ve frontend ayrı modüllerde
2. **Modülerlik**: Her bileşen bağımsız ve test edilebilir
3. **RESTful API**: Stateless, JSON-based communication
4. **Progressive Enhancement**: Basit form'dan interaktif UI'a
5. **Responsive Design**: Bootstrap 5 ile mobil-uyumlu

## 🏗️ Katman Mimarisi

```
┌─────────────────────────────────────────┐
│         Frontend Layer (Browser)        │
│  ┌────────────┐  ┌──────────────────┐  │
│  │ HTML/CSS   │  │   JavaScript     │  │
│  │ Templates  │  │   (Chart.js)     │  │
│  └────────────┘  └──────────────────┘  │
└─────────────────────────────────────────┘
                    ↓ HTTP/AJAX
┌─────────────────────────────────────────┐
│         Application Layer (Flask)        │
│  ┌────────────┐  ┌──────────────────┐  │
│  │   Routes   │  │    API Routes    │  │
│  │  (Pages)   │  │     (JSON)       │  │
│  └────────────┘  └──────────────────┘  │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│        Business Logic Layer              │
│  ┌────────────────────────────────────┐ │
│  │    GeneratorOrchestrator           │ │
│  └────────────────────────────────────┘ │
│  ┌──────────┐  ┌──────────┐  ┌──────┐ │
│  │Distribu- │  │Temporal  │  │Anoma-│ │
│  │tions     │  │Features  │  │lies  │ │
│  └──────────┘  └──────────┘  └──────┘ │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│         Data Layer (Storage)             │
│  ┌──────────┐  ┌──────────┐  ┌───────┐ │
│  │   CSV    │  │ Parquet  │  │  JSON │ │
│  └──────────┘  └──────────┘  └───────┘ │
└─────────────────────────────────────────┘
```

## 📦 Modül Detayları

### 1. Generator Module (`generator/`)

#### `core.py` - Ana Orchestrator
- **GeneratorOrchestrator**: Tüm bileşenleri koordine eder
- **GeneratorConfig**: Tip-güvenli konfigürasyon modeli
- **MetricConfig**: Metrik tanımlamaları
- **İş Akışı**:
  1. Timestamp array oluşturma
  2. Her metrik için distribution generator oluşturma
  3. Base values generation
  4. Temporal patterns ekleme
  5. Anomali enjeksiyonu
  6. Validasyon
  7. DataFrame oluşturma

#### `distributions.py` - İstatistiksel Dağılımlar
- **DistributionGenerator**: Abstract base class
- **GammaGenerator**: Latency metrikleri için
- **LognormalGenerator**: Throughput metrikleri için
- **BetaGenerator**: Success rate metrikleri için
- **PoissonGenerator**: Count-based metrikler için
- **Context**: Dinamik parametre ayarlama

#### `temporal.py` - Zaman Serisi Özellikleri
- **SeasonalityGenerator**: Fourier series ile mevsimsellik
- **ARIMAGenerator**: ARIMA(p,d,q) pattern
- **ChangePointInjector**: Trend değişiklikleri
- **TimeWindowGenerator**: Timestamp generation utilities

#### `anomaly.py` - Anomali Modelleme
- **AnomalyInjector**: Ana anomali enjeksiyon sınıfı
- **AnomalyConfig**: Anomali konfigürasyonu
- **AnomalyType**: Enum (degradation, spike, outage, vb.)
- **Her anomali tipi için özel injection logic**

#### `validation.py` - Kalite Kontrolü
- **DataValidator**: Comprehensive validation
- **QualityAssessor**: Kalite skorlama
- **ValidationResult**: Sonuç container
- **Kontroller**: Missing values, infinite values, data ranges, temporal continuity

### 2. Routes Module (`routes/`)

#### `main.py` - Sayfa Routes
- `GET /`: Ana konfigürasyon sayfası
- `GET /results/<session_id>`: Sonuç görüntüleme
- `GET /about`: Dokümantasyon sayfası

#### `api.py` - API Endpoints
- `POST /api/generate`: Veri üretimi
- `GET /api/download/<session_id>/<format>`: Veri indirme
- `GET /api/visualize/<session_id>/<metric>`: Görselleştirme data
- `GET /api/presets`: Hazır konfigürasyonlar

### 3. Frontend (`static/`, `templates/`)

#### Templates (Jinja2)
- **base.html**: Ana şablon (navbar, footer, scripts)
- **index.html**: Konfigürasyon formu
- **results.html**: Sonuç görüntüleme
- **about.html**: Dokümantasyon

#### Static Assets
- **style.css**: Custom CSS (responsive, animations)
- **app.js**: Dynamic form manipulation, AJAX calls

## 🔄 Veri Akışı

### Generation Flow
```
1. User → Form Submission
   ↓
2. JavaScript → Build Config JSON
   ↓
3. POST /api/generate
   ↓
4. GeneratorOrchestrator.generate()
   ├─ Create distribution generators
   ├─ Generate base values
   ├─ Add seasonality
   ├─ Add ARIMA patterns
   ├─ Inject anomalies
   └─ Validate
   ↓
5. Save to files (CSV, Parquet, JSON)
   ↓
6. Return session_id + metadata
   ↓
7. Redirect to /results/<session_id>
   ↓
8. Display results + visualizations
```

### Visualization Flow
```
1. User selects metric
   ↓
2. GET /api/visualize/<session_id>/<metric>
   ↓
3. Read CSV file
   ↓
4. Calculate:
   ├─ Time series data
   ├─ Statistics (mean, std, min, max)
   └─ Histogram bins
   ↓
5. Return JSON
   ↓
6. JavaScript → Chart.js rendering
```

## 🎨 Frontend Teknolojileri

### Bootstrap 5
- Responsive grid system
- Form components
- Cards, badges, alerts
- Navbar, buttons

### Chart.js 4
- Line charts (time series)
- Bar charts (histogram)
- Responsive, interactive

### Axios
- Promise-based HTTP client
- Request/response interceptors
- Error handling

### Vanilla JavaScript
- Dynamic form generation
- Event handling
- Session storage caching

## 🔐 Güvenlik Konuları

### Input Validation
- Pydantic ile backend validation
- HTML5 form validation
- XSS protection (Flask auto-escaping)

### File Storage
- UUID-based session IDs
- Separate folders (uploads, outputs, temp)
- File size limits

### API Security
- CORS configuration
- Rate limiting (consideration)
- Input sanitization

## 📊 Performans Optimizasyonları

### Backend
- NumPy vectorization
- Efficient DataFrame operations
- Parquet format (compression)

### Frontend
- Session storage caching
- Lazy loading
- Chart data sampling for large datasets

### File Handling
- Streaming for large files
- Async generation (future enhancement)
- Cleanup old files (cron job consideration)

## 🧪 Test Stratejisi

### Unit Tests
- Distribution generators
- Anomaly injection
- Validation logic

### Integration Tests
- API endpoints
- End-to-end generation flow

### UI Tests
- Form validation
- Dynamic element creation

## 🚀 Deployment Considerations

### Production Setup
```python
# Use production config
app = create_app('production')

# Use production WSGI server
# gunicorn --workers 4 --bind 0.0.0.0:5000 app:app
```

### Environment Variables
```bash
SECRET_KEY=<random-secret-key>
FLASK_ENV=production
DATABASE_URL=<if-using-db>
```

### Monitoring
- Logging to files
- Error tracking (Sentry)
- Performance monitoring

## 📈 Gelecek Geliştirmeler

### Özellik İstekleri
1. User authentication
2. Dataset history
3. Comparison tool
4. More distribution types
5. Custom anomaly patterns
6. Real-time generation progress
7. Batch generation
8. API key management
9. Export to database
10. Advanced visualizations (Plotly)

### Teknik İyileştirmeler
1. Async task queue (Celery)
2. Database integration (PostgreSQL)
3. Docker containerization
4. CI/CD pipeline
5. API documentation (Swagger)
6. Unit test coverage
7. Performance profiling
8. Caching layer (Redis)

## 🔍 Notebook'tan Web UI'ya Dönüşüm Notları

### Korunan Özellikler
✅ Tüm distribution generators  
✅ Statistical validation  
✅ Temporal patterns (seasonality, ARIMA)  
✅ Anomaly injection  
✅ Quality assessment  
✅ Multiple output formats  

### Yeni Eklenen Özellikler
✨ Interactive web interface  
✨ Real-time visualizations  
✨ Preset configurations  
✨ Session management  
✨ Responsive design  
✨ API endpoints  

### Basitleştirilen Kısımlar
- Bayesian Network (gelecekte eklenebilir)
- Gaussian Copula (gelecekte eklenebilir)
- Procedure simulation (domain-specific, opsiyonel)

## 📚 Referanslar

- Flask Documentation: https://flask.palletsprojects.com/
- Bootstrap 5: https://getbootstrap.com/
- Chart.js: https://www.chartjs.org/
- NumPy: https://numpy.org/
- Pandas: https://pandas.pydata.org/
- SciPy: https://scipy.org/

---

**Not**: Bu mimari, mevcut fonksiyonaliteyi korurken, web-based kullanıma uygun hale getirilmiştir.
