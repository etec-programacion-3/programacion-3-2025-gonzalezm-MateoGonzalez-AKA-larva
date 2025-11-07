# backend/auth.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone

from . import database, models, schemas

# ==================================
# 1. Configuración de Seguridad
# ==================================

# 🔹 IMPORTANTE: Cambia esto por una clave secreta real y guárdala segura
SECRET_KEY = "tu_clave_secreta_aqui" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Contexto para hashear contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Esquema de autenticación (apunta al endpoint de login)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

# ==================================
# 2. Funciones de Hashing
# ==================================
def verify_password(plain_password, hashed_password):
    # Truncar la contraseña a 72 bytes antes de verificar
    password_bytes = plain_password.encode('utf-8')[:72]
    return pwd_context.verify(password_bytes, hashed_password)

def get_password_hash(password):
    # Truncar la contraseña a 72 bytes antes de hashear
    # bcrypt tiene un límite de 72 bytes
    password_bytes = password.encode('utf-8')[:72]
    return pwd_context.hash(password_bytes)

# ==================================
# 3. Funciones de JWT
# ==================================
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# ==================================
# 4. Dependencia de Autenticación
# (Esta es la función que protegerá las rutas)
# ==================================
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    user = db.query(models.User).filter(models.User.username == token_data.username).first()
    if user is None:
        raise credentials_exception
    return user