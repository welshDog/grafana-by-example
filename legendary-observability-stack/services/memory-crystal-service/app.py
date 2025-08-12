# 🧠💎⚡ MEMORY CRYSTAL SERVICE ⚡💎🧠
# Advanced memory pattern storage and retrieval system
# Optimized for ADHD workflow with intelligent caching

import os
import time
import json
import redis
import hashlib
import random
from datetime import datetime, timedelta
from flask import Flask, jsonify, request, render_template_string
from prometheus_client import generate_latest, Counter, Gauge, Histogram, CONTENT_TYPE_LATEST
import logging
import threading
from collections import defaultdict

# 🎯 ADHD-OPTIMIZED LOGGING SETUP
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('/app/logs/memory-crystal.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

# 🚀 FLASK APPLICATION
app = Flask(__name__)

# 📊 PROMETHEUS METRICS
crystal_operations_counter = Counter('memory_crystal_operations_total', 'Total crystal operations', ['operation'])
crystal_storage_gauge = Gauge('memory_crystal_storage_usage_bytes', 'Crystal storage usage in bytes')
crystal_efficiency_gauge = Gauge('memory_crystal_efficiency_score', 'Crystal efficiency percentage')
crystal_response_time = Histogram('memory_crystal_response_time_seconds', 'Crystal operation response time')
active_crystals_gauge = Gauge('memory_crystal_active_count', 'Number of active memory crystals')
crystal_cache_hits = Counter('memory_crystal_cache_hits_total', 'Cache hit counter')
crystal_cache_misses = Counter('memory_crystal_cache_misses_total', 'Cache miss counter')
broskie_crystals_counter = Counter('memory_crystal_broskie_rewards_total', 'BROski$ from crystal operations')

# 💎 MEMORY CRYSTAL STATE MANAGEMENT
class MemoryCrystalManager:
    def __init__(self):
        self.crystals = {}
        self.access_patterns = defaultdict(int)
        self.efficiency_history = []
        self.total_operations = 0
        self.cache_performance = {'hits': 0, 'misses': 0}
        self.broskie_balance = 0
        self.achievements = []

        # 🎯 ADHD-FRIENDLY CATEGORIES
        self.crystal_categories = {
            'hyperfocus': 'High-priority focus patterns',
            'workflow': 'Workflow optimization memories',
            'achievement': 'Success pattern storage',
            'debug': 'Problem-solving memories',
            'creative': 'Creative breakthrough patterns',
            'social': 'Team collaboration memories'
        }

crystal_manager = MemoryCrystalManager()

# 🔗 REDIS CONNECTION (with fallback to memory)
try:
    redis_client = redis.Redis(
        host=os.environ.get('REDIS_HOST', 'redis'),
        port=int(os.environ.get('REDIS_PORT', 6379)),
        db=0,
        decode_responses=True,
        socket_connect_timeout=5
    )
    redis_client.ping()
    logger.info("💎 Redis connection established for crystal storage")
    REDIS_AVAILABLE = True
except Exception as e:
    logger.warning(f"⚠️ Redis unavailable, using memory storage: {e}")
    redis_client = None
    REDIS_AVAILABLE = False

# 🧠 MEMORY CRYSTAL OPERATIONS
class MemoryCrystal:
    def __init__(self, crystal_id, category='general', pattern_data=None, metadata=None):
        self.crystal_id = crystal_id
        self.category = category
        self.pattern_data = pattern_data or {}
        self.metadata = metadata or {}
        self.created_at = datetime.now()
        self.last_accessed = datetime.now()
        self.access_count = 0
        self.efficiency_score = 0.0

    def to_dict(self):
        return {
            'crystal_id': self.crystal_id,
            'category': self.category,
            'pattern_data': self.pattern_data,
            'metadata': self.metadata,
            'created_at': self.created_at.isoformat(),
            'last_accessed': self.last_accessed.isoformat(),
            'access_count': self.access_count,
            'efficiency_score': self.efficiency_score
        }

    def update_access(self):
        self.last_accessed = datetime.now()
        self.access_count += 1
        # 🎯 Calculate efficiency based on access patterns
        time_factor = min(1.0, self.access_count / 10.0)  # More access = higher efficiency
        recency_factor = max(0.1, 1.0 - (time.time() - self.last_accessed.timestamp()) / (7 * 24 * 3600))
        self.efficiency_score = (time_factor * 0.6 + recency_factor * 0.4) * 100

def generate_crystal_id(pattern_data, category):
    """Generate unique crystal ID based on content"""
    content = f"{category}:{json.dumps(pattern_data, sort_keys=True)}"
    return hashlib.md5(content.encode()).hexdigest()[:12]

def store_crystal(category, pattern_data, metadata=None):
    """Store a new memory crystal"""
    try:
        crystal_id = generate_crystal_id(pattern_data, category)
        crystal = MemoryCrystal(crystal_id, category, pattern_data, metadata)

        # 💎 Store in Redis or memory
        if REDIS_AVAILABLE:
            redis_client.setex(
                f"crystal:{crystal_id}",
                timedelta(days=30),  # 30-day expiration
                json.dumps(crystal.to_dict(), default=str)
            )
        else:
            crystal_manager.crystals[crystal_id] = crystal

        crystal_manager.total_operations += 1
        crystal_operations_counter.labels(operation='store').inc()

        # 🏆 Check for storage achievement
        if crystal_manager.total_operations % 10 == 0:
            reward_broskie_crystals('storage_milestone', crystal_manager.total_operations)

        logger.info(f"💎 Crystal stored: {crystal_id} [{category}]")
        return crystal_id

    except Exception as e:
        logger.error(f"❌ Crystal storage error: {e}")
        return None

def retrieve_crystal(crystal_id):
    """Retrieve a memory crystal"""
    try:
        crystal_data = None

        # 🔍 Try Redis first
        if REDIS_AVAILABLE:
            data = redis_client.get(f"crystal:{crystal_id}")
            if data:
                crystal_data = json.loads(data)
                crystal_manager.cache_performance['hits'] += 1
                crystal_cache_hits.inc()
            else:
                crystal_manager.cache_performance['misses'] += 1
                crystal_cache_misses.inc()
        else:
            # 🧠 Check memory storage
            if crystal_id in crystal_manager.crystals:
                crystal = crystal_manager.crystals[crystal_id]
                crystal.update_access()
                crystal_data = crystal.to_dict()
                crystal_manager.cache_performance['hits'] += 1
                crystal_cache_hits.inc()
            else:
                crystal_manager.cache_performance['misses'] += 1
                crystal_cache_misses.inc()

        if crystal_data:
            crystal_operations_counter.labels(operation='retrieve').inc()
            crystal_manager.access_patterns[crystal_id] += 1
            logger.info(f"💎 Crystal retrieved: {crystal_id}")

        return crystal_data

    except Exception as e:
        logger.error(f"❌ Crystal retrieval error: {e}")
        return None

def search_crystals(category=None, pattern_match=None, limit=10):
    """Search for crystals by category or pattern"""
    try:
        results = []

        if REDIS_AVAILABLE:
            # 🔍 Redis search using key patterns
            pattern = f"crystal:*"
            crystal_keys = redis_client.keys(pattern)

            for key in crystal_keys[:limit * 2]:  # Get extra to filter
                data = redis_client.get(key)
                if data:
                    crystal_data = json.loads(data)
                    if category and crystal_data.get('category') != category:
                        continue
                    if pattern_match and pattern_match.lower() not in json.dumps(crystal_data.get('pattern_data', {})).lower():
                        continue
                    results.append(crystal_data)
                    if len(results) >= limit:
                        break
        else:
            # 🧠 Memory search
            for crystal in crystal_manager.crystals.values():
                if category and crystal.category != category:
                    continue
                if pattern_match and pattern_match.lower() not in json.dumps(crystal.pattern_data).lower():
                    continue
                results.append(crystal.to_dict())
                if len(results) >= limit:
                    break

        crystal_operations_counter.labels(operation='search').inc()
        logger.info(f"💎 Crystal search: {len(results)} results")
        return results

    except Exception as e:
        logger.error(f"❌ Crystal search error: {e}")
        return []

def calculate_crystal_efficiency():
    """Calculate overall crystal system efficiency"""
    try:
        if crystal_manager.cache_performance['hits'] + crystal_manager.cache_performance['misses'] == 0:
            cache_ratio = 100.0
        else:
            total_requests = crystal_manager.cache_performance['hits'] + crystal_manager.cache_performance['misses']
            cache_ratio = (crystal_manager.cache_performance['hits'] / total_requests) * 100

        # 🎯 Factor in access patterns
        active_crystals = len([k for k, v in crystal_manager.access_patterns.items() if v > 0])

        # 💎 Calculate efficiency score
        efficiency = (cache_ratio * 0.6) + (min(100, active_crystals * 2) * 0.4)

        crystal_efficiency_gauge.set(efficiency)
        active_crystals_gauge.set(active_crystals)

        # 🏆 Track efficiency history
        crystal_manager.efficiency_history.append({
            'timestamp': time.time(),
            'efficiency': efficiency,
            'cache_ratio': cache_ratio,
            'active_crystals': active_crystals
        })

        # Keep last 100 points
        if len(crystal_manager.efficiency_history) > 100:
            crystal_manager.efficiency_history.pop(0)

        return efficiency

    except Exception as e:
        logger.error(f"❌ Efficiency calculation error: {e}")
        return 0.0

def reward_broskie_crystals(achievement_type, value):
    """Award BROski$ for crystal achievements"""
    rewards = {
        'storage_milestone': lambda v: v * 10,  # 10 per crystal stored
        'high_efficiency': lambda v: int(v * 5),  # 5 per efficiency point
        'search_master': lambda v: 250,  # Fixed reward
        'cache_champion': lambda v: 500  # Fixed reward
    }

    if achievement_type in rewards:
        reward = rewards[achievement_type](value)
        crystal_manager.broskie_balance += reward
        broskie_crystals_counter.inc(reward)

        crystal_manager.achievements.append({
            'type': achievement_type.replace('_', ' ').title(),
            'time': datetime.now().isoformat(),
            'reward': reward,
            'value': value
        })

        logger.info(f"💰 BROski$ Crystal Reward: {reward} for {achievement_type}")

# 🌐 API ENDPOINTS
@app.route('/')
def dashboard():
    """Memory Crystal Dashboard"""
    dashboard_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>🧠💎 Memory Crystal Service 💎🧠</title>
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
            .efficiency-score { font-size: 2.5em; font-weight: bold; text-align: center; }
            .crystal-category {
                display: flex; justify-content: space-between;
                padding: 8px 0; border-bottom: 1px solid rgba(255,255,255,0.1);
            }
            .broskie-balance {
                background: linear-gradient(45deg, #FFD700, #FFA500);
                color: #000; font-weight: bold; text-align: center;
                padding: 15px; border-radius: 10px; margin: 15px 0;
            }
            .crystal-form {
                background: rgba(255,255,255,0.05);
                padding: 20px; border-radius: 10px; margin: 15px 0;
            }
            .form-input {
                width: 100%; padding: 8px; margin: 5px 0;
                border-radius: 5px; border: 1px solid #ccc;
            }
            .form-button {
                background: #4CAF50; color: white; border: none;
                padding: 12px 24px; border-radius: 6px; cursor: pointer;
                font-size: 16px; margin: 5px;
            }
            .form-button:hover { background: #45a049; }
        </style>
        <script>
            function storeCrystal() {
                const category = document.getElementById('category').value;
                const pattern = document.getElementById('pattern').value;
                const metadata = document.getElementById('metadata').value;

                if (!pattern) {
                    alert('Pattern data is required!');
                    return;
                }

                const data = {
                    category: category,
                    pattern_data: JSON.parse(pattern || '{}'),
                    metadata: JSON.parse(metadata || '{}')
                };

                fetch('/api/crystals', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(data)
                })
                .then(response => response.json())
                .then(result => {
                    if (result.crystal_id) {
                        alert('Crystal stored successfully! ID: ' + result.crystal_id);
                        location.reload();
                    } else {
                        alert('Error storing crystal');
                    }
                })
                .catch(error => alert('Error: ' + error));
            }

            // Auto-refresh every 30 seconds
            setTimeout(() => location.reload(), 30000);
        </script>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🧠💎⚡ MEMORY CRYSTAL SERVICE ⚡💎🧠</h1>
                <p>ADHD-Optimized Pattern Storage & Retrieval</p>
            </div>

            <div class="broskie-balance">
                💰 Crystal BROski$: {{ broskie_balance }} 💎
            </div>

            <div class="metrics-grid">
                <div class="metric-card">
                    <h2>⚡ System Efficiency</h2>
                    <div class="efficiency-score" style="color: {{ efficiency_color }};">
                        {{ efficiency_score }}%
                    </div>
                    <p style="text-align: center;">{{ efficiency_status }}</p>
                </div>

                <div class="metric-card">
                    <h2>📊 Crystal Statistics</h2>
                    <div class="crystal-category">
                        <span>Active Crystals</span>
                        <span>{{ active_crystals }}</span>
                    </div>
                    <div class="crystal-category">
                        <span>Cache Hit Rate</span>
                        <span>{{ cache_hit_rate }}%</span>
                    </div>
                    <div class="crystal-category">
                        <span>Total Operations</span>
                        <span>{{ total_operations }}</span>
                    </div>
                    <div class="crystal-category">
                        <span>Storage Backend</span>
                        <span>{{ storage_backend }}</span>
                    </div>
                </div>

                <div class="metric-card">
                    <h2>🏆 Crystal Achievements</h2>
                    {% if achievements %}
                        {% for achievement in achievements[-3:] %}
                        <div style="background: rgba(255,215,0,0.2); padding: 10px; border-radius: 8px; margin: 8px 0;">
                            <strong>{{ achievement.type }}</strong><br>
                            💰 {{ achievement.reward }} BROski$<br>
                            <small>{{ achievement.time[:19] }}</small>
                        </div>
                        {% endfor %}
                    {% else %}
                        <p>🎯 Store crystals to earn achievements!</p>
                    {% endif %}
                </div>

                <div class="metric-card">
                    <h2>💎 Store New Crystal</h2>
                    <div class="crystal-form">
                        <select id="category" class="form-input">
                            {% for cat, desc in categories.items() %}
                            <option value="{{ cat }}">{{ cat.title() }} - {{ desc }}</option>
                            {% endfor %}
                        </select>
                        <textarea id="pattern" placeholder='Pattern data (JSON): {"key": "value"}' class="form-input" rows="3"></textarea>
                        <textarea id="metadata" placeholder='Metadata (JSON): {"tags": ["tag1"]}' class="form-input" rows="2"></textarea>
                        <button class="form-button" onclick="storeCrystal()">💎 Store Crystal</button>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

    try:
        efficiency_score = calculate_crystal_efficiency()

        # 🎨 Determine efficiency status and color
        if efficiency_score >= 90:
            efficiency_status = "🚀 LEGENDARY"
            efficiency_color = "lime"
        elif efficiency_score >= 75:
            efficiency_status = "💎 EXCELLENT"
            efficiency_color = "gold"
        elif efficiency_score >= 60:
            efficiency_status = "⚡ GOOD"
            efficiency_color = "orange"
        else:
            efficiency_status = "⚠️ NEEDS OPTIMIZATION"
            efficiency_color = "red"

        # 🧮 Calculate cache hit rate
        total_requests = crystal_manager.cache_performance['hits'] + crystal_manager.cache_performance['misses']
        cache_hit_rate = 100.0 if total_requests == 0 else (crystal_manager.cache_performance['hits'] / total_requests) * 100

        return render_template_string(
            dashboard_html,
            efficiency_score=round(efficiency_score, 1),
            efficiency_status=efficiency_status,
            efficiency_color=efficiency_color,
            active_crystals=len(crystal_manager.access_patterns),
            cache_hit_rate=round(cache_hit_rate, 1),
            total_operations=crystal_manager.total_operations,
            storage_backend='Redis' if REDIS_AVAILABLE else 'Memory',
            broskie_balance=crystal_manager.broskie_balance,
            achievements=crystal_manager.achievements,
            categories=crystal_manager.crystal_categories
        )

    except Exception as e:
        logger.error(f"❌ Dashboard render error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    efficiency = calculate_crystal_efficiency()

    return jsonify({
        'status': 'healthy' if efficiency > 50 else 'degraded',
        'efficiency_score': round(efficiency, 1),
        'active_crystals': len(crystal_manager.access_patterns),
        'storage_backend': 'Redis' if REDIS_AVAILABLE else 'Memory',
        'total_operations': crystal_manager.total_operations,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/metrics')
def metrics():
    """Prometheus metrics endpoint"""
    # 📊 Update storage usage gauge
    if REDIS_AVAILABLE:
        try:
            info = redis_client.info('memory')
            crystal_storage_gauge.set(info.get('used_memory', 0))
        except:
            crystal_storage_gauge.set(0)
    else:
        # Estimate memory usage for in-memory crystals
        estimated_size = len(json.dumps([c.to_dict() for c in crystal_manager.crystals.values()]))
        crystal_storage_gauge.set(estimated_size)

    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

@app.route('/api/crystals', methods=['POST'])
def store_crystal_api():
    """API endpoint to store a crystal"""
    try:
        data = request.json
        category = data.get('category', 'general')
        pattern_data = data.get('pattern_data', {})
        metadata = data.get('metadata', {})

        with crystal_response_time.time():
            crystal_id = store_crystal(category, pattern_data, metadata)

        if crystal_id:
            return jsonify({'crystal_id': crystal_id, 'status': 'stored'})
        else:
            return jsonify({'error': 'Storage failed'}), 500

    except Exception as e:
        logger.error(f"❌ API store error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/crystals/<crystal_id>', methods=['GET'])
def retrieve_crystal_api(crystal_id):
    """API endpoint to retrieve a crystal"""
    try:
        with crystal_response_time.time():
            crystal_data = retrieve_crystal(crystal_id)

        if crystal_data:
            return jsonify(crystal_data)
        else:
            return jsonify({'error': 'Crystal not found'}), 404

    except Exception as e:
        logger.error(f"❌ API retrieve error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/crystals/search')
def search_crystals_api():
    """API endpoint to search crystals"""
    try:
        category = request.args.get('category')
        pattern_match = request.args.get('pattern')
        limit = int(request.args.get('limit', 10))

        with crystal_response_time.time():
            results = search_crystals(category, pattern_match, limit)

        return jsonify({
            'crystals': results,
            'count': len(results),
            'search_params': {
                'category': category,
                'pattern': pattern_match,
                'limit': limit
            }
        })

    except Exception as e:
        logger.error(f"❌ API search error: {e}")
        return jsonify({'error': str(e)}), 500

# 🔄 BACKGROUND EFFICIENCY MONITORING
def background_efficiency_monitor():
    """Background thread for efficiency monitoring and rewards"""
    logger.info("🔄 Starting crystal efficiency monitoring...")

    while True:
        try:
            efficiency = calculate_crystal_efficiency()

            # 🏆 Check for efficiency achievements
            if efficiency > 90 and time.time() % 600 < 60:  # Every 10 minutes
                reward_broskie_crystals('high_efficiency', efficiency)

            # 🎯 Check for cache performance
            if crystal_manager.cache_performance['hits'] > 0:
                total = crystal_manager.cache_performance['hits'] + crystal_manager.cache_performance['misses']
                hit_rate = (crystal_manager.cache_performance['hits'] / total) * 100

                if hit_rate > 95 and time.time() % 900 < 60:  # Every 15 minutes
                    reward_broskie_crystals('cache_champion', hit_rate)

            time.sleep(60)  # Monitor every minute

        except Exception as e:
            logger.error(f"❌ Background efficiency monitor error: {e}")
            time.sleep(30)

if __name__ == '__main__':
    # 🚀 STARTUP SEQUENCE
    logger.info("🧠💎⚡ MEMORY CRYSTAL SERVICE STARTING ⚡💎🧠")
    logger.info("🎯 ADHD-optimized pattern storage with intelligent caching")

    # 🔄 Start background monitoring
    monitor_thread = threading.Thread(target=background_efficiency_monitor, daemon=True)
    monitor_thread.start()

    # 🌐 Start Flask application
    port = int(os.environ.get('PORT', 8081))
    app.run(host='0.0.0.0', port=port, debug=False)
