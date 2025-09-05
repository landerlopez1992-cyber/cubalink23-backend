#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para probar la funcionalidad de imágenes de productos
"""

import requests
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def test_product_images():
    """Probar la funcionalidad de imágenes de productos"""
    
    # Configuración de Supabase
    supabase_url = os.getenv('SUPABASE_URL', 'https://zgqrhzuhrwudckwesybg.supabase.co')
    supabase_key = os.getenv('SUPABASE_ANON_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpncXJoenVocnd1ZGNrd2VzeWJnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTU3OTI3OTgsImV4cCI6MjA3MTM2ODc5OH0.lUVK99zmOYD7bNTxilJZWHTmYPfZF5YeMJDVUaJ-FsQ')
    
    print("🔍 Probando funcionalidad de imágenes de productos...")
    
    try:
        headers = {
            'apikey': supabase_key,
            'Authorization': 'Bearer ' + supabase_key,
            'Content-Type': 'application/json'
        }
        
        # 1. Verificar productos existentes
        print("\n📦 1. Verificando productos existentes...")
        response = requests.get(f'{supabase_url}/rest/v1/store_products?select=*', headers=headers)
        
        if response.status_code == 200:
            products = response.json()
            print(f"   Total productos: {len(products)}")
            
            for i, product in enumerate(products[:3]):
                print(f"   {i+1}. {product.get('name', 'Sin nombre')}")
                image_url = product.get('image_url', 'Sin imagen')
                print(f"      Image URL: {image_url}")
                
                # Probar acceso a la imagen
                if image_url and image_url != 'Sin imagen':
                    try:
                        img_response = requests.head(image_url, timeout=5)
                        status = "✅ Accesible" if img_response.status_code == 200 else f"❌ Error {img_response.status_code}"
                        print(f"      Estado: {status}")
                    except:
                        print(f"      Estado: ❌ No accesible")
        else:
            print(f"   Error: {response.status_code} - {response.text}")
        
        # 2. Probar el servicio de storage
        print("\n📷 2. Probando servicio de storage...")
        from supabase_storage_service import storage_service
        
        # Simular un archivo de prueba
        class MockFile:
            def __init__(self):
                self.filename = 'test_product.jpg'
                self.content_type = 'image/jpeg'
            
            def read(self):
                return b'fake image content'
        
        mock_file = MockFile()
        result = storage_service.upload_image(mock_file)
        print(f"   Resultado del upload: {result}")
        
        # 3. Verificar que las URLs generadas son accesibles
        print("\n🌐 3. Verificando accesibilidad de URLs...")
        if result:
            try:
                img_response = requests.head(result, timeout=5)
                status = "✅ Accesible" if img_response.status_code == 200 else f"❌ Error {img_response.status_code}"
                print(f"   URL generada: {status}")
            except Exception as e:
                print(f"   URL generada: ❌ Error - {e}")
        
        print("\n🎉 Prueba completada!")
        
    except Exception as e:
        print(f"❌ Error en la prueba: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_product_images()
