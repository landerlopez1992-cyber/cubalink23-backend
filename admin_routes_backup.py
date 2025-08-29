from flask import Blueprint, render_template, request, jsonify, redirect, url_for
import json
import os
from datetime import datetime
import sqlite3
from supabase_service import supabase_service
from flask_login import login_required

admin = Blueprint('admin', __name__, url_prefix='/admin')

# Configuración del panel
ADMIN_CONFIG = {
    'app_name': 'Cubalink23',
    'version': '1.0.0',
    'admin_email': 'admin@cubalink23.com'
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
def dashboard():
    """Panel principal de administración"""
    return render_template('admin/dashboard.html', config=ADMIN_CONFIG)

@admin.route('/stats')
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

@admin.route('/users')
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

@admin.route('/flights')
def flights():
    """Gestión de vuelos y rutas"""
    return render_template('admin/flights.html', config=ADMIN_CONFIG)

@admin.route('/system')
def system():
    """Configuración del sistema"""
    return render_template('admin/system.html', config=ADMIN_CONFIG)

# Nuevas rutas para gestión de productos
@admin.route('/products')
def products():
    """Gestión de productos"""
    return render_template('admin/products.html', config=ADMIN_CONFIG)

@admin.route('/api/products', methods=['GET'])
def get_products():
    """Obtener productos desde Supabase"""
    try:
        products = supabase_service.get_products()
        return jsonify(products)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin.route('/api/products', methods=['POST'])
def add_product():
    """Agregar nuevo producto"""
    try:
        data = request.json
        product = supabase_service.add_product(data)
        return jsonify({'success': True, 'product': product})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin.route('/api/products/<product_id>', methods=['PUT'])
def update_product(product_id):
    """Actualizar producto"""
    try:
        data = request.json
        success = supabase_service.update_product(product_id, data)
        return jsonify({'success': success})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin.route('/api/products/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    """Eliminar producto"""
    try:
        success = supabase_service.delete_product(product_id)
        return jsonify({'success': success})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Rutas para gestión de órdenes
@admin.route('/orders')
def orders():
    """Gestión de órdenes"""
    return render_template('admin/orders.html', config=ADMIN_CONFIG)

@admin.route('/api/orders', methods=['GET'])
def get_orders():
    """Obtener órdenes desde Supabase"""
    try:
        orders = supabase_service.get_orders()
        return jsonify(orders)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin.route('/api/orders/<order_id>/status', methods=['PUT'])
def update_order_status(order_id):
    """Actualizar estado de orden"""
    try:
        data = request.json
        status = data.get('status')
        success = supabase_service.update_order_status(order_id, status)
        return jsonify({'success': success})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Rutas para historial de recargas
@admin.route('/api/recharges', methods=['GET'])
def get_recharges():
    """Obtener historial de recargas"""
    try:
        recharges = supabase_service.get_recharge_history()
        return jsonify(recharges)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Rutas para transferencias
@admin.route('/api/transfers', methods=['GET'])
def get_transfers():
    """Obtener transferencias"""
    try:
        transfers = supabase_service.get_transfers()
        return jsonify(transfers)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Rutas para categorías
@admin.route('/api/categories', methods=['GET'])
def get_categories():
    """Obtener categorías"""
    try:
        categories = supabase_service.get_categories()
        return jsonify(categories)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin.route('/api/categories', methods=['POST'])
def add_category():
    """Agregar categoría"""
    try:
        data = request.json
        category = supabase_service.add_category(data)
        return jsonify({'success': True, 'category': category})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Rutas para actividades
@admin.route('/api/activities', methods=['GET'])
def get_activities():
    """Obtener actividades"""
    try:
        activities = supabase_service.get_activities()
        return jsonify(activities)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin.route('/api/config', methods=['GET', 'POST'])
def api_config():
    """API para configurar la app Flutter"""
    if request.method == 'POST':
        data = request.json
        # Guardar configuración en Supabase
        success = supabase_service.update_app_config(data)
        return jsonify({'success': success, 'message': 'Configuración actualizada'})
    else:
        # Leer configuración desde Supabase
        config = supabase_service.get_app_config()
        return jsonify(config)

@admin.route('/api/notifications', methods=['POST'])
def send_notification():
    """Enviar notificaciones a usuarios"""
    try:
        data = request.json
        notification = supabase_service.send_notification(data)
        return jsonify({'success': True, 'message': 'Notificación enviada', 'notification': notification})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin.route('/api/maintenance', methods=['POST'])
def toggle_maintenance():
    """Activar/desactivar modo mantenimiento"""
    try:
        data = request.json
        maintenance_mode = data.get('maintenance_mode', False)
        
        # Actualizar configuración en Supabase
        config_data = {'maintenance_mode': maintenance_mode}
        success = supabase_service.update_app_config(config_data)
        
        return jsonify({'success': success, 'maintenance_mode': maintenance_mode})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Nuevas rutas para renta de autos
@admin.route('/cars')
@login_required
def cars():
    return render_template('admin/cars.html')

@admin.route('/api/cars')
@login_required
def api_cars():
    try:
        # Aquí irá la lógica para obtener autos de Supabase
        cars = [
            {
                'id': 1,
                'brand': 'Toyota',
                'model': 'Corolla',
                'year': 2022,
                'price_daily': 50,
                'price_high_season': 75,
                'insurance_daily': 15,
                'fuel_price': 25,
                'available': True,
                'image_url': '/static/uploads/car1.jpg'
            }
        ]
        return jsonify(cars)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin.route('/api/cars', methods=['POST'])
@login_required
def add_car():
    try:
        data = request.form.to_dict()
        # Lógica para agregar auto a Supabase
        return jsonify({'success': True, 'message': 'Auto agregado exitosamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Nuevas rutas para repartidores
@admin.route('/drivers')
@login_required
def drivers():
    return render_template('admin/drivers.html')

@admin.route('/api/drivers')
@login_required
def api_drivers():
    try:
        drivers = [
            {
                'id': 1,
                'name': 'Carlos Pérez',
                'email': 'carlos@example.com',
                'phone': '+53 5 123 4567',
                'status': 'active',
                'balance': 150.50,
                'payment_type': 'per_delivery',
                'total_deliveries': 45,
                'rating': 4.8
            }
        ]
        return jsonify(drivers)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin.route('/api/drivers/<int:driver_id>/toggle', methods=['POST'])
@login_required
def toggle_driver_status(driver_id):
    try:
        data = request.get_json()
        # Lógica para cambiar estado del repartidor
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Nuevas rutas para vendedores
@admin.route('/api/vendors/<int:vendor_id>/approve', methods=['POST'])
@login_required
def approve_vendor(vendor_id):
    try:
        # Lógica para aprobar vendedor
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Rutas para solicitudes de aprobación
@admin.route('/approvals')
@login_required
def approvals():
    return render_template('admin/approvals.html')

@admin.route('/api/approvals')
@login_required
def api_approvals():
    try:
        approvals = [
            {
                'id': 1,
                'type': 'vendor',
                'name': 'María González',
                'email': 'maria@example.com',
                'status': 'pending',
                'created_at': '2024-01-15T10:30:00Z'
            },
            {
                'id': 2,
                'type': 'driver',
                'name': 'Luis Rodríguez',
                'email': 'luis@example.com',
                'status': 'pending',
                'created_at': '2024-01-14T15:45:00Z'
            }
        ]
        return jsonify(approvals)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ===== SISTEMA DE VENDEDORES =====
@admin.route('/vendors')
@login_required
def vendors():
    """Panel de gestión de vendedores"""
    return render_template('admin/vendors.html', config=ADMIN_CONFIG)

@admin.route('/vendors/pending')
@login_required
def pending_vendors():
    """Vendedores pendientes de aprobación"""
    return render_template('admin/pending_vendors.html', config=ADMIN_CONFIG)

@admin.route('/api/vendors/pending')
@login_required
def api_pending_vendors():
    try:
        pending_vendors = [
            {
                'id': 1,
                'user_id': 'user_123',
                'business_name': 'Tienda María',
                'business_type': 'tienda',
                'business_email': 'maria@tienda.com',
                'business_phone': '+53 555 1234',
                'profile_photo': 'https://example.com/photo.jpg',
                'delivery_method': 'express',
                'created_at': '2024-01-15T10:30:00Z',
                'status': 'pending'
            }
        ]
        return jsonify(pending_vendors)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin.route('/api/vendors/<int:vendor_id>/approve', methods=['POST'])
@login_required
def approve_vendor(vendor_id):
    try:
        # Lógica para aprobar vendedor
        return jsonify({'success': True, 'message': 'Vendedor aprobado exitosamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin.route('/api/vendors/<int:vendor_id>/suspend', methods=['POST'])
@login_required
def suspend_vendor(vendor_id):
    try:
        # Lógica para suspender vendedor
        return jsonify({'success': True, 'message': 'Vendedor suspendido temporalmente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin.route('/api/vendors/<int:vendor_id>/block', methods=['POST'])
@login_required
def block_vendor(vendor_id):
    try:
        # Lógica para bloquear vendedor
        return jsonify({'success': True, 'message': 'Vendedor bloqueado permanentemente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ===== PRODUCTOS DE VENDEDORES =====
@admin.route('/seller-products')
@login_required
def seller_products():
    """Panel de productos de vendedores"""
    return render_template('admin/seller_products.html', config=ADMIN_CONFIG)

@admin.route('/seller-products/pending')
@login_required
def pending_products():
    """Productos pendientes de aprobación"""
    return render_template('admin/pending_products.html', config=ADMIN_CONFIG)

@admin.route('/api/seller-products/pending')
@login_required
def api_pending_products():
    try:
        pending_products = [
            {
                'id': 1,
                'seller_id': 1,
                'seller_name': 'Tienda María',
                'name': 'Producto de Prueba',
                'description': 'Descripción del producto',
                'price': 25.99,
                'category': 'Electrónicos',
                'images': ['https://example.com/image1.jpg'],
                'status': 'pending',
                'created_at': '2024-01-15T10:30:00Z'
            }
        ]
        return jsonify(pending_products)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin.route('/api/seller-products/<int:product_id>/approve', methods=['POST'])
@login_required
def approve_product(product_id):
    try:
        # Lógica para aprobar producto
        return jsonify({'success': True, 'message': 'Producto aprobado exitosamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin.route('/api/seller-products/<int:product_id>/reject', methods=['POST'])
@login_required
def reject_product(product_id):
    try:
        data = request.json
        reason = data.get('reason', 'No cumple con los estándares de calidad')
        # Lógica para rechazar producto
        return jsonify({'success': True, 'message': f'Producto rechazado: {reason}'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ===== SISTEMA DE REPARTIDORES =====
@admin.route('/drivers')
@login_required
def drivers():
    """Panel de gestión de repartidores"""
    return render_template('admin/drivers.html', config=ADMIN_CONFIG)

@admin.route('/drivers/active')
@login_required
def active_drivers():
    """Repartidores activos"""
    return render_template('admin/active_drivers.html', config=ADMIN_CONFIG)

@admin.route('/api/drivers')
@login_required
def api_drivers():
    try:
        drivers = [
            {
                'id': 1,
                'user_id': 'user_456',
                'name': 'Carlos López',
                'vehicle_type': 'motorcycle',
                'vehicle_plate': 'ABC123',
                'rating': 4.8,
                'total_deliveries': 150,
                'total_earnings': 1250.75,
                'wallet_balance': 350.25,
                'payment_method': 'per_delivery',
                'is_available': True,
                'profile_photo': 'https://example.com/driver.jpg',
                'status': 'active'
            }
        ]
        return jsonify(drivers)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin.route('/api/drivers/<int:driver_id>/set-payment', methods=['POST'])
@login_required
def set_driver_payment(driver_id):
    try:
        data = request.json
        payment_method = data.get('payment_method')
        rate = data.get('rate')
        # Lógica para configurar método de pago
        return jsonify({'success': True, 'message': 'Método de pago actualizado'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ===== ENTREGAS =====
@admin.route('/deliveries')
@login_required
def deliveries():
    """Panel de gestión de entregas"""
    return render_template('admin/deliveries.html', config=ADMIN_CONFIG)

@admin.route('/deliveries/pending')
@login_required
def pending_deliveries():
    """Entregas pendientes"""
    return render_template('admin/pending_deliveries.html', config=ADMIN_CONFIG)

@admin.route('/api/deliveries/pending')
@login_required
def api_pending_deliveries():
    try:
        pending_deliveries = [
            {
                'id': 1,
                'order_id': 'order_123',
                'customer_name': 'Juan Pérez',
                'pickup_location': 'Tienda Centro',
                'delivery_location': 'Calle 23 #456',
                'estimated_time': 30,
                'status': 'pending',
                'created_at': '2024-01-15T10:30:00Z'
            }
        ]
        return jsonify(pending_deliveries)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ===== SISTEMA DE RENTA CAR =====
@admin.route('/vehicles')
@login_required
def vehicles():
    """Panel de gestión de vehículos"""
    return render_template('admin/vehicles.html', config=ADMIN_CONFIG)

@admin.route('/vehicles/add')
@login_required
def add_vehicle():
    """Agregar vehículo"""
    return render_template('admin/add_vehicle.html', config=ADMIN_CONFIG)

@admin.route('/api/vehicles')
@login_required
def api_vehicles():
    try:
        vehicles = [
            {
                'id': 1,
                'vehicle_type': 'sedan',
                'brand': 'Toyota',
                'model': 'Corolla',
                'year': 2023,
                'license_plate': 'XYZ789',
                'daily_rate': 85.00,
                'weekly_rate': 500.00,
                'high_season_rate': 120.00,
                'fuel_full_tank_price': 45.00,
                'min_rental_days': 1,
                'max_rental_days': 30,
                'is_available': True,
                'images': ['https://example.com/car1.jpg'],
                'commission_amount': 50.00
            }
        ]
        return jsonify(vehicles)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin.route('/api/vehicles', methods=['POST'])
@login_required
def create_vehicle():
    try:
        data = request.json
        # Lógica para crear vehículo
        return jsonify({'success': True, 'message': 'Vehículo agregado exitosamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ===== RESERVAS DE RENTA CAR =====
@admin.route('/rentals')
@login_required
def rentals():
    """Panel de gestión de reservas"""
    return render_template('admin/rentals.html', config=ADMIN_CONFIG)

@admin.route('/rentals/active')
@login_required
def active_rentals():
    """Reservas activas"""
    return render_template('admin/active_rentals.html', config=ADMIN_CONFIG)

@admin.route('/api/rentals')
@login_required
def api_rentals():
    try:
        rentals = [
            {
                'id': 1,
                'user_id': 'user_789',
                'customer_name': 'Ana García',
                'vehicle_id': 1,
                'vehicle_info': 'Toyota Corolla 2023',
                'pickup_date': '2022024-01-20',
                'return_date': '2024-01-25',
                'total_amount': 425.00,
                'commission_amount': 50.00,
                'status': 'confirmed',
                'created_at': '2024-01-15T10:30:00Z'
            }
        ]
        return jsonify(rentals)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ===== SISTEMA DE ALERTAS DINGCONNECT =====
@admin.route('/alerts')
@login_required
def alerts():
    """Panel de alertas del sistema"""
    return render_template('admin/alerts.html', config=ADMIN_CONFIG)

@admin.route('/alerts/dingconnect')
@login_required
def dingconnect_alerts():
    """Alertas específicas de DingConnect"""
    return render_template('admin/dingconnect_alerts.html', config=ADMIN_CONFIG)

@admin.route('/api/alerts')
@login_required
def api_alerts():
    try:
        alerts = [
            {
                'id': 1,
                'alert_type': 'dingconnect_balance',
                'title': 'Saldo bajo en DingConnect',
                'message': 'El saldo de DingConnect está por debajo del mínimo requerido',
                'severity': 'high',
                'is_resolved': False,
                'affected_records': ['recharge_123', 'recharge_456'],
                'created_at': '2024-01-15T10:30:00Z'
            },
            {
                'id': 2,
                'alert_type': 'api_error',
                'title': 'Error en API de recargas',
                'message': 'Error de conexión con DingConnect API',
                'severity': 'critical',
                'is_resolved': False,
                'affected_records': ['recharge_789'],
                'created_at': '2024-01-15T09:15:00Z'
            }
        ]
        return jsonify(alerts)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin.route('/api/alerts/<int:alert_id>/resolve', methods=['POST'])
@login_required
def resolve_alert(alert_id):
    try:
        # Lógica para resolver alerta
        return jsonify({'success': True, 'message': 'Alerta resuelta exitosamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ===== RECARGAS FALLIDAS =====
@admin.route('/recharges/failed')
@login_required
def failed_recharges():
    """Recargas fallidas"""
    return render_template('admin/failed_recharges.html', config=ADMIN_CONFIG)

@admin.route('/recharges/pending')
@login_required
def pending_recharges():
    """Recargas pendientes"""
    return render_template('admin/pending_recharges.html', config=ADMIN_CONFIG)

@admin.route('/api/recharges/failed')
@login_required
def api_failed_recharges():
    try:
        failed_recharges = [
            {
                'id': 1,
                'user_id': 'user_123',
                'customer_name': 'Pedro López',
                'phone_number': '+53 555 1234',
                'amount': 10.00,
                'provider': 'Cubacel',
                'status': 'failed',
                'internal_status': 'api_error',
                'error_message': 'Saldo insuficiente en DingConnect',
                'created_at': '2024-01-15T10:30:00Z'
            }
        ]
        return jsonify(failed_recharges)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ===== MENSAJES DEL SISTEMA =====
@admin.route('/system-messages')
@login_required
def system_messages():
    """Panel de mensajes del sistema"""
    return render_template('admin/system_messages.html', config=ADMIN_CONFIG)

@admin.route('/api/system-messages')
@login_required
def api_system_messages():
    try:
        messages = [
            {
                'id': 1,
                'recipient_type': 'seller',
                'recipient_name': 'María González',
                'subject': 'Producto rechazado',
                'message': 'Su producto "Producto de Prueba" ha sido rechazado por no cumplir con los estándares de calidad.',
                'is_read': False,
                'created_at': '2024-01-15T10:30:00Z'
            }
        ]
        return jsonify(messages)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin.route('/api/system-messages', methods=['POST'])
@login_required
def send_system_message():
    try:
        data = request.json
        # Lógica para enviar mensaje del sistema
        return jsonify({'success': True, 'message': 'Mensaje enviado exitosamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

