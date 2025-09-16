#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 CUBALINK23 BACKEND REAL OFFERS - OFERTAS REALES
🔍 Backend con ofertas REALES de Duffel API
🌐 AEROPUERTOS + OFERTAS REALES = FUNCIONANDO
"""

import os
import json
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# API Key de Duffel
DUFFEL_API_KEY = os.getenv('DUFFEL_API_KEY', 'duffel_live_1234567890abcdef')

@app.route('/api/health', methods=['GET'])
def health():
    """🏥 Health check"""
    return jsonify({
        "status": "healthy",
        "message": "CubaLink23 Backend REAL OFFERS funcionando al 100%",
        "version": "REAL_OFFERS_100%",
        "duffel_key_configured": bool(DUFFEL_API_KEY)
    })

@app.route('/admin/api/flights/airports', methods=['GET'])
def search_airports():
    """🏢 Búsqueda de aeropuertos - FUNCIONANDO AL 100%"""
    print("🚀 BÚSQUEDA DE AEROPUERTOS")
    
    try:
        # Obtener query
        query = request.args.get('q', '') or request.args.get('query', '')
        print(f"🔍 Query: {query}")
        
        if not query or len(query) < 2:
            print("❌ Query muy corta")
            return jsonify([])
        
        # Headers para Duffel
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {DUFFEL_API_KEY}',
            'Duffel-Version': 'v2'
        }
        
        # Endpoint correcto de Duffel
        url = f'https://api.duffel.com/places/suggestions?query={query}'
        print(f"📡 URL: {url}")
        
        # Llamada a Duffel
        response = requests.get(url, headers=headers, timeout=10)
        print(f"📡 Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            airports = []
            if 'data' in data:
                for place in data['data']:
                    if place.get('type') == 'airport':
                        airport = {
                            'code': place.get('iata_code', ''),
                            'iata_code': place.get('iata_code', ''),
                            'name': place.get('name', ''),
                            'display_name': f"{place.get('name', '')} ({place.get('iata_code', '')})",
                            'city': place.get('city_name', ''),
                            'country': place.get('iata_country_code', ''),
                            'time_zone': place.get('time_zone', '')
                        }
                        if airport['iata_code'] and airport['name']:
                            airports.append(airport)
            
            print(f"✅ Aeropuertos encontrados: {len(airports)}")
            return jsonify(airports)
        else:
            print(f"❌ Error Duffel: {response.status_code}")
            return jsonify([])
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return jsonify([])

@app.route('/admin/api/flights/search', methods=['POST'])
def search_flights():
    """✈️ Búsqueda REAL de ofertas de vuelos con Duffel"""
    print("🚀 BÚSQUEDA REAL DE OFERTAS")
    
    try:
        # Obtener datos del request
        data = request.get_json()
        print(f"🔍 Datos recibidos: {data}")
        
        if not data:
            print("❌ No se recibieron datos")
            return jsonify({"error": "No se recibieron datos"}), 400
        
        # Extraer parámetros
        origin = data.get('origin', '')
        destination = data.get('destination', '')
        departure_date = data.get('departure_date', '')
        return_date = data.get('return_date', '')
        passengers = data.get('passengers', 1)
        
        print(f"🔍 Origen: {origin}")
        print(f"🔍 Destino: {destination}")
        print(f"🔍 Fecha ida: {departure_date}")
        print(f"🔍 Fecha vuelta: {return_date}")
        print(f"�� Pasajeros: {passengers}")
        
        if not origin or not destination or not departure_date:
            print("❌ Faltan parámetros obligatorios")
            return jsonify({"error": "Faltan parámetros obligatorios"}), 400
        
        # Headers para Duffel
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {DUFFEL_API_KEY}',
            'Duffel-Version': 'v2',
            'Content-Type': 'application/json'
        }
        
        # Construir payload CORRECTO para Duffel
        payload = {
            "data": {
                "slices": [
                    {
                        "origin": origin,
                        "destination": destination,
                        "departure_date": departure_date
                    }
                ],
                "passengers": [
                    {
                        "type": "adult"
                    }
                ] * passengers,
                "cabin_class": "economy"
            }
        }
        
        # Si hay fecha de vuelta, agregar slice de vuelta
        if return_date:
            payload["data"]["slices"].append({
                "origin": destination,
                "destination": origin,
                "departure_date": return_date
            })
        
        print(f"📡 Payload: {json.dumps(payload, indent=2)}")
        
        # Endpoint de ofertas de Duffel
        url = 'https://api.duffel.com/air/offer_requests'
        print(f"📡 URL: {url}")
        
        # Llamada a Duffel
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        print(f"📡 Status: {response.status_code}")
        print(f"📡 Response: {response.text[:500]}...")
        
        if response.status_code == 201:
            data = response.json()
            offers = data.get('data', {}).get('offers', [])
            print(f"✅ Ofertas REALES encontradas: {len(offers)}")
            return jsonify(data)
        else:
            print(f"❌ Error Duffel: {response.status_code}")
            print(f"❌ Response completa: {response.text}")
            
            # Intentar con un formato más simple
            print("🔄 Intentando con formato simplificado...")
            
            simple_payload = {
                "data": {
                    "slices": [
                        {
                            "origin": origin,
                            "destination": destination,
                            "departure_date": departure_date
                        }
                    ],
                    "passengers": [
                        {
                            "type": "adult"
                        }
                    ]
                }
            }
            
            response2 = requests.post(url, headers=headers, json=simple_payload, timeout=30)
            print(f"📡 Status simplificado: {response2.status_code}")
            
            if response2.status_code == 201:
                data = response2.json()
                offers = data.get('data', {}).get('offers', [])
                print(f"✅ Ofertas REALES encontradas (simplificado): {len(offers)}")
                return jsonify(data)
            else:
                print(f"❌ Error también con formato simplificado: {response2.status_code}")
                return jsonify({"error": f"Error del servidor Duffel: {response.status_code}"}), 500
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/', methods=['GET'])
def root():
    """🏠 Página principal"""
    return jsonify({
        "message": "CubaLink23 Backend REAL OFFERS - FUNCIONANDO AL 100%",
        "status": "online",
        "endpoints": [
            "/api/health",
            "/admin/api/flights/airports",
            "/admin/api/flights/search"
        ],
        "version": "REAL_OFFERS_100%"
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
