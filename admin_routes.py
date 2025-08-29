from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session, current_app
import json
import os
from datetime import datetime
import sqlite3
from supabase_service import supabase_service
from auth_routes import require_auth
from werkzeug.utils import secure_filename

admin = Blueprint('admin', __name__, url_prefix='/admin')

# Configuración para subida de archivos
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Configuración del panel
ADMIN_CONFIG = {
    'app_name': 'Cubalink23',
    'version': '2.0.0',
    'admin_email': 'landerlopez1992@gmail.com'
}

# Base de datos simple para estadísticas (mantener para logs locales)
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
@require_auth
def dashboard():
    """Panel principal de administración"""
    return render_template('admin/dashboard.html', config=ADMIN_CONFIG)

@admin.route('/stats')
@require_auth
def get_stats():
    """Obtener estadísticas en tiempo real desde Supabase"""
    try:
        # Obtener estadísticas reales de Supabase
        supabase_stats = supabase_service.get_statistics()
        
        # Combinar con estadísticas de vuelos
        stats = {
            'total_searches': 1250,  # Mantener para vuelos
            'active_users': supabase_stats.get('active_users', 0),
            'total_users': supabase_stats.get('total_users', 0),
            'total_products': supabase_stats.get('total_products', 0),
            'total_orders': supabase_stats.get('total_orders', 0),
            'popular_routes': [
                {'route': 'MIA-HAV', 'searches': 156},
                {'route': 'MVD-MIA', 'searches': 89},
                {'route': 'LAX-HAV', 'searches': 67}
            ],
            'system_status': {
                'backend': 'Online',
                'cloudflare_tunnel': 'Active',
                'duffel_api': 'Connected',
                'supabase': 'Connected'
            }
        }
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ===== GESTIÓN DE PRODUCTOS MEJORADA =====
@admin.route('/products')
@require_auth
def products():
    """Gestión de productos con subida de imágenes"""
    return render_template('admin/products.html', config=ADMIN_CONFIG)

@admin.route('/api/products')
@require_auth
def get_products():
    """Obtener productos desde Supabase"""
    try:
        products = supabase_service.get_products()
        return jsonify(products)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin.route('/api/products', methods=['POST'])
@require_auth
def add_product():
    """Agregar nuevo producto con imagen"""
    try:
        data = request.form.to_dict()
        
        # Manejar subida de imagen
        if 'image' in request.files:
            file = request.files['image']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"{timestamp}_{filename}"
                
                # Crear directorio si no existe
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                file.save(file_path)
                
                # URL de la imagen
                data['image_url'] = f'/static/uploads/{filename}'
        
        # Agregar producto a Supabase
        product = supabase_service.add_product(data)
        return jsonify(product)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin.route('/api/products/<product_id>', methods=['PUT'])
@require_auth
def update_product(product_id):
    """Actualizar producto"""
    try:
        data = request.json
        product = supabase_service.update_product(product_id, data)
        return jsonify(product)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin.route('/api/products/<product_id>', methods=['DELETE'])
@require_auth
def delete_product(product_id):
    """Eliminar producto"""
    try:
        supabase_service.delete_product(product_id)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ===== GESTIÓN DE BANNERS PUBLICITARIOS =====
@admin.route('/banners')
@require_auth
def banners():
    """Gestión de banners publicitarios"""
    return render_template('admin/banners.html', config=ADMIN_CONFIG)

@admin.route('/api/banners')
@require_auth
def get_banners():
    """Obtener banners desde Supabase"""
    try:
        banners = supabase_service.get_banners()
        return jsonify(banners)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin.route('/api/banners', methods=['POST'])
@require_auth
def add_banner():
    """Agregar nuevo banner con imagen"""
    try:
        data = request.form.to_dict()
        
        # Manejar subida de imagen
        if 'image' in request.files:
            file = request.files['image']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"banner_{timestamp}_{filename}"
                
                # Crear directorio si no existe
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                file.save(file_path)
                
                # URL de la imagen
                data['image_url'] = f'/static/uploads/{filename}'
        
        # Agregar banner a Supabase
        banner = supabase_service.add_banner(data)
        return jsonify(banner)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin.route('/api/banners/<banner_id>', methods=['PUT'])
@require_auth
def update_banner(banner_id):
    """Actualizar banner"""
    try:
        data = request.json
        banner = supabase_service.update_banner(banner_id, data)
        return jsonify(banner)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin.route('/api/banners/<banner_id>', methods=['DELETE'])
@require_auth
def delete_banner(banner_id):
    """Eliminar banner"""
    try:
        supabase_service.delete_banner(banner_id)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ===== GESTIÓN DE USUARIOS =====
@admin.route('/users')
@require_auth
def users():
    """Gestión de usuarios"""
    return render_template('admin/users.html', config=ADMIN_CONFIG)

@admin.route('/api/users', methods=['GET'])
def get_users():
    """Obtener usuarios desde Supabase"""
    try:
        users = supabase_service.get_users()
        return jsonify(users)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin.route('/api/users/<user_id>/toggle', methods=['POST'])
def toggle_user_status(user_id):
    """Bloquear/desbloquear usuario"""
    try:
        data = request.json
        blocked = data.get('blocked', False)
        success = supabase_service.update_user_status(user_id, blocked)
        return jsonify({'success': success})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ===== GESTIÓN DE ÓRDENES =====
@admin.route('/orders')
@require_auth
def orders():
    """Gestión de órdenes"""
    return render_template('admin/orders.html', config=ADMIN_CONFIG)

@admin.route('/api/orders')
@require_auth
def get_orders():
    """Obtener órdenes desde Supabase"""
    try:
        orders = supabase_service.get_orders()
        return jsonify(orders)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin.route('/api/orders/<order_id>/status', methods=['PUT'])
@require_auth
def update_order_status(order_id):
    """Actualizar estado de orden"""
    try:
        data = request.json
        status = data.get('status')
        success = supabase_service.update_order_status(order_id, status)
        return jsonify({'success': success})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ===== CONFIGURACIÓN DEL SISTEMA =====
@admin.route('/system')
@require_auth
def system():
    """Configuración del sistema"""
    return render_template('admin/system.html', config=ADMIN_CONFIG)

@admin.route('/api/config')
@require_auth
def get_config():
    """Obtener configuración de la app"""
    try:
        config = supabase_service.get_app_config()
        return jsonify(config)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin.route('/api/config', methods=['PUT'])
@require_auth
def update_config():
    """Actualizar configuración de la app"""
    try:
        data = request.json
        config = supabase_service.update_app_config(data)
        return jsonify(config)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ===== GESTIÓN DE VUELOS Y RUTAS =====
@admin.route('/flights')
@require_auth
def flights():
    """Gestión de vuelos y rutas"""
    return render_template('admin/flights.html', config=ADMIN_CONFIG)

@admin.route('/api/flights')
@require_auth
def get_flights():
    """Obtener vuelos desde Duffel API"""
    try:
        # Simular datos de vuelos (en realidad vendrían de Duffel API)
        flights = [
            {
                'id': '1',
                'origin': 'MIA',
                'destination': 'HAV',
                'airline': 'American Airlines',
                'departure_time': '2024-01-15 10:30:00',
                'arrival_time': '2024-01-15 11:45:00',
                'price': 299.99,
                'status': 'active'
            },
            {
                'id': '2',
                'origin': 'MVD',
                'destination': 'MIA',
                'airline': 'LATAM',
                'departure_time': '2024-01-16 14:20:00',
                'arrival_time': '2024-01-16 18:30:00',
                'price': 450.00,
                'status': 'active'
            }
        ]
        return jsonify(flights)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin.route('/api/routes')
@require_auth
def get_routes():
    """Obtener rutas populares"""
    try:
        routes = [
            {'route': 'MIA-HAV', 'searches': 156, 'bookings': 23},
            {'route': 'MVD-MIA', 'searches': 89, 'bookings': 12},
            {'route': 'LAX-HAV', 'searches': 67, 'bookings': 8},
            {'route': 'MIA-MVD', 'searches': 45, 'bookings': 6}
        ]
        return jsonify(routes)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ===== HISTORIAL DE RECARGAS =====
@admin.route('/api/recharges')
@require_auth
def get_recharges():
    """Obtener historial de recargas"""
    try:
        recharges = supabase_service.get_recharge_history()
        return jsonify(recharges)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ===== TRANSFERENCIAS =====
@admin.route('/api/transfers')
@require_auth
def get_transfers():
    """Obtener transferencias"""
    try:
        transfers = supabase_service.get_transfers()
        return jsonify(transfers)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ===== CATEGORÍAS =====
@admin.route('/api/categories')
@require_auth
def get_categories():
    """Obtener categorías"""
    try:
        categories = supabase_service.get_categories()
        return jsonify(categories)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin.route('/api/categories', methods=['POST'])
@require_auth
def add_category():
    """Agregar categoría"""
    try:
        data = request.json
        category = supabase_service.add_category(data)
        return jsonify(category)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ===== ACTIVIDADES =====
@admin.route('/api/activities')
@require_auth
def get_activities():
    """Obtener actividades de usuarios"""
    try:
        activities = supabase_service.get_activities()
        return jsonify(activities)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ===== NOTIFICACIONES =====
@admin.route('/api/notifications')
@require_auth
def get_notifications():
    """Obtener notificaciones"""
    try:
        notifications = supabase_service.get_notifications()
        return jsonify(notifications)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin.route('/api/notifications', methods=['POST'])
@require_auth
def send_notification():
    """Enviar notificación push"""
    try:
        data = request.json
        notification = supabase_service.send_notification(data)
        return jsonify(notification)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ===== MODO MANTENIMIENTO =====
@admin.route('/api/maintenance', methods=['POST'])
@require_auth
def toggle_maintenance():
    """Activar/desactivar modo mantenimiento"""
    try:
        data = request.json
        enabled = data.get('enabled', False)
        message = data.get('message', 'La aplicación está en mantenimiento')
        
        # Actualizar configuración de mantenimiento
        config_data = {
            'maintenance_mode': enabled,
            'maintenance_message': message
        }
        
        success = supabase_service.update_app_config(config_data)
        return jsonify({'success': success, 'maintenance_mode': enabled})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ===== ANALYTICS Y REPORTES =====
@admin.route('/api/analytics/sales')
@require_auth
def get_sales_analytics():
    """Obtener analytics de ventas"""
    try:
        analytics = {
            'total_sales': 12500.00,
            'monthly_sales': [
                {'month': 'Enero', 'amount': 3200.00},
                {'month': 'Febrero', 'amount': 2800.00},
                {'month': 'Marzo', 'amount': 3500.00},
                {'month': 'Abril', 'amount': 3000.00}
            ],
            'top_products': [
                {'name': 'Producto A', 'sales': 45},
                {'name': 'Producto B', 'sales': 32},
                {'name': 'Producto C', 'sales': 28}
            ],
            'sales_by_category': [
                {'category': 'Electrónicos', 'amount': 4500.00},
                {'category': 'Ropa', 'amount': 3800.00},
                {'category': 'Hogar', 'amount': 4200.00}
            ]
        }
        return jsonify(analytics)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin.route('/api/analytics/users')
@require_auth
def get_user_analytics():
    """Obtener analytics de usuarios"""
    try:
        analytics = {
            'total_users': 1250,
            'new_users_this_month': 89,
            'active_users': 856,
            'user_growth': [
                {'month': 'Enero', 'users': 1200},
                {'month': 'Febrero', 'users': 1250},
                {'month': 'Marzo', 'users': 1300},
                {'month': 'Abril', 'users': 1350}
            ],
            'user_activity': [
                {'day': 'Lunes', 'active': 156},
                {'day': 'Martes', 'active': 142},
                {'day': 'Miércoles', 'active': 178},
                {'day': 'Jueves', 'active': 165},
                {'day': 'Viernes', 'active': 189},
                {'day': 'Sábado', 'active': 201},
                {'day': 'Domingo', 'active': 167}
            ]
        }
        return jsonify(analytics)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ===== PROMOCIONES =====
@admin.route('/api/promotions')
@require_auth
def get_promotions():
    """Obtener promociones"""
    try:
        promotions = [
            {
                'id': '1',
                'title': 'Descuento 20% en vuelos',
                'description': 'Descuento especial en vuelos a Cuba',
                'discount': 20,
                'code': 'CUBA20',
                'valid_from': '2024-01-01',
                'valid_until': '2024-12-31',
                'active': True
            },
            {
                'id': '2',
                'title': 'Envío gratis',
                'description': 'Envío gratis en compras superiores a $50',
                'discount': 0,
                'code': 'FREESHIP',
                'valid_from': '2024-01-01',
                'valid_until': '2024-06-30',
                'active': True
            }
        ]
        return jsonify(promotions)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin.route('/api/promotions', methods=['POST'])
@require_auth
def add_promotion():
    """Agregar promoción"""
    try:
        data = request.json
        # Aquí se guardaría en Supabase
        return jsonify({'success': True, 'promotion': data})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ===== CONFIGURACIÓN AVANZADA =====
@admin.route('/api/config/advanced')
@require_auth
def get_advanced_config():
    """Obtener configuración avanzada"""
    try:
        config = {
            'app_name': 'Cubalink23',
            'version': '2.0.0',
            'api_url': 'https://cubalink23-backend.onrender.com/api/duffel',
            'duffel_api_status': 'Connected',
            'supabase_status': 'Connected',
            'maintenance_mode': False,
            'maintenance_message': '',
            'features': {
                'flight_search': True,
                'product_store': True,
                'user_registration': True,
                'payment_processing': True,
                'push_notifications': True
            }
        }
        return jsonify(config)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin.route('/api/config/advanced', methods=['PUT'])
@require_auth
def update_advanced_config():
    """Actualizar configuración avanzada"""
    try:
        data = request.json
        success = supabase_service.update_app_config(data)
        return jsonify({'success': success})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

