import requests
import json
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class DuffelService:
    def __init__(self):
        # 🔑 API Key desde variable de entorno
        self.api_token = os.environ.get('DUFFEL_API_KEY', '')
        if not self.api_token:
            raise ValueError("❌ DUFFEL_API_KEY no configurada en variables de entorno")
        self.api_url = 'https://api.duffel.com'
        self.headers = {
            'Authorization': f'Bearer {self.api_token}',
            'Content-Type': 'application/json',
            'Duffel-Version': 'v1',
            'Accept': 'application/json'
        }
        print(f"🔑 DuffelService inicializado")

    def search_airports(self, query):
        """
        🏢 Buscar aeropuertos usando la API real de Duffel
        """
        try:
            print(f"🔍 Buscando aeropuertos: '{query}'")
            
            # Endpoint para buscar aeropuertos
            url = f'{self.api_url}/air/airports'
            params = {
                'name': query,
                'limit': 10
            }
            
            response = requests.get(url, headers=self.headers, params=params)
            print(f"📡 Status API Duffel airports: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                airports = []
                
                if 'data' in data:
                    for airport in data['data']:
                        airport_info = {
                            'iata_code': airport.get('iata_code', ''),
                            'name': airport.get('name', ''),
                            'city': airport.get('city', {}).get('name', ''),
                            'country': airport.get('city', {}).get('country', {}).get('name', ''),
                            'display_name': f"{airport.get('name', '')} ({airport.get('iata_code', '')})"
                        }
                        airports.append(airport_info)
                        print(f"✈️ Aeropuerto encontrado: {airport_info['display_name']}")
                
                print(f"✅ Total aeropuertos encontrados: {len(airports)}")
                return airports
            else:
                print(f"❌ Error API Duffel airports: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"❌ Error buscando aeropuertos: {str(e)}")
            return []

    def search_flights(self, origin, destination, departure_date, passengers=1, cabin_class='economy'):
        """⚙️
        ✈️ Buscar vuelos usando la API real de Duffel
        """
        try:
            print(f"🔍 Buscando vuelos: {origin} → {destination} el {departure_date}")
            
            passengers_input = passengers
            passengers_data = []
            passengers_count = 0

            if isinstance(passengers_input, dict):
                adults = int(passengers_input.get('adults', 0) or 0)
                seniors = int(passengers_input.get('seniors', 0) or 0)
                children = int(passengers_input.get('children', 0) or 0)
                infants = int(passengers_input.get('infants', 0) or 0)
                passengers_count = adults + seniors + children + infants

                if adults + seniors <= 0:
                    raise ValueError('Debe existir al menos un pasajero adulto')

                for _ in range(max(adults + seniors, 0)):
                    passengers_data.append({'type': 'adult'})
                for _ in range(max(children, 0)):
                    passengers_data.append({'type': 'child'})
                for _ in range(max(infants, 0)):
                    passengers_data.append({'type': 'infant_without_seat'})

            elif isinstance(passengers_input, list):
                passengers_data = passengers_input
                passengers_count = len(passengers_data)

                has_adult = any(
                    isinstance(p, dict) and p.get('type') in {'adult', 'adult_with_seat', 'adult_fare'}
                    for p in passengers_data
                )
                if not has_adult:
                    raise ValueError('Debe existir al menos un pasajero adulto')

            else:
                try:
                    passengers_count = int(passengers_input)
                except (ValueError, TypeError):
                    passengers_count = 1
                passengers_count = max(passengers_count, 1)
                passengers_data = [{'type': 'adult'} for _ in range(passengers_count)]

            if passengers_count <= 0:
                raise ValueError('Debe existir al menos un pasajero')

            # Crear offer request
            url = f'{self.api_url}/air/offer_requests'
            
            payload = {
                "data": {
                    "slices": [
                        {
                            "origin": origin,
                            "destination": destination,
                            "departure_date": departure_date
                        }
                    ],
                    "passengers": passengers_data,
                    "cabin_class": cabin_class
                }
            }
            
            print(f"📤 Enviando request a Duffel...")
            response = requests.post(url, headers=self.headers, json=payload)
            print(f"📡 Status API Duffel: {response.status_code}")
            
            if response.status_code == 201:  # Created
                offer_request = response.json()
                offer_request_id = offer_request['data']['id']
                print(f"✅ Offer request creado: {offer_request_id}")
                
                # Obtener ofertas
                offers_url = f'{self.api_url}/air/offers'
                params = {'offer_request_id': offer_request_id}
                
                print(f"📥 Obteniendo ofertas...")
                offers_response = requests.get(offers_url, headers=self.headers, params=params)
                print(f"📡 Status ofertas: {offers_response.status_code}")
                
                if offers_response.status_code == 200:
                    offers_data = offers_response.json()
                    flights = []
                    
                    if 'data' in offers_data:
                        for offer in offers_data['data']:
                            try:
                                # Extraer información del primer slice (ida)
                                first_slice = offer['slices'][0]
                                segments = first_slice['segments']
                                first_segment = segments[0]
                                last_segment = segments[-1]
                                
                                # Extraer origen y destino
                                origin = first_segment['origin']['iata_code']
                                destination = last_segment['destination']['iata_code']
                                
                                # Extraer información de la aerolínea - USAR ESTRUCTURA CORRECTA
                                marketing_carrier = first_segment.get('marketing_carrier', {})
                                operating_carrier = first_segment.get('operating_carrier', {})
                                aircraft = first_segment.get('aircraft', {})
                                
                                # Priorizar marketing_carrier, fallback a operating_carrier
                                airline_name = marketing_carrier.get('name') or operating_carrier.get('name', 'Aerolínea Desconocida')
                                airline_code = marketing_carrier.get('iata_code') or operating_carrier.get('iata_code', '')
                                
                                print(f"🏢 Aerolínea encontrada: {airline_name} ({airline_code})")
                                
                                # Extraer logo de la aerolínea - USAR PNG en lugar de SVG para compatibilidad Android
                                logo_url = marketing_carrier.get('logo_symbol_url') or operating_carrier.get('logo_symbol_url', '')
                                # Convertir SVG a PNG para compatibilidad Android
                                airline_logo = logo_url.replace('.svg', '.png') if logo_url else ''
                                print(f"🖼️ Logo convertido: {logo_url} → {airline_logo}")
                                
                                flight_info = {
                                    'id': offer.get('id'),
                                    'type': 'duffel_real',
                                    'airline': airline_name,
                                    'airline_code': airline_code,
                                    'airline_logo': airline_logo,
                                    'flight_number': first_segment.get('marketing_airline_flight_number', '') or first_segment.get('operating_airline_flight_number', ''),
                                    'aircraft': aircraft.get('name', ''),
                                    'origin': origin,
                                    'destination': destination,
                                    'departure_time': first_segment.get('departing_at'),
                                    'arrival_time': last_segment.get('arriving_at'),
                                    'duration': first_slice.get('duration'),
                                    'price': float(offer.get('total_amount', 0)),
                                    'currency': offer.get('total_currency', 'USD'),
                                    'available_seats': 9,
                                    'refundable': True,
                                    'changeable': True,
                                    'stops': len(segments) - 1,
                                    'cabin_class': offer.get('cabin_class', cabin_class),
                                }
                                
                                flights.append(flight_info)
                                print(f"✅ Vuelo procesado: {airline_name} ${flight_info['price']} {flight_info['currency']}")
                                
                            except Exception as e:
                                print(f"❌ Error procesando oferta: {str(e)}")
                                continue
                    
                    print(f"🎯 Total vuelos encontrados: {len(flights)}")
                    return flights
                else:
                    print(f"❌ Error obteniendo ofertas: {offers_response.status_code}")
                    return []
            else:
                print(f"❌ Error creando offer request: {response.status_code}")
                print(f"Response: {response.text}")
                return []
                
        except Exception as e:
            print(f"❌ Error buscando vuelos: {str(e)}")
            return []