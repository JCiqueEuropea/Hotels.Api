# Hotels.Api 🏨

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.0+-green.svg)](https://www.djangoproject.com/)
[![Framework](https://img.shields.io/badge/DRF-Professional-red.svg)](https://www.django-rest-framework.org/)
[![Architecture](https://img.shields.io/badge/Architecture-DDD%20%2B%20Clean-orange.svg)](#arquitectura)

**Hotels.Api** es un backend profesional diseñado bajo los principios de **Domain-Driven Design (DDD)** y **Clean Architecture**. El objetivo es proporcionar una base sólida, escalable y altamente testeable para la gestión de hoteles, habitaciones y reservas.

---

## 🚀 Características Principales

- **Arquitectura Limpia**: Separación estricta de responsabilidades en capas (Domain, Application, Infrastructure, Core).
- **Domain-Driven Design (DDD)**: Entidades ricas, Value Objects y lógica de negocio centralizada en el dominio, sin dependencias del framework.
- **SOLID & Clean Code**: Implementación estricta de principios de diseño orientado a objetos.
- **MySQL**: Persistencia robusta para entornos de producción.
- **Docker Ready**: Configuración completa con Docker y Docker Compose.
- **Validación Robusta**: Middleware global para manejo de excepciones y respuestas estandarizadas.

---

## 🏗️ Arquitectura

El proyecto sigue una estructura de cebolla (Onion Architecture) donde las dependencias apuntan hacia adentro:

1.  **Domain**: El corazón del negocio. Contiene entidades, value objects, interfaces de repositorios y servicios de dominio. **No depende de Django ni de ninguna librería externa**.
2.  **Application**: Orquesta el flujo de datos. Contiene los casos de uso (Use Cases) y DTOs.
3.  **Infrastructure**: Detalles de implementación. Django ORM, controladores API (DRF), adaptadores de repositorios y servicios externos (notificaciones).
4.  **Core**: Elementos transversales como excepciones base, configuración de settings y middleware.

### Estructura de Carpetas

```text
hotels_api/
├── domain/            # Reglas de negocio puras
├── application/       # Casos de uso y orquestación
├── infrastructure/    # Implementaciones técnicas (Django, API, DB)
├── core/              # Configuración global y excepciones
└── manage.py
```

---

## 🛠️ Tecnologías

- **Lenguaje**: Python 3.12+
- **Framework Web**: Django 5.x
- **API**: Django Rest Framework (DRF)
- **Base de Datos**: MySQL
- **Contenedores**: Docker & Docker Compose
- **Testing**: Pytest / Unittest

---

## 🚦 Guía de Inicio Rápido

### Requisitos Previos

- Docker y Docker Compose instalados.
- O Python 3.12+ y MySQL si se ejecuta localmente.

### Opción 1: Docker (Recomendado)

1.  Copia el archivo de ejemplo de variables de entorno:
    ```bash
    cp .env.example .env
    ```
2.  Levanta los servicios:
    ```bash
    docker-compose up --build
    ```
3.  La API estará disponible en: `http://localhost:8000/api/`

### Opción 2: Local

1.  Crea un entorno virtual e instala dependencias:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # En Windows: .venv\Scripts\activate
    pip install -r requirements.txt
    ```
2.  Configura tus variables de entorno en un archivo `.env`.
3.  Ejecuta las migraciones:
    ```bash
    python manage.py migrate
    ```
4.  Inicia el servidor:
    ```bash
    python manage.py runserver
    ```

---

## 📡 API Endpoints

### Habitaciones (Rooms)
- `GET /api/rooms` - Listar habitaciones (con filtros y paginación)
- `POST /api/rooms` - Crear nueva habitación
- `PUT /api/rooms/{id}` - Actualizar habitación
- `DELETE /api/rooms/{id}` - Soft delete de habitación

### Habitaciones de Eventos (Event Rooms)
- `GET /api/event-rooms` - Listar salas de eventos
- `POST /api/event-rooms` - Crear sala de eventos
- `PUT /api/event-rooms/{id}` - Configurar calendario/horario de sala de eventos

### Reservas (Reservations)
- `GET /api/reservations` - Listar reservas
- `POST /api/reservations` - Crear reserva
- `POST /api/reservations/{id}/approve` - Aprobar reserva
- `POST /api/reservations/{id}/reject` - Rechazar reserva

### Estadísticas
- `GET /api/stats/occupancy?year=2024&month=05` - Ocupación mensual

---

## 🧪 Testing

Para ejecutar los tests unitarios de dominio y casos de uso:

```bash
python manage.py test tests/unit
```

---

## 📝 Reglas de Negocio Implementadas

- **Validaciones de Dominio**: No se permiten precios negativos, emails inválidos o rangos de fechas inconsistentes.
- **Disponibilidad**: No se puede reservar una habitación si ya existe una reserva aprobada en esas fechas.
- **Flujo de Estados**: Una reserva rechazada no puede ser aprobada posteriormente.
- **Notificaciones**: Sistema simulado de notificaciones al cambiar el estado de las reservas.
