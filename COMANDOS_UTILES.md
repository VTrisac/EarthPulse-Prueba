# Comandos Útiles - Google Drive Clone

## Docker Compose

### Iniciar el proyecto
```bash
docker compose up --build
```

### Iniciar en segundo plano (detached)
```bash
docker compose up -d --build
```

### Detener todos los servicios
```bash
docker compose down
```

### Detener y eliminar volúmenes (borrar todos los datos)
```bash
docker compose down -v
rm -rf data/
```

### Ver logs de todos los servicios
```bash
docker compose logs -f
```

### Ver logs de un servicio específico
```bash
docker compose logs -f backend
docker compose logs -f frontend
docker compose logs -f mongo
docker compose logs -f minio
```

### Reconstruir solo un servicio
```bash
docker compose up --build backend
docker compose up --build frontend
```

### Reiniciar un servicio
```bash
docker compose restart backend
docker compose restart frontend
```

### Ver estado de los servicios
```bash
docker compose ps
```

### Ejecutar comando en un contenedor
```bash
docker compose exec backend bash
docker compose exec frontend sh
docker compose exec mongo mongosh
```

## Pruebas con cURL

### Subir un archivo
```bash
curl -X POST "http://localhost:8000/api/files/upload" \
  -F "file=@/ruta/a/tu/archivo.pdf"
```

### Listar todos los archivos
```bash
curl "http://localhost:8000/api/files"
```

### Listar con paginación
```bash
curl "http://localhost:8000/api/files?page=1&limit=10"
```

### Buscar archivos
```bash
curl "http://localhost:8000/api/files?search=documento"
```

### Obtener metadatos de un archivo
```bash
curl "http://localhost:8000/api/files/ARCHIVO_ID"
```

### Descargar un archivo
```bash
curl -OJ "http://localhost:8000/api/files/ARCHIVO_ID/download"
```

### Renombrar un archivo
```bash
curl -X PATCH "http://localhost:8000/api/files/ARCHIVO_ID" \
  -H "Content-Type: application/json" \
  -d '{"name": "nuevo-nombre.pdf"}'
```

### Eliminar un archivo
```bash
curl -X DELETE "http://localhost:8000/api/files/ARCHIVO_ID"
```

## MongoDB

### Conectar a MongoDB desde el contenedor
```bash
docker compose exec mongo mongosh filesdb
```

### Ver todas las colecciones
```javascript
show collections
```

### Ver todos los archivos
```javascript
db.files.find().pretty()
```

### Contar archivos
```javascript
db.files.countDocuments()
```

### Buscar un archivo por nombre
```javascript
db.files.find({name: /pdf/i})
```

### Eliminar todos los archivos (CUIDADO)
```javascript
db.files.deleteMany({})
```

## MinIO

### Acceder a MinIO Console
Abre en el navegador: http://localhost:9001

- Usuario: `minioadmin`
- Contraseña: `minioadmin`

### Usar MinIO Client (mc)
```bash
# Configurar alias
docker compose exec minio-init mc alias set local http://minio:9000 minioadmin minioadmin

# Listar buckets
docker compose exec minio-init mc ls local

# Listar archivos en el bucket
docker compose exec minio-init mc ls local/files

# Eliminar un archivo
docker compose exec minio-init mc rm local/files/ruta/al/archivo

# Eliminar todo el bucket (CUIDADO)
docker compose exec minio-init mc rb --force local/files
```

## Desarrollo Local (sin Docker)

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Variables de entorno necesarias
export MONGO_URL="mongodb://localhost:27017/filesdb"
export MINIO_ENDPOINT="localhost:9000"
export MINIO_ACCESS_KEY="minioadmin"
export MINIO_SECRET_KEY="minioadmin"

# Ejecutar
uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Limpieza y Mantenimiento

### Limpiar imágenes Docker no utilizadas
```bash
docker image prune -a
```

### Limpiar contenedores detenidos
```bash
docker container prune
```

### Limpiar volúmenes no utilizados
```bash
docker volume prune
```

### Ver espacio utilizado por Docker
```bash
docker system df
```

### Limpieza completa de Docker
```bash
docker system prune -a --volumes
```

## Debugging

### Ver variables de entorno de un contenedor
```bash
docker compose exec backend env
```

### Inspeccionar un contenedor
```bash
docker inspect drive-clone-backend
```

### Ver red de Docker Compose
```bash
docker network ls
docker network inspect earthpulse_drive-network
```

### Verificar conectividad entre servicios
```bash
# Desde backend a MongoDB
docker compose exec backend ping mongo

# Desde backend a MinIO
docker compose exec backend ping minio
```

## Testing

### Probar endpoint de health
```bash
curl http://localhost:8000/health
```

### Probar documentación de API
Abre en el navegador: http://localhost:8000/docs

### Subir múltiples archivos
```bash
for file in /ruta/archivos/*; do
  curl -X POST "http://localhost:8000/api/files/upload" -F "file=@$file"
done
```

## Hot Reload

Los cambios en el código se reflejan automáticamente:
- **Backend**: Uvicorn detecta cambios en archivos .py
- **Frontend**: Vite detecta cambios en archivos .svelte y .js

No necesitas reiniciar los contenedores para ver los cambios.

## Puertos Utilizados

- `5173` - Frontend (SvelteKit)
- `8000` - Backend (FastAPI)
- `27017` - MongoDB
- `9000` - MinIO API
- `9001` - MinIO Console

## Solución de Problemas

### Los contenedores no inician
```bash
docker compose down
docker compose up --build
```

### El bucket no se crea
```bash
docker compose restart minio-init
docker compose logs minio-init
```

### Error de conexión entre servicios
Verificar que todos los servicios estén en la misma red:
```bash
docker compose ps
docker network inspect earthpulse_drive-network
```

### Limpiar todo y empezar de nuevo
```bash
docker compose down -v
rm -rf data/
docker compose up --build
```
