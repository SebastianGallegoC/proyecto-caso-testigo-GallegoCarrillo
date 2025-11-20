# Calculadora Avanzada - React + FastAPI

![CI/CD Pipeline](https://github.com/SebastianGallegoC/proyecto-caso-testigo-GallegoCarrillo/actions/workflows/ci-cd.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.11-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-green.svg)
![React](https://img.shields.io/badge/React-18.2.0-blue.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Tests](https://img.shields.io/badge/Tests-71%20passing-success.svg)

Una calculadora moderna y completa con frontend en React y backend en FastAPI, implementando principios SOLID y patrones de diseño. **Completamente dockerizada** con **CI/CD automatizado** para facilitar el desarrollo y despliegue.

## 🚀 Características

### Funcionalidades

- ✅ **Operaciones básicas**: Suma, resta, multiplicación y división
- ⛓️ **Operaciones en cadena**: Realiza múltiples cálculos secuenciales
- 📊 **Historial**: Guarda todas las operaciones realizadas
- 🎨 **Diseño responsivo**: Funciona perfectamente en móviles, tablets y desktop
- 🌙 **Tema oscuro**: Interfaz moderna y amigable con la vista

### Arquitectura

- 🏗️ **Principios SOLID**:

  - **S**ingle Responsibility: Cada clase tiene una única responsabilidad
  - **O**pen/Closed: Abierto para extensión, cerrado para modificación
  - **L**iskov Substitution: Las operaciones son intercambiables
  - **I**nterface Segregation: Interfaces específicas para cada caso
  - **D**ependency Inversion: Dependencias basadas en abstracciones

- 🎯 **Patrones de diseño**:
  - **Strategy Pattern**: Para las operaciones matemáticas
  - **Factory Pattern**: Para crear instancias de operaciones
  - **Singleton Pattern**: Para la instancia de la calculadora y servicios

### Testing

- ✅ **Cobertura completa** con pytest
- 🧪 **Tests unitarios** para operaciones y calculadora
- 🔌 **Tests de integración** para endpoints de la API
- 📈 **95%+ de cobertura** de código

## 📁 Estructura del Proyecto

```
proyecto-caso-testigo-GallegoCarrillo/
├── backend/                    # Servidor FastAPI
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py            # Aplicación FastAPI principal
│   │   ├── operations.py      # Operaciones matemáticas (Strategy Pattern)
│   │   ├── calculator.py      # Lógica de la calculadora
│   │   └── schemas.py         # Esquemas Pydantic
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   ├── test_operations.py # Tests de operaciones
│   │   ├── test_calculator.py # Tests de calculadora
│   │   └── test_api.py        # Tests de endpoints
│   ├── requirements.txt
│   └── pyproject.toml
│
└── frontend/                   # Cliente React
    ├── src/
    │   ├── components/
    │   │   ├── Calculator.jsx # Componente principal
    │   │   ├── Calculator.css
    │   │   ├── History.jsx    # Historial de operaciones
    │   │   └── History.css
    │   ├── services/
    │   │   └── calculatorService.js # Comunicación con API
    │   ├── App.jsx
    │   ├── App.css
    │   ├── main.jsx
    │   └── index.css
    ├── index.html
    ├── package.json
    └── vite.config.js
```

## 🐳 Ejecutar con Docker (Recomendado)

### Prerequisitos

- Docker
- Docker Compose

### Inicio rápido

**1. Construir y ejecutar los contenedores:**

```bash
docker-compose up --build
```

**2. Acceder a la aplicación:**

- **Frontend**: http://localhost:9001
- **Backend API**: http://localhost:9000
- **API Docs**: http://localhost:9000/docs

## 🚀 Deployment en VPS Ubuntu

Este proyecto está configurado para **deployment automático** en un VPS Ubuntu mediante CI/CD.

### Guía Rápida (15 minutos)

1. **Preparar el VPS**: Ejecuta `setup-vps.sh` en tu servidor
2. **Configurar Secretos en GitHub**:
   - `VPS_HOST`: IP de tu VPS
   - `VPS_USER`: Usuario SSH
   - `VPS_PATH`: Ruta de la aplicación
   - `VPS_SSH_KEY`: Llave privada SSH
3. **Push a master**: El deployment se hace automáticamente

**📖 Documentación completa**: Ver [`QUICK-START-VPS.md`](QUICK-START-VPS.md) y [`DEPLOYMENT.md`](DEPLOYMENT.md)

### URLs después del deployment

Una vez deployado en tu VPS:

- Frontend: `http://TU_IP_VPS:9001`
- Backend: `http://TU_IP_VPS:9000`
- API Docs: `http://TU_IP_VPS:9000/docs`
- **Backend API**: http://localhost:9000
- **API Docs**: http://localhost:9000/docs

**3. Detener los contenedores:**

```bash
docker-compose down
```

### Comandos útiles de Docker

```bash
# Ejecutar en segundo plano
docker-compose up -d

# Ver logs
docker-compose logs -f

# Ver logs de un servicio específico
docker-compose logs -f backend
docker-compose logs -f frontend

# Reconstruir después de cambios
docker-compose up --build

# Detener y eliminar volúmenes
docker-compose down -v

# Ejecutar tests en el contenedor del backend
docker-compose exec backend pytest -v
```

## 🛠️ Instalación Manual (Sin Docker)

### Prerequisitos

- Python 3.10 o superior
- Node.js 18 o superior
- npm o yarn

### Backend (FastAPI)

1. **Navegar al directorio del backend**:

```bash
cd backend
```

2. **Crear entorno virtual** (recomendado):

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Instalar dependencias**:

```bash
pip install -r requirements.txt
```

4. **Ejecutar el servidor**:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

El servidor estará disponible en: `http://localhost:8000`

- Documentación interactiva: `http://localhost:8000/docs`
- Documentación alternativa: `http://localhost:8000/redoc`

### Frontend (React)

1. **Navegar al directorio del frontend**:

```bash
cd frontend
```

2. **Instalar dependencias**:

```bash
npm install
```

3. **Ejecutar en modo desarrollo**:

```bash
npm run dev
```

La aplicación estará disponible en: `http://localhost:5173`

## 🧪 Ejecutar Tests

### Backend Tests

```bash
cd backend

# Ejecutar todos los tests
pytest

# Con cobertura
pytest --cov=app --cov-report=html

# Tests específicos
pytest tests/test_operations.py
pytest tests/test_calculator.py
pytest tests/test_api.py

# Modo verbose
pytest -v
```

Los reportes de cobertura HTML se generan en `htmlcov/index.html`

## 📚 API Endpoints

### Operaciones

#### `POST /calculate`

Realiza una operación matemática simple.

**Request:**

```json
{
  "num1": 10,
  "num2": 5,
  "operator": "+"
}
```

**Response:**

```json
{
  "result": 15.0,
  "message": "10 + 5 = 15"
}
```

#### `POST /calculate-chain`

Realiza operaciones en cadena.

**Request:**

```json
{
  "operations": [
    { "num1": 10, "operator": "+", "num2": 5 },
    { "operator": "*", "num2": 2 },
    { "operator": "-", "num2": 3 }
  ]
}
```

**Response:**

```json
{
  "result": 27.0,
  "message": "Operaciones en cadena ejecutadas exitosamente"
}
```

### Historial

#### `GET /history`

Obtiene el historial de operaciones.

**Response:**

```json
{
  "history": [
    {
      "num1": 10,
      "num2": 5,
      "operator": "+",
      "result": 15
    }
  ],
  "count": 1
}
```

#### `DELETE /history`

Limpia el historial de operaciones.

### Información

#### `GET /operations`

Lista las operaciones soportadas.

#### `GET /health`

Verifica el estado del servicio.

#### `GET /`

Endpoint raíz con información de la API.

## 🎨 Características del Frontend

### Modo de Operaciones en Cadena

1. Click en "⛓️ Activar Cadena"
2. Realiza operaciones secuenciales
3. El resultado de cada operación se usa como entrada para la siguiente

### Historial Interactivo

- Visualiza todas las operaciones realizadas
- Contador de operaciones
- Botón para limpiar historial
- Animaciones fluidas

### Diseño Responsivo

- **Desktop**: Diseño amplio con todas las características
- **Tablet**: Adaptación óptima del layout
- **Mobile**: Interfaz táctil optimizada

## 🏗️ Principios SOLID Implementados

### Single Responsibility Principle (SRP)

- `Operation`: Solo define la interfaz de operaciones
- `Calculator`: Solo maneja lógica de cálculos
- `OperationFactory`: Solo crea instancias de operaciones

### Open/Closed Principle (OCP)

- Nuevas operaciones se agregan extendiendo `Operation`, sin modificar código existente

### Liskov Substitution Principle (LSP)

- Todas las operaciones son intercambiables a través de la interfaz `Operation`

### Interface Segregation Principle (ISP)

- Esquemas Pydantic específicos para cada tipo de request/response

### Dependency Inversion Principle (DIP)

- La calculadora depende de la abstracción `Operation`, no de implementaciones concretas

## 🎯 Patrones de Diseño

### Strategy Pattern

```python
class Operation(ABC):
    @abstractmethod
    def execute(self, a: float, b: float) -> float:
        pass

class Addition(Operation):
    def execute(self, a: float, b: float) -> float:
        return a + b
```

### Factory Pattern

```python
class OperationFactory:
    @classmethod
    def create_operation(cls, operator: str) -> Operation:
        operation_class = cls._operations.get(operator)
        return operation_class()
```

### Singleton Pattern

- Instancia única de `Calculator` en el backend
- Instancia única de `CalculatorService` en el frontend

## 🔒 Manejo de Errores

- Validación de datos con Pydantic
- Manejo de división por cero
- Validación de operadores
- Mensajes de error descriptivos
- Estados de carga en el frontend

## 🚀 Deployment y Producción

### CI/CD Pipeline

Este proyecto cuenta con un pipeline de CI/CD completamente automatizado usando **GitHub Actions**. El pipeline se ejecuta automáticamente en cada push y pull request.

#### Flujo de trabajo del CI/CD

**1. Code Quality & Linting** 🔍

- Linting del código Python con `flake8`
- Verificación de formato con `black`
- Linting del código React con ESLint

**2. Backend Tests** 🧪

- Ejecución de 71 tests unitarios e integración con pytest
- Generación de reportes de cobertura de código
- Upload de coverage reports a Codecov

**3. Docker Build & Test** 🐳

- Build de imagen Docker del backend
- Build de imagen Docker del frontend
- Validación de docker-compose.yml
- Cache de capas de Docker para builds más rápidos

**4. Security Scan** 🔒

- Escaneo de vulnerabilidades con Trivy
- Verificación de dependencias Python con Safety
- Upload de resultados a GitHub Security

**5. Integration Tests** 🔗

- Tests de integración con servicios levantados
- Verificación de endpoints de API
- Validación de comunicación frontend-backend

**6. Deployment (solo master/main)** 🚀

- Build y push de imágenes a Docker Hub (opcional)
- Deploy automático a producción
- Notificación de éxito del deployment

#### Configurar secretos en GitHub

Para habilitar el deployment completo, configura estos secretos en tu repositorio:

1. Ve a `Settings > Secrets and variables > Actions`
2. Agrega los siguientes secretos:

```
CODECOV_TOKEN          # Token de Codecov (opcional)
DOCKER_USERNAME        # Usuario de Docker Hub (opcional)
DOCKER_PASSWORD        # Password/Token de Docker Hub (opcional)
```

#### Badges de estado

El badge de CI/CD en el README muestra el estado actual del pipeline:

- ✅ Verde: Todas las pruebas pasaron
- ❌ Rojo: Alguna prueba falló
- 🟡 Amarillo: Pipeline en ejecución

### Deployment Manual

#### Backend

```bash
# Instalar dependencias de producción
pip install -r requirements.txt

# Ejecutar con Gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

#### Frontend

```bash
# Construir para producción
npm run build

# Los archivos estarán en dist/
```

### Deployment con Docker

#### Opción 1: Docker Hub

```bash
# Backend
docker build -t tu-usuario/calculadora-backend:latest ./backend
docker push tu-usuario/calculadora-backend:latest

# Frontend
docker build -t tu-usuario/calculadora-frontend:latest ./frontend
docker push tu-usuario/calculadora-frontend:latest
```

#### Opción 2: GitHub Container Registry

```bash
# Login
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin

# Backend
docker build -t ghcr.io/tu-usuario/calculadora-backend:latest ./backend
docker push ghcr.io/tu-usuario/calculadora-backend:latest

# Frontend
docker build -t ghcr.io/tu-usuario/calculadora-frontend:latest ./frontend
docker push ghcr.io/tu-usuario/calculadora-frontend:latest
```

### Plataformas de deployment recomendadas

- **AWS ECS/EKS**: Para despliegue enterprise con alta disponibilidad
- **Google Cloud Run**: Serverless con escalado automático
- **Heroku**: Deployment simple con Docker
- **DigitalOcean App Platform**: Económico y fácil de usar
- **Railway**: Deployment moderno con soporte para Docker Compose
- **Render**: Free tier generoso con soporte para servicios múltiples

## 📝 Licencia

Este proyecto está bajo la Licencia MIT.

## 👨‍💻 Autor

Desarrollado como proyecto de Codificación y Pruebas de Software - FESC Universidad

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📞 Soporte

Para preguntas o soporte, por favor abre un issue en el repositorio.

---

**Desarrollado con ❤️ usando Python, FastAPI, React y principios de ingeniería de software**
