#!/bin/bash

# 🚀 SERVIDOR DE PRODUCCIÓN CUBALINK23 - INICIO AUTOMÁTICO
# Este script mantiene el backend funcionando 24/7

echo "🚀 INICIANDO SERVIDOR DE PRODUCCIÓN CUBALINK23..."
echo "📱 Tu laptop será el servidor de producción para la app"
echo "🌐 Funcionará desde internet para Google Play/Apple Store"

# Configurar variables de entorno
export DUFFEL_API_KEY="duffel_live_Rj6u0G0cT2hUeIw53ou2HRTNNf0tXl6oP-pVzcGvI7e"
export FLASK_ENV="production"
export FLASK_DEBUG="0"

# Función para reiniciar el servidor si se cae
restart_server() {
    echo "🔄 Reiniciando servidor..."
    pkill -f "python.*app.py" || true
    sleep 2
    python3 app.py &
    echo "✅ Servidor reiniciado en $(date)"
}

# Función para verificar si el servidor está funcionando
check_server() {
    if ! curl -s http://localhost:5000/admin/api/health > /dev/null; then
        echo "❌ Servidor caído - reiniciando..."
        restart_server
    fi
}

# Iniciar servidor principal
echo "🔥 Iniciando servidor Flask..."
python3 app.py &

# Esperar a que inicie
sleep 5

# Verificar que esté funcionando
if curl -s http://localhost:5000/admin/api/health > /dev/null; then
    echo "✅ SERVIDOR FUNCIONANDO EN PUERTO 5000"
    echo "🌐 URL LOCAL: http://localhost:5000"
    echo "📱 La app Flutter usará este servidor"
else
    echo "❌ Error al iniciar servidor"
    exit 1
fi

# Loop infinito para mantener el servidor funcionando
echo "🔄 Monitor iniciado - manteniendo servidor funcionando 24/7..."
while true; do
    check_server
    sleep 30  # Verificar cada 30 segundos
done
