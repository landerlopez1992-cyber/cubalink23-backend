from flask import Blueprint, render_template, request, jsonify, redirect, url_for
import json
import os
from datetime import datetime
import sqlite3

admin = Blueprint('admin', __name__, url_prefix='/admin')

# Configuración del panel
ADMIN_CONFIG = {
    'app_name': 'Cubalink23',
    'version': '1.0.0',
    'admin_email': 'admin@cubalink23.com'
}

# Base de datos simple para estadísticas
def init_db():
    conn = sqlite3.connect('admin_stats.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS stats
                 (id INTEGER PRIMARY KEY, date TEXT, searches INTEGER, 
                  users INTEGER, errors INTEGER)''')
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, user_id TEXT, searches INTEGER,
                  last_seen TEXT, blocked INTEGER DEFAULT 0)''')
    conn.commit()
    conn.close()

@admin.route('/')
def dashboard():
    """Panel principal de administración"""
    return render_template('admin/dashboard.html', config=ADMIN_CONFIG)

@admin.route('/stats')
def get_stats():
    """Obtener estadísticas en tiempo real"""
    try:
        # Simular estadísticas (en producción esto vendría de una base de datos real)
        stats = {
            'total_searches': 1250,
            'active_users': 45,
            'popular_routes': [
                {'route': 'MIA-HAV', 'searches': 156},
                {'route': 'MVD-MIA', 'searches': 89},
                {'route': 'LAX-HAV', 'searches': 67}
            ],
            'system_status': {
                'backend': 'Online',
                'cloudflare_tunnel': 'Active',
                'duffel_api': 'Connected'
            }
        }
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin.route('/users')
def users():
    """Gestión de usuarios"""
    return render_template('admin/users.html', config=ADMIN_CONFIG)

@admin.route('/flights')
def flights():
    """Gestión de vuelos y rutas"""
    return render_template('admin/flights.html', config=ADMIN_CONFIG)

@admin.route('/products')
def products():
    """Gestión de productos"""
    return render_template('admin/products.html', config=ADMIN_CONFIG)

@admin.route('/system')
def system():
    """Configuración del sistema"""
    return render_template('admin/system.html', config=ADMIN_CONFIG)

@admin.route('/api/config', methods=['GET', 'POST'])
def api_config():
    """API para configurar la app Flutter"""
    if request.method == 'POST':
        data = request.json
        # Guardar configuración que afectará la app
        config_file = 'app_config.json'
        with open(config_file, 'w') as f:
            json.dump(data, f)
        return jsonify({'success': True, 'message': 'Configuración actualizada'})
    else:
        # Leer configuración actual
        config_file = 'app_config.json'
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                return jsonify(json.load(f))
        return jsonify({'app_name': 'Cubalink23', 'maintenance_mode': False})

@admin.route('/api/notifications', methods=['POST'])
def send_notification():
    """Enviar notificaciones a usuarios"""
    data = request.json
    # Aquí implementarías el envío de notificaciones push
    return jsonify({'success': True, 'message': 'Notificación enviada'})

@admin.route('/api/maintenance', methods=['POST'])
def toggle_maintenance():
    """Activar/desactivar modo mantenimiento"""
    data = request.json
    maintenance_mode = data.get('maintenance_mode', False)
    
    # Actualizar configuración que la app Flutter leerá
    config = {'maintenance_mode': maintenance_mode}
    with open('app_config.json', 'w') as f:
        json.dump(config, f)
    
    return jsonify({'success': True, 'maintenance_mode': maintenance_mode})

# ==================== PRODUCTOS API ====================

@admin.route('/api/products', methods=['GET'])
def get_products():
    """Obtener todos los productos desde Supabase"""
    try:
        import requests
        
        # Configuración de Supabase
        SUPABASE_URL = 'https://zgqrhzuhrwudckwesybg.supabase.co'
        SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpncXJoenVocnd1ZGNrd2VzeWJnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTU3OTI3OTgsImV4cCI6MjA3MTM2ODc5OH0.lUVK99zmOYD7bNTxilJZWHTmYPfZF5YeMJDVUaJ-FsQ'
        
        headers = {
            'apikey': SUPABASE_KEY,
            'Authorization': f'Bearer {SUPABASE_KEY}',
            'Content-Type': 'application/json'
        }
        
        response = requests.get(
            f'{SUPABASE_URL}/rest/v1/store_products?select=*&order=created_at.desc',
            headers=headers
        )
        
        if response.status_code == 200:
            products = response.json()
            return jsonify({
                'success': True,
                'products': products,
                'total': len(products)
            })
        else:
            return jsonify({
                'success': False,
                'error': f'Error de Supabase: {response.status_code}',
                'products': []
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'products': []
        }), 500

@admin.route('/api/products', methods=['POST'])
def create_product():
    """Crear nuevo producto en Supabase"""
    try:
        import requests
        
        data = request.json
        SUPABASE_URL = 'https://zgqrhzuhrwudckwesybg.supabase.co'
        SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpncXJoenVocnd1ZGNrd2VzeWJnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTU3OTI3OTgsImV4cCI6MjA3MTM2ODc5OH0.lUVK99zmOYD7bNTxilJZWHTmYPfZF5YeMJDVUaJ-FsQ'
        
        headers = {
            'apikey': SUPABASE_KEY,
            'Authorization': f'Bearer {SUPABASE_KEY}',
            'Content-Type': 'application/json'
        }
        
        # Preparar datos del producto
        product_data = {
            'name': data.get('name'),
            'description': data.get('description', ''),
            'price': float(data.get('price', 0)),
            'category': data.get('category'),
            'stock': int(data.get('stock', 0)),
            'is_active': True,
            'image_url': data.get('image_url', '')
        }
        
        response = requests.post(
            f'{SUPABASE_URL}/rest/v1/store_products',
            headers=headers,
            json=product_data
        )
        
        if response.status_code == 201:
            return jsonify({
                'success': True,
                'message': 'Producto creado exitosamente',
                'product': response.json()
            })
        else:
            return jsonify({
                'success': False,
                'error': f'Error de Supabase: {response.status_code} - {response.text}'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@admin.route('/api/products/<product_id>', methods=['PUT'])
def update_product(product_id):
    """Actualizar producto en Supabase"""
    try:
        import requests
        
        data = request.json
        SUPABASE_URL = 'https://zgqrhzuhrwudckwesybg.supabase.co'
        SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpncXJoenVocnd1ZGNrd2VzeWJnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTU3OTI3OTgsImV4cCI6MjA3MTM2ODc5OH0.lUVK99zmOYD7bNTxilJZWHTmYPfZF5YeMJDVUaJ-FsQ'
        
        headers = {
            'apikey': SUPABASE_KEY,
            'Authorization': f'Bearer {SUPABASE_KEY}',
            'Content-Type': 'application/json'
        }
        
        # Preparar datos actualizados
        update_data = {}
        if 'name' in data:
            update_data['name'] = data['name']
        if 'description' in data:
            update_data['description'] = data['description']
        if 'price' in data:
            update_data['price'] = float(data['price'])
        if 'category' in data:
            update_data['category'] = data['category']
        if 'stock' in data:
            update_data['stock'] = int(data['stock'])
        if 'is_active' in data:
            update_data['is_active'] = data['is_active']
        if 'image_url' in data:
            update_data['image_url'] = data['image_url']
        
        response = requests.patch(
            f'{SUPABASE_URL}/rest/v1/store_products?id=eq.{product_id}',
            headers=headers,
            json=update_data
        )
        
        if response.status_code == 200:
            return jsonify({
                'success': True,
                'message': 'Producto actualizado exitosamente'
            })
        else:
            return jsonify({
                'success': False,
                'error': f'Error de Supabase: {response.status_code} - {response.text}'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@admin.route('/api/products/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    """Eliminar producto de Supabase"""
    try:
        import requests
        
        SUPABASE_URL = 'https://zgqrhzuhrwudckwesybg.supabase.co'
        SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpncXJoenVocnd1ZGNrd2VzeWJnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTU3OTI3OTgsImV4cCI6MjA3MTM2ODc5OH0.lUVK99zmOYD7bNTxilJZWHTmYPfZF5YeMJDVUaJ-FsQ'
        
        headers = {
            'apikey': SUPABASE_KEY,
            'Authorization': f'Bearer {SUPABASE_KEY}',
            'Content-Type': 'application/json'
        }
        
        response = requests.delete(
            f'{SUPABASE_URL}/rest/v1/store_products?id=eq.{product_id}',
            headers=headers
        )
        
        if response.status_code == 204:
            return jsonify({
                'success': True,
                'message': 'Producto eliminado exitosamente'
            })
        else:
            return jsonify({
                'success': False,
                'error': f'Error de Supabase: {response.status_code} - {response.text}'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
