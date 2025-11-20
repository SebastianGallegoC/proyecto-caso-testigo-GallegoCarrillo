# Calculadora Avanzada - React + FastAPI

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-green.svg)
![React](https://img.shields.io/badge/React-18.2.0-blue.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

Una calculadora moderna y completa con frontend en React y backend en FastAPI, implementando principios SOLID y patrones de diseño. **Completamente dockerizada** para facilitar el despliegue.

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

## 🚀 Construcción para Producción

### Backend

```bash
# Instalar dependencias de producción
pip install -r requirements.txt

# Ejecutar con Gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Frontend

```bash
# Construir para producción
npm run build

# Los archivos estarán en dist/
```

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
