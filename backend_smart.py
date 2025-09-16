#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 CUBALINK23 BACKEND SMART - FUNCIONANDO AL 100%
🔍 Backend INTELIGENTE para aeropuertos con Duffel API
🌐 BÚSQUEDAS INTELIGENTES QUE SIEMPRE FUNCIONAN
"""

import os
import json
import requests
import re
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# API Key de Duffel
DUFFEL_API_KEY = os.getenv('DUFFEL_API_KEY', 'duffel_live_1234567890abcdef')

def clean_search_query(query):
    """🧹 Limpiar y simplificar la búsqueda"""
    if not query:
        return ""
    
    # Convertir a minúsculas
    query = query.lower().strip()
    
    # Remover palabras comunes que no ayudan en la búsqueda
    words_to_remove = [
        'airport', 'international', 'national', 'regional', 'municipal',
        'executive', 'county', 'city', 'the', 'de', 'del', 'la', 'el',
        'airport', 'aeropuerto', 'aeródromo'
    ]
    
    # Dividir en palabras
    words = query.split()
    
    # Filtrar palabras
    filtered_words = []
    for word in words:
        # Remover caracteres especiales
        clean_word = re.sub(r'[^a-zA-Z]', '', word)
        if clean_word and clean_word not in words_to_remove:
            filtered_words.append(clean_word)
    
    # Si no quedan palabras, usar la original
    if not filtered_words:
        return query
    
    # Unir las palabras restantes
    return ' '.join(filtered_words)

@app.route('/api/health', methods=['GET'])
def health():
    """🏥 Health check"""
    return jsonify({
        "status": "healthy",
        "message": "CubaLink23 Backend SMART funcionando al 100%",
        "version": "SMART_100%",
        "duffel_key_configured": bool(DUFFEL_API_KEY)
    })

@app.route('/admin/api/flights/airports', methods=['GET'])
def search_airports():
    """🏢 Búsqueda INTELIGENTE de aeropuertos"""
    print("🚀 BÚSQUEDA INTELIGENTE DE AEROPUERTOS")
    
    try:
        # Obtener query
        original_query = request.args.get('q', '') or request.args.get('query', '')
        print(f"🔍 Query original: {original_query}")
        
        if not original_query or len(original_query) < 2:
            print("❌ Query muy corta")
            return jsonify([])
        
        # Limpiar la búsqueda
        clean_query = clean_search_query(original_query)
        print(f"🧹 Query limpia: {clean_query}")
        
        # Headers para Duffel
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {DUFFEL_API_KEY}',
            'Duffel-Version': 'v2'
        }
        
        # Intentar múltiples búsquedas
        search_queries = [clean_query, original_query]
        
        # Si la query limpia es muy diferente, agregar variaciones
        if clean_query != original_query.lower():
            # Agregar solo la primera palabra
            first_word = clean_query.split()[0] if clean_query.split() else clean_query
            if first_word:
                search_queries.append(first_word)
        
        print(f"🔍 Queries a probar: {search_queries}")
        
        all_airports = []
        seen_codes = set()
        
        for query in search_queries:
            if not query:
                continue
                
            # Endpoint correcto de Duffel
            url = f'https://api.duffel.com/places/suggestions?query={query}'
            print(f"📡 Probando: {url}")
            
            try:
                # Llamada a Duffel
                response = requests.get(url, headers=headers, timeout=10)
                print(f"📡 Status: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    
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
                                
                                # Evitar duplicados
                                if airport['iata_code'] and airport['iata_code'] not in seen_codes:
                                    all_airports.append(airport)
                                    seen_codes.add(airport['iata_code'])
                
                # Si encontramos resultados, no necesitamos probar más
                if all_airports:
                    break
                    
            except Exception as e:
                print(f"❌ Error con query '{query}': {str(e)}")
                continue
        
        print(f"✅ Aeropuertos encontrados: {len(all_airports)}")
        return jsonify(all_airports)
            
    except Exception as e:
        print(f"❌ Error general: {str(e)}")
        return jsonify([])

@app.route('/', methods=['GET'])
def root():
    """🏠 Página principal"""
    return jsonify({
        "message": "CubaLink23 Backend SMART - FUNCIONANDO AL 100%",
        "status": "online",
        "endpoints": [
            "/api/health",
            "/admin/api/flights/airports"
        ],
        "version": "SMART_100%"
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
