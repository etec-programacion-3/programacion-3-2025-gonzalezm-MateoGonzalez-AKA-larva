from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from .database import SessionLocal, engine, Base
from .models import Producto, Proveedor, MovimientoDeStock, TipoMovimiento


# Crear tablas
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependencia para la sesión
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Crear un producto
@app.post("/api/products")
def create_product(nombre: str, sku: str, precio_compra: float, precio_venta: float, stock_actual: int = 0, db: Session = Depends(get_db)):
    producto = Producto(nombre=nombre, sku=sku, precio_compra=precio_compra, precio_venta=precio_venta, stock_actual=stock_actual)
    db.add(producto)
    db.commit()
    db.refresh(producto)
    return producto

# Listar productos
@app.get("/api/products")
def list_products(db: Session = Depends(get_db)):
    return db.query(Producto).all()

# Obtener producto por ID
@app.get("/api/products/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)):
    producto = db.query(Producto).filter(Producto.id == product_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

# Actualizar producto por ID
@app.put("/api/products/{product_id}")
def update_product(product_id: int, nombre: str = None, sku: str = None, precio_compra: float = None, precio_venta: float = None, stock_actual: int = None, db: Session = Depends(get_db)):
    producto = db.query(Producto).filter(Producto.id == product_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    if nombre is not None:
        producto.nombre = nombre
    if sku is not None:
        producto.sku = sku
    if precio_compra is not None:
        producto.precio_compra = precio_compra
    if precio_venta is not None:
        producto.precio_venta = precio_venta
    if stock_actual is not None:
        producto.stock_actual = stock_actual
    db.commit()
    db.refresh(producto)
    return producto

# Eliminar producto por ID
@app.delete("/api/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    producto = db.query(Producto).filter(Producto.id == product_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    db.delete(producto)
    db.commit()
    return {"detail": "Producto eliminado"}
