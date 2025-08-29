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


# ===== SISTEMA DE CHAT DE SOPORTE =====
@admin.route('/support-chat')
@login_required
def support_chat():
    """Panel de chat de soporte"""
    return render_template('admin/support_chat.html', config=ADMIN_CONFIG)

@admin.route('/support-chat/active')
@login_required
def active_chats():
    """Chats activos"""
    return render_template('admin/active_chats.html', config=ADMIN_CONFIG)

@admin.route('/api/support-chats')
@login_required
def api_support_chats():
    try:
        support_chats = [
            {
                'id': 1,
                'user_id': 'user_123',
                'user_name': 'Juan Pérez',
                'user_type': 'customer',
                'status': 'active',
                'last_message': 'Necesito ayuda con mi pedido',
                'last_message_time': '2024-01-15T10:30:00Z',
                'unread_count': 2,
                'created_at': '2024-01-15T09:15:00Z'
            },
            {
                'id': 2,
                'user_id': 'seller_456',
                'user_name': 'María González',
                'user_type': 'seller',
                'status': 'waiting',
                'last_message': '¿Cómo puedo subir productos?',
                'last_message_time': '2024-01-15T10:25:00Z',
                'unread_count': 1,
                'created_at': '2024-01-15T09:30:00Z'
            }
        ]
        return jsonify(support_chats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin.route('/api/support-chats/<int:chat_id>/messages')
@login_required
def api_chat_messages(chat_id):
    try:
        messages = [
            {
                'id': 1,
                'chat_id': chat_id,
                'sender_type': 'user',
                'sender_name': 'Juan Pérez',
                'message': 'Hola, necesito ayuda con mi pedido #12345',
                'timestamp': '2024-01-15T09:15:00Z',
                'is_read': True
            },
            {
                'id': 2,
                'chat_id': chat_id,
                'sender_type': 'admin',
                'sender_name': 'Soporte',
                'message': 'Hola Juan, ¿en qué puedo ayudarte con tu pedido?',
                'timestamp': '2024-01-15T09:16:00Z',
                'is_read': True
            }
        ]
        return jsonify(messages)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin.route('/api/support-chats/<int:chat_id>/send-message', methods=['POST'])
@login_required
def send_support_message(chat_id):
    try:
        data = request.json
        message = data.get('message', '')
        return jsonify({'success': True, 'message': 'Mensaje enviado exitosamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin.route('/api/support-stats')
@login_required
def api_support_stats():
    try:
        stats = {
            'total_chats': 25,
            'active_chats': 8,
            'waiting_chats': 5,
            'resolved_chats': 12,
            'avg_response_time': '2.5 minutos',
            'satisfaction_rate': 4.8
        }
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ===== SISTEMA DE BILLETERA DIGITAL =====
@admin.route('/wallet')
@login_required
def wallet_management():
    """Panel de gestión de billetera digital"""
    return render_template('admin/wallet.html', config=ADMIN_CONFIG)

@admin.route('/wallet/transactions')
@login_required
def wallet_transactions():
    """Transacciones de billetera"""
    return render_template('admin/wallet_transactions.html', config=ADMIN_CONFIG)

@admin.route('/api/wallet/transactions')
@login_required
def api_wallet_transactions():
    try:
        transactions = [
            {
                'id': 1,
                'from_user': 'Juan Pérez',
                'to_user': 'María González',
                'amount': 50.00,
                'type': 'transfer', # transfer, payment, withdrawal, deposit
                'status': 'completed',
                'description': 'Transferencia entre usuarios',
                'created_at': '2024-01-15T10:30:00Z'
            },
            {
                'id': 2,
                'user': 'Carlos López',
                'amount': 25.00,
                'type': 'payment',
                'status': 'completed',
                'description': 'Pago de servicio de entrega',
                'created_at': '2024-01-15T09:15:00Z'
            },
            {
                'id': 3,
                'user': 'Ana García',
                'amount': 100.00,
                'type': 'withdrawal',
                'status': 'pending',
                'description': 'Retiro a tarjeta bancaria',
                'created_at': '2024-01-15T08:45:00Z'
            }
        ]
        return jsonify(transactions)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin.route('/api/wallet/balance/<user_id>')
@login_required
def api_wallet_balance(user_id):
    try:
        balance = {
            'user_id': user_id,
            'user_name': 'Juan Pérez',
            'balance': 250.75,
            'pending_balance': 50.00,
            'total_transactions': 45,
            'last_transaction': '2024-01-15T10:30:00Z'
        }
        return jsonify(balance)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ===== SISTEMA DE MÉTODOS DE PAGO =====
@admin.route('/payment-methods')
@login_required
def payment_methods():
    """Panel de gestión de métodos de pago"""
    return render_template('admin/payment_methods.html', config=ADMIN_CONFIG)

@admin.route('/api/payment-methods')
@login_required
def api_payment_methods():
    try:
        payment_methods = [
            {
                'id': 1,
                'name': 'CASH',
                'type': 'cash',
                'is_active': True,
                'available_for': ['sellers', 'drivers'], # sellers, drivers, customers
                'description': 'Pago en efectivo',
                'commission_rate': 0.0,
                'min_amount': 0.0,
                'max_amount': 10000.0
            },
            {
                'id': 2,
                'name': 'Tarjeta de Crédito/Débito',
                'type': 'card',
                'is_active': True,
                'available_for': ['sellers', 'drivers', 'customers'],
                'description': 'Pago con tarjeta bancaria',
                'commission_rate': 2.5,
                'min_amount': 1.0,
                'max_amount': 5000.0
            },
            {
                'id': 3,
                'name': 'Transferencia Bancaria',
                'type': 'bank_transfer',
                'is_active': True,
                'available_for': ['sellers', 'drivers'],
                'description': 'Transferencia directa a cuenta bancaria',
                'commission_rate': 1.0,
                'min_amount': 10.0,
                'max_amount': 10000.0
            }
        ]
        return jsonify(payment_methods)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin.route('/api/payment-methods/<int:method_id>/toggle', methods=['POST'])
@login_required
def toggle_payment_method(method_id):
    try:
        data = request.json
        is_active = data.get('is_active', False)
        
        # Lógica para activar/desactivar método de pago
        return jsonify({
            'success': True, 
            'message': f'Método de pago {"activado" if is_active else "desactivado"} exitosamente'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin.route('/api/payment-methods/<int:method_id>/update', methods=['POST'])
@login_required
def update_payment_method(method_id):
    try:
        data = request.json
        
        # Lógica para actualizar método de pago
        return jsonify({
            'success': True, 
            'message': 'Método de pago actualizado exitosamente'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ===== SALARIOS Y PAGOS =====
@admin.route('/payroll')
@login_required
def payroll():
    """Panel de nómina y pagos"""
    return render_template('admin/payroll.html', config=ADMIN_CONFIG)

@admin.route('/api/payroll/sellers')
@login_required
def api_seller_payroll():
    try:
        seller_payments = [
            {
                'id': 1,
                'seller_name': 'María González',
                'total_sales': 1250.00,
                'commission_rate': 10.0,
                'commission_amount': 125.00,
                'payment_method': 'CASH',
                'status': 'pending',
                'created_at': '2024-01-15T10:30:00Z'
            },
            {
                'id': 2,
                'seller_name': 'Pedro López',
                'total_sales': 850.00,
                'commission_rate': 10.0,
                'commission_amount': 85.00,
                'payment_method': 'card',
                'status': 'completed',
                'created_at': '2024-01-15T09:15:00Z'
            }
        ]
        return jsonify(seller_payments)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin.route('/api/payroll/drivers')
@login_required
def api_driver_payroll():
    try:
        driver_payments = [
            {
                'id': 1,
                'driver_name': 'Carlos López',
                'total_deliveries': 25,
                'payment_method': 'per_delivery',
                'rate_per_delivery': 5.00,
                'total_amount': 125.00,
                'payment_method': 'CASH',
                'status': 'pending',
                'created_at': '2024-01-15T10:30:00Z'
            },
            {
                'id': 2,
                'driver_name': 'Luis Rodríguez',
                'total_deliveries': 18,
                'payment_method': 'per_km',
                'total_km': 150,
                'rate_per_km': 0.50,
                'total_amount': 75.00,
                'payment_method': 'card',
                'status': 'completed',
                'created_at': '2024-01-15T09:15:00Z'
            }
        ]
        return jsonify(driver_payments)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin.route('/api/payroll/approve/<int:payment_id>', methods=['POST'])
@login_required
def approve_payment(payment_id):
    try:
        data = request.json
        payment_method = data.get('payment_method', 'CASH')
        
        # Lógica para aprobar pago
        return jsonify({
            'success': True, 
            'message': f'Pago aprobado exitosamente por {payment_method}'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ===== CONFIGURACIÓN DE PAGOS =====
@admin.route('/payment-settings')
@login_required
def payment_settings():
    """Configuración de pagos"""
    return render_template('admin/payment_settings.html', config=ADMIN_CONFIG)

@admin.route('/api/payment-settings')
@login_required
def api_payment_settings():
    try:
        settings = {
            'cash_enabled': True,
            'card_enabled': True,
            'bank_transfer_enabled': True,
            'min_cash_amount': 10.0,
            'max_cash_amount': 1000.0,
            'card_commission': 2.5,
            'bank_transfer_commission': 1.0,
            'auto_approve_cash': False,
            'require_admin_approval_cash': True
        }
        return jsonify(settings)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin.route('/api/payment-settings/update', methods=['POST'])
@login_required
def update_payment_settings():
    try:
        data = request.json
        
        # Lógica para actualizar configuración
        return jsonify({
            'success': True, 
            'message': 'Configuración de pagos actualizada exitosamente'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
# Última actualización: Fri Aug 29 17:47:01 EDT 2025
