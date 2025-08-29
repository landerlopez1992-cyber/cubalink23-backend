import requests
import json
import os
from datetime import datetime
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class SupabaseService:
    def __init__(self):
        # Configuración de Supabase desde variables de entorno
        self.supabase_url = os.getenv('SUPABASE_URL', 'https://your-project.supabase.co')
        self.supabase_key = os.getenv('SUPABASE_ANON_KEY', 'your-anon-key')
        self.supabase_service_key = os.getenv('SUPABASE_SERVICE_KEY', 'your-service-key')
        
        self.headers = {
            'apikey': self.supabase_service_key,
            'Authorization': f'Bearer {self.supabase_service_key}',
            'Content-Type': 'application/json'
        }
    
    def get_users(self):
        """Obtener todos los usuarios"""
        try:
            response = requests.get(
                f'{self.supabase_url}/rest/v1/users',
                headers=self.headers
            )
            return response.json() if response.status_code == 200 else []
        except Exception as e:
            print(f"Error getting users: {e}")
            return []
    
    def get_user_by_id(self, user_id):
        """Obtener usuario específico"""
        try:
            response = requests.get(
                f'{self.supabase_url}/rest/v1/users?id=eq.{user_id}',
                headers=self.headers
            )
            return response.json()[0] if response.status_code == 200 and response.json() else None
        except Exception as e:
            print(f"Error getting user: {e}")
            return None
    
    def update_user_status(self, user_id, blocked):
        """Bloquear/desbloquear usuario"""
        try:
            data = {'blocked': blocked}
            response = requests.patch(
                f'{self.supabase_url}/rest/v1/users?id=eq.{user_id}',
                headers=self.headers,
                json=data
            )
            return response.status_code == 204
        except Exception as e:
            print(f"Error updating user status: {e}")
            return False
    
    def get_products(self):
        """Obtener productos con imágenes"""
        try:
            response = requests.get(f'{self.supabase_url}/rest/v1/products?select=*', headers=self.headers)
            if response.status_code == 200:
                return response.json()
            else:
                return []
        except Exception as e:
            print(f"Error getting products: {e}")
            return []
    
    def add_product(self, data):
        """Agregar producto con imagen"""
        try:
            product_data = {
                'name': data.get('name', ''),
                'description': data.get('description', ''),
                'price': float(data.get('price', 0)),
                'category': data.get('category', ''),
                'image_url': data.get('image_url', ''),
                'stock': int(data.get('stock', 0)),
                'active': data.get('active', True),
                'created_at': datetime.now().isoformat()
            }
            
            response = requests.post(
                f'{self.supabase_url}/rest/v1/products',
                headers=self.headers,
                json=product_data
            )
            
            if response.status_code == 201:
                return response.json()
            else:
                raise Exception(f"Error adding product: {response.text}")
        except Exception as e:
            print(f"Error adding product: {e}")
            raise e
    
    def update_product(self, product_id, data):
        """Actualizar producto"""
        try:
            response = requests.patch(
                f'{self.supabase_url}/rest/v1/products?id=eq.{product_id}',
                headers=self.headers,
                json=data
            )
            
            if response.status_code == 204:
                return {'success': True}
            else:
                raise Exception(f"Error updating product: {response.text}")
        except Exception as e:
            print(f"Error updating product: {e}")
            raise e
    
    def delete_product(self, product_id):
        """Eliminar producto"""
        try:
            response = requests.delete(
                f'{self.supabase_url}/rest/v1/products?id=eq.{product_id}',
                headers=self.headers
            )
            
            if response.status_code == 204:
                return True
            else:
                raise Exception(f"Error deleting product: {response.text}")
        except Exception as e:
            print(f"Error deleting product: {e}")
            raise e

    # ===== GESTIÓN DE BANNERS PUBLICITARIOS =====
    def get_banners(self):
        """Obtener banners publicitarios"""
        try:
            response = requests.get(f'{self.supabase_url}/rest/v1/banners?select=*', headers=self.headers)
            if response.status_code == 200:
                return response.json()
            else:
                return []
        except Exception as e:
            print(f"Error getting banners: {e}")
            return []
    
    def add_banner(self, data):
        """Agregar banner con imagen"""
        try:
            banner_data = {
                'title': data.get('title', ''),
                'description': data.get('description', ''),
                'image_url': data.get('image_url', ''),
                'banner_type': data.get('banner_type', 'welcome'),  # 'welcome' o 'flights'
                'active': data.get('active', True),
                'order': int(data.get('order', 0)),
                'created_at': datetime.now().isoformat()
            }
            
            response = requests.post(
                f'{self.supabase_url}/rest/v1/banners',
                headers=self.headers,
                json=banner_data
            )
            
            if response.status_code == 201:
                return response.json()
            else:
                raise Exception(f"Error adding banner: {response.text}")
        except Exception as e:
            print(f"Error adding banner: {e}")
            raise e
    
    def update_banner(self, banner_id, data):
        """Actualizar banner"""
        try:
            response = requests.patch(
                f'{self.supabase_url}/rest/v1/banners?id=eq.{banner_id}',
                headers=self.headers,
                json=data
            )
            
            if response.status_code == 204:
                return {'success': True}
            else:
                raise Exception(f"Error updating banner: {response.text}")
        except Exception as e:
            print(f"Error updating banner: {e}")
            raise e
    
    def delete_banner(self, banner_id):
        """Eliminar banner"""
        try:
            response = requests.delete(
                f'{self.supabase_url}/rest/v1/banners?id=eq.{banner_id}',
                headers=self.headers
            )
            
            if response.status_code == 204:
                return True
            else:
                raise Exception(f"Error deleting banner: {response.text}")
        except Exception as e:
            print(f"Error deleting banner: {e}")
            raise e
    
    def get_orders(self):
        """Obtener todas las órdenes"""
        try:
            response = requests.get(
                f'{self.supabase_url}/rest/v1/orders',
                headers=self.headers
            )
            return response.json() if response.status_code == 200 else []
        except Exception as e:
            print(f"Error getting orders: {e}")
            return []
    
    def update_order_status(self, order_id, status):
        """Actualizar estado de orden"""
        try:
            data = {'status': status, 'updated_at': datetime.now().isoformat()}
            response = requests.patch(
                f'{self.supabase_url}/rest/v1/orders?id=eq.{order_id}',
                headers=self.headers,
                json=data
            )
            return response.status_code == 204
        except Exception as e:
            print(f"Error updating order status: {e}")
            return False
    
    def get_recharge_history(self):
        """Obtener historial de recargas"""
        try:
            response = requests.get(
                f'{self.supabase_url}/rest/v1/recharge_history',
                headers=self.headers
            )
            return response.json() if response.status_code == 200 else []
        except Exception as e:
            print(f"Error getting recharge history: {e}")
            return []
    
    def get_transfers(self):
        """Obtener transferencias"""
        try:
            response = requests.get(
                f'{self.supabase_url}/rest/v1/transfers',
                headers=self.headers
            )
            return response.json() if response.status_code == 200 else []
        except Exception as e:
            print(f"Error getting transfers: {e}")
            return []
    
    def get_categories(self):
        """Obtener categorías"""
        try:
            response = requests.get(
                f'{self.supabase_url}/rest/v1/store_categories',
                headers=self.headers
            )
            return response.json() if response.status_code == 200 else []
        except Exception as e:
            print(f"Error getting categories: {e}")
            return []
    
    def add_category(self, category_data):
        """Agregar categoría"""
        try:
            response = requests.post(
                f'{self.supabase_url}/rest/v1/store_categories',
                headers=self.headers,
                json=category_data
            )
            return response.json() if response.status_code == 201 else None
        except Exception as e:
            print(f"Error adding category: {e}")
            return None
    
    def get_activities(self):
        """Obtener actividades de usuarios"""
        try:
            response = requests.get(
                f'{self.supabase_url}/rest/v1/activities',
                headers=self.headers
            )
            return response.json() if response.status_code == 200 else []
        except Exception as e:
            print(f"Error getting activities: {e}")
            return []
    
    def get_notifications(self):
        """Obtener notificaciones"""
        try:
            response = requests.get(
                f'{self.supabase_url}/rest/v1/notifications',
                headers=self.headers
            )
            return response.json() if response.status_code == 200 else []
        except Exception as e:
            print(f"Error getting notifications: {e}")
            return []
    
    def send_notification(self, notification_data):
        """Enviar notificación"""
        try:
            response = requests.post(
                f'{self.supabase_url}/rest/v1/notifications',
                headers=self.headers,
                json=notification_data
            )
            return response.json() if response.status_code == 201 else None
        except Exception as e:
            print(f"Error sending notification: {e}")
            return None
    
    def get_app_config(self):
        """Obtener configuración de la app"""
        try:
            response = requests.get(
                f'{self.supabase_url}/rest/v1/app_config',
                headers=self.headers
            )
            return response.json()[0] if response.status_code == 200 and response.json() else {}
        except Exception as e:
            print(f"Error getting app config: {e}")
            return {}
    
    def update_app_config(self, config_data):
        """Actualizar configuración de la app"""
        try:
            response = requests.patch(
                f'{self.supabase_url}/rest/v1/app_config?id=eq.1',
                headers=self.headers,
                json=config_data
            )
            return response.status_code == 204
        except Exception as e:
            print(f"Error updating app config: {e}")
            return False
    
    def get_statistics(self):
        """Obtener estadísticas generales"""
        try:
            # Obtener conteos de diferentes tablas
            users_response = requests.get(
                f'{self.supabase_url}/rest/v1/users?select=count',
                headers=self.headers
            )
            products_response = requests.get(
                f'{self.supabase_url}/rest/v1/products?select=count',
                headers=self.headers
            )
            orders_response = requests.get(
                f'{self.supabase_url}/rest/v1/orders?select=count',
                headers=self.headers
            )
            
            stats = {
                'total_users': len(users_response.json()) if users_response.status_code == 200 else 0,
                'total_products': len(products_response.json()) if products_response.status_code == 200 else 0,
                'total_orders': len(orders_response.json()) if orders_response.status_code == 200 else 0,
                'active_users': len([u for u in users_response.json() if not u.get('blocked', False)]) if users_response.status_code == 200 else 0
            }
            
            return stats
        except Exception as e:
            print(f"Error getting statistics: {e}")
            return {
                'total_users': 0,
                'total_products': 0,
                'total_orders': 0,
                'active_users': 0
            }

# Instancia global del servicio
supabase_service = SupabaseService()
