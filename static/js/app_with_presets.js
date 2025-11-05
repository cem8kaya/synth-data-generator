/**
 * Generic Synthetic Data Generator - JavaScript with Quick Presets
 * Enhanced version with domain-specific quick preset examples
 */

// State
let selectedDomain = null;
let currentConfig = null;

// Domain Presets Definition
const domainPresets = {
    telecom: [
        {
            id: 'ims_volte',
            name: 'IMS & VoLTE Monitor',
            icon: 'telephone-fill',
            description: 'IMS core and VoLTE service quality metrics',
            duration: '24h',
            entities: [
                {
                    entity_id: 'IMS-CSCF-01',
                    entity_type: 'IMS_CSCF',
                    capacity: 50000,
                    metadata: { location: 'core-network', function: 'CSCF' },
                    metrics: [
                        { name: 'sip_register_rate', display_name: 'SIP Registration Rate', distribution: { type: 'poisson', mean: 250, std: 25 }, unit: 'reg/min', category: 'ims' },
                        { name: 'sip_register_success', display_name: 'SIP Registration Success Rate', distribution: { type: 'beta', mean: 99.7, std: 0.2 }, unit: '%', category: 'ims' },
                        { name: 'invite_setup_time', display_name: 'INVITE Setup Time', distribution: { type: 'gamma', mean: 180, std: 35 }, unit: 'ms', category: 'ims' },
                        { name: 'volte_call_setup_success', display_name: 'VoLTE Call Setup Success', distribution: { type: 'beta', mean: 99.5, std: 0.3 }, unit: '%', category: 'volte' },
                        { name: 'volte_mos_score', display_name: 'VoLTE MOS Score', distribution: { type: 'beta', mean: 4.2, std: 0.3, min_value: 3.5, max_value: 4.5 }, unit: 'MOS', category: 'volte' },
                        { name: 'call_drop_rate', display_name: 'Call Drop Rate', distribution: { type: 'beta', mean: 0.5, std: 0.15 }, unit: '%', category: 'volte' }
                    ]
                }
            ]
        },
        {
            id: '5g_core_amf',
            name: '5G Core - AMF',
            icon: 'reception-4',
            description: '5G Access and Mobility Management Function',
            duration: '24h',
            entities: [
                {
                    entity_id: '5GC-AMF-01',
                    entity_type: '5G_AMF',
                    capacity: 500000,
                    metadata: { network: '5G-SA', nf_type: 'AMF' },
                    metrics: [
                        { name: 'registration_requests', display_name: 'Registration Requests', distribution: { type: 'poisson', mean: 300, std: 30 }, unit: 'req/min', category: '5g_registration' },
                        { name: 'registration_success_rate', display_name: 'Registration Success Rate', distribution: { type: 'beta', mean: 99.8, std: 0.15 }, unit: '%', category: '5g_registration' },
                        { name: 'handover_success_rate', display_name: 'Handover Success Rate', distribution: { type: 'beta', mean: 99.6, std: 0.25 }, unit: '%', category: '5g_mobility' },
                        { name: 'n2_signaling_latency', display_name: 'N2 Signaling Latency', distribution: { type: 'gamma', mean: 25, std: 8 }, unit: 'ms', category: '5g_performance' },
                        { name: 'active_ue_count', display_name: 'Active UE Count', distribution: { type: 'normal', mean: 25000, std: 3000 }, unit: 'UEs', category: '5g_capacity' }
                    ]
                }
            ]
        },
        {
            id: '5g_core_smf',
            name: '5G Core - SMF',
            icon: 'hdd-network',
            description: '5G Session Management Function',
            duration: '24h',
            entities: [
                {
                    entity_id: '5GC-SMF-01',
                    entity_type: '5G_SMF',
                    capacity: 300000,
                    metadata: { network: '5G-SA', nf_type: 'SMF' },
                    metrics: [
                        { name: 'pdu_session_establishment_rate', display_name: 'PDU Session Establishment Rate', distribution: { type: 'poisson', mean: 200, std: 20 }, unit: 'sessions/min', category: '5g_session' },
                        { name: 'pdu_session_success_rate', display_name: 'PDU Session Success Rate', distribution: { type: 'beta', mean: 99.7, std: 0.2 }, unit: '%', category: '5g_session' },
                        { name: 'qos_flow_setup_success', display_name: 'QoS Flow Setup Success', distribution: { type: 'beta', mean: 99.8, std: 0.15 }, unit: '%', category: '5g_qos' },
                        { name: 'n4_session_latency', display_name: 'N4 Session Setup Latency', distribution: { type: 'gamma', mean: 30, std: 10 }, unit: 'ms', category: '5g_performance' },
                        { name: 'active_pdu_sessions', display_name: 'Active PDU Sessions', distribution: { type: 'normal', mean: 50000, std: 5000 }, unit: 'sessions', category: '5g_capacity' }
                    ]
                }
            ]
        },
        {
            id: '5g_core_upf',
            name: '5G Core - UPF',
            icon: 'diagram-3',
            description: '5G User Plane Function',
            duration: '24h',
            entities: [
                {
                    entity_id: '5GC-UPF-01',
                    entity_type: '5G_UPF',
                    capacity: 100000,
                    metadata: { network: '5G-SA', nf_type: 'UPF' },
                    metrics: [
                        { name: 'throughput_uplink', display_name: 'Uplink Throughput', distribution: { type: 'lognormal', mean: 2500, std: 400 }, unit: 'Mbps', category: '5g_throughput' },
                        { name: 'throughput_downlink', display_name: 'Downlink Throughput', distribution: { type: 'lognormal', mean: 5000, std: 800 }, unit: 'Mbps', category: '5g_throughput' },
                        { name: 'packet_loss_rate', display_name: 'Packet Loss Rate', distribution: { type: 'beta', mean: 0.3, std: 0.1 }, unit: '%', category: '5g_quality' },
                        { name: 'latency', display_name: 'User Plane Latency', distribution: { type: 'gamma', mean: 15, std: 5 }, unit: 'ms', category: '5g_performance' },
                        { name: 'cpu_utilization', display_name: 'CPU Utilization', distribution: { type: 'beta', mean: 65, std: 10 }, unit: '%', category: '5g_resources' },
                        { name: 'active_bearers', display_name: 'Active Bearers', distribution: { type: 'normal', mean: 80000, std: 8000 }, unit: 'bearers', category: '5g_capacity' }
                    ]
                }
            ]
        },
        {
            id: '5g_core_nssf',
            name: '5G Core - NSSF',
            icon: 'layers',
            description: '5G Network Slice Selection Function',
            duration: '24h',
            entities: [
                {
                    entity_id: '5GC-NSSF-01',
                    entity_type: '5G_NSSF',
                    capacity: 100000,
                    metadata: { network: '5G-SA', nf_type: 'NSSF' },
                    metrics: [
                        { name: 'slice_selection_rate', display_name: 'Slice Selection Rate', distribution: { type: 'poisson', mean: 150, std: 15 }, unit: 'req/min', category: '5g_slicing' },
                        { name: 'slice_selection_success', display_name: 'Slice Selection Success Rate', distribution: { type: 'beta', mean: 99.9, std: 0.1 }, unit: '%', category: '5g_slicing' },
                        { name: 'slice_response_time', display_name: 'Slice Selection Response Time', distribution: { type: 'gamma', mean: 20, std: 5 }, unit: 'ms', category: '5g_performance' }
                    ]
                }
            ]
        },
        {
            id: 'telco_cloud',
            name: 'Telco Cloud Infrastructure',
            icon: 'cloud-fill',
            description: 'Cloud infrastructure metrics for NFV/VNF',
            duration: '24h',
            entities: [
                {
                    entity_id: 'TELCO-CLOUD-01',
                    entity_type: 'TelcoCloud',
                    capacity: 10000,
                    metadata: { deployment: 'openstack', type: 'nfvi' },
                    metrics: [
                        { name: 'vnf_deployment_success', display_name: 'VNF Deployment Success Rate', distribution: { type: 'beta', mean: 98.5, std: 0.8 }, unit: '%', category: 'cloud_orchestration' },
                        { name: 'vnf_scaling_time', display_name: 'VNF Auto-Scaling Time', distribution: { type: 'gamma', mean: 120, std: 30 }, unit: 'seconds', category: 'cloud_orchestration' },
                        { name: 'vm_cpu_utilization', display_name: 'VM CPU Utilization', distribution: { type: 'beta', mean: 60, std: 12 }, unit: '%', category: 'cloud_resources' },
                        { name: 'vm_memory_utilization', display_name: 'VM Memory Utilization', distribution: { type: 'beta', mean: 70, std: 10 }, unit: '%', category: 'cloud_resources' },
                        { name: 'storage_iops', display_name: 'Storage IOPS', distribution: { type: 'lognormal', mean: 15000, std: 2500 }, unit: 'IOPS', category: 'cloud_storage' },
                        { name: 'network_bandwidth', display_name: 'Network Bandwidth Usage', distribution: { type: 'lognormal', mean: 3500, std: 600 }, unit: 'Mbps', category: 'cloud_network' }
                    ]
                }
            ]
        },
        {
            id: 'voip_service',
            name: 'VoIP Service Monitor',
            icon: 'telephone',
            description: 'Monitor VoIP call quality and success rates',
            duration: '24h',
            entities: [
                {
                    entity_id: 'VOIP-SERVER-01',
                    entity_type: 'VoIPServer',
                    capacity: 10000,
                    metadata: { location: 'datacenter-1' },
                    metrics: [
                        { name: 'call_setup_rate', display_name: 'Call Setup Rate', distribution: { type: 'poisson', mean: 120, std: 15 }, unit: 'calls/min', category: 'performance' },
                        { name: 'call_success_rate', display_name: 'Call Success Rate', distribution: { type: 'beta', mean: 99.5, std: 0.3 }, unit: '%', category: 'quality' },
                        { name: 'jitter', display_name: 'Jitter', distribution: { type: 'gamma', mean: 15, std: 5 }, unit: 'ms', category: 'quality' },
                        { name: 'packet_loss', display_name: 'Packet Loss', distribution: { type: 'beta', mean: 0.8, std: 0.3 }, unit: '%', category: 'quality' }
                    ]
                }
            ]
        },
        {
            id: 'network_latency',
            name: 'Network Performance',
            icon: 'speedometer2',
            description: 'Track network latency and throughput',
            duration: '12h',
            entities: [
                {
                    entity_id: 'ROUTER-CORE-01',
                    entity_type: 'CoreRouter',
                    capacity: 100000,
                    metadata: { tier: 'core' },
                    metrics: [
                        { name: 'latency', display_name: 'Network Latency', distribution: { type: 'gamma', mean: 45, std: 12 }, unit: 'ms', category: 'performance' },
                        { name: 'throughput', display_name: 'Throughput', distribution: { type: 'lognormal', mean: 850, std: 150 }, unit: 'Mbps', category: 'bandwidth' },
                        { name: 'packet_loss', display_name: 'Packet Loss', distribution: { type: 'beta', mean: 0.5, std: 0.2 }, unit: '%', category: 'quality' }
                    ]
                }
            ]
        }
    ],
    finance: [
        {
            id: 'trading_system',
            name: 'High-Frequency Trading',
            icon: 'graph-up-arrow',
            description: 'Trading system performance metrics',
            duration: '24h',
            entities: [
                {
                    entity_id: 'TRADING-SYS-01',
                    entity_type: 'TradingEngine',
                    capacity: 100000,
                    metadata: { exchange: 'NYSE' },
                    metrics: [
                        { name: 'order_rate', display_name: 'Order Rate', distribution: { type: 'poisson', mean: 500, std: 50 }, unit: 'orders/sec', category: 'volume' },
                        { name: 'execution_latency', display_name: 'Execution Latency', distribution: { type: 'gamma', mean: 8, std: 2 }, unit: 'ms', category: 'performance' },
                        { name: 'fill_rate', display_name: 'Fill Rate', distribution: { type: 'beta', mean: 98.5, std: 0.8 }, unit: '%', category: 'quality' }
                    ]
                }
            ]
        },
        {
            id: 'payment_gateway',
            name: 'Payment Gateway Monitor',
            icon: 'credit-card',
            description: 'Transaction processing and success rates',
            duration: '24h',
            entities: [
                {
                    entity_id: 'PAYMENT-GW-01',
                    entity_type: 'PaymentGateway',
                    capacity: 50000,
                    metadata: { provider: 'stripe' },
                    metrics: [
                        { name: 'transaction_volume', display_name: 'Transaction Volume', distribution: { type: 'lognormal', mean: 1000, std: 200 }, unit: 'transactions/min', category: 'volume' },
                        { name: 'success_rate', display_name: 'Success Rate', distribution: { type: 'beta', mean: 99.2, std: 0.5 }, unit: '%', category: 'quality' },
                        { name: 'processing_time', display_name: 'Processing Time', distribution: { type: 'gamma', mean: 250, std: 50 }, unit: 'ms', category: 'performance' }
                    ]
                }
            ]
        },
        {
            id: 'fraud_detection',
            name: 'Fraud Detection System',
            icon: 'shield-check',
            description: 'Monitor fraud detection metrics',
            duration: '24h',
            entities: [
                {
                    entity_id: 'FRAUD-DETECTOR-01',
                    entity_type: 'FraudDetection',
                    capacity: 20000,
                    metadata: { model: 'ml-v2' },
                    metrics: [
                        { name: 'scan_rate', display_name: 'Transaction Scan Rate', distribution: { type: 'poisson', mean: 300, std: 30 }, unit: 'scans/min', category: 'throughput' },
                        { name: 'detection_rate', display_name: 'Fraud Detection Rate', distribution: { type: 'beta', mean: 2.5, std: 0.5 }, unit: '%', category: 'detection' },
                        { name: 'false_positive_rate', display_name: 'False Positive Rate', distribution: { type: 'beta', mean: 1.2, std: 0.3 }, unit: '%', category: 'accuracy' }
                    ]
                }
            ]
        }
    ],
    healthcare: [
        {
            id: 'er_monitoring',
            name: 'Emergency Room Monitor',
            icon: 'hospital',
            description: 'ER patient flow and wait times',
            duration: '24h',
            entities: [
                {
                    entity_id: 'ER-UNIT-01',
                    entity_type: 'EmergencyRoom',
                    capacity: 50,
                    metadata: { hospital: 'General Hospital' },
                    metrics: [
                        { name: 'patient_arrivals', display_name: 'Patient Arrivals', distribution: { type: 'poisson', mean: 8, std: 2 }, unit: 'patients/hour', category: 'admissions' },
                        { name: 'wait_time', display_name: 'Wait Time', distribution: { type: 'gamma', mean: 45, std: 15 }, unit: 'minutes', category: 'service' },
                        { name: 'bed_occupancy', display_name: 'Bed Occupancy', distribution: { type: 'beta', mean: 85, std: 8 }, unit: '%', category: 'capacity' }
                    ]
                }
            ]
        },
        {
            id: 'icu_operations',
            name: 'ICU Operations',
            icon: 'heart-pulse',
            description: 'Intensive care unit metrics',
            duration: '7days',
            entities: [
                {
                    entity_id: 'ICU-WARD-01',
                    entity_type: 'ICU',
                    capacity: 20,
                    metadata: { ward: 'ICU-A' },
                    metrics: [
                        { name: 'admissions', display_name: 'ICU Admissions', distribution: { type: 'poisson', mean: 3, std: 1 }, unit: 'patients/day', category: 'admissions' },
                        { name: 'ventilator_usage', display_name: 'Ventilator Usage', distribution: { type: 'beta', mean: 65, std: 12 }, unit: '%', category: 'equipment' },
                        { name: 'nurse_patient_ratio', display_name: 'Nurse-Patient Ratio', distribution: { type: 'normal', mean: 0.5, std: 0.1 }, unit: 'ratio', category: 'staffing' }
                    ]
                }
            ]
        }
    ],
    manufacturing: [
        {
            id: 'assembly_line',
            name: 'Assembly Line Monitor',
            icon: 'gear',
            description: 'Production line performance tracking',
            duration: '24h',
            entities: [
                {
                    entity_id: 'PROD-LINE-01',
                    entity_type: 'AssemblyLine',
                    capacity: 1000,
                    metadata: { factory: 'Plant-A' },
                    metrics: [
                        { name: 'throughput', display_name: 'Production Throughput', distribution: { type: 'normal', mean: 100, std: 10 }, unit: 'units/hour', category: 'production' },
                        { name: 'defect_rate', display_name: 'Defect Rate', distribution: { type: 'beta', mean: 2.5, std: 0.5 }, unit: '%', category: 'quality' },
                        { name: 'cycle_time', display_name: 'Cycle Time', distribution: { type: 'gamma', mean: 45, std: 8 }, unit: 'seconds', category: 'efficiency' }
                    ]
                }
            ]
        },
        {
            id: 'quality_control',
            name: 'Quality Control System',
            icon: 'clipboard-check',
            description: 'Product quality inspection metrics',
            duration: '24h',
            entities: [
                {
                    entity_id: 'QC-STATION-01',
                    entity_type: 'QualityControl',
                    capacity: 500,
                    metadata: { inspection: 'automated' },
                    metrics: [
                        { name: 'inspection_rate', display_name: 'Inspection Rate', distribution: { type: 'poisson', mean: 80, std: 10 }, unit: 'items/hour', category: 'throughput' },
                        { name: 'pass_rate', display_name: 'Pass Rate', distribution: { type: 'beta', mean: 96.5, std: 1.2 }, unit: '%', category: 'quality' },
                        { name: 'inspection_time', display_name: 'Inspection Time', distribution: { type: 'gamma', mean: 30, std: 5 }, unit: 'seconds', category: 'efficiency' }
                    ]
                }
            ]
        }
    ],
    ecommerce: [
        {
            id: 'web_analytics',
            name: 'Web Traffic Analytics',
            icon: 'cart',
            description: 'Website traffic and conversion tracking',
            duration: '24h',
            entities: [
                {
                    entity_id: 'WEBSTORE-01',
                    entity_type: 'Ecommerce',
                    capacity: 100000,
                    metadata: { platform: 'shopify' },
                    metrics: [
                        { name: 'page_views', display_name: 'Page Views', distribution: { type: 'poisson', mean: 500, std: 50 }, unit: 'views/min', category: 'traffic' },
                        { name: 'conversion_rate', display_name: 'Conversion Rate', distribution: { type: 'beta', mean: 3.8, std: 0.8 }, unit: '%', category: 'conversions' },
                        { name: 'cart_abandonment', display_name: 'Cart Abandonment', distribution: { type: 'beta', mean: 68, std: 5 }, unit: '%', category: 'behavior' }
                    ]
                }
            ]
        },
        {
            id: 'checkout_performance',
            name: 'Checkout System',
            icon: 'credit-card-2-front',
            description: 'Checkout flow and payment processing',
            duration: '24h',
            entities: [
                {
                    entity_id: 'CHECKOUT-01',
                    entity_type: 'CheckoutSystem',
                    capacity: 50000,
                    metadata: { version: 'v3.2' },
                    metrics: [
                        { name: 'checkout_rate', display_name: 'Checkout Attempts', distribution: { type: 'poisson', mean: 80, std: 12 }, unit: 'checkouts/min', category: 'transactions' },
                        { name: 'payment_success', display_name: 'Payment Success Rate', distribution: { type: 'beta', mean: 97.5, std: 1.0 }, unit: '%', category: 'payments' },
                        { name: 'avg_order_value', display_name: 'Avg Order Value', distribution: { type: 'lognormal', mean: 85, std: 30 }, unit: 'USD', category: 'revenue' }
                    ]
                }
            ]
        }
    ],
    iot: [
        {
            id: 'smart_city',
            name: 'Smart City Sensors',
            icon: 'thermometer',
            description: 'Environmental monitoring sensors',
            duration: '7days',
            entities: [
                {
                    entity_id: 'SENSOR-CLUSTER-01',
                    entity_type: 'SensorArray',
                    capacity: 1000,
                    metadata: { deployment: 'downtown' },
                    metrics: [
                        { name: 'temperature', display_name: 'Temperature', distribution: { type: 'normal', mean: 22, std: 5 }, unit: '°C', category: 'environmental' },
                        { name: 'humidity', display_name: 'Humidity', distribution: { type: 'beta', mean: 65, std: 10 }, unit: '%', category: 'environmental' },
                        { name: 'air_quality', display_name: 'Air Quality Index', distribution: { type: 'gamma', mean: 45, std: 15 }, unit: 'AQI', category: 'environmental' }
                    ]
                }
            ]
        },
        {
            id: 'industrial_iot',
            name: 'Industrial IoT Monitor',
            icon: 'cpu',
            description: 'Machine health and performance tracking',
            duration: '24h',
            entities: [
                {
                    entity_id: 'MACHINE-01',
                    entity_type: 'IndustrialMachine',
                    capacity: 100,
                    metadata: { type: 'press' },
                    metrics: [
                        { name: 'vibration', display_name: 'Vibration Level', distribution: { type: 'gamma', mean: 12, std: 3 }, unit: 'mm/s', category: 'health' },
                        { name: 'temperature', display_name: 'Operating Temperature', distribution: { type: 'normal', mean: 75, std: 8 }, unit: '°C', category: 'health' },
                        { name: 'power_consumption', display_name: 'Power Consumption', distribution: { type: 'normal', mean: 45, std: 5 }, unit: 'kW', category: 'efficiency' }
                    ]
                }
            ]
        }
    ]
};

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    const now = new Date();
    const tomorrow = new Date(now.getTime() + 24 * 60 * 60 * 1000);

    document.getElementById('startDate').value = now.toISOString().slice(0, 16);
    document.getElementById('endDate').value = tomorrow.toISOString().slice(0, 16);

    updateDuration();
    updateStatistics();

    document.getElementById('startDate').addEventListener('change', function() {
        updateDuration();
        updateStatistics();
    });

    document.getElementById('endDate').addEventListener('change', function() {
        updateDuration();
        updateStatistics();
    });

    document.getElementById('granularity').addEventListener('change', function() {
        updateStatistics();
    });
});

// Domain Selection
function selectDomain(domain) {
    selectedDomain = domain;
    
    // Update UI
    document.querySelectorAll('.domain-card').forEach(card => {
        card.classList.remove('selected');
    });
    document.getElementById('domain-' + domain).classList.add('selected');
    
    // Show info
    const info = {
        telecom: { title: 'Telecommunications', desc: 'Network performance metrics, call data, latency' },
        finance: { title: 'Financial Services', desc: 'Trading systems, transactions, market metrics' },
        healthcare: { title: 'Healthcare', desc: 'Patient data, bed occupancy, operations' },
        manufacturing: { title: 'Manufacturing', desc: 'Production metrics, quality data, cycle times' },
        ecommerce: { title: 'E-commerce', desc: 'Web traffic, conversions, revenue metrics' },
        iot: { title: 'IoT/Sensors', desc: 'Sensor data, environmental metrics' },
        custom: { title: 'Custom', desc: 'Build your own domain-specific configuration' }
    };
    
    document.getElementById('templateTitle').textContent = info[domain].title;
    document.getElementById('templateDesc').textContent = info[domain].desc;
    document.getElementById('templateInfo').style.display = 'block';
    
    // Show presets for this domain
    showPresets(domain);
}

// Show Presets
function showPresets(domain) {
    const presetsSection = document.getElementById('presetsSection');
    const presetsList = document.getElementById('presetsList');
    
    if (domain === 'custom' || !domainPresets[domain]) {
        presetsSection.style.display = 'none';
        return;
    }
    
    const presets = domainPresets[domain];
    let html = '';
    
    presets.forEach(preset => {
        html += `
            <div class="col-md-4">
                <div class="preset-card glass-card p-3" onclick="loadPreset('${domain}', '${preset.id}')">
                    <div class="d-flex align-items-center mb-2">
                        <i class="bi bi-${preset.icon} icon-lg text-primary me-2"></i>
                        <h6 class="mb-0">${preset.name}</h6>
                    </div>
                    <p class="small text-muted mb-2">${preset.description}</p>
                    <div class="d-flex justify-content-between align-items-center">
                        <span class="badge bg-info">${preset.duration}</span>
                        <span class="badge bg-secondary">${preset.entities.length} entities</span>
                        <span class="badge bg-success">${preset.entities.reduce((sum, e) => sum + e.metrics.length, 0)} metrics</span>
                    </div>
                </div>
            </div>
        `;
    });
    
    presetsList.innerHTML = html;
    presetsSection.style.display = 'block';
}

// Load Preset
function loadPreset(domain, presetId) {
    const preset = domainPresets[domain].find(p => p.id === presetId);
    
    if (!preset) {
        showNotification('Preset not found', 'danger');
        return;
    }
    
    clearAll();
    
    // Set duration based on preset
    const now = new Date();
    let endDate;
    
    if (preset.duration === '12h') {
        endDate = new Date(now.getTime() + 12 * 60 * 60 * 1000);
    } else if (preset.duration === '7days') {
        endDate = new Date(now.getTime() + 7 * 24 * 60 * 60 * 1000);
    } else {
        endDate = new Date(now.getTime() + 24 * 60 * 60 * 1000);
    }
    
    document.getElementById('endDate').value = endDate.toISOString().slice(0, 16);
    updateDuration();
    
    // Load entities and metrics
    preset.entities.forEach(entity => {
        addEntity(entity);
    });
    
    // Enable seasonality for most presets
    document.getElementById('enableSeasonality').checked = true;
    
    showNotification(`✓ Preset "${preset.name}" loaded successfully!`, 'success');
    updateCounts();
}

// Load Full Template (from API)
async function loadSelectedTemplate() {
    if (!selectedDomain) {
        showNotification('Please select a domain first', 'warning');
        return;
    }

    if (selectedDomain === 'custom') {
        showNotification('Custom domain selected. Please configure manually or use a quick preset.', 'info');
        return;
    }

    showLoading(true);

    try {
        const response = await fetch(`/api/template/${selectedDomain}`);
        const data = await response.json();
        
        if (data.success) {
            applyTemplate(data.config);
            showNotification('Full template loaded successfully!', 'success');
        } else {
            showNotification('Error: ' + data.error, 'danger');
        }
    } catch (error) {
        console.error('Error:', error);
        showNotification('Failed to load template', 'danger');
    } finally {
        showLoading(false);
    }
}

// Apply Template
function applyTemplate(config) {
    clearAll();
    
    if (config.entities) {
        config.entities.forEach(entity => {
            addEntity(entity);
        });
    }

    if (config.seasonality) {
        document.getElementById('enableSeasonality').checked = true;
    }

    if (config.arima) {
        document.getElementById('enableArima').checked = true;
    }

    updateCounts();
}

// Add Entity
function addEntity(data = null) {
    const template = document.getElementById('entityTemplate');
    const clone = template.content.cloneNode(true);

    if (data) {
        clone.querySelector('.entity-id').value = data.entity_id;
        clone.querySelector('.entity-type').value = data.entity_type;
        clone.querySelector('.entity-capacity').value = data.capacity || '';
        clone.querySelector('.entity-metadata').value = JSON.stringify(data.metadata || {});
    }

    // Append entity to DOM first so metrics can find it
    document.getElementById('entitiesList').appendChild(clone);
    updateCounts();
    updateMetricSelectors();

    // Add metrics after entity is in the DOM
    if (data && data.metrics) {
        data.metrics.forEach(metric => {
            addMetric({ ...metric, entity_id: data.entity_id });
        });
    }
}

// Remove Entity
function removeEntity(btn) {
    btn.closest('.entity-item').remove();
    updateCounts();
    updateMetricSelectors();
}

// Add Metric
function addMetric(data = null) {
    const template = document.getElementById('metricTemplate');
    const clone = template.content.cloneNode(true);

    // Populate entity selector
    const select = clone.querySelector('.metric-entity');
    const entityIds = [];
    document.querySelectorAll('.entity-id').forEach(input => {
        if (input.value) {
            const option = document.createElement('option');
            option.value = input.value;
            option.textContent = input.value;
            select.appendChild(option);
            entityIds.push(input.value);
        }
    });

    if (data) {
        clone.querySelector('.metric-entity').value = data.entity_id || '';
        clone.querySelector('.metric-name').value = data.name;
        clone.querySelector('.metric-display').value = data.display_name || data.name;
        clone.querySelector('.metric-distribution').value = data.distribution.type;
        clone.querySelector('.metric-mean').value = data.distribution.mean;
        clone.querySelector('.metric-std').value = data.distribution.std || '';
        clone.querySelector('.metric-unit').value = data.unit || '';
        clone.querySelector('.metric-category').value = data.category || '';
    } else if (entityIds.length === 1) {
        // Auto-select the first entity if there's only one
        select.value = entityIds[0];
    }

    document.getElementById('metricsList').appendChild(clone);
    updateCounts();
}

// Remove Metric
function removeMetric(btn) {
    btn.closest('.metric-item').remove();
    updateCounts();
}

// Update Counts
function updateCounts() {
    const entityCount = document.querySelectorAll('.entity-item').length;
    const metricCount = document.querySelectorAll('.metric-item').length;

    const entityBadge = document.getElementById('entityCount');
    const metricBadge = document.getElementById('metricCount');

    // Add animation when count changes
    entityBadge.classList.add('count-up');
    metricBadge.classList.add('count-up');

    entityBadge.textContent = entityCount;
    metricBadge.textContent = metricCount;

    setTimeout(() => {
        entityBadge.classList.remove('count-up');
        metricBadge.classList.remove('count-up');
    }, 300);

    // Update statistics dashboard
    updateStatistics();
}

// Update Statistics Dashboard
function updateStatistics() {
    const entityCount = document.querySelectorAll('.entity-item').length;
    const metricCount = document.querySelectorAll('.metric-item').length;

    // Show/hide stats section
    const statsSection = document.getElementById('configStats');
    if (entityCount > 0 || metricCount > 0) {
        statsSection.style.display = 'flex';
    } else {
        statsSection.style.display = 'none';
        return;
    }

    // Update entity count
    document.getElementById('statEntities').textContent = entityCount;

    // Update metric count
    document.getElementById('statMetrics').textContent = metricCount;

    // Calculate duration
    const startDate = new Date(document.getElementById('startDate').value);
    const endDate = new Date(document.getElementById('endDate').value);
    const diff = endDate - startDate;
    const hours = Math.floor(diff / (1000 * 60 * 60));
    const days = Math.floor(hours / 24);

    let durationText = '';
    if (days > 0) {
        durationText = `${days}d ${hours % 24}h`;
    } else {
        durationText = `${hours}h`;
    }
    document.getElementById('statDuration').textContent = durationText;

    // Estimate data points
    const granularity = parseInt(document.getElementById('granularity').value);
    const totalMinutes = diff / (1000 * 60);
    const dataPoints = Math.floor(totalMinutes / granularity) * metricCount;

    if (dataPoints > 1000000) {
        document.getElementById('statPoints').textContent = (dataPoints / 1000000).toFixed(1) + 'M';
    } else if (dataPoints > 1000) {
        document.getElementById('statPoints').textContent = (dataPoints / 1000).toFixed(1) + 'K';
    } else {
        document.getElementById('statPoints').textContent = dataPoints.toLocaleString();
    }
}

// Update Metric Selectors
function updateMetricSelectors() {
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

// Build Config
function buildConfig() {
    const config = {
        seed: parseInt(document.getElementById('seed').value) || Math.floor(Math.random() * 1000000),
        domain_type: selectedDomain || 'custom',
        time_window: {
            start_time: document.getElementById('startDate').value,
            end_time: document.getElementById('endDate').value,
            granularity_minutes: parseInt(document.getElementById('granularity').value)
        },
        enable_seasonality: document.getElementById('enableSeasonality').checked,
        enable_arima: document.getElementById('enableArima').checked,
        entities: [],
        output: {
            format: document.getElementById('outputFormat').value,
            include_metadata: true
        }
    };

    // Collect entities
    document.querySelectorAll('.entity-item').forEach(item => {
        const entity = {
            entity_id: item.querySelector('.entity-id').value,
            entity_type: item.querySelector('.entity-type').value,
            capacity: parseInt(item.querySelector('.entity-capacity').value) || null,
            metadata: {},
            metrics: []
        };

        try {
            const meta = item.querySelector('.entity-metadata').value;
            if (meta) entity.metadata = JSON.parse(meta);
        } catch (e) {}

        // Find metrics for this entity
        document.querySelectorAll('.metric-item').forEach(metricItem => {
            if (metricItem.querySelector('.metric-entity').value === entity.entity_id) {
                entity.metrics.push({
                    name: metricItem.querySelector('.metric-name').value,
                    display_name: metricItem.querySelector('.metric-display').value,
                    distribution: {
                        type: metricItem.querySelector('.metric-distribution').value,
                        mean: parseFloat(metricItem.querySelector('.metric-mean').value),
                        std: parseFloat(metricItem.querySelector('.metric-std').value) || null
                    },
                    unit: metricItem.querySelector('.metric-unit').value || '',
                    category: metricItem.querySelector('.metric-category').value || 'general'
                });
            }
        });

        config.entities.push(entity);
    });

    return config;
}

// Validate Config
async function validateConfig() {
    const config = buildConfig();

    if (config.entities.length === 0) {
        showNotification('Please add at least one entity or use a quick preset', 'warning');
        return;
    }

    const btn = event.target.closest('button');
    btn.setAttribute('data-loading', 'true');
    btn.disabled = true;
    showLoading(true);

    try {
        const response = await fetch('/api/validate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(config)
        });

        const data = await response.json();

        if (data.valid) {
            showNotification('✓ Configuration is valid!', 'success');
        } else {
            showNotification('Validation errors found', 'danger');
            data.errors.forEach(err => showNotification(err, 'warning'));
        }
    } catch (error) {
        console.error('Error:', error);
        showNotification('Validation failed', 'danger');
    } finally {
        showLoading(false);
        btn.setAttribute('data-loading', 'false');
        btn.disabled = false;
    }
}

// Generate Data
async function generateData() {
    const config = buildConfig();

    if (config.entities.length === 0) {
        showNotification('Please add at least one entity or use a quick preset', 'warning');
        return;
    }

    const btn = event.target.closest('button');
    btn.setAttribute('data-loading', 'true');
    btn.disabled = true;
    showLoading(true);

    try {
        const response = await fetch('/api/generate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(config)
        });

        const data = await response.json();

        if (data.success) {
            showNotification('✓ Data generated successfully!', 'success');
            showResult(data);
        } else {
            showNotification('Generation failed: ' + data.error, 'danger');
        }
    } catch (error) {
        console.error('Error:', error);
        showNotification('Generation failed', 'danger');
    } finally {
        showLoading(false);
        btn.setAttribute('data-loading', 'false');
        btn.disabled = false;
    }
}

// Show Result
function showResult(data) {
    // Build preview table if preview data exists
    let previewHtml = '';
    if (data.preview && data.preview.length > 0) {
        const columns = Object.keys(data.preview[0]);
        previewHtml = `
            <div class="mt-4" id="dataPreviewSection">
                <h6><i class="bi bi-table"></i> Data Preview (First 10 Rows)</h6>
                <div class="table-responsive" style="max-height: 400px; overflow-y: auto;">
                    <table class="table table-sm table-striped table-hover">
                        <thead class="table-dark sticky-top">
                            <tr>
                                ${columns.map(col => `<th>${col}</th>`).join('')}
                            </tr>
                        </thead>
                        <tbody>
                            ${data.preview.map(row => `
                                <tr>
                                    ${columns.map(col => `<td>${formatValue(row[col])}</td>`).join('')}
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                </div>
            </div>
        `;
    }

    // Build statistics table if statistics exist
    let statsHtml = '';
    let chartDataHtml = '';
    if (data.statistics && Object.keys(data.statistics).length > 0) {
        statsHtml = `
            <div class="mt-4">
                <h6><i class="bi bi-bar-chart"></i> Statistics Summary</h6>
                <div class="table-responsive">
                    <table class="table table-sm table-bordered">
                        <thead class="table-light">
                            <tr>
                                <th>Metric</th>
                                <th>Mean</th>
                                <th>Std Dev</th>
                                <th>Min</th>
                                <th>Max</th>
                                <th>Median</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${Object.entries(data.statistics).map(([metric, stats]) => `
                                <tr>
                                    <td><strong>${metric}</strong></td>
                                    <td>${stats.mean.toFixed(2)}</td>
                                    <td>${stats.std.toFixed(2)}</td>
                                    <td>${stats.min.toFixed(2)}</td>
                                    <td>${stats.max.toFixed(2)}</td>
                                    <td>${stats.median.toFixed(2)}</td>
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                </div>
            </div>
        `;

        // Prepare chart data for visualizations
        chartDataHtml = `
            <div class="mt-4">
                <h6><i class="bi bi-graph-up-arrow"></i> Interactive Data Visualizations</h6>
                <div class="row g-3 mt-2">
                    <div class="col-md-6">
                        <div class="glass-card p-3">
                            <h6 class="text-center mb-3">Metric Distributions (Mean Values)</h6>
                            <canvas id="metricsBarChart" style="max-height: 300px;"></canvas>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="glass-card p-3">
                            <h6 class="text-center mb-3">Variability Analysis (Std Dev)</h6>
                            <canvas id="variabilityChart" style="max-height: 300px;"></canvas>
                        </div>
                    </div>
                </div>
                <div class="row g-3 mt-2">
                    <div class="col-md-12">
                        <div class="glass-card p-3">
                            <h6 class="text-center mb-3">Range Analysis (Min-Max)</h6>
                            <canvas id="rangeChart" style="max-height: 300px;"></canvas>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    const html = `
        <div class="glass-card position-relative" id="resultsCard">
            <button class="btn btn-sm btn-outline-danger position-absolute"
                    style="top: 10px; right: 10px; z-index: 10;"
                    onclick="closeResultsCard()"
                    title="Close preview">
                <i class="bi bi-x-lg"></i>
            </button>
            <div class="card-body">
                <div class="alert alert-success alert-fancy mb-0">
                    <h5><i class="bi bi-check-circle-fill"></i> Generation Complete!</h5>
                    <div class="row mt-3">
                        <div class="col-md-3">
                            <div class="text-center p-2">
                                <i class="bi bi-file-earmark-text icon-lg text-primary"></i>
                                <h4 class="mt-2 mb-0">${data.metadata.num_records.toLocaleString()}</h4>
                                <small>Records</small>
                            </div>
                        </div>
                        <div class="col-md-3">
                            <div class="text-center p-2">
                                <i class="bi bi-server icon-lg text-success"></i>
                                <h4 class="mt-2 mb-0">${data.metadata.num_entities}</h4>
                                <small>Entities</small>
                            </div>
                        </div>
                        <div class="col-md-3">
                            <div class="text-center p-2">
                                <i class="bi bi-graph-up icon-lg text-info"></i>
                                <h4 class="mt-2 mb-0">${data.metadata.num_metrics}</h4>
                                <small>Metrics</small>
                            </div>
                        </div>
                        <div class="col-md-3">
                            <div class="text-center p-2">
                                <i class="bi bi-file-binary icon-lg text-warning"></i>
                                <h4 class="mt-2 mb-0">${data.metadata.file_size_mb.toFixed(2)} MB</h4>
                                <small>File Size</small>
                            </div>
                        </div>
                    </div>
                    <div class="text-center mt-4">
                        <a href="${data.download_url}" class="btn btn-success-fancy btn-lg" download>
                            <i class="bi bi-download"></i> Download Generated Data
                        </a>
                    </div>
                    ${previewHtml}
                    ${statsHtml}
                    ${chartDataHtml}
                </div>
            </div>
        </div>
    `;
    document.getElementById('statusContainer').innerHTML = html;

    // Create charts if statistics exist
    if (data.statistics && Object.keys(data.statistics).length > 0) {
        createCharts(data.statistics);
    }

    // Scroll to results
    setTimeout(() => {
        document.getElementById('resultsCard').scrollIntoView({ behavior: 'smooth', block: 'center' });
    }, 100);
}

// Close results card
function closeResultsCard() {
    const card = document.getElementById('resultsCard');
    if (card) {
        card.style.transition = 'opacity 0.3s ease-out';
        card.style.opacity = '0';
        setTimeout(() => {
            card.remove();
        }, 300);
    }
}

// Create interactive charts
function createCharts(statistics) {
    const metrics = Object.keys(statistics);
    const means = metrics.map(m => statistics[m].mean);
    const stds = metrics.map(m => statistics[m].std);
    const mins = metrics.map(m => statistics[m].min);
    const maxs = metrics.map(m => statistics[m].max);

    // Chart colors
    const colors = [
        'rgba(59, 130, 246, 0.8)',  // blue
        'rgba(16, 185, 129, 0.8)',  // green
        'rgba(249, 115, 22, 0.8)',  // orange
        'rgba(139, 92, 246, 0.8)',  // purple
        'rgba(236, 72, 153, 0.8)',  // pink
        'rgba(245, 158, 11, 0.8)',  // amber
    ];

    // Bar Chart - Mean Values
    const barCtx = document.getElementById('metricsBarChart');
    if (barCtx) {
        new Chart(barCtx, {
            type: 'bar',
            data: {
                labels: metrics,
                datasets: [{
                    label: 'Mean Value',
                    data: means,
                    backgroundColor: colors,
                    borderColor: colors.map(c => c.replace('0.8', '1')),
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return 'Mean: ' + context.parsed.y.toFixed(2);
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        },
                        ticks: {
                            color: '#fff'
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        },
                        ticks: {
                            color: '#fff',
                            maxRotation: 45,
                            minRotation: 45
                        }
                    }
                }
            }
        });
    }

    // Radar Chart - Variability
    const radarCtx = document.getElementById('variabilityChart');
    if (radarCtx) {
        new Chart(radarCtx, {
            type: 'radar',
            data: {
                labels: metrics,
                datasets: [{
                    label: 'Standard Deviation',
                    data: stds,
                    backgroundColor: 'rgba(59, 130, 246, 0.2)',
                    borderColor: 'rgba(59, 130, 246, 1)',
                    borderWidth: 2,
                    pointBackgroundColor: 'rgba(59, 130, 246, 1)',
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: 'rgba(59, 130, 246, 1)'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    r: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        },
                        angleLines: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        },
                        ticks: {
                            color: '#fff',
                            backdropColor: 'transparent'
                        },
                        pointLabels: {
                            color: '#fff',
                            font: {
                                size: 11
                            }
                        }
                    }
                }
            }
        });
    }

    // Line Chart - Range (Min-Max)
    const rangeCtx = document.getElementById('rangeChart');
    if (rangeCtx) {
        new Chart(rangeCtx, {
            type: 'line',
            data: {
                labels: metrics,
                datasets: [
                    {
                        label: 'Maximum',
                        data: maxs,
                        borderColor: 'rgba(239, 68, 68, 1)',
                        backgroundColor: 'rgba(239, 68, 68, 0.1)',
                        fill: false,
                        tension: 0.4,
                        borderWidth: 2,
                        pointRadius: 4
                    },
                    {
                        label: 'Mean',
                        data: means,
                        borderColor: 'rgba(59, 130, 246, 1)',
                        backgroundColor: 'rgba(59, 130, 246, 0.1)',
                        fill: false,
                        tension: 0.4,
                        borderWidth: 2,
                        pointRadius: 4
                    },
                    {
                        label: 'Minimum',
                        data: mins,
                        borderColor: 'rgba(16, 185, 129, 1)',
                        backgroundColor: 'rgba(16, 185, 129, 0.1)',
                        fill: false,
                        tension: 0.4,
                        borderWidth: 2,
                        pointRadius: 4
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top',
                        labels: {
                            color: '#fff',
                            usePointStyle: true,
                            padding: 15
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        },
                        ticks: {
                            color: '#fff'
                        }
                    },
                    x: {
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        },
                        ticks: {
                            color: '#fff',
                            maxRotation: 45,
                            minRotation: 45
                        }
                    }
                }
            }
        });
    }
}

// Helper function to format values in preview table
function formatValue(value) {
    if (value === null || value === undefined) {
        return '<span class="text-muted">null</span>';
    }
    if (typeof value === 'number') {
        return value.toFixed(2);
    }
    if (typeof value === 'string' && value.length > 50) {
        return value.substring(0, 47) + '...';
    }
    return value;
}

// Export Config
function exportConfig() {
    const config = buildConfig();
    const blob = new Blob([JSON.stringify(config, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `config_${new Date().toISOString().slice(0, 10)}.json`;
    a.click();
    showNotification('Configuration exported', 'success');
}

// Clear All
function clearAll() {
    const entityCount = document.querySelectorAll('.entity-item').length;
    const metricCount = document.querySelectorAll('.metric-item').length;

    // Confirm if there's data to clear
    if (entityCount > 0 || metricCount > 0) {
        const message = `Are you sure you want to clear ${entityCount} entities and ${metricCount} metrics?`;
        if (!confirm(message)) {
            return;
        }
    }

    document.getElementById('entitiesList').innerHTML = '';
    document.getElementById('metricsList').innerHTML = '';
    document.getElementById('statusContainer').innerHTML = '';
    updateCounts();

    showNotification('Configuration cleared', 'info');
}

// Toggle Advanced
function toggleAdvanced() {
    const section = document.getElementById('advancedSettings');
    const icon = document.getElementById('advancedIcon');
    
    if (section.style.display === 'none') {
        section.style.display = 'block';
        icon.classList.remove('bi-chevron-down');
        icon.classList.add('bi-chevron-up');
    } else {
        section.style.display = 'none';
        icon.classList.remove('bi-chevron-up');
        icon.classList.add('bi-chevron-down');
    }
}

// Update Duration
function updateDuration() {
    const start = new Date(document.getElementById('startDate').value);
    const end = new Date(document.getElementById('endDate').value);
    const diff = end - start;
    const hours = Math.floor(diff / (1000 * 60 * 60));
    const days = Math.floor(hours / 24);
    
    let display = '';
    if (days > 0) {
        display = `${days}d ${hours % 24}h`;
    } else {
        display = `${hours}h`;
    }
    
    document.getElementById('duration').value = display;
}

// Show Loading
function showLoading(show) {
    document.getElementById('loadingOverlay').style.display = show ? 'flex' : 'none';
}

// Show Notification
function showNotification(message, type = 'info') {
    const colors = {
        success: 'alert-success',
        danger: 'alert-danger',
        warning: 'alert-warning',
        info: 'alert-info'
    };

    const icons = {
        success: 'check-circle-fill',
        danger: 'exclamation-triangle-fill',
        warning: 'exclamation-circle-fill',
        info: 'info-circle-fill'
    };

    const html = `
        <div class="alert ${colors[type]} alert-fancy alert-dismissible fade show mt-3" role="alert">
            <i class="bi bi-${icons[type]} me-2"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;

    const container = document.getElementById('statusContainer');
    container.insertAdjacentHTML('beforeend', html);

    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        const alerts = container.querySelectorAll('.alert');
        if (alerts.length > 0) {
            alerts[0].classList.remove('show');
            setTimeout(() => alerts[0]?.remove(), 150);
        }
    }, 5000);

    // Keep max 3 alerts
    const alerts = container.querySelectorAll('.alert');
    if (alerts.length > 3) {
        alerts[0].remove();
    }
}

// Add visual feedback for all buttons
document.addEventListener('DOMContentLoaded', function() {
    // Add ripple effect to all buttons
    document.querySelectorAll('.btn, .domain-card, .preset-card').forEach(element => {
        element.addEventListener('click', function(e) {
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;

            ripple.style.cssText = `
                position: absolute;
                width: ${size}px;
                height: ${size}px;
                border-radius: 50%;
                background: rgba(255, 255, 255, 0.5);
                left: ${x}px;
                top: ${y}px;
                pointer-events: none;
                transform: scale(0);
                animation: ripple 0.6s ease-out;
            `;

            this.style.position = 'relative';
            this.style.overflow = 'hidden';
            this.appendChild(ripple);

            setTimeout(() => ripple.remove(), 600);
        });
    });

    // Add CSS for ripple animation
    const style = document.createElement('style');
    style.textContent = `
        @keyframes ripple {
            to {
                transform: scale(4);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);

    // Enhance form validation with visual feedback
    document.querySelectorAll('input, select, textarea').forEach(input => {
        input.addEventListener('invalid', function() {
            this.classList.add('shake');
            setTimeout(() => this.classList.remove('shake'), 500);
        });

        input.addEventListener('input', function() {
            if (this.validity.valid) {
                this.style.borderColor = '#10b981';
            } else if (this.value.length > 0) {
                this.style.borderColor = '#ef4444';
            }
        });
    });
});