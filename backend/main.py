from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from .database import SessionLocal, engine, Base
from .models import Producto, MovimientoDeStock

# ==========================
# Crear tablas si no existen
# ==========================
Base.metadata.create_all(bind=engine)

app = FastAPI()

# ==========================
# Dependencia de sesión DB
# ==========================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ==========================
# Schemas Pydantic
# ==========================
class ProductoCreate(BaseModel):
    nombre: str
    sku: str
    precio_compra: float
    precio_venta: float
    stock_actual: int = 0

class ProductoUpdate(BaseModel):
    nombre: str | None = None
    sku: str | None = None
    precio_compra: float | None = None
    precio_venta: float | None = None
    stock_actual: int | None = None

class MovimientoCreate(BaseModel):
    producto_id: int
    cantidad: int
    tipo: str  # 'ingreso', 'venta', 'ajuste'

# ==========================
# CRUD Productos
# ==========================
@app.post("/api/products")
def create_product(producto: ProductoCreate, db: Session = Depends(get_db)):
    nuevo_producto = Producto(
        nombre=producto.nombre,
        sku=producto.sku,
        precio_compra=producto.precio_compra,
        precio_venta=producto.precio_venta,
        stock_actual=producto.stock_actual
    )
    db.add(nuevo_producto)
    db.commit()
    db.refresh(nuevo_producto)
    return nuevo_producto

@app.get("/api/products")
def list_products(db: Session = Depends(get_db)):
    return db.query(Producto).all()

@app.get("/api/products/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)):
    producto = db.query(Producto).filter(Producto.id == product_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

@app.put("/api/products/{product_id}")
def update_product(product_id: int, producto: ProductoUpdate, db: Session = Depends(get_db)):
    existing = db.query(Producto).filter(Producto.id == product_id).first()
    if not existing:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    for field, value in producto.dict(exclude_unset=True).items():
        setattr(existing, field, value)
    db.commit()
    db.refresh(existing)
    return existing

@app.delete("/api/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    producto = db.query(Producto).filter(Producto.id == product_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    db.delete(producto)
    db.commit()
    return {"detail": "Producto eliminado"}

# ==========================
# Movimientos de Stock
# ==========================
@app.post("/api/stock/movements")
def create_stock_movement(movimiento: MovimientoCreate, db: Session = Depends(get_db)):
    producto = db.query(Producto).filter(Producto.id == movimiento.producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    # Verificar stock suficiente si es salida
    if movimiento.tipo in ["venta", "ajuste"] and movimiento.cantidad > producto.stock_actual:
        raise HTTPException(status_code=400, detail="Cantidad mayor al stock disponible")

    # Ajustar stock según tipo
    if movimiento.tipo == "ingreso":
        producto.stock_actual += movimiento.cantidad
    else:  # 'venta' o 'ajuste'
        producto.stock_actual -= movimiento.cantidad

    # Crear registro de movimiento
    nuevo_movimiento = MovimientoDeStock(
        producto_id=producto.id,
        cantidad=movimiento.cantidad,
        tipo=movimiento.tipo
    )

    # Transacción atómica
    try:
        db.add(nuevo_movimiento)
        db.commit()
        db.refresh(nuevo_movimiento)
    except:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error al registrar movimiento")

    return {"producto": producto, "movimiento": nuevo_movimiento}
