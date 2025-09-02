# -*- coding: utf-8 -*-
from flask import Flask, render_template, jsonify
from flask_cors import CORS
import os
from datetime import datetime
from admin_routes import admin
from auth_routes import auth
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv('config.env')

app = Flask(__name__)
CORS(app)

# Configuración de la aplicación
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'tu-clave-secreta-aqui')
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Registrar los blueprints
app.register_blueprint(admin)
app.register_blueprint(auth)

@app.route('/')
def home():
    """Página principal - Website profesional"""
    return render_template('index.html')

@app.route('/api/health')
def health_check():
    """Health check para Render.com"""
    return jsonify({
        'status': 'healthy',
        'message': 'Cubalink23 Backend is running',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/test')
def test():
    """Endpoint de prueba"""
    return jsonify({
        'message': 'API funcionando correctamente',
        'version': '1.0.0'
    })

if __name__ == '__main__':
    print('🚀 Iniciando CubaLink23 Backend v2.2 - FIXED DEPS...')
    port = int(os.environ.get('PORT', 3005))
    app.run(host='0.0.0.0', port=port, debug=False)
