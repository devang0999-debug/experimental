# ZepIris — Configuration Guide

Complete configuration reference for ZepIris services.

## Environment Variables

All configuration uses the `ZEPIRIS_` prefix. Values can be set via:
1. Environment variables: `export ZEPIRIS_MILVUS_HOST=localhost`
2. `.env` file: Create `.env` in project root
3. Python code: Edit `zepiris/config.py`

## API Configuration

### ZEPIRIS_API_TITLE
**Type**: `str`
**Default**: `"ZepIris"`
**Description**: API service name (displayed in OpenAPI docs)

```env
ZEPIRIS_API_TITLE=ZepIris Face Auth
```

### ZEPIRIS_API_VERSION
**Type**: `str`
**Default**: `"1.0.0"`
**Description**: API version (follows semantic versioning)

```env
ZEPIRIS_API_VERSION=1.0.0
```

## MinIO / S3 Configuration

### ZEPIRIS_MINIO_ENDPOINT
**Type**: `str`
**Default**: `"localhost:9002"`
**Description**: MinIO/S3 server address with port

**Examples**:
```env
# Local MinIO (Docker Compose)
ZEPIRIS_MINIO_ENDPOINT=localhost:9002

# AWS S3
ZEPIRIS_MINIO_ENDPOINT=s3.amazonaws.com

# Custom S3-compatible (DigitalOcean Spaces, etc.)
ZEPIRIS_MINIO_ENDPOINT=nyc3.digitaloceanspaces.com
```

### ZEPIRIS_MINIO_ACCESS_KEY
**Type**: `str`
**Default**: `"minioadmin"`
**Description**: Access key for S3 authentication

### ZEPIRIS_MINIO_SECRET_KEY
**Type**: `str`
**Default**: `"minioadmin"`
**Description**: Secret key for S3 authentication

⚠️ **Security Warning**: Use strong passwords in production!

```env
ZEPIRIS_MINIO_ACCESS_KEY=your_strong_access_key_here
ZEPIRIS_MINIO_SECRET_KEY=your_strong_secret_key_here
```

### ZEPIRIS_MINIO_BUCKET
**Type**: `str`
**Default**: `"zepiris"`
**Description**: Bucket name for storing images

**Notes**:
- Must follow S3 bucket naming rules (lowercase, no underscores)
- Created automatically if doesn't exist

```env
ZEPIRIS_MINIO_BUCKET=face-auth-prod
```

### ZEPIRIS_MINIO_SECURE
**Type**: `bool`
**Default**: `false`
**Description**: Use HTTPS/TLS for MinIO connection

```env
# Local development (HTTP)
ZEPIRIS_MINIO_SECURE=false

# Production (HTTPS)
ZEPIRIS_MINIO_SECURE=true
```

## Milvus Configuration

### ZEPIRIS_MILVUS_HOST
**Type**: `str`
**Default**: `"localhost"`
**Description**: Milvus server hostname or IP

```env
# Docker Compose
ZEPIRIS_MILVUS_HOST=milvus

# Local
ZEPIRIS_MILVUS_HOST=localhost

# Remote
ZEPIRIS_MILVUS_HOST=milvus.example.com
```

### ZEPIRIS_MILVUS_PORT
**Type**: `int`
**Default**: `19530`
**Description**: Milvus gRPC API port

```env
ZEPIRIS_MILVUS_PORT=19530
```

### ZEPIRIS_MILVUS_COLLECTION
**Type**: `str`
**Default**: `"zepiris_faces"`
**Description**: Milvus collection name for face embeddings

**Notes**:
- Collection is created automatically on startup
- Schema: `face_id (PK), tenant, object_key, embedding (FLOAT_VECTOR)`
- Supports multi-tenancy: each tenant has isolated face namespace

```env
ZEPIRIS_MILVUS_COLLECTION=face_embeddings_prod
```

### ZEPIRIS_MILVUS_EMBEDDING_DIM
**Type**: `int`
**Default**: `512`
**Description**: Dimensionality of face embedding vectors

**Common Values**:
- `128` - Fast but less accurate
- `256` - Good balance
- `512` - Default, good accuracy
- `768` - High accuracy (slower)

⚠️ **Important**: This must match your embedding model output!

```env
ZEPIRIS_MILVUS_EMBEDDING_DIM=512
```

### ZEPIRIS_ML_INFERENCE_SERVICE_URL
**Type**: `str` (**required**)
**Description**: Base URL of the ML inference microservice. The main API **always** calls it for **`POST /v1/iqa/assess`** (NSFW, spoof, blur) and **`POST /v1/face/embed`** (face embedding) after encoding the upload as base64 JPEG.

If `ZEPIRIS_ML_INFERENCE_SERVICE_URL` is empty, **`ML_INFERENCE_SERVICE_URL`** (no `ZEPIRIS_` prefix) is used instead. One of these must be set or **startup fails**.

```env
# Docker Compose (service name)
ZEPIRIS_ML_INFERENCE_SERVICE_URL=http://ml-inference:8001

# API on host, ML published on 8001
ZEPIRIS_ML_INFERENCE_SERVICE_URL=http://localhost:8001
```

## Image quality (IQA)

There are **no** `ZEPIRIS_IQA_*` knobs on the main API. Image quality is determined entirely by the **ml-inference** service (`POST /v1/iqa/assess`). Tune blur, NSFW, and spoof behavior with **`ML_SERVICE_*`** environment variables on that container (see `zepiris/ml_inference/app.py` and `.env.example`).

## Advanced Configuration

### Custom Milvus Settings

Edit `/milvus/configs/milvus.yaml` (in Docker) or environment:

```env
# Search parameters
MILVUS_SEARCH_NLIST=128
MILVUS_SEARCH_NPROBE=8

# Memory settings
MILVUS_MEMORY_HIGH_WATERMARK=0.95
MILVUS_MEMORY_LOW_WATERMARK=0.85
```

### Custom MinIO Settings

For production S3/MinIO deployments:

```env
# Performance
MINIO_ACCESS_CONCURRENCY=20
MINIO_UPLOAD_TIMEOUT=24h

# Security
MINIO_ENABLE_HTTPS=true
MINIO_CERT_FILE=/path/to/cert.pem
MINIO_KEY_FILE=/path/to/key.pem
```

## Configuration Presets

### Development Preset
```env
# .env for local development
ZEPIRIS_MINIO_ENDPOINT=localhost:9002
ZEPIRIS_MINIO_SECURE=false
ZEPIRIS_MILVUS_HOST=localhost
ZEPIRIS_ML_INFERENCE_SERVICE_URL=http://localhost:8001
```

### Production Preset (AWS)
```env
# .env for production with AWS
ZEPIRIS_MINIO_ENDPOINT=s3.amazonaws.com
ZEPIRIS_MINIO_BUCKET=your-prod-bucket
ZEPIRIS_MINIO_SECURE=true
ZEPIRIS_MILVUS_HOST=milvus-prod.internal
ZEPIRIS_ML_INFERENCE_SERVICE_URL=http://ml-inference.internal:8001
ZEPIRIS_MILVUS_EMBEDDING_DIM=768
```

### Kubernetes Preset
```env
# .env for Kubernetes deployment
ZEPIRIS_MINIO_ENDPOINT=minio.default.svc.cluster.local:9000
ZEPIRIS_MILVUS_HOST=milvus.default.svc.cluster.local
ZEPIRIS_MINIO_BUCKET=zepiris-prod
ZEPIRIS_MILVUS_COLLECTION=zepiris_faces_prod
```

## Configuration Validation

On startup, ZepIris validates:
- ✓ `ZEPIRIS_ML_INFERENCE_SERVICE_URL` (or `ML_INFERENCE_SERVICE_URL`) is set
- ✓ Milvus connectivity
- ✓ MinIO bucket accessibility
- ✓ Embedding dimension is positive

**Validation Errors** appear in logs:
```
[ERROR] Could not connect to Milvus at localhost:19530
[ERROR] MinIO bucket 'zepiris' does not exist and could not be created
```

## Performance Tuning

### For High Throughput
```env
ZEPIRIS_MILVUS_EMBEDDING_DIM=256  # Smaller vectors = faster search
# Stricter or looser IQA: adjust ML_SERVICE_* on the ml-inference container
```

### For High Accuracy
```env
ZEPIRIS_MILVUS_EMBEDDING_DIM=768  # Larger vectors = more accurate
# Stricter blur/NSFW/spoof: adjust ML_SERVICE_* on the ml-inference container
```

### For Large Datasets
```env
ZEPIRIS_MILVUS_COLLECTION=zepiris_faces_large
# Use distributed Milvus setup (see Kubernetes guide)
```

## Troubleshooting Configuration

### Issue: "Connection refused" for Milvus
```bash
# Check Milvus is running
docker-compose ps milvus

# Check host/port
echo $ZEPIRIS_MILVUS_HOST
echo $ZEPIRIS_MILVUS_PORT
```

### Issue: "MinIO bucket not found"
```bash
# Create bucket
docker exec zepiris-minio mc mb minio/zepiris
```

### Issue: Images failing IQA
IQA is enforced by **ml-inference** (`/v1/iqa/assess`). Loosen thresholds there, e.g.:

```env
ML_SERVICE_BLUR_THRESHOLD=0.85
```
(Set on the `ml-inference` service / its `.env`, not on the main API.)

## Environment Variable Priority

Settings are loaded in order (highest priority first):
1. Environment variables (`export ZEPIRIS_...`)
2. `.env` file
3. Docker secrets (Kubernetes)
4. Hardcoded defaults in `config.py`

Example:
```bash
# Override with environment variable
export ZEPIRIS_MILVUS_HOST=remote-milvus.com
docker-compose up
```

## Configuration File Format

### .env File Format
```env
# Comments start with #
ZEPIRIS_API_TITLE=ZepIris

# Multiline values (not typical for config)
# Quote if value contains spaces
ZEPIRIS_API_TITLE="My ZepIris Service"

# Boolean values
ZEPIRIS_MINIO_SECURE=true  # or false

# Numbers
ZEPIRIS_MILVUS_PORT=19530
ZEPIRIS_IQA_MIN_LAPLACIAN_VARIANCE=50.0
```

## Loading Custom Configuration

### Programmatically
```python
from zepiris.config import Settings

settings = Settings(
    minio_endpoint="custom:9000",
    milvus_host="custom-milvus"
)
```

### From File
```bash
# Create custom.env
source custom.env
poetry run uvicorn zepiris.main:app
```

## Security Best Practices

1. **Never commit `.env` with real credentials**
   ```bash
   echo ".env" >> .gitignore
   ```

2. **Use strong passwords**
   ```bash
   # Generate secure key
   openssl rand -base64 32
   ```

3. **Rotate credentials regularly**
   - Update MinIO keys monthly
   - Audit Milvus access logs

4. **Use TLS/HTTPS in production**
   ```env
   ZEPIRIS_MINIO_SECURE=true
   ```

5. **Restrict network access**
   - Milvus: only from API servers
   - MinIO: only from API servers

## See Also

- [README.md](../README.md) - Project overview
- [SETUP_GUIDE.md](../SETUP_GUIDE.md) - Setup instructions
- [API_REFERENCE.md](API_REFERENCE.md) - API endpoints
