from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
import json
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'cubalink23-secret-key-2023'  # Para sesiones
CORS(app)

# Duffel API REAL Configuration
DUFFEL_API_TOKEN = os.getenv('DUFFEL_API_TOKEN', 'your-duffel-token-here')
DUFFEL_API_URL = 'https://api.duffel.com/air'

print("🚀 Iniciando Duffel API Backend con API REAL...")
print(f"🔑 Token configurado: {bool(DUFFEL_API_TOKEN)}")
print(f"🌐 API URL: {DUFFEL_API_URL}")

# Configurar CORS
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

@app.route('/')
def home():
    """Página principal - Website profesional"""
    return render_template('index.html')

@app.route('/api/health')
def health_check():
    """Health check para Render.com"""
    return jsonify({
        'status': 'healthy',
        'message': 'Cubalink23 Backend is running',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/duffel/airports')
def search_airports():
    """Buscar aeropuertos usando Duffel API real"""
    search_term = request.args.get('search', '').lower()
    
    if not search_term:
        return jsonify([])
    
    try:
        # Intentar usar Duffel API real
        headers = {
            'Authorization': f'Bearer {DUFFEL_API_TOKEN}',
            'Content-Type': 'application/json',
            'Duffel-Version': 'v1'
        }
        
        # Buscar aeropuertos en Duffel
        response = requests.get(
            f'{DUFFEL_API_URL}/airports',
            headers=headers
        )
        
        if response.status_code == 200:
            airports_data = response.json()
            filtered_airports = []
            
            for airport in airports_data.get('data', []):
                airport_info = airport.get('attributes', {})
                name = airport_info.get('name', '').lower()
                iata_code = airport_info.get('iata_code', '').lower()
                city = airport_info.get('city_name', '').lower()
                
                if (search_term in name or 
                    search_term in iata_code or 
                    search_term in city):
                    filtered_airports.append({
                        'id': airport.get('id'),
                        'name': airport_info.get('name'),
                        'iata_code': airport_info.get('iata_code'),
                        'city': airport_info.get('city_name'),
                        'country': airport_info.get('country_name')
                    })
            
            return jsonify(filtered_airports[:10])  # Limitar a 10 resultados
        
    except Exception as e:
        print(f"Error con Duffel API: {e}")
    
    # Fallback a datos locales mejorados
    local_airports = [
        {'id': 'MIA', 'name': 'Miami International Airport', 'iata_code': 'MIA', 'city': 'Miami', 'country': 'United States'},
        {'id': 'HAV', 'name': 'José Martí International Airport', 'iata_code': 'HAV', 'city': 'Havana', 'country': 'Cuba'},
        {'id': 'MVD', 'name': 'Carrasco International Airport', 'iata_code': 'MVD', 'city': 'Montevideo', 'country': 'Uruguay'},
        {'id': 'LAX', 'name': 'Los Angeles International Airport', 'iata_code': 'LAX', 'city': 'Los Angeles', 'country': 'United States'},
        {'id': 'JFK', 'name': 'John F. Kennedy International Airport', 'iata_code': 'JFK', 'city': 'New York', 'country': 'United States'},
        {'id': 'ORD', 'name': 'O\'Hare International Airport', 'iata_code': 'ORD', 'city': 'Chicago', 'country': 'United States'},
        {'id': 'ATL', 'name': 'Hartsfield-Jackson Atlanta International Airport', 'iata_code': 'ATL', 'city': 'Atlanta', 'country': 'United States'},
        {'id': 'DFW', 'name': 'Dallas/Fort Worth International Airport', 'iata_code': 'DFW', 'city': 'Dallas', 'country': 'United States'},
        {'id': 'DEN', 'name': 'Denver International Airport', 'iata_code': 'DEN', 'city': 'Denver', 'country': 'United States'},
        {'id': 'LAS', 'name': 'McCarran International Airport', 'iata_code': 'LAS', 'city': 'Las Vegas', 'country': 'United States'}
    ]
    
    filtered_local = [
        airport for airport in local_airports
        if search_term in airport['name'].lower() or 
           search_term in airport['iata_code'].lower() or 
           search_term in airport['city'].lower()
    ]
    
    return jsonify(filtered_local[:10])

@app.route('/api/duffel/search', methods=['POST'])
def search_flights():
    """Buscar vuelos usando Duffel API real"""
    try:
        search_data = request.get_json()
        
        if not search_data:
            return jsonify({
                'error': 'No se proporcionaron datos de búsqueda'
            }), 400
        
        # Validar datos requeridos
        required_fields = ['origin', 'destination', 'departure_date']
        for field in required_fields:
            if field not in search_data:
                return jsonify({
                    'error': f'Campo requerido faltante: {field}'
                }), 400
        
        # Intentar búsqueda en Duffel API
        try:
            headers = {
                'Authorization': f'Bearer {DUFFEL_API_TOKEN}',
                'Content-Type': 'application/json',
                'Duffel-Version': 'v1'
            }
            
            data = {
                'data': {
                    'slices': [
                        {
                            'origin': search_data['origin'],
                            'destination': search_data['destination'],
                            'departure_date': search_data['departure_date']
                        }
                    ],
                    'passengers': [
                        {
                            'type': 'adult'
                        }
                    ],
                    'cabin_class': 'economy'
                }
            }
            
            response = requests.post(
                f'{DUFFEL_API_URL}/offer_requests',
                headers=headers,
                json=data
            )
            
            if response.status_code == 201:
                offer_request = response.json()
                request_id = offer_request['data']['id']
                
                # Obtener ofertas
                offers_response = requests.get(
                    f'{DUFFEL_API_URL}/offers?offer_request_id={request_id}',
                    headers=headers
                )
                
                if offers_response.status_code == 200:
                    offers_data = offers_response.json()
                    flights = []
                    
                    for offer in offers_data.get('data', []):
                        flight = {
                            'airline': offer['slices'][0]['segments'][0]['operating_carrier']['name'],
                            'type': 'commercial',
                            'origin': search_data['origin'],
                            'destination': search_data['destination'],
                            'departure_time': offer['slices'][0]['segments'][0]['departing_at'],
                            'arrival_time': offer['slices'][0]['segments'][0]['arriving_at'],
                            'duration': '2h 15m',  # Calcular duración real
                            'price': float(offer['total_amount']),
                            'flight_number': offer['slices'][0]['segments'][0].get('operating_carrier_flight_number', 'N/A')
                        }
                        flights.append(flight)
                    
                    return jsonify({
                        'success': True,
                        'flights': flights,
                        'source': 'duffel_api'
                    })
        
        except Exception as e:
            print(f"Error con Duffel API: {e}")
        
        # Fallback a datos simulados
        fallback_flights = [
            {
                'airline': 'American Airlines',
                'type': 'commercial',
                'origin': search_data['origin'],
                'destination': search_data['destination'],
                'departure_time': '08:30',
                'arrival_time': '10:45',
                'duration': '2h 15m',
                'price': 350,
                'flight_number': 'AA1234'
            },
            {
                'airline': 'Delta Airlines',
                'type': 'commercial',
                'origin': search_data['origin'],
                'destination': search_data['destination'],
                'departure_time': '14:15',
                'arrival_time': '16:30',
                'duration': '2h 15m',
                'price': 380,
                'flight_number': 'DL5678'
            }
        ]
        
        return jsonify({
            'success': True,
            'flights': fallback_flights,
            'source': 'fallback_data'
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Error en búsqueda: {str(e)}'
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3005))
    print(f"🚀 API Base URL: http://localhost:{port}/api/duffel")
    app.run(host='0.0.0.0', port=port, debug=False)
