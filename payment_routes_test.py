#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rutas de pagos SIMPLES para testing
"""

from flask import Blueprint, request, jsonify

payment_bp = Blueprint('payment', __name__, url_prefix='/api/payments')

@payment_bp.route('/process', methods=['POST'])
def process_payment():
    """Procesar pago - VERSIÓN SIMPLE PARA TESTING"""
    try:
        data = request.get_json()
        print(f"💳 Recibido request de pago: {data}")
        
        return jsonify({
            'success': True,
            'checkout_url': 'https://example.com/checkout',
            'message': 'Payment endpoint funcionando correctamente'
        })
        
    except Exception as e:
        print(f"❌ Error procesando pago: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Error interno: {str(e)}'
        }), 500

@payment_bp.route('/status', methods=['GET'])
def payment_status():
    """Verificar estado del servicio de pagos"""
    return jsonify({
        'status': 'active',
        'service': 'Payment Test Service'
    })
