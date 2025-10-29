from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
from .database import Base
import enum

class TipoMovimiento(enum.Enum):
    entrada = "entrada"
    salida = "salida"

class Proveedor(Base):
    __tablename__ = "proveedores"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)

    # 🔹 CORREGIDO: Especificar la ruta completa del módulo
    productos = relationship("backend.models.Producto", back_populates="proveedor")


class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String, unique=True, index=True)
    nombre = Column(String, index=True)
    descripcion = Column(String, nullable=True)
    precio_compra = Column(Float)
    precio_venta = Column(Float)
    stock_actual = Column(Integer, default=0)
    proveedor_id = Column(Integer, ForeignKey("proveedores.id"), nullable=True)

    # 🔹 CORREGIDO: Especificar la ruta completa del módulo
    proveedor = relationship("backend.models.Proveedor", back_populates="productos")
    movimientos = relationship("backend.models.MovimientoDeStock", back_populates="producto")


class MovimientoDeStock(Base):
    __tablename__ = "movimientos"

    id = Column(Integer, primary_key=True, index=True)
    producto_id = Column(Integer, ForeignKey("productos.id"))
    tipo = Column(Enum(TipoMovimiento))
    cantidad = Column(Integer)

    # 🔹 CORREGIDO: Especificar la ruta completa del módulo
    producto = relationship("backend.models.Producto", back_populates="movimientos")

# ==================================
# Modelo de Usuario (Añadido en la Issue 5.1)
# ==================================
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)