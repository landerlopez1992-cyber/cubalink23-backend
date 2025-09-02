# -*- coding: utf-8 -*-
from flask import Flask, jsonify
from flask_cors import CORS
import os
from datetime import datetime

# Importar solo admin_routes que contiene los endpoints necesarios
try:
    from admin_routes import admin
    ADMIN_LOADED = True
except ImportError as e:
    print(f"⚠️ Error cargando admin_routes: {e}")
    ADMIN_LOADED = False

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Configuración mínima
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'cubalink23-secret-key')

# Registrar blueprint solo si se cargó correctamente
if ADMIN_LOADED:
    app.register_blueprint(admin)
    print("✅ Admin routes cargadas correctamente")
else:
    print("❌ Admin routes no pudieron cargarse")

@app.route('/')
def home():
    """Página principal"""
    return jsonify({
        'message': 'CubaLink23 Backend API',
        'status': 'running',
        'endpoints': ['/api/health', '/admin/api/flights/search', '/admin/api/flights/airports']
    })

@app.route('/api/health')
def health_check():
    """Health check para Render.com"""
    return jsonify({
        'status': 'healthy',
        'message': 'Cubalink23 Backend is running',
        'timestamp': datetime.now().isoformat(),
        'admin_routes': ADMIN_LOADED,
        'duffel_key_configured': bool(os.environ.get('DUFFEL_API_KEY'))
    })

if __name__ == '__main__':
    print('🚀 Iniciando CubaLink23 Backend v2.3 - MINIMAL & STABLE...')
    port = int(os.environ.get('PORT', 3005))
    app.run(host='0.0.0.0', port=port, debug=False)
