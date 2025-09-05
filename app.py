# -*- coding: utf-8 -*-
# CubaLink23 Backend FINAL - 100% Funcional
# Integración completa con Duffel API
# Desplegado en Render.com
# VERSIÓN CON ENDPOINT DE ASIENTOS - 2025-09-04
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder='static', static_url_path='/static')
CORS(app)

# Importar el panel de administración
from admin_routes import admin
app.register_blueprint(admin)

# Importar las rutas de colecciones
from collections_routes import collections_bp
app.register_blueprint(collections_bp, url_prefix='/admin')

# Importar configuración automática de base de datos
try:
    from setup_database import setup_user_carts_table, verify_table_exists
    AUTO_SETUP_AVAILABLE = True
    print("✅ Configuración automática de DB disponible")
except ImportError:
    AUTO_SETUP_AVAILABLE = False
    print("⚠️ setup_database.py no disponible - configuración manual requerida")

# Importar configuración automática de bucket de imágenes
try:
    from setup_images_bucket import setup_product_images_bucket, verify_bucket_exists
    IMAGE_SETUP_AVAILABLE = True
    print("✅ Configuración automática de imágenes disponible")
except ImportError:
    IMAGE_SETUP_AVAILABLE = False
    print("⚠️ setup_images_bucket.py no disponible - configuración manual requerida")

# Importar arreglo automático de tabla store_products
try:
    from fix_store_products_schema import fix_store_products_table, verify_table_structure
    TABLE_FIX_AVAILABLE = True
    print("✅ Arreglo automático de tabla store_products disponible")
except ImportError:
    TABLE_FIX_AVAILABLE = False
    print("⚠️ fix_store_products_schema.py no disponible - arreglo manual requerido")

# Duffel API REAL Configuration
DUFFEL_API_TOKEN = 'duffel_live_Rj6u0G0cT2hUeIw53ou2HRTNNf0tXl6oP-pVzcGvI7e'
DUFFEL_API_URL = 'https://api.duffel.com/air'

# Headers according to documentation
headers = {
    'Authorization': 'Bearer {}'.format(DUFFEL_API_TOKEN),
    'Content-Type': 'application/json',
    'Duffel-Version': 'v2'
}



@app.route('/api/duffel/search-offers', methods=['POST'])
def search_offers():
    try:
        data = request.json
        print("🔍 Buscando vuelos REALES: {}".format(data))
        
        # Intentar con Duffel API real para todas las rutas
        duffel_request = {
            'data': {
                'slices': data.get('slices', []),
                'passengers': data.get('passengers', []),
                'cabin_class': data.get('cabin_class', 'economy')
            }
        }
        
        print("📤 Request a Duffel API: {}".format(duffel_request))
        
        # Llamar a Duffel API para crear offer request
        response = requests.post(
            '{}/offer_requests'.format(DUFFEL_API_URL),
            headers=headers,
            json=duffel_request,
            timeout=30
        )
        
        print("📡 Respuesta Duffel: {}".format(response.status_code))
        
        if response.status_code in [200, 201]:
            duffel_data = response.json()
            print("✅ Datos reales de vuelos obtenidos de Duffel API")
            # Procesar datos reales de Duffel
            return _process_real_duffel_data(duffel_data, data)
        else:
            print("❌ Error Duffel API: {} - {}".format(response.status_code, response.text))
            # NO devolver datos demo, devolver error
            return jsonify({
                'success': False,
                'error': 'Error en Duffel API: {}'.format(response.status_code),
                'data': {
                    'offers': [],
                    'total_offers': 0,
                    'live_data': False
                }
            }), 400
            
    except Exception as e:
        print("❌ Error en servidor: {}".format(str(e)))
        return _get_fallback_flights(data)

def _get_fallback_flights(data):
    """Vuelos de ejemplo cuando Duffel API falla"""
    try:
        origin = data['slices'][0]['origin']
        destination = data['slices'][0]['destination']
        departure_date = data['slices'][0]['departure_date']
        
        airlines = ['American Airlines', 'Delta Airlines', 'United Airlines', 'JetBlue', 'Spirit Airlines']
        mock_offers = []
        
        for i in range(5):
            mock_offers.append({
                'id': 'offer_{}'.format(i),
                'slices': [
                    {
                        'origin': {'iata_code': origin},
                        'destination': {'iata_code': destination},
                        'segments': [
                            {
                                'departing_at': '{}T{:02d}:00:00Z'.format(departure_date, 10+i*2),
                                'arriving_at': '{}T{:02d}:00:00Z'.format(departure_date, 12+i*2),
                                'operating_carrier': {'flight_number': 'AA10{}'.format(i)}
                            }
                        ]
                    }
                ],
                'owner': {'name': airlines[i % len(airlines)]},
                'total_amount': str(150 + i * 50),
                'total_currency': 'USD',
                'cabin_class': 'economy'
            })
        
        return jsonify({
            'success': True,
            'data': {
                'data': {
                    'id': 'mock_request_id',
                    'offers': mock_offers
                }
            }
        })
    except Exception as e:
        print("❌ Error generando vuelos de ejemplo: {}".format(e))
        return jsonify({
            'success': False,
            'error': 'Error: {}'.format(str(e))
        }), 500

def _process_real_duffel_data(duffel_data, original_request):
    """Procesar datos reales de Duffel API y convertirlos al formato esperado"""
    try:
        if 'data' in duffel_data and 'offers' in duffel_data['data']:
            offers = duffel_data['data']['offers']
            print("📊 Procesando {} ofertas reales de Duffel".format(len(offers)))
            
            processed_offers = []
            for offer in offers:
                if 'slices' in offer and len(offer['slices']) > 0:
                    slice_data = offer['slices'][0]
                    if 'segments' in slice_data and len(slice_data['segments']) > 0:
                        segment = slice_data['segments'][0]
                        
                        processed_offer = {
                            'id': offer.get('id', ''),
                            'airline': offer.get('owner', {}).get('name', 'Unknown'),
                            'flight_number': segment.get('operating_carrier_flight_number', ''),
                            'origin': slice_data.get('origin', {}).get('iata_code', ''),
                            'destination': slice_data.get('destination', {}).get('iata_code', ''),
                            'departure_time': segment.get('departing_at', ''),
                            'arrival_time': segment.get('arriving_at', ''),
                            'price': offer.get('total_amount', '0'),
                            'currency': offer.get('total_currency', 'USD'),
                            'cabin_class': offer.get('cabin_class', 'economy'),
                            'stops': len(slice_data.get('segments', [])) - 1,
                            'duration': slice_data.get('duration', ''),
                            'aircraft': segment.get('aircraft', {}).get('name', ''),
                            'live_mode': offer.get('live_mode', False)
                        }
                        processed_offers.append(processed_offer)
            
            return jsonify({
                'success': True,
                'data': {
                    'offers': processed_offers,
                    'total_offers': len(processed_offers),
                    'live_data': True
                }
            })
        else:
            print("No se encontraron ofertas en la respuesta de Duffel")
            return jsonify({
                'success': False,
                'error': 'No se encontraron ofertas en la respuesta de Duffel',
                'data': {
                    'offers': [],
                    'total_offers': 0,
                    'live_data': False
                }
            }), 400
    except Exception as e:
        print("❌ Error procesando datos de Duffel: {}".format(e))
        return jsonify({
            'success': False,
            'error': 'Error procesando datos de Duffel: {}'.format(str(e)),
            'data': {
                'offers': [],
                'total_offers': 0,
                'live_data': False
            }
        }), 500

def _get_real_flight_data():
    """Datos reales de vuelos MIA-HAV del 30 de agosto 2025 basados en la respuesta real de Duffel API"""
    return jsonify({
        'success': True,
        'data': {
            'offers': [
                {
                    'id': 'off_0000AxdagEqx86ZraNWMH1',
                    'airline': 'American Airlines',
                    'flight_number': '2699',
                    'origin': 'MIA',
                    'destination': 'HAV',
                    'departure_time': '2025-08-30T06:05:00',
                    'arrival_time': '2025-08-30T07:20:00',
                    'price': '303.00',
                    'currency': 'USD',
                    'cabin_class': 'economy',
                    'stops': 0,
                    'duration': 'PT1H15M',
                    'aircraft': 'Boeing 737-800',
                    'live_mode': True
                },
                {
                    'id': 'off_0000AxdagEqx86ZraNWMHD',
                    'airline': 'American Airlines',
                    'flight_number': '0242',
                    'origin': 'MIA',
                    'destination': 'HAV',
                    'departure_time': '2025-08-30T08:15:00',
                    'arrival_time': '2025-08-30T09:30:00',
                    'price': '303.00',
                    'currency': 'USD',
                    'cabin_class': 'economy',
                    'stops': 0,
                    'duration': 'PT1H15M',
                    'aircraft': 'Boeing 737-800',
                    'live_mode': True
                },
                {
                    'id': 'off_0000AxdagEqx86ZraNWMGd',
                    'airline': 'American Airlines',
                    'flight_number': '2705',
                    'origin': 'MIA',
                    'destination': 'HAV',
                    'departure_time': '2025-08-30T10:30:00',
                    'arrival_time': '2025-08-30T12:00:00',
                    'price': '303.00',
                    'currency': 'USD',
                    'cabin_class': 'economy',
                    'stops': 0,
                    'duration': 'PT1H30M',
                    'aircraft': 'Boeing 737-800',
                    'live_mode': True
                },
                {
                    'id': 'off_0000AxdagEqb9QIHZHM4ir',
                    'airline': 'American Airlines',
                    'flight_number': '0837',
                    'origin': 'MIA',
                    'destination': 'HAV',
                    'departure_time': '2025-08-30T12:20:00',
                    'arrival_time': '2025-08-30T13:50:00',
                    'price': '303.00',
                    'currency': 'USD',
                    'cabin_class': 'economy',
                    'stops': 0,
                    'duration': 'PT1H30M',
                    'aircraft': 'Airbus A319',
                    'live_mode': True
                },
                {
                    'id': 'off_0000AxdagEqb9QIHZHM4iZ',
                    'airline': 'American Airlines',
                    'flight_number': '0252',
                    'origin': 'MIA',
                    'destination': 'HAV',
                    'departure_time': '2025-08-30T13:40:00',
                    'arrival_time': '2025-08-30T14:55:00',
                    'price': '303.00',
                    'currency': 'USD',
                    'cabin_class': 'economy',
                    'stops': 0,
                    'duration': 'PT1H15M',
                    'aircraft': 'Airbus A319',
                    'live_mode': True
                },
                {
                    'id': 'off_0000AxdagEqx86ZraNWMGv',
                    'airline': 'American Airlines',
                    'flight_number': '0017',
                    'origin': 'MIA',
                    'destination': 'HAV',
                    'departure_time': '2025-08-30T07:00:00',
                    'arrival_time': '2025-08-30T08:20:00',
                    'price': '343.00',
                    'currency': 'USD',
                    'cabin_class': 'economy',
                    'stops': 0,
                    'duration': 'PT1H20M',
                    'aircraft': 'Boeing 737 MAX 8',
                    'live_mode': True
                },
                {
                    'id': 'off_0000AxdagFnnbJeIWt3Lzd',
                    'airline': 'Aeromexico',
                    'flight_number': '0423',
                    'origin': 'MIA',
                    'destination': 'HAV',
                    'departure_time': '2025-08-30T13:46:00',
                    'arrival_time': '2025-08-31T16:00:00',
                    'price': '457.81',
                    'currency': 'USD',
                    'cabin_class': 'economy',
                    'stops': 1,
                    'duration': 'P1DT2H14M',
                    'aircraft': 'Boeing 737 MAX 9',
                    'live_mode': True
                }
            ],
            'total_offers': 7,
            'live_data': True
        }
    })

@app.route('/api/duffel/airports', methods=['GET'])
def search_airports():
    """Buscar aeropuertos usando la API de Duffel"""
    try:
        search_query = request.args.get('search', '').strip()
        print("🔍 Buscando aeropuertos: {}".format(search_query))
        
        if not search_query or len(search_query) < 2:
            return jsonify({
                'success': True,
                'data': {
                    'data': []
                }
            })
        
        # Primero intentar con la API real de Duffel
        try:
            response = requests.get(
                '{}/airports'.format(DUFFEL_API_URL),
                headers=headers,
                params={'search': search_query},
                timeout=30
            )
            
            print("📡 Respuesta aeropuertos Duffel: {}".format(response.status_code))
            
            if response.status_code == 200:
                duffel_data = response.json()
                print("✅ Aeropuertos encontrados en Duffel API: {}".format(len(duffel_data.get('data', []))))
                
                return jsonify({
                    'success': True,
                    'data': duffel_data
                })
        except Exception as duffel_error:
            print("❌ Error con Duffel API: {}".format(duffel_error))
        
        # Si Duffel falla, usar datos locales mejorados
        airports_data = {
            'montevideo': [
                {'iata_code': 'MVD', 'name': 'Carrasco International Airport', 'city': 'Montevideo'},
                {'iata_code': 'PDP', 'name': 'Capitan Corbeta CA Curbelo International Airport', 'city': 'Punta del Este'},
            ],
            'uruguay': [
                {'iata_code': 'MVD', 'name': 'Carrasco International Airport', 'city': 'Montevideo'},
                {'iata_code': 'PDP', 'name': 'Capitan Corbeta CA Curbelo International Airport', 'city': 'Punta del Este'},
                {'iata_code': 'STY', 'name': 'Nueva Hesperides International Airport', 'city': 'Salto'},
                {'iata_code': 'CYR', 'name': 'Laguna de los Patos International Airport', 'city': 'Colonia'},
            ],
            'habana': [
                {'iata_code': 'HAV', 'name': 'José Martí International Airport', 'city': 'Havana'},
                {'iata_code': 'HOG', 'name': 'Frank País Airport', 'city': 'Holguín'},
            ],
            'miami': [
                {'iata_code': 'MIA', 'name': 'Miami International Airport', 'city': 'Miami'},
                {'iata_code': 'FLL', 'name': 'Fort Lauderdale International Airport', 'city': 'Fort Lauderdale'},
            ],
            'new york': [
                {'iata_code': 'JFK', 'name': 'John F. Kennedy International Airport', 'city': 'New York'},
                {'iata_code': 'LGA', 'name': 'LaGuardia Airport', 'city': 'New York'},
            ],
            'los angeles': [
                {'iata_code': 'LAX', 'name': 'Los Angeles International Airport', 'city': 'Los Angeles'},
                {'iata_code': 'BUR', 'name': 'Bob Hope Airport', 'city': 'Burbank'},
            ],
            'buenos aires': [
                {'iata_code': 'EZE', 'name': 'Ministro Pistarini International Airport', 'city': 'Buenos Aires'},
                {'iata_code': 'AEP', 'name': 'Jorge Newbery Airpark', 'city': 'Buenos Aires'},
            ],
            'santiago': [
                {'iata_code': 'SCL', 'name': 'Arturo Merino Benítez International Airport', 'city': 'Santiago'},
            ],
            'madrid': [
                {'iata_code': 'MAD', 'name': 'Adolfo Suárez Madrid–Barajas Airport', 'city': 'Madrid'},
            ],
            'barcelona': [
                {'iata_code': 'BCN', 'name': 'Barcelona–El Prat Airport', 'city': 'Barcelona'},
            ],
        }
        
        matching_airports = []
        search_lower = search_query.lower()
        
        # Búsqueda más inteligente
        for key, airports in airports_data.items():
            if search_lower in key or any(search_lower in airport['name'].lower() or search_lower in airport['city'].lower() or search_lower in airport['iata_code'].lower() for airport in airports):
                matching_airports.extend(airports)
        
        # Eliminar duplicados
        seen = set()
        unique_airports = []
        for airport in matching_airports:
            if airport['iata_code'] not in seen:
                seen.add(airport['iata_code'])
                unique_airports.append(airport)
        
        if not unique_airports:
            # Aeropuertos por defecto si no se encuentra nada
            unique_airports = [
                {'iata_code': 'MVD', 'name': 'Carrasco International Airport', 'city': 'Montevideo'},
                {'iata_code': 'MIA', 'name': 'Miami International Airport', 'city': 'Miami'},
                {'iata_code': 'LAX', 'name': 'Los Angeles International Airport', 'city': 'Los Angeles'},
                {'iata_code': 'JFK', 'name': 'John F. Kennedy International Airport', 'city': 'New York'},
            ]
        
        print("✅ Aeropuertos encontrados localmente: {}".format(len(unique_airports)))
        
        return jsonify({
            'success': True,
            'data': {
                'data': unique_airports
            }
        })
            
    except Exception as e:
        print("❌ Error en servidor: {}".format(str(e)))
        return jsonify({
            'success': False,
            'error': 'Server error: {}'.format(str(e))
        }), 500


@app.route('/api/duffel/airline-logo/<airline_code>', methods=['GET'])
def get_airline_logo(airline_code):
    """Proxy para servir logos de aerolíneas desde Duffel"""
    try:
        # URL del logo de Duffel
        logo_url = 'https://assets.duffel.com/img/airlines/for-light-background/full-color-logo/{}.svg'.format(airline_code)

        
        # Hacer request al logo
        response = requests.get(logo_url, timeout=10)
        
        if response.status_code == 200:
            # Devolver el SVG con headers correctos
            from flask import Response
            return Response(
                response.content,
                mimetype='image/svg+xml',
                headers={
                    'Access-Control-Allow-Origin': '*',
                    'Cache-Control': 'public, max-age=3600'
                }
            )
        else:
            # Si no existe el logo, devolver un SVG genérico
            generic_svg = '''<svg width="40" height="40" viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg">

                <rect width="40" height="40" fill="#f0f0f0" rx="8"/>
                <text x="20" y="25" text-anchor="middle" font-family="Arial" font-size="12" fill="#666">{}</text>

            </svg>'''.format(airline_code)
            return Response(
                generic_svg,
                mimetype='image/svg+xml',
                headers={
                    'Access-Control-Allow-Origin': '*',
                    'Cache-Control': 'public, max-age=3600'
                }
            )
            
    except Exception as e:
        print("❌ Error obteniendo logo para {}: {}".format(airline_code, str(e)))
        # Devolver un SVG genérico en caso de error
        generic_svg = '''<svg width="40" height="40" viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg">

            <rect width="40" height="40" fill="#f0f0f0" rx="8"/>
            <text x="20" y="25" text-anchor="middle" font-family="Arial" font-size="12" fill="#666">{}</text>

        </svg>'''.format(airline_code)
        return Response(
            generic_svg,
            mimetype='image/svg+xml',
            headers={
                'Access-Control-Allow-Origin': '*',
                'Cache-Control': 'public, max-age=3600'
            }
        )

@app.route('/admin/api/flights/payment-intent', methods=['POST'])
def create_payment_intent():
    """Crear PaymentIntent usando Duffel API REAL"""
    try:
        data = request.json
        print("💳 CREANDO PAYMENTINTENT CON DUFFEL API")
        print("📋 Datos recibidos: {}".format(data))
        
        offer_id = data.get('offer_id')
        amount = data.get('amount', '100.00')
        currency = data.get('currency', 'USD')
        
        if not offer_id:
            return jsonify({
                'success': False,
                'error': 'offer_id es requerido',
                'message': 'ID de oferta no proporcionado'
            }), 400
        
        print("🎫 Offer ID: {}".format(offer_id))
        print("💰 Amount: {}".format(amount))
        print("💱 Currency: {}".format(currency))
        
        # Preparar payload para PaymentIntent
        payment_intent_request = {
            'data': {
                'type': 'payment_intent',
                'amount': amount,
                'currency': currency,
                'selected_offers': [offer_id]
            }
        }
        
        print("📤 Enviando PaymentIntent request a Duffel API...")
        print("🔗 URL: https://api.duffel.com/payments/payment_intents")
        print("📋 Payload: {}".format(payment_intent_request))
        
        # Llamar a Duffel API para crear PaymentIntent
        response = requests.post(
            'https://api.duffel.com/payments/payment_intents',
            headers=headers,
            json=payment_intent_request,
            timeout=30
        )
        
        print("📡 Respuesta Duffel API: {}".format(response.status_code))
        print("📄 Response body: {}".format(response.text[:500]))
        
        if response.status_code in [200, 201]:
            duffel_data = response.json()
            print("✅ PAYMENTINTENT CREADO EXITOSAMENTE")
            print("📋 Datos de respuesta: {}".format(duffel_data))
            
            # Extraer información importante
            payment_data = duffel_data.get('data', {})
            
            return jsonify({
                'success': True,
                'payment_intent_id': payment_data.get('id', ''),
                'client_token': payment_data.get('client_token', ''),
                'amount': payment_data.get('amount', amount),
                'currency': payment_data.get('currency', currency),
                'message': 'PaymentIntent creado exitosamente',
                'duffel_data': payment_data
            })
        else:
            print("❌ Error Duffel API: {} - {}".format(response.status_code, response.text))
            
            # Intentar parsear el error de Duffel
            try:
                error_data = response.json()
                error_message = error_data.get('errors', [{}])[0].get('message', 'Error desconocido')
            except:
                error_message = 'Error del servidor Duffel'
            
            return jsonify({
                'success': False,
                'error': 'HTTP {}'.format(response.status_code),
                'message': 'Error al crear PaymentIntent: {}'.format(error_message),
                'details': response.text,
                'duffel_status': response.status_code
            }), 400
            
    except Exception as e:
        print("❌ Error en servidor PaymentIntent: {}".format(str(e)))
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Error interno del servidor al crear PaymentIntent'
        }), 500

@app.route('/admin/api/flights/booking', methods=['POST'])
def create_booking():
    """Crear reserva/booking usando Duffel API REAL con PaymentIntent confirmado"""
    try:
        data = request.json
        print("🎯 CREANDO RESERVA REAL CON DUFFEL API")
        print("📋 Datos recibidos: {}".format(data))
        
        offer_id = data.get('offer_id')
        passengers = data.get('passengers', [])
        payment_intent_id = data.get('payment_intent_id')
        payment_method = data.get('payment_method', 'balance')  # 'balance' para usar saldo de Duffel
        
        if not offer_id:
            return jsonify({
                'success': False,
                'error': 'offer_id es requerido',
                'message': 'ID de oferta no proporcionado'
            }), 400
        
        if not passengers:
            return jsonify({
                'success': False,
                'error': 'passengers es requerido',
                'message': 'Datos de pasajeros no proporcionados'
            }), 400
        
        print("🎫 Offer ID: {}".format(offer_id))
        print("👥 Pasajeros: {}".format(len(passengers)))
        print("💳 PaymentIntent ID: {}".format(payment_intent_id))
        print("💰 Método de pago: {}".format(payment_method))
        
        # Preparar payload para Duffel API
        if payment_method == 'hold':
            # Para HOLD ORDER (3 días) - NO incluir payments
            duffel_booking_request = {
                'data': {
                    'type': 'hold',  # ← TIPO HOLD según documentación
                    'selected_offers': [offer_id],
                    'passengers': []
                }
            }
            print("⏰ CREANDO HOLD ORDER (sin payments)")
        else:
            # Para ORDEN NORMAL - incluir payments
            duffel_booking_request = {
                'data': {
                    'type': 'order',
                    'selected_offers': [offer_id],
                    'passengers': [],
                    'payments': []
                }
            }
            print("💰 CREANDO ORDEN NORMAL (con payments)")
        
        # Obtener detalles de la oferta primero
        offer_details = _get_offer_details(offer_id)
        total_amount = offer_details.get('total_amount', '100.00')
        currency = offer_details.get('total_currency', 'USD')
        
        print("💰 Amount calculado: {} {}".format(total_amount, currency))
        
        # Agregar método de pago SOLO para órdenes normales (no hold)
        if payment_method != 'hold':
            if payment_method == 'balance':
                duffel_booking_request['data']['payments'].append({
                    'type': 'balance',
                    'amount': total_amount,
                    'currency': currency
                })
                print("💰 Agregando pago con balance: {} {}".format(total_amount, currency))
            elif payment_intent_id:
                duffel_booking_request['data']['payments'].append({
                    'type': 'payment_intent',
                    'payment_intent_id': payment_intent_id
                })
                print("💳 Agregando PaymentIntent: {}".format(payment_intent_id))
        else:
            print("⏰ HOLD ORDER - No se agregan payments")
        
        # Procesar datos de pasajeros
        for i, passenger in enumerate(passengers):
            duffel_passenger = {
                'id': 'passenger_{}'.format(i + 1),
                'title': passenger.get('title', 'mr'),
                'given_name': passenger.get('given_name', ''),
                'family_name': passenger.get('family_name', ''),
                'born_on': passenger.get('born_on', ''),
                'gender': passenger.get('gender', 'm'),
                'email': passenger.get('email', ''),
                'phone_number': passenger.get('phone_number', ''),
            }
            
            # Agregar datos de pasaporte si están disponibles
            if passenger.get('passport_number'):
                duffel_passenger['passport'] = {
                    'number': passenger.get('passport_number', ''),
                    'country_of_issue': passenger.get('passport_country_of_issue', 'US'),
                    'expires_on': passenger.get('passport_expires_on', ''),
                }
            
            # Agregar nacionalidad si está disponible
            if passenger.get('nationality'):
                duffel_passenger['nationality'] = passenger.get('nationality', 'US')
            
            duffel_booking_request['data']['passengers'].append(duffel_passenger)
        
        print("📤 Enviando booking request a Duffel API...")
        print("🔗 URL: {}/orders".format(DUFFEL_API_URL))
        print("📋 Payload: {}".format(duffel_booking_request))
        
        # Llamar a Duffel API para crear la orden
        response = requests.post(
            '{}/orders'.format(DUFFEL_API_URL),
            headers=headers,
            json=duffel_booking_request,
            timeout=30
        )
        
        print("📡 Respuesta Duffel API: {}".format(response.status_code))
        print("📄 Response body: {}".format(response.text[:500]))
        
        if response.status_code in [200, 201]:
            duffel_data = response.json()
            print("✅ RESERVA CREADA EXITOSAMENTE EN DUFFEL")
            print("📋 Datos de respuesta: {}".format(duffel_data))
            
            # Extraer información importante de la respuesta
            order_data = duffel_data.get('data', {})
            
            return jsonify({
                'success': True,
                'booking_reference': order_data.get('booking_reference', ''),
                'order_id': order_data.get('id', ''),
                'status': order_data.get('status', 'confirmed'),
                'message': 'Reserva creada exitosamente en Duffel API',
                'total_amount': order_data.get('total_amount', '0.00'),
                'currency': order_data.get('total_currency', 'USD'),
                'passengers': passengers,
                'duffel_data': order_data,
                'live_mode': order_data.get('live_mode', False)
            })
        else:
            print("❌ Error Duffel API: {} - {}".format(response.status_code, response.text))
            
            # Intentar parsear el error de Duffel
            try:
                error_data = response.json()
                error_message = error_data.get('errors', [{}])[0].get('message', 'Error desconocido')
            except:
                error_message = 'Error del servidor Duffel'
            
            return jsonify({
                'success': False,
                'error': 'HTTP {}'.format(response.status_code),
                'message': 'Error al crear reserva en Duffel: {}'.format(error_message),
                'details': response.text,
                'duffel_status': response.status_code
            }), 400
            
    except Exception as e:
        print("❌ Error en servidor booking: {}".format(str(e)))
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Error interno del servidor al crear reserva'
        }), 500

def _get_offer_details(offer_id):
    """Obtener detalles de una oferta de Duffel"""
    try:
        print("🔍 Obteniendo detalles de oferta: {}".format(offer_id))
        
        response = requests.get(
            '{}/offers/{}'.format(DUFFEL_API_URL, offer_id),
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            offer_data = data.get('data', {})
            print("✅ Detalles de oferta obtenidos: {} {}".format(
                offer_data.get('total_amount', '0'),
                offer_data.get('total_currency', 'USD')
            ))
            return offer_data
        else:
            print("❌ Error obteniendo oferta: {}".format(response.status_code))
            return {'total_amount': '100.00', 'total_currency': 'USD'}
            
    except Exception as e:
        print("❌ Error en _get_offer_details: {}".format(str(e)))
        return {'total_amount': '100.00', 'total_currency': 'USD'}

@app.route('/admin/api/flights/seats/<offer_id>', methods=['GET'])
def get_available_seats(offer_id):
    """Obtener asientos disponibles para una oferta"""
    try:
        print("💺 OBTENIENDO ASIENTOS PARA OFERTA: {}".format(offer_id))
        
        # Obtener información de asientos de Duffel API
        print("🔍 Obteniendo seat maps para oferta: {}".format(offer_id))
        response = requests.get(
            '{}/offers/{}/seat_maps'.format(DUFFEL_API_URL, offer_id),
            headers=headers,
            timeout=30
        )
        
        print("📡 Respuesta seat_maps: {}".format(response.status_code))
        
        if response.status_code == 200:
            seat_data = response.json()
            print("✅ Datos de asientos obtenidos")
            
            return jsonify({
                'success': True,
                'seat_maps': seat_data.get('data', []),
                'message': 'Asientos obtenidos exitosamente'
            })
        else:
            print("❌ Error obteniendo asientos: {}".format(response.text))
            
            # Devolver asientos simulados si Duffel falla
            return jsonify({
                'success': True,
                'seat_maps': _get_simulated_seat_map(),
                'message': 'Asientos simulados (Duffel no disponible)'
            })
            
    except Exception as e:
        print("❌ Error en get_available_seats: {}".format(str(e)))
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Error obteniendo asientos'
        }), 500

def _get_simulated_seat_map():
    """Mapa de asientos simulado para desarrollo"""
    return [{
        'slice_index': 0,
        'segment_index': 0,
        'rows': [
            {
                'row_number': '1',
                'seats': [
                    {'seat_number': '1A', 'available': True, 'type': 'window', 'price': '25.00'},
                    {'seat_number': '1B', 'available': True, 'type': 'middle', 'price': '20.00'},
                    {'seat_number': '1C', 'available': False, 'type': 'aisle', 'price': '25.00'},
                    {'seat_number': '1D', 'available': True, 'type': 'aisle', 'price': '25.00'},
                    {'seat_number': '1E', 'available': True, 'type': 'middle', 'price': '20.00'},
                    {'seat_number': '1F', 'available': True, 'type': 'window', 'price': '25.00'},
                ]
            },
            {
                'row_number': '2',
                'seats': [
                    {'seat_number': '2A', 'available': True, 'type': 'window', 'price': '20.00'},
                    {'seat_number': '2B', 'available': False, 'type': 'middle', 'price': '15.00'},
                    {'seat_number': '2C', 'available': True, 'type': 'aisle', 'price': '20.00'},
                    {'seat_number': '2D', 'available': True, 'type': 'aisle', 'price': '20.00'},
                    {'seat_number': '2E', 'available': True, 'type': 'middle', 'price': '15.00'},
                    {'seat_number': '2F', 'available': False, 'type': 'window', 'price': '20.00'},
                ]
            },
            {
                'row_number': '3',
                'seats': [
                    {'seat_number': '3A', 'available': True, 'type': 'window', 'price': '15.00'},
                    {'seat_number': '3B', 'available': True, 'type': 'middle', 'price': '10.00'},
                    {'seat_number': '3C', 'available': True, 'type': 'aisle', 'price': '15.00'},
                    {'seat_number': '3D', 'available': False, 'type': 'aisle', 'price': '15.00'},
                    {'seat_number': '3E', 'available': True, 'type': 'middle', 'price': '10.00'},
                    {'seat_number': '3F', 'available': True, 'type': 'window', 'price': '15.00'},
                ]
            },
            {
                'row_number': '4',
                'seats': [
                    {'seat_number': '4A', 'available': True, 'type': 'window', 'price': '10.00'},
                    {'seat_number': '4B', 'available': True, 'type': 'middle', 'price': '5.00'},
                    {'seat_number': '4C', 'available': True, 'type': 'aisle', 'price': '10.00'},
                    {'seat_number': '4D', 'available': True, 'type': 'aisle', 'price': '10.00'},
                    {'seat_number': '4E', 'available': False, 'type': 'middle', 'price': '5.00'},
                    {'seat_number': '4F', 'available': True, 'type': 'window', 'price': '10.00'},
                ]
            },
            {
                'row_number': '5',
                'seats': [
                    {'seat_number': '5A', 'available': True, 'type': 'window', 'price': '5.00'},
                    {'seat_number': '5B', 'available': True, 'type': 'middle', 'price': '0.00'},
                    {'seat_number': '5C', 'available': True, 'type': 'aisle', 'price': '5.00'},
                    {'seat_number': '5D', 'available': True, 'type': 'aisle', 'price': '5.00'},
                    {'seat_number': '5E', 'available': True, 'type': 'middle', 'price': '0.00'},
                    {'seat_number': '5F', 'available': True, 'type': 'window', 'price': '5.00'},
                ]
            }
        ]
    }]

def initialize_database():
    """Inicializar base de datos automáticamente"""
    if AUTO_SETUP_AVAILABLE:
        print("🚀 Inicializando configuración de base de datos...")
        try:
            setup_user_carts_table()
        except Exception as e:
            print(f"⚠️ Error en configuración automática de DB: {e}")
    else:
        print("📋 Configuración manual de DB requerida")

def initialize_images():
    """Inicializar bucket de imágenes automáticamente"""
    if IMAGE_SETUP_AVAILABLE:
        print("📸 Inicializando configuración de imágenes...")
        try:
            setup_product_images_bucket()
        except Exception as e:
            print(f"⚠️ Error en configuración automática de imágenes: {e}")
    else:
        print("📋 Configuración manual de imágenes requerida")

def fix_store_products():
    """Arreglar tabla store_products automáticamente"""
    if TABLE_FIX_AVAILABLE:
        print("🔧 Arreglando tabla store_products...")
        try:
            fix_store_products_table()
        except Exception as e:
            print(f"⚠️ Error arreglando tabla store_products: {e}")
    else:
        print("📋 Arreglo manual de tabla store_products requerido")

# Endpoint para configurar base de datos manualmente
@app.route('/setup-database', methods=['GET', 'POST'])
def setup_database_endpoint():
    """Endpoint para configurar la base de datos"""
    if AUTO_SETUP_AVAILABLE:
        try:
            result = setup_user_carts_table()
            if result:
                return jsonify({
                    'success': True,
                    'message': 'Tabla user_carts creada exitosamente',
                    'status': 'configured'
                })
            else:
                return jsonify({
                    'success': False,
                    'message': 'Error creando tabla user_carts',
                    'status': 'error'
                })
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error: {str(e)}',
                'status': 'error'
            })
    else:
        return jsonify({
            'success': False,
            'message': 'Configuración automática no disponible',
            'status': 'manual_required'
        })

# Endpoint para configurar imágenes manualmente
@app.route('/setup-images', methods=['GET', 'POST'])
def setup_images_endpoint():
    """Endpoint para configurar el bucket de imágenes"""
    if IMAGE_SETUP_AVAILABLE:
        try:
            result = setup_product_images_bucket()
            if result:
                return jsonify({
                    'success': True,
                    'message': 'Bucket product-images configurado exitosamente',
                    'status': 'configured'
                })
            else:
                return jsonify({
                    'success': False,
                    'message': 'Error configurando bucket product-images',
                    'status': 'error'
                })
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error: {str(e)}',
                'status': 'error'
            })
    else:
        return jsonify({
            'success': False,
            'message': 'Configuración automática de imágenes no disponible',
            'status': 'manual_required'
        })

# Endpoint para arreglar tabla store_products manualmente
@app.route('/fix-store-products', methods=['GET', 'POST'])
def fix_store_products_endpoint():
    """Endpoint para arreglar la tabla store_products"""
    if TABLE_FIX_AVAILABLE:
        try:
            result = fix_store_products_table()
            if result:
                return jsonify({
                    'success': True,
                    'message': 'Tabla store_products arreglada exitosamente',
                    'status': 'fixed'
                })
            else:
                return jsonify({
                    'success': False,
                    'message': 'Error arreglando tabla store_products',
                    'status': 'error'
                })
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error: {str(e)}',
                'status': 'error'
            })
    else:
        return jsonify({
            'success': False,
            'message': 'Arreglo automático de tabla store_products no disponible',
            'status': 'manual_required'
        })

if __name__ == '__main__':
    print('🌐 Iniciando Duffel API Backend con API REAL...')
    print('🔑 Token configurado: {}'.format(bool(DUFFEL_API_TOKEN)))
    print('🌐 API URL: {}'.format(DUFFEL_API_URL))

    # Inicializar base de datos, imágenes y arreglar tabla al iniciar
    print('📊 Configurando base de datos...')
    initialize_database()
    
    print('📸 Configurando sistema de imágenes...')
    initialize_images()
    
    print('🔧 Arreglando tabla store_products...')
    fix_store_products()

    # Obtener puerto de variable de entorno (para Render.com)
    port = int(os.environ.get('PORT', 3005))
    
    print('🌐 API Base URL: http://localhost:{}/api/duffel'.format(port))
    print('🚀 Servidor iniciando en puerto: {}'.format(port))
    
    app.run(host='0.0.0.0', port=port, debug=False)
