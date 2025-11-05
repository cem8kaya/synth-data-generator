/**
 * Generic Synthetic Data Generator - Frontend JavaScript
 * Multi-domain support with template system
 */

// State management
const state = {
    entities: [],
    metrics: [],
    correlations: [],
    anomalies: [],
    generatedData: null,
    currentTemplate: null
};

// Domain template descriptions
const domainDescriptions = {
    telecom: {
        name: 'Telecommunications',
        description: 'Network performance metrics, call data, latency, success rates',
        metrics: 'call_setup_rate, call_success_rate, latency, throughput',
        useCases: 'Network monitoring, Capacity planning, QoS analysis'
    },
    finance: {
        name: 'Financial Services',
        description: 'Trading systems, transaction data, order flow, market metrics',
        metrics: 'transaction_volume, execution_latency, success_rate, order_book_depth',
        useCases: 'Trading analytics, Risk management, Performance monitoring'
    },
    healthcare: {
        name: 'Healthcare',
        description: 'Patient data, bed occupancy, response times, equipment usage',
        metrics: 'patient_admissions, bed_occupancy_rate, response_time, equipment_utilization',
        useCases: 'Resource optimization, Patient flow analysis, Capacity planning'
    },
    manufacturing: {
        name: 'Manufacturing',
        description: 'Production metrics, quality data, machine utilization, cycle times',
        metrics: 'throughput, defect_rate, machine_utilization, cycle_time',
        useCases: 'Production optimization, Quality control, Predictive maintenance'
    },
    ecommerce: {
        name: 'E-commerce',
        description: 'Website traffic, conversion rates, cart data, revenue metrics',
        metrics: 'page_views, conversion_rate, cart_abandonment_rate, avg_order_value',
        useCases: 'Marketing analytics, Customer behavior, Revenue optimization'
    },
    iot: {
        name: 'IoT/Sensors',
        description: 'Sensor data, environmental metrics, network stats, device health',
        metrics: 'temperature, humidity, data_rate, battery_level',
        useCases: 'Smart cities, Environmental monitoring, Asset tracking'
    },
    custom: {
        name: 'Custom Domain',
        description: 'Build your own domain-specific configuration from scratch',
        metrics: 'Define your own metrics',
        useCases: 'Any custom use case'
    }
};

/**
 * Load domain template
 */
async function loadDomainTemplate() {
    const select = document.getElementById('domainTemplate');
    const domainType = select.value;
    
    if (!domainType) {
        showNotification('Please select a domain template', 'warning');
        return;
    }

    // Update domain type field
    document.getElementById('domainType').value = domainType;

    // Show template description
    if (domainDescriptions[domainType]) {
        const desc = domainDescriptions[domainType];
        document.getElementById('templateName').textContent = desc.name;
        document.getElementById('templateDesc').textContent = desc.description;
        document.getElementById('templateMetrics').textContent = desc.metrics;
        document.getElementById('templateUseCases').textContent = desc.useCases;
        document.getElementById('templateDescription').style.display = 'block';
    }

    if (domainType === 'custom') {
        showNotification('Custom domain selected. Please configure entities and metrics manually.', 'info');
        return;
    }

    // Load template from API
    try {
        const response = await fetch(`/api/template/${domainType}`);
        const data = await response.json();
        
        if (data.success) {
            applyTemplate(data.config);
            showNotification(`Template "${desc.name}" loaded successfully!`, 'success');
        } else {
            showNotification('Error loading template: ' + data.error, 'error');
        }
    } catch (error) {
        console.error('Error loading template:', error);
        showNotification('Failed to load template', 'error');
    }
}

/**
 * Apply template configuration to UI
 */
function applyTemplate(config) {
    // Clear existing configuration
    clearConfiguration();

    // Apply time window
    if (config.time_window) {
        document.getElementById('startDate').value = new Date(config.time_window.start_time).toISOString().slice(0, 16);
        document.getElementById('endDate').value = new Date(config.time_window.end_time).toISOString().slice(0, 16);
        document.getElementById('samplingInterval').value = config.time_window.granularity_minutes.toString();
    }

    // Apply entities
    if (config.entities) {
        config.entities.forEach(entity => {
            addEntity(entity);
        });
    }

    // Apply seasonality
    if (config.seasonality) {
        document.getElementById('enableSeasonality').checked = true;
    }

    // Apply ARIMA
    if (config.arima) {
        document.getElementById('enableArima').checked = true;
    }

    // Apply correlations
    if (config.correlations) {
        config.correlations.forEach(corr => {
            addCorrelation(corr);
        });
    }

    // Apply anomalies
    if (config.anomalies) {
        config.anomalies.forEach(anomaly => {
            addAnomaly(anomaly);
        });
    }

    // Update domain type
    document.getElementById('domainType').value = config.domain_type || 'custom';

    updateCounters();
}

/**
 * Show all available templates
 */
async function showAllTemplates() {
    try {
        const response = await fetch('/api/templates');
        const data = await response.json();
        
        if (data.success) {
            let html = '<div class="modal fade" id="templatesModal" tabindex="-1"><div class="modal-dialog modal-lg"><div class="modal-content">';
            html += '<div class="modal-header"><h5 class="modal-title">Available Domain Templates</h5><button type="button" class="btn-close" data-bs-dismiss="modal"></button></div>';
            html += '<div class="modal-body"><div class="row">';
            
            data.templates.forEach(template => {
                const desc = data.descriptions[template];
                if (desc) {
                    html += `
                        <div class="col-md-6 mb-3">
                            <div class="card">
                                <div class="card-body">
                                    <h6 class="card-title">${desc.name}</h6>
                                    <p class="card-text small">${desc.description}</p>
                                    <p class="small mb-1"><strong>Typical Metrics:</strong><br>${desc.typical_metrics.join(', ')}</p>
                                    <p class="small mb-2"><strong>Use Cases:</strong><br>${desc.use_cases.join(', ')}</p>
                                    <button class="btn btn-sm btn-primary" onclick="selectTemplateFromModal('${template}')">
                                        <i class="bi bi-check"></i> Select
                                    </button>
                                </div>
                            </div>
                        </div>
                    `;
                }
            });
            
            html += '</div></div></div></div></div>';
            
            // Remove existing modal if any
            const existingModal = document.getElementById('templatesModal');
            if (existingModal) existingModal.remove();
            
            // Add modal to body
            document.body.insertAdjacentHTML('beforeend', html);
            
            // Show modal
            const modal = new bootstrap.Modal(document.getElementById('templatesModal'));
            modal.show();
        }
    } catch (error) {
        console.error('Error fetching templates:', error);
        showNotification('Failed to fetch templates', 'error');
    }
}

/**
 * Select template from modal
 */
function selectTemplateFromModal(templateName) {
    document.getElementById('domainTemplate').value = templateName;
    bootstrap.Modal.getInstance(document.getElementById('templatesModal')).hide();
    loadDomainTemplate();
}

/**
 * Add entity
 */
function addEntity(entityData = null) {
    const template = document.getElementById('entityTemplate');
    const clone = template.content.cloneNode(true);
    
    if (entityData) {
        clone.querySelector('.entity-id').value = entityData.entity_id;
        clone.querySelector('.entity-type').value = entityData.entity_type;
        clone.querySelector('.entity-capacity').value = entityData.capacity || '';
        clone.querySelector('.entity-metadata').value = JSON.stringify(entityData.metadata || {});
        
        // Add metrics for this entity
        if (entityData.metrics) {
            entityData.metrics.forEach(metric => {
                addMetric({
                    ...metric,
                    entity_id: entityData.entity_id
                });
            });
        }
    }
    
    document.getElementById('entitiesList').appendChild(clone);
    state.entities.push({});
    updateCounters();
    updateMetricEntitySelectors();
}

/**
 * Remove entity
 */
function removeEntity(element) {
    element.remove();
    state.entities.pop();
    updateCounters();
    updateMetricEntitySelectors();
}

/**
 * Add metric
 */
function addMetric(metricData = null) {
    const template = document.getElementById('metricTemplate');
    const clone = template.content.cloneNode(true);
    
    // Populate entity selector
    const entitySelect = clone.querySelector('.metric-entity');
    document.querySelectorAll('.entity-id').forEach(input => {
        if (input.value) {
            const option = document.createElement('option');
            option.value = input.value;
            option.textContent = input.value;
            entitySelect.appendChild(option);
        }
    });
    
    if (metricData) {
        clone.querySelector('.metric-entity').value = metricData.entity_id || metricData.node_id || '';
        clone.querySelector('.metric-name').value = metricData.name;
        clone.querySelector('.metric-display').value = metricData.display_name || metricData.name;
        clone.querySelector('.metric-distribution').value = metricData.distribution.type;
        clone.querySelector('.metric-mean').value = metricData.distribution.mean;
        clone.querySelector('.metric-std').value = metricData.distribution.std || '';
        clone.querySelector('.metric-unit').value = metricData.unit || '';
        clone.querySelector('.metric-category').value = metricData.category || '';
    }
    
    document.getElementById('metricsList').appendChild(clone);
    state.metrics.push({});
    updateCounters();
}

/**
 * Remove metric
 */
function removeMetric(element) {
    element.remove();
    state.metrics.pop();
    updateCounters();
}

/**
 * Add correlation
 */
function addCorrelation(corrData = null) {
    const html = `
        <div class="correlation-item card mb-2 p-2">
            <div class="row g-2">
                <div class="col-md-4">
                    <select class="form-select form-select-sm corr-source">
                        <option value="">Source Metric</option>
                    </select>
                </div>
                <div class="col-md-4">
                    <select class="form-select form-select-sm corr-target">
                        <option value="">Target Metric</option>
                    </select>
                </div>
                <div class="col-md-3">
                    <input type="number" class="form-control form-control-sm corr-coefficient" 
                           placeholder="Coefficient (-1 to 1)" step="0.1" min="-1" max="1"
                           value="${corrData ? corrData.coefficient : ''}">
                </div>
                <div class="col-md-1">
                    <button class="btn btn-sm btn-danger" onclick="removeCorrelation(this.closest('.correlation-item'))">
                        <i class="bi bi-x"></i>
                    </button>
                </div>
            </div>
        </div>
    `;
    
    document.getElementById('correlationsList').insertAdjacentHTML('beforeend', html);
    
    // Update metric selectors
    updateAdvancedMetricSelectors();
    
    // Set values if provided
    if (corrData) {
        const items = document.querySelectorAll('.correlation-item');
        const lastItem = items[items.length - 1];
        lastItem.querySelector('.corr-source').value = corrData.source;
        lastItem.querySelector('.corr-target').value = corrData.target;
    }
}

/**
 * Remove correlation
 */
function removeCorrelation(element) {
    element.remove();
}

/**
 * Add anomaly
 */
function addAnomaly(anomalyData = null) {
    const html = `
        <div class="anomaly-item card mb-2 p-2">
            <div class="row g-2">
                <div class="col-md-2">
                    <input type="text" class="form-control form-control-sm anomaly-id" placeholder="Anomaly ID"
                           value="${anomalyData ? anomalyData.anomaly_id : ''}">
                </div>
                <div class="col-md-2">
                    <select class="form-select form-select-sm anomaly-type">
                        <option value="spike">Spike</option>
                        <option value="drop">Drop</option>
                        <option value="oscillation">Oscillation</option>
                        <option value="degradation">Degradation</option>
                        <option value="outage">Outage</option>
                        <option value="congestion">Congestion</option>
                        <option value="drift">Drift</option>
                    </select>
                </div>
                <div class="col-md-2">
                    <input type="datetime-local" class="form-control form-control-sm anomaly-start"
                           value="${anomalyData ? new Date(anomalyData.start_time).toISOString().slice(0, 16) : ''}">
                </div>
                <div class="col-md-2">
                    <input type="number" class="form-control form-control-sm anomaly-duration" 
                           placeholder="Duration (min)" value="${anomalyData ? anomalyData.duration_minutes : ''}">
                </div>
                <div class="col-md-2">
                    <input type="number" class="form-control form-control-sm anomaly-severity" 
                           placeholder="Severity (0-1)" step="0.1" min="0" max="1"
                           value="${anomalyData ? anomalyData.severity : ''}">
                </div>
                <div class="col-md-1">
                    <div class="form-check">
                        <input class="form-check-input anomaly-propagate" type="checkbox"
                               ${anomalyData && anomalyData.propagate ? 'checked' : ''}>
                        <label class="form-check-label small">Propagate</label>
                    </div>
                </div>
                <div class="col-md-1">
                    <button class="btn btn-sm btn-danger" onclick="removeAnomaly(this.closest('.anomaly-item'))">
                        <i class="bi bi-x"></i>
                    </button>
                </div>
            </div>
        </div>
    `;
    
    document.getElementById('anomaliesList').insertAdjacentHTML('beforeend', html);
    
    if (anomalyData) {
        const items = document.querySelectorAll('.anomaly-item');
        const lastItem = items[items.length - 1];
        lastItem.querySelector('.anomaly-type').value = anomalyData.anomaly_type;
    }
}

/**
 * Remove anomaly
 */
function removeAnomaly(element) {
    element.remove();
}

/**
 * Update counters
 */
function updateCounters() {
    const entityCount = document.querySelectorAll('.entity-item').length;
    const metricCount = document.querySelectorAll('.metric-item').length;
    
    document.getElementById('entityCounter').textContent = `${entityCount} entities`;
    document.getElementById('metricCounter').textContent = `${metricCount} metrics`;
}

/**
 * Update metric entity selectors
 */
function updateMetricEntitySelectors() {
    document.querySelectorAll('.metric-entity').forEach(select => {
        const currentValue = select.value;
        select.innerHTML = '<option value="">Select Entity</option>';
        
        document.querySelectorAll('.entity-id').forEach(input => {
            if (input.value) {
                const option = document.createElement('option');
                option.value = input.value;
                option.textContent = input.value;
                select.appendChild(option);
            }
        });
        
        select.value = currentValue;
    });
}

/**
 * Update advanced metric selectors (for correlations, anomalies)
 */
function updateAdvancedMetricSelectors() {
    const metrics = [];
    document.querySelectorAll('.metric-item').forEach(item => {
        const entityId = item.querySelector('.metric-entity').value;
        const metricName = item.querySelector('.metric-name').value;
        if (entityId && metricName) {
            metrics.push(`${entityId}_${metricName}`);
        }
    });
    
    // Update correlation selectors
    document.querySelectorAll('.corr-source, .corr-target').forEach(select => {
        const currentValue = select.value;
        select.innerHTML = '<option value="">Select Metric</option>';
        
        metrics.forEach(metric => {
            const option = document.createElement('option');
            option.value = metric;
            option.textContent = metric;
            select.appendChild(option);
        });
        
        select.value = currentValue;
    });
}

/**
 * Build configuration
 */
function buildConfig() {
    const config = {
        seed: parseInt(document.getElementById('randomSeed').value) || Math.floor(Math.random() * 1000000),
        domain_type: document.getElementById('domainType').value || 'custom',
        time_window: {
            start_time: document.getElementById('startDate').value,
            end_time: document.getElementById('endDate').value,
            granularity_minutes: parseInt(document.getElementById('samplingInterval').value)
        },
        enable_seasonality: document.getElementById('enableSeasonality').checked,
        enable_arima: document.getElementById('enableArima').checked,
        entities: [],
        correlations: [],
        anomalies: [],
        output: {
            output_dir: document.getElementById('outputDir').value || './output',
            format: document.getElementById('outputFormat').value,
            include_metadata: document.getElementById('includeMetadata').checked,
            compress: document.getElementById('compressOutput').checked
        }
    };
    
    // Collect entities and their metrics
    document.querySelectorAll('.entity-item').forEach(item => {
        const entity = {
            entity_id: item.querySelector('.entity-id').value,
            entity_type: item.querySelector('.entity-type').value,
            capacity: parseInt(item.querySelector('.entity-capacity').value) || null,
            metadata: {},
            metrics: []
        };
        
        try {
            const metadataStr = item.querySelector('.entity-metadata').value;
            if (metadataStr) {
                entity.metadata = JSON.parse(metadataStr);
            }
        } catch (e) {
            console.warn('Invalid metadata JSON:', e);
        }
        
        // Find metrics for this entity
        document.querySelectorAll('.metric-item').forEach(metricItem => {
            if (metricItem.querySelector('.metric-entity').value === entity.entity_id) {
                const metric = {
                    name: metricItem.querySelector('.metric-name').value,
                    display_name: metricItem.querySelector('.metric-display').value,
                    distribution: {
                        type: metricItem.querySelector('.metric-distribution').value,
                        mean: parseFloat(metricItem.querySelector('.metric-mean').value),
                        std: parseFloat(metricItem.querySelector('.metric-std').value) || null
                    },
                    unit: metricItem.querySelector('.metric-unit').value || '',
                    category: metricItem.querySelector('.metric-category').value || 'general'
                };
                entity.metrics.push(metric);
            }
        });
        
        config.entities.push(entity);
    });
    
    // Collect correlations
    document.querySelectorAll('.correlation-item').forEach(item => {
        config.correlations.push({
            source: item.querySelector('.corr-source').value,
            target: item.querySelector('.corr-target').value,
            coefficient: parseFloat(item.querySelector('.corr-coefficient').value)
        });
    });
    
    // Collect anomalies
    document.querySelectorAll('.anomaly-item').forEach(item => {
        config.anomalies.push({
            anomaly_id: item.querySelector('.anomaly-id').value,
            anomaly_type: item.querySelector('.anomaly-type').value,
            start_time: item.querySelector('.anomaly-start').value,
            duration_minutes: parseInt(item.querySelector('.anomaly-duration').value),
            severity: parseFloat(item.querySelector('.anomaly-severity').value),
            propagate: item.querySelector('.anomaly-propagate').checked,
            epicenter: '' // Will be set by backend from first metric
        });
    });
    
    return config;
}

/**
 * Validate configuration
 */
async function validateConfiguration() {
    const config = buildConfig();
    
    try {
        const response = await fetch('/api/validate', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(config)
        });
        
        const data = await response.json();
        
        if (data.valid) {
            showNotification('✓ Configuration is valid!', 'success');
            console.log('Validation summary:', data.summary);
            console.log('Estimates:', data.estimates);
        } else {
            showNotification('Configuration errors found', 'error');
            data.errors.forEach(err => showNotification(err, 'error'));
        }
        
        if (data.warnings && data.warnings.length > 0) {
            data.warnings.forEach(warn => showNotification(warn, 'warning'));
        }
    } catch (error) {
        console.error('Validation error:', error);
        showNotification('Failed to validate configuration', 'error');
    }
}

/**
 * Generate data
 */
async function generateData() {
    const config = buildConfig();
    
    // Show loading
    document.getElementById('loadingSpinner').style.display = 'block';
    document.getElementById('generateBtn').disabled = true;
    
    try {
        const response = await fetch('/api/generate', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(config)
        });
        
        const data = await response.json();
        
        if (data.success) {
            state.generatedData = data;
            showNotification('✓ Data generated successfully!', 'success');
            displayResults(data);
        } else {
            showNotification('Generation failed: ' + data.error, 'error');
        }
    } catch (error) {
        console.error('Generation error:', error);
        showNotification('Failed to generate data', 'error');
    } finally {
        document.getElementById('loadingSpinner').style.display = 'none';
        document.getElementById('generateBtn').disabled = false;
    }
}

/**
 * Display results
 */
function displayResults(data) {
    let html = '<div class="alert alert-success">';
    html += '<h6><i class="bi bi-check-circle"></i> Generation Complete</h6>';
    html += `<p><strong>Records:</strong> ${data.metadata.num_records}</p>`;
    html += `<p><strong>Entities:</strong> ${data.metadata.num_entities}</p>`;
    html += `<p><strong>Metrics:</strong> ${data.metadata.num_metrics}</p>`;
    html += `<p><strong>File:</strong> ${data.metadata.file_path}</p>`;
    html += `<p><strong>Size:</strong> ${data.metadata.file_size_mb.toFixed(2)} MB</p>`;
    html += `<a href="${data.download_url}" class="btn btn-primary btn-sm mt-2">`;
    html += '<i class="bi bi-download"></i> Download Data</a>';
    html += '</div>';
    
    document.getElementById('statusMessages').innerHTML = html;
}

/**
 * Clear configuration
 */
function clearConfiguration() {
    document.getElementById('entitiesList').innerHTML = '';
    document.getElementById('metricsList').innerHTML = '';
    document.getElementById('correlationsList').innerHTML = '';
    document.getElementById('anomaliesList').innerHTML = '';
    document.getElementById('templateDescription').style.display = 'none';
    
    state.entities = [];
    state.metrics = [];
    state.correlations = [];
    state.anomalies = [];
    
    updateCounters();
}

/**
 * Export configuration
 */
function exportConfiguration() {
    const config = buildConfig();
    const blob = new Blob([JSON.stringify(config, null, 2)], {type: 'application/json'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `config_${new Date().toISOString().slice(0, 10)}.json`;
    a.click();
}

/**
 * Import configuration
 */
function importConfiguration() {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.json';
    input.onchange = e => {
        const file = e.target.files[0];
        const reader = new FileReader();
        reader.onload = event => {
            try {
                const config = JSON.parse(event.target.result);
                applyTemplate(config);
                showNotification('Configuration imported successfully', 'success');
            } catch (error) {
                showNotification('Failed to parse configuration file', 'error');
            }
        };
        reader.readAsText(file);
    };
    input.click();
}

/**
 * Show notification
 */
function showNotification(message, type = 'info') {
    const colors = {
        success: 'alert-success',
        error: 'alert-danger',
        warning: 'alert-warning',
        info: 'alert-info'
    };
    
    const html = `
        <div class="alert ${colors[type]} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    document.getElementById('statusMessages').insertAdjacentHTML('beforeend', html);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        const alerts = document.querySelectorAll('.alert');
        if (alerts.length > 3) {
            alerts[0].remove();
        }
    }, 5000);
}