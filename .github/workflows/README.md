# CI/CD Pipeline - Calculadora React + FastAPI

Este directorio contiene la configuración del pipeline de CI/CD usando GitHub Actions.

## 📋 Descripción General

El pipeline automatiza todo el proceso de integración continua y despliegue continuo:

- ✅ Validación de calidad de código
- 🧪 Ejecución de tests
- 🐳 Build de imágenes Docker
- 🔒 Escaneo de seguridad
- 🚀 Deployment automático

## 🔄 Flujo de Trabajo

### Triggers

El pipeline se ejecuta automáticamente cuando:

- Se hace `push` a las ramas: `master`, `main`, `develop`
- Se crea un `pull request` hacia: `master`, `main`

### Jobs Secuenciales

```
code-quality (Linting y formato)
       ↓
   ┌───┴───┐
   │       │
backend-tests  security-scan
   │       │
   └───┬───┘
       ↓
  docker-build
       ↓
integration-tests
       ↓
  build-success
       ↓
   deploy (solo master/main)
```

## 🔧 Jobs Detallados

### 1. Code Quality & Linting

**Propósito**: Verificar la calidad y formato del código

**Backend:**

- `flake8`: Detecta errores de sintaxis y problemas de estilo
- `black --check`: Verifica el formato del código Python

**Frontend:**

- `npm run lint`: ESLint para código React/JavaScript

**Tiempo estimado**: ~1-2 minutos

### 2. Backend Tests

**Propósito**: Ejecutar todos los tests del backend

**Acciones:**

- Ejecuta 71 tests con pytest
- Genera reporte de cobertura (XML, HTML, terminal)
- Sube coverage a Codecov (opcional)
- Archiva reporte HTML como artefacto

**Comandos:**

```bash
pytest -v --tb=short
pytest --cov=app --cov-report=xml --cov-report=html --cov-report=term
```

**Tiempo estimado**: ~2-3 minutos

### 3. Docker Build & Test

**Propósito**: Construir y validar imágenes Docker

**Acciones:**

- Build de imagen backend con cache
- Build de imagen frontend con cache
- Validación de docker-compose.yml

**Optimizaciones:**

- GitHub Actions Cache para capas de Docker
- Builds paralelos de backend y frontend

**Tiempo estimado**: ~3-5 minutos

### 4. Security Scan

**Propósito**: Detectar vulnerabilidades de seguridad

**Herramientas:**

- **Trivy**: Escaneo de archivos y dependencias
- **Safety**: Verificación de paquetes Python

**Outputs:**

- Reporte SARIF subido a GitHub Security
- Resultados visibles en la pestaña Security del repo

**Tiempo estimado**: ~2-3 minutos

### 5. Integration Tests

**Propósito**: Probar la integración completa del sistema

**Acciones:**

- Levanta servicios con `docker-compose up -d`
- Verifica health del backend (http://localhost:9000/health)
- Verifica accesibilidad del frontend (http://localhost:9001)
- Ejecuta tests de API dentro del contenedor
- Limpia contenedores al finalizar

**Tiempo estimado**: ~2-4 minutos

### 6. Build Success

**Propósito**: Notificación de éxito

Un job simple que confirma que todos los tests pasaron.

### 7. Deploy (Producción)

**Propósito**: Deployment automático a producción

**Condiciones:**

- Solo se ejecuta en `push` (no en PR)
- Solo en las ramas `master` o `main`
- Solo si todos los jobs anteriores pasaron

**Opciones de deployment:**

#### Opción A: Docker Hub

```yaml
- Log in to Docker Hub
- Build and push backend:latest
- Build and push backend:<commit-sha>
- Build and push frontend:latest
- Build and push frontend:<commit-sha>
```

#### Opción B: AWS ECR

```yaml
- Configure AWS credentials
- Login to Amazon ECR
- Build, tag, and push to ECR
- Update ECS service
```

#### Opción C: Kubernetes

```yaml
- Setup kubectl
- Update deployment images
- Apply manifests
- Verify rollout
```

**Tiempo estimado**: ~5-10 minutos

## ⚙️ Configuración de Secretos

Para habilitar todas las funcionalidades del pipeline, configura estos secretos en GitHub:

### Requeridos para Deployment

```bash
DOCKER_USERNAME         # Usuario de Docker Hub
DOCKER_PASSWORD         # Token de Docker Hub
```

### Opcionales para features adicionales

```bash
CODECOV_TOKEN          # Para reportes de cobertura en Codecov
AWS_ACCESS_KEY_ID      # Para deployment en AWS
AWS_SECRET_ACCESS_KEY  # Para deployment en AWS
KUBE_CONFIG            # Para deployment en Kubernetes
```

### Cómo agregar secretos

1. Ve a tu repositorio en GitHub
2. Click en `Settings` → `Secrets and variables` → `Actions`
3. Click en `New repository secret`
4. Agrega el nombre y valor del secreto
5. Click en `Add secret`

## 📊 Artefactos Generados

El pipeline genera y almacena los siguientes artefactos:

| Artefacto                 | Job           | Descripción                        | Retención  |
| ------------------------- | ------------- | ---------------------------------- | ---------- |
| `backend-coverage-report` | backend-tests | Reporte HTML de cobertura          | 30 días    |
| `trivy-results.sarif`     | security-scan | Resultados de escaneo de seguridad | Permanente |

## 🔍 Monitoreo y Debugging

### Ver el estado del pipeline

1. Ve a la pestaña `Actions` en tu repositorio
2. Selecciona el workflow "CI/CD Pipeline - Calculadora"
3. Click en cualquier ejecución para ver detalles

### Debugging de fallos

**Si falla code-quality:**

```bash
# Ejecutar localmente
cd backend
flake8 app
black --check app tests

cd ../frontend
npm run lint
```

**Si fallan los tests:**

```bash
cd backend
pytest -v --tb=short
# Para ver más detalles:
pytest -vv --tb=long
```

**Si falla el Docker build:**

```bash
# Probar build local
docker build -t test-backend ./backend
docker build -t test-frontend ./frontend

# Verificar docker-compose
docker-compose config
docker-compose up --build
```

**Si falla integration-tests:**

```bash
# Levantar servicios localmente
docker-compose up -d
docker-compose logs -f

# Verificar endpoints
curl http://localhost:9000/health
curl http://localhost:9001
```

## 🚀 Personalización del Pipeline

### Agregar nuevos tests

Edita `.github/workflows/ci-cd.yml`:

```yaml
- name: Run custom tests
  run: |
    cd backend
    pytest tests/new_tests/ -v
```

### Cambiar versiones de Python/Node

```yaml
- name: Set up Python
  uses: actions/setup-python@v5
  with:
    python-version: "3.12" # Cambiar versión

- name: Set up Node.js
  uses: actions/setup-node@v4
  with:
    node-version: "20" # Cambiar versión
```

### Agregar linter adicional

```yaml
- name: Run pylint
  run: |
    cd backend
    pip install pylint
    pylint app tests
```

### Modificar estrategia de deployment

```yaml
deploy:
  name: Deploy to Production
  steps:
    # Tu estrategia personalizada aquí
    - name: Deploy to Heroku
      run: |
        heroku container:push web --app tu-app
        heroku container:release web --app tu-app
```

## 📈 Métricas y Rendimiento

### Tiempo total de ejecución

- **Sin cache**: ~15-20 minutos
- **Con cache**: ~8-12 minutos

### Optimizaciones aplicadas

1. **Cache de dependencias**: Python pip cache, npm cache
2. **Cache de Docker layers**: GitHub Actions cache
3. **Jobs paralelos**: code-quality + backend-tests + security-scan
4. **Builds incrementales**: Solo rebuild cuando hay cambios

## 🔒 Seguridad

### Buenas prácticas implementadas

- ✅ Nunca exponer secretos en logs
- ✅ Usar tokens de solo lectura cuando sea posible
- ✅ Validar inputs de usuario
- ✅ Escaneo automático de vulnerabilidades
- ✅ Pinning de versiones de actions
- ✅ Principle of least privilege para permisos

### Escaneos de seguridad

**Trivy** detecta:

- Vulnerabilidades en dependencias
- Configuraciones inseguras
- Secretos hardcodeados
- Licenses de código

**Safety** verifica:

- CVEs conocidos en paquetes Python
- Versiones desactualizadas
- Dependencias deprecadas

## 📚 Referencias

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Build Action](https://github.com/docker/build-push-action)
- [Pytest Documentation](https://docs.pytest.org/)
- [Trivy Security Scanner](https://github.com/aquasecurity/trivy)
- [Codecov](https://about.codecov.io/)

## 🤝 Contribuir

Para mejorar el pipeline:

1. Haz fork del repositorio
2. Crea una rama para tu mejora
3. Modifica `.github/workflows/ci-cd.yml`
4. Prueba localmente con [act](https://github.com/nektos/act)
5. Abre un Pull Request

## ❓ FAQ

**P: ¿Por qué falla el deployment?**
R: Verifica que los secretos `DOCKER_USERNAME` y `DOCKER_PASSWORD` estén configurados correctamente.

**P: ¿Puedo ejecutar el pipeline localmente?**
R: Sí, usa [act](https://github.com/nektos/act):

```bash
# Instalar act
brew install act

# Ejecutar workflow
act -j code-quality
act -j backend-tests
```

**P: ¿Cómo desactivo el deployment automático?**
R: Comenta o elimina el job `deploy` en `ci-cd.yml`.

**P: ¿Puedo agregar más plataformas de deployment?**
R: Sí, duplica el job `deploy` y personaliza los steps según tu plataforma.

---

**Última actualización**: 2024
**Mantenedor**: Sebastian Gallego
