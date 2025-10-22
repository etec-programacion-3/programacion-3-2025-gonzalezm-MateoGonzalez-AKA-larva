# backend/main.py
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel

# Importar los módulos locales
from . import models, database

# Crear las tablas en la base de datos
models.Base.metadata.create_all(bind=database.engine)

# Inicializar FastAPI
app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica los orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================
# Schemas Pydantic
# ==========================
class ProductoCreate(BaseModel):
    nombre: str
    sku: str
    descripcion: str | None = None
    precio_compra: float
    precio_venta: float
    stock_actual: int = 0
    proveedor_id: int | None = None

class ProductoUpdate(BaseModel):
    nombre: str | None = None
    sku: str | None = None
    descripcion: str | None = None
    precio_compra: float | None = None
    precio_venta: float | None = None
    stock_actual: int | None = None
    proveedor_id: int | None = None

class MovimientoCreate(BaseModel):
    producto_id: int
    cantidad: int
    tipo: str  # 'entrada' o 'salida'

# ==========================
# Rutas
# ==========================
@app.get("/")
def root():
    return {"message": "API backend funcionando correctamente"}

# ==========================
# CRUD Productos
# ==========================
@app.post("/api/products")
def create_product(producto: ProductoCreate, db: Session = Depends(database.get_db)):
    nuevo_producto = models.Producto(
        nombre=producto.nombre,
        sku=producto.sku,
        descripcion=producto.descripcion,
        precio_compra=producto.precio_compra,
        precio_venta=producto.precio_venta,
        stock_actual=producto.stock_actual,
        proveedor_id=producto.proveedor_id
    )
    db.add(nuevo_producto)
    db.commit()
    db.refresh(nuevo_producto)
    return nuevo_producto

@app.get("/")
def root():
    return {"message": "API backend funcionando correctamente"}

# Agregar esta nueva ruta:
@app.get("/productos")
def get_productos(db: Session = Depends(database.get_db)):
    productos = db.query(models.Producto).all()
    return productos

@app.get("/api/products")
def list_products(db: Session = Depends(database.get_db)):
    return db.query(models.Producto).all()

@app.get("/api/products/{product_id}")
def get_product(product_id: int, db: Session = Depends(database.get_db)):
    producto = db.query(models.Producto).filter(models.Producto.id == product_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

@app.put("/api/products/{product_id}")
def update_product(product_id: int, producto: ProductoUpdate, db: Session = Depends(database.get_db)):
    existing = db.query(models.Producto).filter(models.Producto.id == product_id).first()
    if not existing:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    for field, value in producto.dict(exclude_unset=True).items():
        setattr(existing, field, value)
    
    db.commit()
    db.refresh(existing)
    return existing

@app.delete("/api/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(database.get_db)):
    producto = db.query(models.Producto).filter(models.Producto.id == product_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    db.delete(producto)
    db.commit()
    return {"detail": "Producto eliminado"}

# ==========================
# Movimientos de Stock
# ==========================
@app.post("/api/stock/movements")
def create_stock_movement(movimiento: MovimientoCreate, db: Session = Depends(database.get_db)):
    producto = db.query(models.Producto).filter(models.Producto.id == movimiento.producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    # Validar tipo de movimiento
    if movimiento.tipo not in ["entrada", "salida"]:
        raise HTTPException(status_code=400, detail="Tipo debe ser 'entrada' o 'salida'")

    # Verificar stock suficiente si es salida
    if movimiento.tipo == "salida" and movimiento.cantidad > producto.stock_actual:
        raise HTTPException(status_code=400, detail="Stock insuficiente")

    # Ajustar stock según tipo
    if movimiento.tipo == "entrada":
        producto.stock_actual += movimiento.cantidad
    else:  # salida
        producto.stock_actual -= movimiento.cantidad

    # Crear registro de movimiento
    tipo_enum = models.TipoMovimiento.entrada if movimiento.tipo == "entrada" else models.TipoMovimiento.salida
    nuevo_movimiento = models.MovimientoDeStock(
        producto_id=producto.id,
        cantidad=movimiento.cantidad,
        tipo=tipo_enum
    )

    try:
        db.add(nuevo_movimiento)
        db.commit()
        db.refresh(nuevo_movimiento)
        db.refresh(producto)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al registrar movimiento: {str(e)}")
       
    return {"producto": producto, "movimiento": nuevo_movimiento}