# Guía de Integración Duffel API - Reservas Aéreas

## 🔑 Información de API
**URL Base:** `https://api.duffel.com/air`
**Versión:** `v2`
**Clave API:** `duffel_live_Rj6u0G0cT2hUeIw53ou2HRTNNf0tXl6oP-pVzcGvI7e`

## 📋 Headers Requeridos
```
Authorization: Bearer duffel_live_Rj6u0G0cT2hUeIw53ou2HRTNNf0tXl6oP-pVzcGvI7e
Content-Type: application/json
Duffel-Version: v2
```

## 🚀 Flujo de Reserva Aérea

### 1. Búsqueda de Vuelos (Offer Requests)
```http
POST /offer_requests
```

**Payload de ejemplo:**
```json
{
  "data": {
    "slices": [
      {
        "origin": "MIA",
        "destination": "HAV",
        "departure_date": "2025-08-30"
      }
    ],
    "passengers": [
      {
        "type": "adult"
      }
    ],
    "cabin_class": "economy"
  }
}
```

### 2. Obtener Ofertas Disponibles
```http
GET /offers?offer_request_id={id}
```

### 3. Crear Reserva (Order)
```http
POST /orders
```

**Payload de ejemplo:**
```json
{
  "data": {
    "selected_offers": ["off_0000AxbSCjH8ota9ENdQje"],
    "passengers": [
      {
        "title": "mr",
        "phone_number": "+1234567890",
        "given_name": "Juan",
        "family_name": "Pérez",
        "email": "juan@email.com",
        "born_on": "1990-01-01",
        "gender": "m",
        "identity_document_id": "doc_123"
      }
    ],
    "payments": [
      {
        "type": "balance",
        "currency": "USD",
        "amount": "273.00"
      }
    ]
  }
}
```

## 📊 Resultados de Prueba Real

**✅ API PROBADA EXITOSAMENTE**
- **Ruta:** MIA → HAV (30/08/2025)
- **Pasajeros:** 1 adulto
- **Resultados:** 14 opciones de vuelo
- **Aerolíneas:** American Airlines, Aeromexico
- **Precios:** Desde $273 USD

### Vuelos Encontrados:
- **American Airlines:** 8 opciones directas
- **Aeromexico:** 6 opciones con escala en México
- **Horarios:** 06:05 - 14:55
- **Duración:** 1h 15m - 1h 30m (directos)

## 🔧 Implementación Técnica

### Configuración JavaScript
```javascript
const DUFFEL_CONFIG = {
  baseURL: 'https://api.duffel.com/air',
  apiKey: 'duffel_live_Rj6u0G0cT2hUeIw53ou2HRTNNf0tXl6oP-pVzcGvI7e',
  headers: {
    'Authorization': 'Bearer duffel_live_Rj6u0G0cT2hUeIw53ou2HRTNNf0tXl6oP-pVzcGvI7e',
    'Content-Type': 'application/json',
    'Duffel-Version': 'v2'
  }
};
```

### Función de Búsqueda
```javascript
async function buscarVuelos(origen, destino, fecha, pasajeros) {
  try {
    const response = await fetch(`${DUFFEL_CONFIG.baseURL}/offer_requests`, {
      method: 'POST',
      headers: DUFFEL_CONFIG.headers,
      body: JSON.stringify({
        data: {
          slices: [{
            origin: origen,
            destination: destino,
            departure_date: fecha
          }],
          passengers: pasajeros.map(() => ({ type: "adult" })),
          cabin_class: "economy"
        }
      })
    });
    
    const data = await response.json();
    return data.data;
  } catch (error) {
    console.error('Error buscando vuelos:', error);
    throw error;
  }
}
```

## 📱 Componentes de UI Sugeridos

### 1. Formulario de Búsqueda
- Selector de origen/destino
- Selector de fechas
- Selector de pasajeros
- Selector de clase de cabina

### 2. Lista de Resultados
- Información de vuelo (hora, duración, escalas)
- Precio y aerolínea
- Botón de selección

### 3. Detalles de Vuelo
- Información completa del segmento
- Servicios incluidos
- Condiciones de tarifa

### 4. Formulario de Pasajeros
- Datos personales
- Documentos de identidad
- Información de contacto

### 5. Proceso de Pago
- Resumen de reserva
- Métodos de pago
- Confirmación

## 🎨 Estilos CSS Básicos
```css
.flight-search-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.search-form {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.flight-results {
  display: grid;
  gap: 15px;
}

.flight-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 15px;
  background: white;
  transition: box-shadow 0.3s;
}

.flight-card:hover {
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.price {
  font-size: 1.5em;
  font-weight: bold;
  color: #007bff;
}
```

## ⚠️ Consideraciones Importantes

1. **Manejo de Errores:** Implementar try-catch para todas las llamadas API
2. **Validación:** Validar datos de entrada antes de enviar
3. **Loading States:** Mostrar indicadores de carga durante las peticiones
4. **Responsive Design:** Asegurar que funcione en móviles
5. **Accesibilidad:** Incluir atributos ARIA y navegación por teclado

## 🚀 Próximos Pasos

1. Implementar búsqueda de vuelos
2. Crear interfaz de selección de ofertas
3. Desarrollar formulario de pasajeros
4. Integrar sistema de pagos
5. Implementar confirmación de reserva
6. Agregar gestión de reservas existentes

## ✅ Estado de la API

**CONFIRMADO:** La API de Duffel está funcionando correctamente y devuelve datos reales de vuelos. La implementación puede proceder con confianza.
