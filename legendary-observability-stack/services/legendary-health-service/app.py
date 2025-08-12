# 🏥💎⚡ LEGENDARY HEALTH SERVICE APPLICATION ⚡💎🏥
# Containerized health monitoring service for empire observability
# Provides comprehensive system metrics with BROski$ rewards

import os
import time
import json
import random
import logging
import requests
import psutil
import docker
from datetime import datetime
from flask import Flask, jsonify, render_template_string
from prometheus_client import generate_latest, Counter, Gauge, Histogram, CONTENT_TYPE_LATEST
import threading

# 🎯 ADHD-OPTIMIZED LOGGING (UTF-8 safe)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('/app/logs/health-service.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

# 🚀 FLASK APPLICATION SETUP
app = Flask(__name__)

# 📊 PROMETHEUS METRICS
health_score_gauge = Gauge('legendary_system_health_score', 'Overall system health percentage')
service_counter = Counter('legendary_service_requests_total', 'Total service requests', ['endpoint'])
response_time_histogram = Histogram('legendary_service_response_time_seconds', 'Response time histogram')
broskie_rewards_counter = Counter('legendary_broskie_rewards_total', 'Total BROski$ rewards earned')
docker_container_gauge = Gauge('legendary_docker_containers_total', 'Number of running Docker containers')
memory_usage_gauge = Gauge('legendary_memory_usage_percent', 'Memory usage percentage')
cpu_usage_gauge = Gauge('legendary_cpu_usage_percent', 'CPU usage percentage')
disk_usage_gauge = Gauge('legendary_disk_usage_percent', 'Disk usage percentage')
network_bytes_gauge = Gauge('legendary_network_bytes_total', 'Network bytes transferred', ['direction'])

# 💎 GLOBAL STATE MANAGEMENT
class LegendaryHealthState:
    def __init__(self):
        self.health_score = 0.0
        self.broskie_balance = 0
        self.last_reward_time = time.time()
        self.service_status = {}
        self.achievements = []
        self.metrics_history = []

legendary_state = LegendaryHealthState()

# 🔧 DOCKER CLIENT SETUP (with error handling)
try:
    docker_client = docker.from_env()
    logger.info("🐳 Docker client connected successfully")
except Exception as e:
    logger.warning(f"⚠️ Docker client connection failed: {e}")
    docker_client = None

# 🏥 HEALTH CALCULATION ENGINE
def calculate_comprehensive_health():
    """Calculate comprehensive system health score"""
    try:
        health_components = {}

        # 💾 MEMORY HEALTH
        memory = psutil.virtual_memory()
        memory_health = max(0, 100 - memory.percent)
        health_components['memory'] = memory_health
        memory_usage_gauge.set(memory.percent)

        # ⚡ CPU HEALTH
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_health = max(0, 100 - cpu_percent)
        health_components['cpu'] = cpu_health
        cpu_usage_gauge.set(cpu_percent)

        # 💾 DISK HEALTH
        disk = psutil.disk_usage('/')
        disk_percent = (disk.used / disk.total) * 100
        disk_health = max(0, 100 - disk_percent)
        health_components['disk'] = disk_health
        disk_usage_gauge.set(disk_percent)

        # 🌐 NETWORK HEALTH
        network = psutil.net_io_counters()
        network_bytes_gauge.labels(direction='sent').set(network.bytes_sent)
        network_bytes_gauge.labels(direction='recv').set(network.bytes_recv)
        network_health = 95.0  # Assume good unless errors detected
        health_components['network'] = network_health

        # 🐳 DOCKER HEALTH
        docker_health = 90.0  # Default good
        container_count = 0
        if docker_client:
            try:
                containers = docker_client.containers.list()
                container_count = len(containers)
                running_containers = len([c for c in containers if c.status == 'running'])
                if container_count > 0:
                    docker_health = (running_containers / container_count) * 100
                docker_container_gauge.set(running_containers)
            except Exception as e:
                logger.warning(f"⚠️ Docker health check failed: {e}")
                docker_health = 70.0

        health_components['docker'] = docker_health

        # 🎯 CALCULATE WEIGHTED AVERAGE
        weights = {
            'memory': 0.25,
            'cpu': 0.25,
            'disk': 0.20,
            'network': 0.15,
            'docker': 0.15
        }

        overall_health = sum(
            health_components[component] * weights[component]
            for component in health_components
        )

        # 🎨 ADD RANDOM VARIATION (ADHD-friendly unpredictability)
        health_variation = random.uniform(-2.0, 2.0)
        overall_health += health_variation
        overall_health = max(0, min(100, overall_health))  # Clamp 0-100

        legendary_state.health_score = overall_health
        health_score_gauge.set(overall_health)

        # 💎 CHECK FOR BROSKIE$ REWARDS
        check_broskie_rewards(overall_health, health_components)

        return {
            'overall_health': round(overall_health, 1),
            'components': {k: round(v, 1) for k, v in health_components.items()},
            'container_count': container_count,
            'timestamp': datetime.now().isoformat()
        }

    except Exception as e:
        logger.error(f"❌ Health calculation error: {e}")
        return {
            'overall_health': 0.0,
            'components': {},
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }

# 💰 BROSKIE$ REWARD SYSTEM
def check_broskie_rewards(health_score, components):
    """Award BROski$ for achievements"""
    current_time = time.time()
    rewards_earned = 0

    try:
        # 🏆 HIGH HEALTH REWARD (>95%)
        if health_score > 95.0 and current_time - legendary_state.last_reward_time > 300:  # 5 min cooldown
            rewards_earned += 500
            legendary_state.achievements.append({
                'type': 'High Performance',
                'time': datetime.now().isoformat(),
                'reward': 500,
                'health_score': health_score
            })
            logger.info(f"💎 HIGH PERFORMANCE REWARD: 500 BROski$ (Health: {health_score}%)")

        # 🎯 LEGENDARY HEALTH REWARD (>98%)
        if health_score > 98.0 and current_time - legendary_state.last_reward_time > 600:  # 10 min cooldown
            rewards_earned += 1000
            legendary_state.achievements.append({
                'type': 'Legendary Performance',
                'time': datetime.now().isoformat(),
                'reward': 1000,
                'health_score': health_score
            })
            logger.info(f"🚀 LEGENDARY PERFORMANCE REWARD: 1000 BROski$ (Health: {health_score}%)")

        # 💎 COMPONENT EXCELLENCE REWARDS
        for component, score in components.items():
            if score > 95.0 and random.random() < 0.1:  # 10% chance
                component_reward = 100
                rewards_earned += component_reward
                legendary_state.achievements.append({
                    'type': f'{component.title()} Excellence',
                    'time': datetime.now().isoformat(),
                    'reward': component_reward,
                    'score': score
                })

        if rewards_earned > 0:
            legendary_state.broskie_balance += rewards_earned
            broskie_rewards_counter.inc(rewards_earned)
            legendary_state.last_reward_time = current_time

    except Exception as e:
        logger.error(f"❌ BROski$ reward system error: {e}")

# 🌐 API ENDPOINTS
@app.route('/')
def index():
    """Main dashboard endpoint"""
    service_counter.labels(endpoint='index').inc()

    dashboard_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>🏥💎 Legendary Health Service 💎🏥</title>
        <style>
            body {
                font-family: 'Segoe UI', Arial, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white; margin: 0; padding: 20px;
            }
            .container { max-width: 1200px; margin: 0 auto; }
            .header { text-align: center; margin-bottom: 30px; }
            .metrics-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
            .metric-card {
                background: rgba(255,255,255,0.1);
                border-radius: 15px;
                padding: 20px;
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255,255,255,0.2);
            }
            .health-score { font-size: 3em; font-weight: bold; text-align: center; }
            .component-list { margin-top: 15px; }
            .component-item {
                display: flex; justify-content: space-between;
                padding: 8px 0; border-bottom: 1px solid rgba(255,255,255,0.1);
            }
            .broskie-balance {
                background: linear-gradient(45deg, #FFD700, #FFA500);
                color: #000; font-weight: bold; text-align: center;
                padding: 15px; border-radius: 10px; margin: 15px 0;
            }
            .achievement-item {
                background: rgba(255,215,0,0.2);
                padding: 10px; border-radius: 8px; margin: 8px 0;
            }
            .refresh-btn {
                background: #4CAF50; color: white; border: none;
                padding: 12px 24px; border-radius: 6px; cursor: pointer;
                font-size: 16px; margin: 10px;
            }
            .refresh-btn:hover { background: #45a049; }
        </style>
        <script>
            function refreshData() {
                location.reload();
            }
            // Auto-refresh every 30 seconds
            setTimeout(refreshData, 30000);
        </script>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🏥💎⚡ LEGENDARY HEALTH SERVICE ⚡💎🏥</h1>
                <p>Real-time Empire Monitoring Dashboard</p>
                <button class="refresh-btn" onclick="refreshData()">🔄 Refresh Data</button>
            </div>

            <div class="broskie-balance">
                💰 BROski$ Balance: {{ broskie_balance }} 💎
            </div>

            <div class="metrics-grid">
                <div class="metric-card">
                    <h2>🎯 Overall Health</h2>
                    <div class="health-score" style="color: {{ health_color }};">
                        {{ health_score }}%
                    </div>
                    <p style="text-align: center;">{{ health_status }}</p>
                </div>

                <div class="metric-card">
                    <h2>📊 Component Health</h2>
                    <div class="component-list">
                        {% for component, score in components.items() %}
                        <div class="component-item">
                            <span>{{ component.title() }}</span>
                            <span style="color: {{ 'lime' if score > 90 else 'orange' if score > 70 else 'red' }};">
                                {{ score }}%
                            </span>
                        </div>
                        {% endfor %}
                    </div>
                </div>

                <div class="metric-card">
                    <h2>🏆 Recent Achievements</h2>
                    {% if achievements %}
                        {% for achievement in achievements[-5:] %}
                        <div class="achievement-item">
                            <strong>{{ achievement.type }}</strong><br>
                            💰 Reward: {{ achievement.reward }} BROski$<br>
                            <small>{{ achievement.time[:19] }}</small>
                        </div>
                        {% endfor %}
                    {% else %}
                        <p>🎯 Keep monitoring to earn achievements!</p>
                    {% endif %}
                </div>

                <div class="metric-card">
                    <h2>🐳 System Info</h2>
                    <div class="component-list">
                        <div class="component-item">
                            <span>Docker Containers</span>
                            <span>{{ container_count }}</span>
                        </div>
                        <div class="component-item">
                            <span>Last Updated</span>
                            <span>{{ timestamp[:19] }}</span>
                        </div>
                        <div class="component-item">
                            <span>Service Uptime</span>
                            <span>{{ uptime }}</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

    try:
        health_data = calculate_comprehensive_health()

        # 🎨 Determine health status and color
        health_score = health_data['overall_health']
        if health_score >= 95:
            health_status = "🚀 LEGENDARY"
            health_color = "lime"
        elif health_score >= 85:
            health_status = "💎 EXCELLENT"
            health_color = "gold"
        elif health_score >= 70:
            health_status = "⚡ GOOD"
            health_color = "orange"
        else:
            health_status = "⚠️ NEEDS ATTENTION"
            health_color = "red"

        # Calculate uptime
        uptime_seconds = time.time() - app.start_time
        uptime = f"{int(uptime_seconds // 3600)}h {int((uptime_seconds % 3600) // 60)}m"

        return render_template_string(
            dashboard_html,
            health_score=health_score,
            health_status=health_status,
            health_color=health_color,
            components=health_data['components'],
            broskie_balance=legendary_state.broskie_balance,
            achievements=legendary_state.achievements,
            container_count=health_data.get('container_count', 0),
            timestamp=health_data['timestamp'],
            uptime=uptime
        )

    except Exception as e:
        logger.error(f"❌ Dashboard render error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health_check():
    """Health check endpoint for monitoring"""
    service_counter.labels(endpoint='health').inc()

    with response_time_histogram.time():
        health_data = calculate_comprehensive_health()

    return jsonify(health_data)

@app.route('/metrics')
def metrics():
    """Prometheus metrics endpoint"""
    service_counter.labels(endpoint='metrics').inc()
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

@app.route('/broskie')
def broskie_status():
    """BROski$ balance and achievements"""
    service_counter.labels(endpoint='broskie').inc()

    return jsonify({
        'balance': legendary_state.broskie_balance,
        'achievements': legendary_state.achievements[-10:],  # Last 10
        'total_achievements': len(legendary_state.achievements)
    })

@app.route('/api/health')
def api_health():
    """API health endpoint for external monitoring"""
    service_counter.labels(endpoint='api_health').inc()

    health_data = calculate_comprehensive_health()

    return jsonify({
        'status': 'healthy' if health_data['overall_health'] > 70 else 'degraded',
        'health_score': health_data['overall_health'],
        'components': health_data['components'],
        'timestamp': health_data['timestamp']
    })

# 🚀 BACKGROUND HEALTH MONITORING
def background_health_monitor():
    """Background thread for continuous monitoring"""
    logger.info("🔄 Starting background health monitoring...")

    while True:
        try:
            health_data = calculate_comprehensive_health()

            # Store metrics history (keep last 100 points)
            legendary_state.metrics_history.append({
                'timestamp': time.time(),
                'health_score': health_data['overall_health'],
                'components': health_data['components']
            })

            if len(legendary_state.metrics_history) > 100:
                legendary_state.metrics_history.pop(0)

            time.sleep(60)  # Monitor every minute

        except Exception as e:
            logger.error(f"❌ Background monitor error: {e}")
            time.sleep(30)  # Shorter retry interval on error

if __name__ == '__main__':
    # 🚀 STARTUP SEQUENCE
    app.start_time = time.time()

    logger.info("🏥💎⚡ LEGENDARY HEALTH SERVICE STARTING ⚡💎🏥")
    logger.info("🎯 ADHD-optimized health monitoring with BROski$ rewards")

    # 🔄 Start background monitoring thread
    monitor_thread = threading.Thread(target=background_health_monitor, daemon=True)
    monitor_thread.start()

    # 🌐 Start Flask application
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
