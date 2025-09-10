from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship, declarative_base
import enum
from datetime import datetime

Base = declarative_base()

class Producto(Base):
    __tablename__ = "productos"
    id = Column(Integer, primary_key=True)
    sku = Column(String, unique=True, nullable=False)
    nombre = Column(String, nullable=False)
    descripcion = Column(String)
    precio_compra = Column(Float)
    precio_venta = Column(Float)
    stock_actual = Column(Integer, default=0)
    proveedor_id = Column(Integer, ForeignKey("proveedores.id"))
    proveedor = relationship("Proveedor", back_populates="productos")
    movimientos = relationship("MovimientoDeStock", back_populates="producto")

class Proveedor(Base):
    __tablename__ = "proveedores"
    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    contacto = Column(String)
    productos = relationship("Producto", back_populates="proveedor")

class TipoMovimiento(enum.Enum):
    entrada = "entrada"
    salida = "salida"

class MovimientoDeStock(Base):
    __tablename__ = "movimientos_de_stock"
    id = Column(Integer, primary_key=True)
    tipo = Column(Enum(TipoMovimiento))
    cantidad = Column(Integer)
    fecha = Column(DateTime, default=datetime.utcnow)
    producto_id = Column(Integer, ForeignKey("productos.id"))
    producto = relationship("Producto", back_populates="movimientos")
