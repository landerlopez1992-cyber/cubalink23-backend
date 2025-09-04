# 📁 Crear Bucket de Imágenes en Supabase Storage

## 🔧 Pasos para crear el bucket 'product-images':

### 1. Ir al Dashboard de Supabase
- Ve a: https://supabase.com/dashboard/project/zgqrhzuhrwudckwesybg/storage/buckets

### 2. Crear Nuevo Bucket
- Haz clic en **"Create bucket"**
- Nombre: `product-images`
- Descripción: `Bucket para imágenes de productos de la tienda`
- ✅ Marcar **"Public bucket"** (para que las imágenes sean accesibles públicamente)
- Tamaño máximo de archivo: `50 MB`
- Tipos de archivo permitidos: `image/jpeg, image/png, image/gif, image/webp`

### 3. Configurar Políticas (RLS - Row Level Security)
Una vez creado el bucket, configurar las siguientes políticas:

#### Política de Lectura Pública:
```sql
-- Permitir lectura pública de todas las imágenes
CREATE POLICY "Public read access" ON storage.objects 
FOR SELECT USING (bucket_id = 'product-images');
```

#### Política de Escritura para Usuarios Autenticados:
```sql
-- Permitir subida de imágenes a usuarios autenticados
CREATE POLICY "Authenticated users can upload" ON storage.objects 
FOR INSERT WITH CHECK (bucket_id = 'product-images');
```

#### Política de Actualización:
```sql
-- Permitir actualización de imágenes
CREATE POLICY "Authenticated users can update" ON storage.objects 
FOR UPDATE USING (bucket_id = 'product-images');
```

### 4. Verificar Configuración
- El bucket debe aparecer en la lista
- Debe tener el ícono 🌐 indicando que es público
- Las políticas deben estar activas

## 🧪 Probar Upload
Una vez configurado, el sistema intentará subir imágenes a:
- `https://zgqrhzuhrwudckwesybg.supabase.co/storage/v1/object/product-images/[filename]`
- URL pública: `https://zgqrhzuhrwudckwesybg.supabase.co/storage/v1/object/public/product-images/[filename]`

## 🔄 Buckets Alternativos
Si `product-images` no funciona, el sistema intentará:
1. `public`
2. `images`  
3. `avatars`

## 📝 Notas
- Las imágenes se guardan con nombres únicos usando UUID
- Formato: `{nombre_producto}_{uuid}.jpg`
- Conversión automática a base64 desde el frontend
- Fallback a placeholders si falla el upload
