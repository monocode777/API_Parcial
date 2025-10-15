# Configuración de JWT
import os

# Clave secreta (usa una variable de entorno para mayor seguridad)
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "clave_secreta_por_defecto")

# Dónde se espera recibir el token (en los headers normalmente)
JWT_TOKEN_LOCATION = ["headers"]

# Tiempo de expiración del token en segundos (1 hora)
JWT_ACCESS_TOKEN_EXPIRES = 3600

# Nombre y tipo de encabezado usado para enviar el token
JWT_HEADER_NAME = "Authorization"
JWT_HEADER_TYPE = "Bearer"
