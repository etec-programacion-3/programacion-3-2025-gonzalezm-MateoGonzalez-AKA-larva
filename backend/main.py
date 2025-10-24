# backend/main.py
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

# Importar los módulos locales
from . import models, database, schemas # 🔹 Importamos schemas
from .routers import products # 🔹 Importamos el nuevo router

# Crear las tablas en la base de datos
models.Base.metadata.create_all(bind=database.engine)

# Inicializar FastAPI
app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# Rutas
# =========================

# 🔹 Incluimos el router de productos
app.include_router(products.router)

@app.get("/")
def root():
    return {"message": "API de Gestión de Stock"}

# ==================================
# Rutas de Movimientos de Stock
# (Se mantienen aquí por ahora)
# ==================================
@app.post("/api/stock/movements")
def create_movement(movimiento: schemas.MovimientoCreate, db: Session = Depends(database.get_db)):
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