# Instrucciones para DreamFlow AI - Duffel API

## 🎯 IMPLEMENTA RESERVAS AÉREAS CON DUFFEL API

### ✅ API CONFIRMADA Y FUNCIONANDO
- **URL Base:** `https://api.duffel.com/air`
- **Versión:** `v2`
- **Clave API:** `duffel_live_Rj6u0G0cT2hUeIw53ou2HRTNNf0tXl6oP-pVzcGvI7e`
- **Estado:** ✅ **PROBADA** - Obtuvimos 14 vuelos reales de MIA a HAV

## 🔧 CONFIGURACIÓN RÁPIDA

```javascript
const DUFFEL_CONFIG = {
  baseURL: 'https://api.duffel.com/air',
  headers: {
    'Authorization': 'Bearer duffel_live_Rj6u0G0cT2hUeIw53ou2HRTNNf0tXl6oP-pVzcGvI7e',
    'Content-Type': 'application/json',
    'Duffel-Version': 'v2'
  }
};
```

## 🚀 FUNCIONES PRINCIPALES

### 1. Buscar Vuelos
```javascript
async function buscarVuelos(origen, destino, fecha, pasajeros) {
  const response = await fetch(`${DUFFEL_CONFIG.baseURL}/offer_requests`, {
    method: 'POST',
    headers: DUFFEL_CONFIG.headers,
    body: JSON.stringify({
      data: {
        slices: [{ origin, destination: destino, departure_date: fecha }],
        passengers: pasajeros.map(() => ({ type: "adult" })),
        cabin_class: "economy"
      }
    })
  });
  return response.json();
}
```

### 2. Obtener Ofertas
```javascript
async function obtenerOfertas(offerRequestId) {
  const response = await fetch(`${DUFFEL_CONFIG.baseURL}/offers?offer_request_id=${offerRequestId}`, {
    headers: DUFFEL_CONFIG.headers
  });
  return response.json();
}
```

### 3. Crear Reserva
```javascript
async function crearReserva(offerId, datosPasajero) {
  const response = await fetch(`${DUFFEL_CONFIG.baseURL}/orders`, {
    method: 'POST',
    headers: DUFFEL_CONFIG.headers,
    body: JSON.stringify({
      data: {
        selected_offers: [offerId],
        passengers: [datosPasajero],
        payments: [{ type: 'balance', currency: 'USD', amount: datosPasajero.precio }]
      }
    })
  });
  return response.json();
}
```

## 📱 COMPONENTES UI NECESARIOS

### Formulario de Búsqueda
- Input origen (ej: MIA)
- Input destino (ej: HAV)
- Input fecha
- Select clase cabina
- Botón buscar

### Lista de Resultados
- Precio y moneda
- Aerolínea
- Duración
- Horarios
- Botón seleccionar

### Formulario de Pasajeros
- Nombre y apellido
- Email y teléfono
- Fecha nacimiento
- Botón confirmar

## 🎨 ESTILOS BÁSICOS

```css
.flight-search-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.formulario-busqueda {
  background: #f8f9fa;
  padding: 25px;
  border-radius: 12px;
  display: grid;
  gap: 15px;
}

.oferta-card {
  border: 2px solid #e9ecef;
  border-radius: 12px;
  padding: 20px;
  background: white;
  transition: all 0.3s;
}

.precio {
  font-size: 2em;
  font-weight: bold;
  color: #007bff;
}
```

## 📋 FLUJO DE IMPLEMENTACIÓN

1. **Usuario ingresa datos** → Formulario de búsqueda
2. **Buscar vuelos** → POST `/offer_requests`
3. **Obtener ofertas** → GET `/offers?offer_request_id={id}`
4. **Usuario selecciona** → Mostrar detalles
5. **Ingresar datos pasajero** → Formulario de pasajeros
6. **Crear reserva** → POST `/orders`
7. **Mostrar confirmación** → Estado de la reserva

## ⚠️ IMPORTANTE

- Manejar errores con try-catch
- Mostrar loading states
- Validar datos de entrada
- Diseño responsive
- La API está probada y funciona

## ✅ RESULTADO ESPERADO

Una aplicación completa de reservas aéreas que permite:
- Buscar vuelos por origen, destino y fecha
- Ver lista de ofertas disponibles
- Seleccionar vuelo
- Ingresar datos de pasajeros
- Confirmar reserva
- Ver estado de la reserva

**¡La API está confirmada y funcionando! Procede con confianza.**
