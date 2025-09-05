from flask import Blueprint, render_template, request, jsonify, redirect, url_for
import json
import os
from datetime import datetime
import sqlite3
import base64
import uuid

# Importar sistema mejorado de upload de imágenes
try:
    from improved_image_upload import ImprovedImageUploader
    IMAGE_UPLOADER = ImprovedImageUploader()
    IMPROVED_UPLOAD_AVAILABLE = True
    print("✅ Sistema mejorado de upload de imágenes disponible")
except ImportError:
    IMAGE_UPLOADER = None
    IMPROVED_UPLOAD_AVAILABLE = False
    print("⚠️ Sistema mejorado de upload no disponible - usando método básico")

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

@admin.route('/orders')
def orders():
    """Gestión de órdenes"""
    return render_template('admin/orders.html', config=ADMIN_CONFIG)

@admin.route('/banners')
def banners():
    """Gestión de banners"""
    return render_template('admin/banners.html', config=ADMIN_CONFIG)

@admin.route('/vendors')
def vendors():
    """Gestión de vendedores"""
    return render_template('admin/vendors.html', config=ADMIN_CONFIG)

@admin.route('/drivers')
def drivers():
    """Gestión de repartidores"""
    return render_template('admin/drivers.html', config=ADMIN_CONFIG)

@admin.route('/vehicles')
def vehicles():
    """Gestión de vehículos"""
    return render_template('admin/vehicles.html', config=ADMIN_CONFIG)

@admin.route('/support-chat')
def support_chat():
    """Chat de soporte"""
    return render_template('admin/support_chat.html', config=ADMIN_CONFIG)

@admin.route('/alerts')
def alerts():
    """Gestión de alertas"""
    return render_template('admin/alerts.html', config=ADMIN_CONFIG)

@admin.route('/wallet')
def wallet():
    """Gestión de billetera"""
    return render_template('admin/wallet.html', config=ADMIN_CONFIG)

@admin.route('/payment-methods')
def payment_methods():
    """Métodos de pago"""
    return render_template('admin/payment_methods.html', config=ADMIN_CONFIG)

@admin.route('/payroll')
def payroll():
    """Gestión de nómina"""
    return render_template('admin/payroll.html', config=ADMIN_CONFIG)

@admin.route('/system-rules')
def system_rules():
    """Reglas del sistema"""
    return render_template('admin/system_rules.html', config=ADMIN_CONFIG)

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
        
        # Verificar que tenemos datos JSON válidos
        if not request.is_json:
            return jsonify({
                'success': False,
                'error': 'Content-Type debe ser application/json'
            }), 400
            
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'No se recibieron datos JSON'
            }), 400
        
        SUPABASE_URL = 'https://zgqrhzuhrwudckwesybg.supabase.co'
        SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpncXJoenVocnd1ZGNrd2VzeWJnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTU3OTI3OTgsImV4cCI6MjA3MTM2ODc5OH0.lUVK99zmOYD7bNTxilJZWHTmYPfZF5YeMJDVUaJ-FsQ'
        
        headers = {
            'apikey': SUPABASE_KEY,
            'Authorization': f'Bearer {SUPABASE_KEY}',
            'Content-Type': 'application/json'
        }
        
        # Manejar imagen del producto
        image_url = data.get('image_url', '')
        if data.get('image_base64'):
            # Si hay imagen en base64, subirla a Supabase Storage
            image_url = upload_image_to_supabase(data.get('image_base64'), data.get('name', 'product'))
        
        # Preparar datos del producto - SOLO campos que existen en Supabase
        product_data = {
            'name': data.get('name'),
            'description': data.get('description', ''),
            'price': float(data.get('price', 0)),
            'category': data.get('category'),
            'subcategory': data.get('subcategory', ''),
            'stock': int(data.get('stock', 0)),
            'weight': data.get('weight'),
            'shipping_cost': float(data.get('shipping_cost', 0)) if data.get('shipping_cost') else 0,
            'vendor_id': data.get('vendor_id', 'admin'),
            'shipping_methods': data.get('shipping_methods', []),
            'tags': data.get('tags', []),
            'is_active': True,
            'image_url': image_url
        }
        
        # Validar datos requeridos
        if not product_data['name'] or not product_data['category']:
            return jsonify({
                'success': False,
                'error': 'Nombre y categoría son requeridos'
            }), 400
        
        response = requests.post(
            f'{SUPABASE_URL}/rest/v1/store_products',
            headers=headers,
            json=product_data
        )
        
        print(f"🔍 Supabase Response Status: {response.status_code}")
        print(f"🔍 Supabase Response Text: {response.text}")
        
        if response.status_code == 201:
            try:
                product_response = response.json()
                return jsonify({
                    'success': True,
                    'message': 'Producto creado exitosamente',
                    'product': product_response
                })
            except Exception as e:
                return jsonify({
                    'success': True,
                    'message': 'Producto creado exitosamente',
                    'product': {'id': 'created'}
                })
        else:
            return jsonify({
                'success': False,
                'error': f'Error de Supabase: {response.status_code} - {response.text}'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error interno: {str(e)}'
        }), 500

def upload_image_to_supabase(image_base64, product_name):
    """Subir imagen a Supabase Storage con sistema mejorado o básico"""
    
    # Usar sistema mejorado si está disponible
    if IMPROVED_UPLOAD_AVAILABLE and IMAGE_UPLOADER:
        try:
            print("📸 Usando sistema mejorado de upload...")
            return IMAGE_UPLOADER.upload_image_to_supabase(image_base64, product_name)
        except Exception as e:
            print(f"⚠️ Error en sistema mejorado, usando método básico: {e}")
    
    # Fallback al método básico
    print("📸 Usando método básico de upload...")
    try:
        import requests
        
        # Configuración de Supabase
        SUPABASE_URL = 'https://zgqrhzuhrwudckwesybg.supabase.co'
        SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpncXJoenVocnd1ZGNrd2VzeWJnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTU3OTI3OTgsImV4cCI6MjA3MTM2ODc5OH0.lUVK99zmOYD7bNTxilJZWHTmYPfZF5YeMJDVUaJ-FsQ'
        
        # Generar nombre único para la imagen
        image_id = str(uuid.uuid4())
        filename = f"{product_name.replace(' ', '_')}_{image_id}.jpg"
        
        # Decodificar imagen base64
        image_data = base64.b64decode(image_base64.split(',')[1])
        
        # Determinar el tipo MIME correcto
        mime_type = 'image/jpeg'  # Por defecto
        if 'data:image/png' in image_base64:
            mime_type = 'image/png'
        elif 'data:image/gif' in image_base64:
            mime_type = 'image/gif'
        elif 'data:image/webp' in image_base64:
            mime_type = 'image/webp'
        
        headers = {
            'apikey': SUPABASE_KEY,
            'Authorization': f'Bearer {SUPABASE_KEY}',
            'Content-Type': mime_type,
        }
        
        # Intentar diferentes buckets en orden de prioridad
        buckets_to_try = ['product-images', 'images', 'public']
        
        for bucket_name in buckets_to_try:
            print(f"🔍 Intentando subir a bucket: {bucket_name}")
            print(f"📸 MIME Type: {mime_type}")
            print(f"📁 Filename: {filename}")
            
            response = requests.post(
                f'{SUPABASE_URL}/storage/v1/object/{bucket_name}/{filename}',
                headers=headers,
                data=image_data
            )
            
            print(f"📡 Response Status: {response.status_code}")
            print(f"📊 Response Text: {response.text}")
            
            if response.status_code == 200:
                # Retornar URL pública de la imagen
                public_url = f'{SUPABASE_URL}/storage/v1/object/public/{bucket_name}/{filename}'
                print(f"✅ Imagen subida exitosamente a {bucket_name}: {public_url}")
                return public_url
            elif response.status_code == 404 and "bucket not found" in response.text.lower():
                print(f"⚠️ Bucket {bucket_name} no existe, probando siguiente...")
                continue
            else:
                print(f"❌ Error en bucket {bucket_name}: {response.status_code} - {response.text}")
                continue
        
        # Si todos los buckets fallan, usar placeholder
        print("❌ Todos los buckets fallaron, usando placeholder")
        return f'https://via.placeholder.com/400x300/007bff/ffffff?text={filename.replace("_", "%20")}'
            
    except Exception as e:
        print(f"Error en upload_image_to_supabase: {e}")
        return ''

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
        
        # Manejar imagen del producto
        if data.get('image_base64'):
            # Si hay imagen en base64, subirla a Supabase Storage
            image_url = upload_image_to_supabase(data.get('image_base64'), data.get('name', 'product'))
            if image_url:
                data['image_url'] = image_url
        
        # Preparar datos actualizados con nuevas funcionalidades
        update_data = {}
        if 'name' in data:
            update_data['name'] = data['name']
        if 'description' in data:
            update_data['description'] = data['description']
        if 'price' in data:
            update_data['price'] = float(data['price'])
        if 'category' in data:
            update_data['category'] = data['category']
        if 'subcategory' in data:
            update_data['subcategory'] = data['subcategory']
        if 'stock' in data:
            update_data['stock'] = int(data['stock'])
        if 'weight' in data:
            update_data['weight'] = data['weight']
        if 'shipping_cost' in data:
            update_data['shipping_cost'] = float(data['shipping_cost']) if data['shipping_cost'] else 0
        if 'vendor_id' in data:
            update_data['vendor_id'] = data['vendor_id']
        if 'shipping_methods' in data:
            update_data['shipping_methods'] = data['shipping_methods']
        if 'tags' in data:
            update_data['tags'] = data['tags']
        if 'is_active' in data:
            update_data['is_active'] = data['is_active']
        if 'image_url' in data:
            update_data['image_url'] = data['image_url']
        
        response = requests.patch(
            f'{SUPABASE_URL}/rest/v1/store_products?id=eq.{product_id}',
            headers=headers,
            json=update_data
        )
        
        print(f"🔍 Update Response Status: {response.status_code}")
        print(f"🔍 Update Response Text: {response.text}")
        
        # Supabase devuelve 204 para actualizaciones exitosas
        if response.status_code in [200, 204]:
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
