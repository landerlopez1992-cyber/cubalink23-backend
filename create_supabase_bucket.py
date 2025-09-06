#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para crear el bucket 'product-images' en Supabase Storage
"""

import requests
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def create_product_images_bucket():
    """Crear bucket product-images en Supabase Storage"""
    
    # Configuración de Supabase
    supabase_url = os.getenv('SUPABASE_URL', 'https://zgqrhzuhrwudckwesybg.supabase.co')
    supabase_service_key = os.getenv('SUPABASE_SERVICE_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpncXJoenVocnd1ZGNrd2VzeWJnIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1NTc5Mjc5OCwiZXhwIjoyMDcxMzY4Nzk4fQ.Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8')
    
    headers = {
        'apikey': supabase_service_key,
        'Authorization': 'Bearer ' + supabase_service_key,
        'Content-Type': 'application/json'
    }
    
    bucket_data = {
        'id': 'product-images',
        'name': 'product-images',
        'public': True,
        'file_size_limit': 52428800,  # 50MB
        'allowed_mime_types': ['image/jpeg', 'image/png', 'image/webp', 'image/gif']
    }
    
    print("🔧 Creando bucket 'product-images' en Supabase Storage...")
    
    try:
        # Crear bucket
        response = requests.post(
            f'{supabase_url}/storage/v1/bucket',
            headers=headers,
            json=bucket_data
        )
        
        if response.status_code == 200:
            print("✅ Bucket 'product-images' creado exitosamente!")
        elif response.status_code == 409:
            print("ℹ️ Bucket 'product-images' ya existe.")
        else:
            print(f"❌ Error creando bucket: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Crear políticas de acceso
    print("🔧 Configurando políticas de acceso...")
    
    policies = [
        {
            'id': 'product-images-public-read',
            'bucket_id': 'product-images',
            'policy': 'CREATE POLICY "Public read access" ON storage.objects FOR SELECT USING (bucket_id = \'product-images\');'
        },
        {
            'id': 'product-images-authenticated-write',
            'bucket_id': 'product-images', 
            'policy': 'CREATE POLICY "Authenticated users can upload" ON storage.objects FOR INSERT WITH CHECK (bucket_id = \'product-images\');'
        },
        {
            'id': 'product-images-authenticated-update',
            'bucket_id': 'product-images',
            'policy': 'CREATE POLICY "Authenticated users can update" ON storage.objects FOR UPDATE USING (bucket_id = \'product-images\');'
        },
        {
            'id': 'product-images-authenticated-delete',
            'bucket_id': 'product-images',
            'policy': 'CREATE POLICY "Authenticated users can delete" ON storage.objects FOR DELETE USING (bucket_id = \'product-images\');'
        }
    ]
    
    for policy in policies:
        try:
            policy_response = requests.post(
                f'{supabase_url}/rest/v1/rpc/exec_sql',
                headers=headers,
                json={'sql': policy['policy']}
            )
            
            if policy_response.status_code == 200:
                print(f"✅ Política '{policy['id']}' creada")
            else:
                print(f"⚠️ Error en política '{policy['id']}': {policy_response.status_code}")
                
        except Exception as e:
            print(f"⚠️ Error creando política '{policy['id']}': {e}")
    
    print("\n🎉 Configuración completada!")
    print("📋 URLs de ejemplo:")
    print("- https://zgqrhzuhrwudckwesybg.supabase.co/storage/v1/object/product-images/[filename]")
    print("- URL pública: https://zgqrhzuhrwudckwesybg.supabase.co/storage/v1/object/public/product-images/[filename]")
    
    return True

if __name__ == "__main__":
    create_product_images_bucket()

