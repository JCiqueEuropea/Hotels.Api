# Cómo arrancar la aplicación

## 1. Crear el archivo `.env`

Antes de arrancar, crea un archivo `.env` en la raíz del proyecto con, como mínimo, estas variables:

```dotenv
MYSQL_DATABASE=some
MYSQL_USER=some
MYSQL_PASSWORD=some
MYSQL_ROOT_PASSWORD=some
MYSQL_HOST=some
MYSQL_PORT=some
```

## 2. Instalar dependencias

Ejecuta:

```bash
pip install -r requirements.txt
```

## 3. Ejecutar migraciones

Ejecuta:

```bash
python manage.py migrate
```

## 4. Arrancar la aplicación

Una vez completados los pasos anteriores, ya puedes arrancar la aplicación.

## Advertencia importante

Si ya tienes datos en la base de datos SQLite que crea Django por defecto, haz un dump/exportación de esos datos antes de ejecutar la migración.
