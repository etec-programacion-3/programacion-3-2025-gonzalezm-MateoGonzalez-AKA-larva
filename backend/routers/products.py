# backend/routers/products.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

# 🔹 Importamos 'auth' y 'schemas' (para el User)
from .. import models, schemas, database, auth

router = APIRouter(
    prefix="/api/products",
    tags=["products"]
)

# 🔹 Definimos la dependencia una vez
UserDependency = Depends(auth.get_current_user)

# 🔹 Protegemos TODOS los endpoints con UserDependency
@router.get("/", response_model=List[schemas.Producto])
def get_products(
    db: Session = Depends(database.get_db), 
    current_user: schemas.User = UserDependency, # Protegido
    nombre: str | None = None,
    skip: int = 0, 
    limit: int = 100
):
    # ... (código existente) ...
    query = db.query(models.Producto)
    if nombre:
        query = query.filter(models.Producto.nombre.contains(nombre))
    productos = query.offset(skip).limit(limit).all()
    return productos

@router.post("/", response_model=schemas.Producto, status_code=201)
def create_product(
    product: schemas.ProductoCreate, 
    db: Session = Depends(database.get_db),
    current_user: schemas.User = UserDependency # Protegido
):
    # ... (código existente) ...
    db_product_sku = db.query(models.Producto).filter(models.Producto.sku == product.sku).first()
    if db_product_sku:
        raise HTTPException(status_code=400, detail="SKU ya registrado")
    db_product = models.Producto(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.get("/{product_id}", response_model=schemas.Producto)
def get_product(
    product_id: int, 
    db: Session = Depends(database.get_db),
    current_user: schemas.User = UserDependency # Protegido
):
    # ... (código existente) ...
    db_product = db.query(models.Producto).filter(models.Producto.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return db_product

@router.put("/{product_id}", response_model=schemas.Producto)
def update_product(
    product_id: int, 
    product: schemas.ProductoUpdate, 
    db: Session = Depends(database.get_db),
    current_user: schemas.User = UserDependency # Protegido
):
    # ... (código existente) ...
    db_product = db.query(models.Producto).filter(models.Producto.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    update_data = product.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.delete("/{product_id}", status_code=204)
def delete_product(
    product_id: int, 
    db: Session = Depends(database.get_db),
    current_user: schemas.User = UserDependency # Protegido
):
    # ... (código existente) ...
    db_product = db.query(models.Producto).filter(models.Producto.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    db.delete(db_product)
    db.commit()
    return