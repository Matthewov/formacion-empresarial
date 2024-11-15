from pydantic import BaseModel, Field
from datetime import date
from typing import Optional



class ProductoCreate(BaseModel):
    nombre: str = Field(..., description="Nombre del producto")
    inventario: int = Field(default=0)
    precio_venta: float
    costo: float
    codigo_id: int
    tipo_id: int
    bodega_id: int
    categoria_id: int
    marca_id: int
    unidad_medida_id: int

class Producto(ProductoCreate):
    id_producto: int


class CodigoCreate(BaseModel):
    codigo: str = Field(..., description="Código único del producto")

class Codigo(CodigoCreate):
    id_codigo: int


class TipoCreate(BaseModel):
    tipo: str = Field(..., description="Tipo de producto")

class Tipo(TipoCreate):
    id_tipo: int


class BodegaCreate(BaseModel):
    nombre: str = Field(..., description="Nombre de la bodega")

class Bodega(BodegaCreate):
    id_bodega: int


class CategoriaCreate(BaseModel):
    nombre: str = Field(..., description="Nombre de la categoría")

class Categoria(CategoriaCreate):
    id_categoria: int


class MarcaCreate(BaseModel):
    nombre: str = Field(..., description="Nombre de la marca")

class Marca(MarcaCreate):
    id_marca: int


class UnidadMedidaCreate(BaseModel):
    nombre: str = Field(..., description="Nombre de la unidad de medida")

class UnidadMedida(UnidadMedidaCreate):
    id_unidad_medida: int