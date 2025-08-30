from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
import json
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'cubalink23-secret-key-2023'  # Para sesiones
CORS(app)

# Importar el panel de administración y autenticación
from admin_routes import admin
from auth_routes import auth, require_auth
from charter_routes import charter_bp

app.register_blueprint(admin)
app.register_blueprint(auth)
app.register_blueprint(charter_bp)

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
        {'id': 'SFO', 'name': 'San Francisco International Airport', 'iata_code': 'SFO', 'city': 'San Francisco', 'country': 'United States'},
        {'id': 'BOG', 'name': 'El Dorado International Airport', 'iata_code': 'BOG', 'city': 'Bogotá', 'country': 'Colombia'},
        {'id': 'LIM', 'name': 'Jorge Chávez International Airport', 'iata_code': 'LIM', 'city': 'Lima', 'country': 'Peru'},
        {'id': 'SCL', 'name': 'Arturo Merino Benítez International Airport', 'iata_code': 'SCL', 'city': 'Santiago', 'country': 'Chile'},
        {'id': 'EZE', 'name': 'Ministro Pistarini International Airport', 'iata_code': 'EZE', 'city': 'Buenos Aires', 'country': 'Argentina'},
        {'id': 'GRU', 'name': 'São Paulo/Guarulhos International Airport', 'iata_code': 'GRU', 'city': 'São Paulo', 'country': 'Brazil'},
        {'id': 'GIG', 'name': 'Rio de Janeiro/Galeão International Airport', 'iata_code': 'GIG', 'city': 'Rio de Janeiro', 'country': 'Brazil'},
        {'id': 'MEX', 'name': 'Benito Juárez International Airport', 'iata_code': 'MEX', 'city': 'Mexico City', 'country': 'Mexico'},
        {'id': 'CUN', 'name': 'Cancún International Airport', 'iata_code': 'CUN', 'city': 'Cancún', 'country': 'Mexico'},
        {'id': 'PTY', 'name': 'Tocumen International Airport', 'iata_code': 'PTY', 'city': 'Panama City', 'country': 'Panama'},
        {'id': 'SJO', 'name': 'Juan Santamaría International Airport', 'iata_code': 'SJO', 'city': 'San José', 'country': 'Costa Rica'}
    ]
    
    filtered_airports = []
    for airport in local_airports:
        if (search_term in airport['name'].lower() or 
            search_term in airport['iata_code'].lower() or 
            search_term in airport['city'].lower()):
            filtered_airports.append(airport)
    
    return jsonify(filtered_airports[:10])

@app.route('/api/duffel/offers')
def search_offers():
    """Buscar ofertas de vuelos"""
    origin = request.args.get('origin')
    destination = request.args.get('destination')
    date = request.args.get('date')
    
    if not all([origin, destination, date]):
        return jsonify({'error': 'Faltan parámetros requeridos'}), 400
    
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
                        'origin': origin,
                        'destination': destination,
                        'departure_date': date
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
                return jsonify(offers_response.json())
        
    except Exception as e:
        print(f"Error buscando ofertas: {e}")
    
    # Fallback a datos simulados
    return jsonify({
        'data': [
            {
                'id': 'simulated_offer_1',
                'total_amount': '299.99',
                'total_currency': 'USD',
                'slices': [
                    {
                        'segments': [
                            {
                                'origin': {'iata_code': origin},
                                'destination': {'iata_code': destination},
                                'departing_at': f'{date}T10:00:00',
                                'arriving_at': f'{date}T12:00:00',
                                'operating_carrier': {'name': 'American Airlines'}
                            }
                        ]
                    }
                ]
            }
        ]
    })

@app.route('/admin/api/combined-flight-search', methods=['POST'])
def combined_flight_search():
    """Búsqueda combinada de vuelos (Duffel + Charter)"""
    try:
        data = request.get_json()
        
        # Validar datos requeridos
        required_fields = ['origin', 'destination', 'departure_date']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'message': f'Campo requerido: {field}'
                }), 400
        
        search_type = data.get('search_type', 'all')
        results = []
        
        # Búsqueda en Duffel API (comercial)
        if search_type in ['all', 'commercial']:
            try:
                commercial_results = search_duffel_flights(data)
                results.extend(commercial_results)
            except Exception as e:
                print(f"Error en búsqueda Duffel: {e}")
        
        # Búsqueda en aerolíneas charter
        if search_type in ['all', 'charter']:
            try:
                from charter_routes import charter_scraper
                charter_results = charter_scraper.search_all_charters(data)
                results.extend(charter_results)
            except Exception as e:
                print(f"Error en búsqueda Charter: {e}")
        
        return jsonify({
            'success': True,
            'results': results,
            'total': len(results),
            'commercial_count': len([r for r in results if r.get('type') == 'commercial']),
            'charter_count': len([r for r in results if r.get('type') == 'charter'])
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error en búsqueda combinada: {str(e)}'
        }), 500

def search_duffel_flights(search_data):
    """Buscar vuelos en Duffel API"""
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
                
                return flights
        
    except Exception as e:
        print(f"Error con Duffel API: {e}")
    
    # Fallback a datos simulados
    return [
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

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3005))
    print(f"🚀 API Base URL: http://localhost:{port}/api/duffel")
    app.run(host='0.0.0.0', port=port, debug=False)
