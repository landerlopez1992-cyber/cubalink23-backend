#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
💳 SQUARE PAYMENTS API - IMPLEMENTACIÓN COMPLETA
🔒 Tokenización nativa + Card on File + Cobros directos
🌐 Backend Flask para CubaLink23
"""

import os
import uuid
import logging
from flask import Blueprint, request, jsonify
from square.client import Client

# Configurar logging
log = logging.getLogger("square")

# Crear blueprint
bp = Blueprint("square", __name__, url_prefix="/api/square")

# Configuración de Square
ENV = os.getenv("SQUARE_ENV", "sandbox")
SQUARE_ACCESS_TOKEN = os.environ.get("SQUARE_ACCESS_TOKEN")
SQUARE_LOCATION_ID = os.environ.get("SQUARE_LOCATION_ID")

if not SQUARE_ACCESS_TOKEN:
    log.error("❌ SQUARE_ACCESS_TOKEN no configurado")
    raise ValueError("SQUARE_ACCESS_TOKEN es requerido")

# Inicializar cliente Square
client = Client(
    access_token=SQUARE_ACCESS_TOKEN,
    environment="production" if ENV == "production" else "sandbox"
)

payments = client.payments
cards = client.cards
customers = client.customers

print(f"✅ Square client inicializado - ENV: {ENV}")
print(f"📍 Location ID: {SQUARE_LOCATION_ID}")

@bp.route("/health", methods=["GET"])
def health():
    """💚 Health check del servicio Square"""
    return jsonify({
        "ok": True, 
        "env": ENV,
        "location_id": SQUARE_LOCATION_ID,
        "service": "square-payments"
    })

@bp.route("/charge", methods=["POST"])
def charge_nonce():
    """💳 Cobrar con nonce de tarjeta (tokenización directa)"""
    try:
        data = request.get_json()
        nonce = data.get("nonce")
        amount = int(data.get("amount"))
        currency = data.get("currency", "USD")
        customer_id = data.get("customer_id")
        
        if not nonce:
            return jsonify({"ok": False, "error": "nonce es requerido"}), 400
        
        if not amount or amount <= 0:
            return jsonify({"ok": False, "error": "amount debe ser mayor a 0"}), 400
        
        # Generar idempotency_key único
        idem = str(uuid.uuid4())
        
        # Preparar request body
        body = {
            "source_id": nonce,
            "idempotency_key": idem,
            "amount_money": {"amount": amount, "currency": currency},
            "location_id": SQUARE_LOCATION_ID
        }
        
        if customer_id:
            body["customer_id"] = customer_id
        
        # Ejecutar pago
        res = payments.create_payment(body)
        
        if res.is_success():
            payment = res.body["payment"]
            log.info(f"✅ [charge] Pago exitoso - idem={idem} payment_id={payment['id']}")
            return jsonify({
                "ok": True, 
                "payment": payment,
                "idempotency_key": idem
            })
        else:
            log.error(f"❌ [charge] Error - idem={idem} errors={res.errors}")
            return jsonify({
                "ok": False, 
                "error": "Error procesando pago",
                "details": res.errors,
                "idempotency_key": idem
            }), 502
            
    except Exception as e:
        log.error(f"❌ [charge] Excepción: {str(e)}")
        return jsonify({
            "ok": False, 
            "error": f"Error interno: {str(e)}"
        }), 500

@bp.route("/save-card", methods=["POST"])
def save_card():
    """💾 Guardar tarjeta para uso futuro (Card on File)"""
    try:
        data = request.get_json()
        nonce = data.get("nonce")
        customer_id = data.get("customer_id")
        
        if not nonce:
            return jsonify({"ok": False, "error": "nonce es requerido"}), 400
        
        if not customer_id:
            return jsonify({"ok": False, "error": "customer_id es requerido"}), 400
        
        # Generar idempotency_key único
        idem = str(uuid.uuid4())
        
        # Preparar request body
        body = {
            "idempotency_key": idem,
            "source_id": nonce,
            "card": {
                "customer_id": customer_id
            }
        }
        
        # Crear tarjeta
        res = cards.create_card(body)
        
        if res.is_success():
            card = res.body["card"]
            log.info(f"✅ [save-card] Tarjeta guardada - idem={idem} card_id={card['id']}")
            return jsonify({
                "ok": True, 
                "card": card,
                "idempotency_key": idem
            })
        else:
            log.error(f"❌ [save-card] Error - idem={idem} errors={res.errors}")
            return jsonify({
                "ok": False, 
                "error": "Error guardando tarjeta",
                "details": res.errors,
                "idempotency_key": idem
            }), 502
            
    except Exception as e:
        log.error(f"❌ [save-card] Excepción: {str(e)}")
        return jsonify({
            "ok": False, 
            "error": f"Error interno: {str(e)}"
        }), 500

@bp.route("/charge-cof", methods=["POST"])
def charge_cof():
    """💳 Cobrar con tarjeta guardada (Card on File)"""
    try:
        data = request.get_json()
        customer_id = data.get("customer_id")
        card_id = data.get("card_id")
        amount = int(data.get("amount"))
        currency = data.get("currency", "USD")
        
        if not customer_id:
            return jsonify({"ok": False, "error": "customer_id es requerido"}), 400
        
        if not card_id:
            return jsonify({"ok": False, "error": "card_id es requerido"}), 400
        
        if not amount or amount <= 0:
            return jsonify({"ok": False, "error": "amount debe ser mayor a 0"}), 400
        
        # Generar idempotency_key único
        idem = str(uuid.uuid4())
        
        # Preparar request body
        body = {
            "source_id": card_id,  # card on file
            "idempotency_key": idem,
            "amount_money": {"amount": amount, "currency": currency},
            "customer_id": customer_id,
            "location_id": SQUARE_LOCATION_ID
        }
        
        # Ejecutar pago
        res = payments.create_payment(body)
        
        if res.is_success():
            payment = res.body["payment"]
            log.info(f"✅ [charge-cof] Pago exitoso - idem={idem} payment_id={payment['id']}")
            return jsonify({
                "ok": True, 
                "payment": payment,
                "idempotency_key": idem
            })
        else:
            log.error(f"❌ [charge-cof] Error - idem={idem} errors={res.errors}")
            return jsonify({
                "ok": False, 
                "error": "Error procesando pago",
                "details": res.errors,
                "idempotency_key": idem
            }), 502
            
    except Exception as e:
        log.error(f"❌ [charge-cof] Excepción: {str(e)}")
        return jsonify({
            "ok": False, 
            "error": f"Error interno: {str(e)}"
        }), 500

@bp.route("/create-customer", methods=["POST"])
def create_customer():
    """👤 Crear cliente en Square"""
    try:
        data = request.get_json()
        email = data.get("email")
        given_name = data.get("given_name", "Usuario")
        family_name = data.get("family_name", "CubaLink23")
        
        if not email:
            return jsonify({"ok": False, "error": "email es requerido"}), 400
        
        # Generar idempotency_key único
        idem = str(uuid.uuid4())
        
        # Preparar request body
        body = {
            "idempotency_key": idem,
            "given_name": given_name,
            "family_name": family_name,
            "email_address": email
        }
        
        # Crear cliente
        res = customers.create_customer(body)
        
        if res.is_success():
            customer = res.body["customer"]
            log.info(f"✅ [create-customer] Cliente creado - idem={idem} customer_id={customer['id']}")
            return jsonify({
                "ok": True, 
                "customer": customer,
                "idempotency_key": idem
            })
        else:
            log.error(f"❌ [create-customer] Error - idem={idem} errors={res.errors}")
            return jsonify({
                "ok": False, 
                "error": "Error creando cliente",
                "details": res.errors,
                "idempotency_key": idem
            }), 502
            
    except Exception as e:
        log.error(f"❌ [create-customer] Excepción: {str(e)}")
        return jsonify({
            "ok": False, 
            "error": f"Error interno: {str(e)}"
        }), 500
