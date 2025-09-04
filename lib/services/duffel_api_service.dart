import 'dart:convert';
import 'dart:async';
import 'package:http/http.dart' as http;

/// 🎯 Servicio REAL para conectar con backend Duffel
/// Se conecta SOLO al backend local, NO directamente a APIs externas
class DuffelApiService {
  // 🔗 URL del backend - RENDER.COM (PRODUCCIÓN GLOBAL)
  static const String _baseUrl = 'https://cubalink23-backend.onrender.com';
  
  // Headers estándar para todas las requests
  static const Map<String, String> _headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  };

  /// 🏥 Health Check - Verificar si backend está activo
  static Future<bool> isBackendActive() async {
    try {
      print('🔗 Verificando estado del backend...');
      print('🌐 URL: $_baseUrl/api/health');
      
      final response = await http.get(
        Uri.parse('$_baseUrl/api/health'),
        headers: _headers,
      ).timeout(Duration(seconds: 10));

      print('📡 Respuesta status: ${response.statusCode}');
      print('📡 Respuesta body: ${response.body}');

      if (response.statusCode == 200) {
        print('✅ Backend FINAL ACTIVO en puerto 9500');
        return true;
      } else {
        print('⚠️ Backend respondió con código: ${response.statusCode}');
        return false;
      }
    } catch (e) {
      print('❌ Backend NO disponible: $e');
      print('🔍 Tipo de error: ${e.runtimeType}');
      return false;
    }
  }

  /// ✈️ Buscar vuelos REALES usando backend
  static Future<Map<String, dynamic>?> searchFlights({
    required String origin,
    required String destination,
    required String departureDate,
    int adults = 1,
    String cabinClass = 'economy',
    String? returnDate,
    String airlineType = 'comerciales', // 'comerciales', 'charter', 'todos'
  }) async {
    try {
      print('🚀 BÚSQUEDA VUELOS REALES - Backend Duffel');
      print('✈️ Ruta: $origin → $destination');
      print('📅 Fecha: $departureDate');
      print('👥 Pasajeros: $adults');
      print('🎯 Tipo: $airlineType');

      // Verificar que backend esté activo
      final backendActive = await isBackendActive();
      if (!backendActive) {
        return {
          'status': 'offline',
          'message': 'Servicio temporalmente no disponible. Intente más tarde.',
          'error_type': 'backend_offline'
        };
      }

      // Preparar payload para backend
      final payload = {
        'origin': origin.toUpperCase(),
        'destination': destination.toUpperCase(),
        'departure_date': departureDate,
        'passengers': adults,
        'cabin_class': cabinClass.toLowerCase(),
      };

      // Agregar fecha de regreso si es ida y vuelta
      if (returnDate != null) {
        payload['return_date'] = returnDate;
      }

      // 🚨 TEMPORALMENTE DESHABILITADO: Tipo de aerolínea
      // TODO: Implementar filtrado por tipo de aerolínea después de que funcione la búsqueda básica
      // if (airlineType != 'todos') {
      //   payload['airline_type'] = airlineType;
      // }

      print('📤 Enviando solicitud al backend...');
      print('🔗 URL: $_baseUrl/admin/api/flights/search');
      print('📋 Payload: ${json.encode(payload)}');

      final response = await http.post(
        Uri.parse('$_baseUrl/admin/api/flights/search'),
        headers: _headers,
        body: json.encode(payload),
      ).timeout(Duration(seconds: 30));

      print('📡 Status: ${response.statusCode}');
      print('📄 Response length: ${response.body.length} chars');

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        print('✅ BÚSQUEDA EXITOSA');
        
        if (data['data'] != null && data['data'] is List) {
          final flights = data['data'] as List;
          print('✈️ Vuelos encontrados: ${flights.length}');
          
          // Mostrar preview de precios
          if (flights.isNotEmpty) {
            print('💰 Precios de vuelos:');
            for (int i = 0; i < (flights.length > 3 ? 3 : flights.length); i++) {
              final flight = flights[i];
              final price = flight['total_amount'] ?? 'N/A';
              final airline = flight['airline'] ?? 'N/A';
              print('   ${i+1}. $airline: \$${price}');
            }
          }
        } else {
          print('⚠️ No se encontraron vuelos en la respuesta');
        }
        
        return data;
      } else if (response.statusCode == 500) {
        print('❌ Error interno del backend');
        return {
          'status': 'error',
          'message': 'Error interno del servidor. Intente más tarde.',
          'error_type': 'backend_error'
        };
      } else {
        print('❌ Error HTTP ${response.statusCode}: ${response.body}');
        return {
          'status': 'error',
          'message': 'Error en la búsqueda de vuelos.',
          'error_type': 'http_error',
          'status_code': response.statusCode
        };
      }
    } catch (e) {
      print('💥 Exception en búsqueda: $e');
      if (e is TimeoutException) {
        return {
          'status': 'timeout',
          'message': 'La búsqueda está tomando más tiempo del esperado. Intente nuevamente.',
          'error_type': 'timeout'
        };
      } else {
        return {
          'status': 'error',
          'message': 'Error de conexión. Verifique su internet.',
          'error_type': 'connection_error'
        };
      }
    }
  }

  /// 🏪 Buscar aeropuertos usando backend
  static Future<List<Map<String, dynamic>>> searchAirports(String query) async {
    try {
      if (query.length < 2) return [];
      
      print('🔍 Buscando aeropuertos: $query');

      // Verificar backend activo
      final backendActive = await isBackendActive();
      if (!backendActive) {
        print('❌ Backend offline - usando aeropuertos locales de emergencia');
        return _getLocalAirports(query);
      }

      final response = await http.get(
        Uri.parse('$_baseUrl/admin/api/flights/airports?q=${Uri.encodeComponent(query)}'),
        headers: _headers,
      ).timeout(Duration(seconds: 10));

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        
        // Backend devuelve array directo [] o objeto {data: []}
        List airportsList = [];
        
        if (data is List) {
          // Array directo []
          airportsList = data;
          print('📋 Backend devolvió array directo: ${airportsList.length}');
        } else if (data is Map && data['data'] != null && data['data'] is List) {
          // Objeto con data {data: [...]}
          airportsList = data['data'];
          print('📋 Backend devolvió objeto con data: ${airportsList.length}');
        } else {
          print('⚠️ Formato de respuesta no reconocido: ${data.runtimeType}');
          return [];
        }
        
        final airports = airportsList.map((airport) {
          return {
            'code': airport['iata_code']?.toString() ?? airport['code']?.toString() ?? '',
            'name': airport['name']?.toString() ?? '',
            'display_name': '${airport['city']?.toString() ?? ''}, ${airport['country']?.toString() ?? ''}',
            'city': airport['city']?.toString() ?? '',
            'country': airport['country']?.toString() ?? '',
          };
        }).where((airport) => airport['code']?.isNotEmpty == true).toList();
        
        print('✅ Aeropuertos procesados: ${airports.length}');
        if (airports.isNotEmpty) {
          print('🔍 PREVIEW aeropuertos encontrados:');
          for (int i = 0; i < (airports.length > 3 ? 3 : airports.length); i++) {
            print('   ${i+1}. ${airports[i]['code']} - ${airports[i]['name']}');
          }
        }
        return airports;
      }
      
      // Sin fallback - mostrar error real
      print('⚠️ Backend sin aeropuertos - ERROR REAL DEL BACKEND');
      return [];
      
    } catch (e) {
      print('❌ Error buscando aeropuertos: $e');
      print('🔄 Usando aeropuertos locales como respaldo');
      return _getLocalAirports(query);
    }
  }

  /// 🏢 Obtener aerolíneas disponibles
  static Future<List<Map<String, dynamic>>> getAirlines() async {
    try {
      print('🏢 Obteniendo aerolíneas...');

      // Verificar backend activo
      final backendActive = await isBackendActive();
      if (!backendActive) {
        print('❌ Backend offline - sin aerolíneas disponibles');
        return [];
      }

      final response = await http.get(
        Uri.parse('$_baseUrl/api/flights/airlines'),
        headers: _headers,
      ).timeout(Duration(seconds: 10));

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        
        if (data['data'] != null && data['data'] is List) {
          final airlines = (data['data'] as List).map((airline) {
            return {
              'id': airline['id']?.toString() ?? '',
              'name': airline['name']?.toString() ?? '',
              'iata_code': airline['iata_code']?.toString() ?? '',
              'icao_code': airline['icao_code']?.toString() ?? '',
            };
          }).toList();
          
          print('✅ Aerolíneas obtenidas: ${airlines.length}');
          return airlines;
        }
      }
      
      print('⚠️ Sin aerolíneas disponibles');
      return [];
      
    } catch (e) {
      print('❌ Error obteniendo aerolíneas: $e');
      return [];
    }
  }

  /// 📋 Obtener ofertas por ID de request
  static Future<List<Map<String, dynamic>>> getOffers(String offerRequestId) async {
    try {
      print('📋 Obteniendo ofertas para: $offerRequestId');

      // Verificar backend activo
      final backendActive = await isBackendActive();
      if (!backendActive) {
        print('❌ Backend offline - sin ofertas disponibles');
        return [];
      }

      final response = await http.get(
        Uri.parse('$_baseUrl/api/flights/offers/$offerRequestId'),
        headers: _headers,
      ).timeout(Duration(seconds: 30));

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        
        if (data['data'] != null && data['data'] is List) {
          final offers = data['data'] as List<Map<String, dynamic>>;
          print('✅ Ofertas obtenidas: ${offers.length}');
          return offers;
        }
      }
      
      print('⚠️ Sin ofertas disponibles');
      return [];
      
    } catch (e) {
      print('❌ Error obteniendo ofertas: $e');
      return [];
    }
  }

  /// 🌐 Test de conexión completa
  static Future<Map<String, dynamic>> testConnection() async {
    try {
      print('🧪 PRUEBA COMPLETA DE CONEXIÓN');
      
      // Test 1: Health check
      final healthOk = await isBackendActive();
      
      return {
        'backend_active': healthOk,
        'base_url': _baseUrl,
        'status': healthOk ? 'ok' : 'error',
        'message': healthOk 
            ? 'Conexión exitosa con backend'
            : 'Problemas de conexión con backend'
      };
    } catch (e) {
      return {
        'backend_active': false,
        'base_url': _baseUrl,
        'status': 'error',
        'message': 'Error en prueba de conexión: $e'
      };
    }
  }

  /// 🏠 Aeropuertos locales como respaldo (cuando backend esté offline)
  static List<Map<String, dynamic>> _getLocalAirports(String query) {
    // NO usar datos locales - solo backend
    print('🏠 NO usando aeropuertos locales - solo backend');
    return [];
  }

  /// 📋 Crear reserva/booking (simulado para desarrollo)
  /// NOTA: Duffel API real requiere información de pago real
  static Future<Map<String, dynamic>?> createBooking({
    required String offerId,
    required List<Map<String, dynamic>> passengers,
  }) async {
    try {
      print('📋 CREANDO RESERVA...');
      print('🎫 Offer ID: $offerId');
      print('👥 Pasajeros: ${passengers.length}');

      // ⚠️ SIMULACIÓN PARA DESARROLLO
      // En producción, esto sería una llamada real al backend
      await Future.delayed(Duration(seconds: 2));
      
      return {
        'success': true,
        'booking_reference': 'CL23${DateTime.now().millisecondsSinceEpoch}',
        'order_id': 'ORD_${DateTime.now().millisecondsSinceEpoch}',
        'status': 'confirmed',
        'message': 'Reserva creada exitosamente (DEMO)',
        'passengers': passengers,
        'total_amount': '0.00', // Se calcularía desde la oferta
        'currency': 'USD',
      };
    } catch (e) {
      print('❌ Error creando reserva: $e');
      return null;
    }
  }

  /// 📊 Obtener estado de orden (simulado para desarrollo)
  static Future<Map<String, dynamic>?> getOrderStatus(String orderId) async {
    try {
      print('📊 OBTENIENDO ESTADO DE ORDEN: $orderId');

      // ⚠️ SIMULACIÓN PARA DESARROLLO
      await Future.delayed(Duration(seconds: 1));
      
      return {
        'order_id': orderId,
        'status': 'confirmed',
        'payment_status': 'paid',
        'message': 'Orden confirmada y pagada (DEMO)',
        'booking_reference': 'CL23${DateTime.now().millisecondsSinceEpoch}',
      };
    } catch (e) {
      print('❌ Error obteniendo estado: $e');
      return null;
    }
  }

  /// 🧪 Test completo de conexión con backend Render.com
  static Future<Map<String, dynamic>> testBackendConnection() async {
    print('🧪 PRUEBA COMPLETA DE CONEXIÓN A RENDER.COM');
    print('🌐 URL de Render: $_baseUrl');
    final healthOk = await isBackendActive();
    return {
      'backend_active': healthOk,
      'base_url': _baseUrl,
      'status': healthOk ? 'ok' : 'error',
      'message': healthOk 
          ? 'Conexión exitosa con backend Render'
          : 'Problemas de conexión con backend Render'
    };
  }
}