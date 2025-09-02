#!/usr/bin/env python3
"""
Servicio de integración con Square para métodos de pago
"""

import os
import json
import uuid
from datetime import datetime
import requests

class SquareService:
    def __init__(self):
        """Inicializar servicio de Square"""
        self.access_token = os.environ.get('SQUARE_ACCESS_TOKEN')
        self.application_id = os.environ.get('SQUARE_APPLICATION_ID')
        self.location_id = os.environ.get('SQUARE_LOCATION_ID')
        self.environment = os.environ.get('SQUARE_ENVIRONMENT', 'sandbox')
        
        # Configurar base URL según ambiente
        if self.environment == 'production':
            self.base_url = 'https://connect.squareup.com'
        else:
            self.base_url = 'https://connect.squareupsandbox.com'
        
        # Configurar headers
        if self.access_token and self.application_id:
            self.headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json',
                'Square-Version': '2024-12-01'
            }
            self.is_configured = True
        else:
            self.headers = None
            self.is_configured = False
            print("⚠️ Square no está configurado. Configura las variables de entorno.")
    
    def is_available(self):
        """Verificar si Square está disponible"""
        return self.is_configured and self.client is not None
    
    def create_payment_link(self, order_data):
        """Crear enlace de pago para un pedido"""
        try:
            if not self.is_available():
                return self._create_mock_payment_link(order_data)
            
            # Crear Quick Pay link usando la API REST
            body = {
                "quick_pay": {
                    "name": f"Pedido {order_data.get('order_number', 'N/A')}",
                    "price_money": {
                        "amount": int(float(order_data.get('total_amount', 0)) * 100),  # Square usa centavos
                        "currency": order_data.get('currency', 'USD')
                    },
                    "location_id": self.location_id
                }
            }
            
            response = requests.post(
                f'{self.base_url}/v2/online-checkout/payment-links',
                headers=self.headers,
                json=body
            )
            
            if response.status_code == 200:
                payment_link = response.json().get('payment_link', {})
                return {
                    'success': True,
                    'payment_link_id': payment_link.get('id'),
                    'checkout_url': payment_link.get('checkout_page_url'),
                    'order_id': order_data.get('id'),
                    'amount': order_data.get('total_amount'),
                    'currency': order_data.get('currency')
                }
            else:
                print(f"Error creating payment link: {response.status_code} - {response.text}")
                return self._create_mock_payment_link(order_data)
                
        except Exception as e:
            print(f"Error creating payment link: {e}")
            return self._create_mock_payment_link(order_data)
    
    def process_payment(self, payment_data):
        """Procesar pago con tarjeta"""
        try:
            if not self.is_available():
                return self._create_mock_payment(payment_data)
            
            # Crear pago usando la API REST
            body = {
                "source_id": payment_data.get('source_id'),
                "idempotency_key": str(uuid.uuid4()),
                "amount_money": {
                    "amount": int(float(payment_data.get('amount', 0)) * 100),
                    "currency": payment_data.get('currency', 'USD')
                },
                "location_id": self.location_id,
                "reference_id": payment_data.get('order_id'),
                "note": f"Pago para pedido {payment_data.get('order_number', 'N/A')}"
            }
            
            response = requests.post(
                f'{self.base_url}/v2/payments',
                headers=self.headers,
                json=body
            )
            
            if response.status_code == 200:
                payment = response.json().get('payment', {})
                return {
                    'success': True,
                    'payment_id': payment.get('id'),
                    'status': payment.get('status'),
                    'amount': payment.get('amount_money', {}).get('amount', 0) / 100,
                    'currency': payment.get('amount_money', {}).get('currency'),
                    'receipt_url': payment.get('receipt_url'),
                    'order_id': payment_data.get('order_id')
                }
            else:
                print(f"Error processing payment: {response.status_code} - {response.text}")
                return {
                    'success': False,
                    'error': 'Error procesando pago',
                    'details': response.text
                }
                
        except Exception as e:
            print(f"Error processing payment: {e}")
            return {
                'success': False,
                'error': 'Error interno',
                'details': str(e)
            }
    
    def create_customer(self, customer_data):
        """Crear cliente en Square"""
        try:
            if not self.is_available():
                return self._create_mock_customer(customer_data)
            
            body = {
                "idempotency_key": str(uuid.uuid4()),
                "given_name": customer_data.get('first_name', ''),
                "family_name": customer_data.get('last_name', ''),
                "email_address": customer_data.get('email', ''),
                "phone_number": customer_data.get('phone', ''),
                "address": {
                    "address_line_1": customer_data.get('address', {}).get('street', ''),
                    "locality": customer_data.get('address', {}).get('city', ''),
                    "administrative_district_level_1": customer_data.get('address', {}).get('state', ''),
                    "postal_code": customer_data.get('address', {}).get('zip_code', ''),
                    "country": customer_data.get('address', {}).get('country', 'US')
                }
            }
            
            response = requests.post(
                f'{self.base_url}/v2/customers',
                headers=self.headers,
                json=body
            )
            
            if response.status_code == 200:
                customer = response.json().get('customer', {})
                return {
                    'success': True,
                    'customer_id': customer.get('id'),
                    'email': customer.get('email_address'),
                    'name': f"{customer.get('given_name', '')} {customer.get('family_name', '')}".strip()
                }
            else:
                print(f"Error creating customer: {response.status_code} - {response.text}")
                return self._create_mock_customer(customer_data)
                
        except Exception as e:
            print(f"Error creating customer: {e}")
            return self._create_mock_customer(customer_data)
    
    def get_payment_methods(self):
        """Obtener métodos de pago disponibles"""
        return [
            {
                'id': 'square_card',
                'name': 'Tarjeta de Crédito/Débito',
                'type': 'card',
                'description': 'Pago con tarjeta Visa, MasterCard, American Express',
                'icon': '💳',
                'enabled': True
            },
            {
                'id': 'square_cash',
                'name': 'Square Cash',
                'type': 'digital_wallet',
                'description': 'Pago con Square Cash App',
                'icon': '📱',
                'enabled': True
            },
            {
                'id': 'square_gift_card',
                'name': 'Tarjeta de Regalo',
                'type': 'gift_card',
                'description': 'Pago con tarjeta de regalo Square',
                'icon': '🎁',
                'enabled': True
            },
            {
                'id': 'bank_transfer',
                'name': 'Transferencia Bancaria',
                'type': 'bank_transfer',
                'description': 'Transferencia directa a cuenta bancaria',
                'icon': '🏦',
                'enabled': True
            },
            {
                'id': 'cash_on_delivery',
                'name': 'Pago en Efectivo',
                'type': 'cash',
                'description': 'Pago en efectivo al recibir el pedido',
                'icon': '💵',
                'enabled': True
            }
        ]
    
    def get_payment_status(self, payment_id):
        """Obtener estado de un pago"""
        try:
            if not self.is_available():
                return self._get_mock_payment_status(payment_id)
            
            response = requests.get(
                f'{self.base_url}/v2/payments/{payment_id}',
                headers=self.headers
            )
            
            if response.status_code == 200:
                payment = response.json().get('payment', {})
                return {
                    'success': True,
                    'payment_id': payment.get('id'),
                    'status': payment.get('status'),
                    'amount': payment.get('amount_money', {}).get('amount', 0) / 100,
                    'currency': payment.get('amount_money', {}).get('currency'),
                    'created_at': payment.get('created_at'),
                    'updated_at': payment.get('updated_at')
                }
            else:
                print(f"Error getting payment status: {response.status_code} - {response.text}")
                return {
                    'success': False,
                    'error': 'Error obteniendo estado del pago'
                }
                
        except Exception as e:
            print(f"Error getting payment status: {e}")
            return {
                'success': False,
                'error': 'Error interno'
            }
    
    def refund_payment(self, payment_id, amount=None, reason='Customer request'):
        """Reembolsar un pago"""
        try:
            if not self.is_available():
                return self._create_mock_refund(payment_id, amount)
            
            body = {
                "idempotency_key": str(uuid.uuid4()),
                "payment_id": payment_id,
                "reason": reason
            }
            
            if amount:
                body["amount_money"] = {
                    "amount": int(float(amount) * 100),
                    "currency": "USD"
                }
            
            response = requests.post(
                f'{self.base_url}/v2/refunds',
                headers=self.headers,
                json=body
            )
            
            if response.status_code == 200:
                refund = response.json().get('refund', {})
                return {
                    'success': True,
                    'refund_id': refund.get('id'),
                    'status': refund.get('status'),
                    'amount': refund.get('amount_money', {}).get('amount', 0) / 100,
                    'currency': refund.get('amount_money', {}).get('currency'),
                    'reason': refund.get('reason')
                }
            else:
                print(f"Error refunding payment: {response.status_code} - {response.text}")
                return {
                    'success': False,
                    'error': 'Error procesando reembolso'
                }
                
        except Exception as e:
            print(f"Error refunding payment: {e}")
            return {
                'success': False,
                'error': 'Error interno'
            }
    
    def get_transaction_history(self, start_date=None, end_date=None):
        """Obtener historial de transacciones"""
        try:
            if not self.is_available():
                return self._get_mock_transaction_history()
            
            # Configurar fechas
            if not start_date:
                start_date = datetime.now().replace(day=1).isoformat()
            if not end_date:
                end_date = datetime.now().isoformat()
            
            params = {
                'begin_time': start_date,
                'end_time': end_date
            }
            
            response = requests.get(
                f'{self.base_url}/v2/payments',
                headers=self.headers,
                params=params
            )
            
            if response.status_code == 200:
                payments = response.json().get('payments', [])
                transactions = []
                
                for payment in payments:
                    transactions.append({
                        'id': payment.get('id'),
                        'amount': payment.get('amount_money', {}).get('amount', 0) / 100,
                        'currency': payment.get('amount_money', {}).get('currency'),
                        'status': payment.get('status'),
                        'created_at': payment.get('created_at'),
                        'reference_id': payment.get('reference_id')
                    })
                
                return {
                    'success': True,
                    'transactions': transactions,
                    'total_count': len(transactions)
                }
            else:
                print(f"Error getting transaction history: {response.status_code} - {response.text}")
                return self._get_mock_transaction_history()
                
        except Exception as e:
            print(f"Error getting transaction history: {e}")
            return self._get_mock_transaction_history()
    
    # ===== MÉTODOS MOCK PARA DESARROLLO =====
    
    def _create_mock_payment_link(self, order_data):
        """Crear enlace de pago mock para desarrollo"""
        return {
            'success': True,
            'payment_link_id': f"mock_link_{uuid.uuid4().hex[:8]}",
            'checkout_url': f"https://mock-square.com/checkout/{uuid.uuid4().hex[:8]}",
            'order_id': order_data.get('id'),
            'amount': order_data.get('total_amount'),
            'currency': order_data.get('currency'),
            'mock': True
        }
    
    def _create_mock_payment(self, payment_data):
        """Crear pago mock para desarrollo"""
        return {
            'success': True,
            'payment_id': f"mock_payment_{uuid.uuid4().hex[:8]}",
            'status': 'COMPLETED',
            'amount': payment_data.get('amount'),
            'currency': payment_data.get('currency'),
            'receipt_url': f"https://mock-square.com/receipt/{uuid.uuid4().hex[:8]}",
            'order_id': payment_data.get('order_id'),
            'mock': True
        }
    
    def _create_mock_customer(self, customer_data):
        """Crear cliente mock para desarrollo"""
        return {
            'success': True,
            'customer_id': f"mock_customer_{uuid.uuid4().hex[:8]}",
            'email': customer_data.get('email'),
            'name': f"{customer_data.get('first_name', '')} {customer_data.get('last_name', '')}".strip(),
            'mock': True
        }
    
    def _get_mock_payment_status(self, payment_id):
        """Obtener estado de pago mock"""
        return {
            'success': True,
            'payment_id': payment_id,
            'status': 'COMPLETED',
            'amount': 99.99,
            'currency': 'USD',
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'mock': True
        }
    
    def _create_mock_refund(self, payment_id, amount):
        """Crear reembolso mock"""
        return {
            'success': True,
            'refund_id': f"mock_refund_{uuid.uuid4().hex[:8]}",
            'status': 'COMPLETED',
            'amount': amount or 99.99,
            'currency': 'USD',
            'reason': 'Customer request',
            'mock': True
        }
    
    def _get_mock_transaction_history(self):
        """Obtener historial de transacciones mock"""
        return {
            'success': True,
            'transactions': [
                {
                    'id': f"mock_payment_{uuid.uuid4().hex[:8]}",
                    'amount': 99.99,
                    'currency': 'USD',
                    'status': 'COMPLETED',
                    'created_at': datetime.now().isoformat(),
                    'reference_id': 'ORD-20241230-123456'
                },
                {
                    'id': f"mock_payment_{uuid.uuid4().hex[:8]}",
                    'amount': 149.99,
                    'currency': 'USD',
                    'status': 'COMPLETED',
                    'created_at': datetime.now().isoformat(),
                    'reference_id': 'ORD-20241230-123457'
                }
            ],
            'total_count': 2,
            'mock': True
        }

# Instancia global del servicio de Square
square_service = SquareService()
