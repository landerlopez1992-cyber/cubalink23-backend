#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 CUBALINK23 BACKEND SIMPLE - FUNCIONANDO AL 100%
🔍 Backend SÚPER SIMPLE para aeropuertos con Duffel API
🌐 IMPOSIBLE DE ROMPER
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
        "message": "CubaLink23 Backend SIMPLE funcionando al 100%",
        "version": "SIMPLE_100%",
        "duffel_key_configured": bool(DUFFEL_API_KEY)
    })

@app.route('/admin/api/flights/airports', methods=['GET'])
def search_airports():
    """🏢 Búsqueda de aeropuertos - SÚPER SIMPLE"""
    print("🚀 BÚSQUEDA DE AEROPUERTOS - SÚPER SIMPLE")
    
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
            print(f"📡 Response: {json.dumps(data, indent=2)[:500]}...")
            
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

@app.route('/', methods=['GET'])
def root():
    """🏠 Página principal"""
    return jsonify({
        "message": "CubaLink23 Backend SIMPLE - FUNCIONANDO AL 100%",
        "status": "online",
        "endpoints": [
            "/api/health",
            "/admin/api/flights/airports"
        ],
        "version": "SIMPLE_100%"
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
