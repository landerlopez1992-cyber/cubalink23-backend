#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rutas de pagos SIMPLIFICADAS para Cubalink23 con integración Square
"""

from flask import Blueprint, request, jsonify
import os
import requests
import uuid

payment_bp = Blueprint('payment', __name__, url_prefix='/api/payments')

@payment_bp.route('/process', methods=['POST'])
def process_payment():
    """Procesar pago con Square API usando Payment Links"""
    try:
        data = request.get_json()
        print(f"💳 Recibido request de pago: {data}")
        
        # Obtener datos del request
        amount = data.get('amount', 0)
        description = data.get('description', 'Pago Cubalink23')
        email = data.get('email', 'test@example.com')
        
        # Configuración de Square
        access_token = os.environ.get('SQUARE_ACCESS_TOKEN')
        location_id = os.environ.get('SQUARE_LOCATION_ID', 'LZVTP0YQ9YQBB')
        
        if not access_token:
            return jsonify({
                'success': False,
                'error': 'Square no está configurado'
            }), 500
        
        print(f"💰 Procesando pago: ${amount} - {description}")
        
        # Crear Payment Link con Square
        payment_link_data = {
            "idempotency_key": str(uuid.uuid4()),
            "checkout_options": {
                "ask_for_shipping_address": False,
                "merchant_support_email": "support@cubalink23.com"
            },
            "order": {
                "location_id": location_id,
                "line_items": [
                    {
                        "name": description,
                        "quantity": "1",
                        "item_type": "ITEM",
                        "base_price_money": {
                            "amount": int(amount * 100),  # Convertir a centavos
                            "currency": "USD"
                        }
                    }
                ]
            },
            "pre_populated_data": {
                "buyer_email": email
            }
        }
        
        # Llamar a Square API
        headers = {
            'Square-Version': '2023-10-18',
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        response = requests.post(
            'https://connect.squareupsandbox.com/v2/online-checkout/payment-links',
            headers=headers,
            json=payment_link_data,
            timeout=30
        )
        
        print(f"📡 Square API Response: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            payment_link = result.get('payment_link', {})
            checkout_url = payment_link.get('url')
            
            if checkout_url:
                return jsonify({
                    'success': True,
                    'checkout_url': checkout_url,
                    'payment_link_id': payment_link.get('id'),
                    'amount': amount,
                    'message': 'Payment Link creado exitosamente'
                })
            else:
                return jsonify({
                    'success': False,
                    'error': 'No se pudo obtener URL de checkout'
                }), 500
        else:
            error_data = response.json()
            errors = error_data.get('errors', [])
            error_message = errors[0].get('detail', 'Error desconocido') if errors else 'Error de pago'
            
            return jsonify({
                'success': False,
                'error': error_message,
                'status_code': response.status_code
            }), 500
            
    except Exception as e:
        print(f"❌ Error procesando pago: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Error interno del servidor: {str(e)}'
        }), 500

@payment_bp.route('/status', methods=['GET'])
def payment_status():
    """Verificar estado del servicio de pagos"""
    return jsonify({
        'status': 'active',
        'service': 'Square Payment Links',
        'environment': os.environ.get('SQUARE_ENVIRONMENT', 'sandbox')
    })
