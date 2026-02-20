"""
Capa Application
- Orquesta casos de uso (aplica reglas del dominio coordinando repositorios y servicios).
- Define DTOs de entrada/salida para no acoplarse a transporte (HTTP) ni a infraestructura.
- No conoce HTTP ni Django; solo depende de las interfaces del dominio.
"""
