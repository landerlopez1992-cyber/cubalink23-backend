from flask import Flask, render_template, jsonify
from flask_cors import CORS
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

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
    port = int(os.environ.get('PORT', 3005))
    app.run(host='0.0.0.0', port=port, debug=False)
