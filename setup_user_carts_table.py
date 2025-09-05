#!/usr/bin/env python3
"""
Script para crear la tabla user_carts en Supabase
"""

import os
import sys
from supabase import create_client, Client

def setup_user_carts_table():
    """Crear tabla user_carts en Supabase"""
    
    # Configuración de Supabase
    url = "https://your-project.supabase.co"  # Reemplazar con tu URL
    key = "your-anon-key"  # Reemplazar con tu clave anon
    
    # Intentar obtener desde variables de entorno
    url = os.getenv('SUPABASE_URL', url)
    key = os.getenv('SUPABASE_ANON_KEY', key)
    
    if url == "https://your-project.supabase.co" or key == "your-anon-key":
        print("❌ Error: Necesitas configurar SUPABASE_URL y SUPABASE_ANON_KEY")
        print("   O editar este script con tus credenciales reales")
        return False
    
    try:
        # Crear cliente Supabase
        supabase: Client = create_client(url, key)
        print("✅ Conectado a Supabase")
        
        # Leer el archivo SQL
        with open('create_user_carts_table.sql', 'r') as f:
            sql_content = f.read()
        
        print("📄 SQL leído desde create_user_carts_table.sql")
        print("🔧 Ejecutando SQL en Supabase...")
        
        # Ejecutar SQL usando rpc
        result = supabase.rpc('exec_sql', {'query': sql_content}).execute()
        
        print("✅ Tabla user_carts creada exitosamente")
        print("📋 Características:")
        print("   - Persistencia de carritos por usuario")
        print("   - RLS habilitado (usuarios solo ven su carrito)")
        print("   - Índices para mejor performance")
        print("   - Triggers para updated_at automático")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creando tabla user_carts: {e}")
        print("\n🔧 INSTRUCCIONES MANUALES:")
        print("1. Ve a tu dashboard de Supabase")
        print("2. Abre el SQL Editor")
        print("3. Copia y pega el contenido de create_user_carts_table.sql")
        print("4. Ejecuta el SQL")
        return False

if __name__ == "__main__":
    print("🚀 Configurando tabla user_carts en Supabase...")
    success = setup_user_carts_table()
    
    if success:
        print("\n✅ ¡Configuración completada!")
        print("   Ahora los carritos se guardarán automáticamente en Supabase")
    else:
        print("\n⚠️  Configuración manual requerida")
        print("   Sigue las instrucciones arriba para crear la tabla manualmente")
