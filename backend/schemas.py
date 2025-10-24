# backend/schemas.py
from pydantic import BaseModel

# =========================
# Schemas Pydantic
# =========================

# Schema para la creación de Producto
class ProductoCreate(BaseModel):
    nombre: str
    sku: str
    descripcion: str | None = None
    precio_compra: float
    precio_venta: float
    stock_actual: int = 0
    proveedor_id: int | None = None

# Schema para la actualización de Producto
class ProductoUpdate(BaseModel):
    nombre: str | None = None
    sku: str | None = None
    descripcion: str | None = None
    precio_compra: float | None = None
    precio_venta: float | None = None
    stock_actual: int | None = None
    proveedor_id: int | None = None

# Schema para la respuesta (lectura) de Producto
# (Usado en products.py, aunque no lo subiste, lo necesitarás)
class Producto(ProductoCreate):
    id: int

    class Config:
        from_attributes = True  # Para Pydantic v2 (reemplaza orm_mode)

# Schema para la creación de Movimiento
class MovimientoCreate(BaseModel):
    producto_id: int
    cantidad: int
    tipo: str  # 'entrada' o 'salida'

# Schema para la respuesta (lectura) de Movimiento
class Movimiento(MovimientoCreate):
    id: int
    
    class Config:
        from_attributes = True