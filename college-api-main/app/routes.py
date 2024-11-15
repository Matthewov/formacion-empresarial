from fastapi import APIRouter, HTTPException
from app.models import (ProductoCreate, Producto, CodigoCreate, Codigo,
                       TipoCreate, Tipo, BodegaCreate, Bodega,
                       CategoriaCreate, Categoria, MarcaCreate, Marca,
                       UnidadMedidaCreate, UnidadMedida)
from app.database import get_db_connection
from typing import List

router = APIRouter()


@router.post("/productos/", response_model=Producto)
def create_producto(producto: ProductoCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        query = """
        INSERT INTO productos (nombre, inventario, precio_venta, costo, codigo_id, 
        tipo_id, bodega_id, categoria_id, marca_id, unidad_medida_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (producto.nombre, producto.inventario, producto.precio_venta, 
                 producto.costo, producto.codigo_id, producto.tipo_id, 
                 producto.bodega_id, producto.categoria_id, producto.marca_id, 
                 producto.unidad_medida_id)
        
        cursor.execute(query, values)
        conn.commit()
        
        producto_id = cursor.lastrowid
        return Producto(id_producto=producto_id, **producto.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.get("/productos/", response_model=List[Producto])
def list_productos():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        query = "SELECT * FROM productos"
        cursor.execute(query)
        productos = cursor.fetchall()
        return [Producto(**producto) for producto in productos]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.post("/productos/bulk/", response_model=List[Producto])
def create_productos_bulk(productos: List[ProductoCreate]):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        created_productos = []
        for producto in productos:
            query = """
            INSERT INTO productos (nombre, inventario, precio_venta, costo, codigo_id, 
            tipo_id, bodega_id, categoria_id, marca_id, unidad_medida_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (producto.nombre, producto.inventario, producto.precio_venta, 
                     producto.costo, producto.codigo_id, producto.tipo_id, 
                     producto.bodega_id, producto.categoria_id, producto.marca_id, 
                     producto.unidad_medida_id)
            
            cursor.execute(query, values)
            producto_id = cursor.lastrowid
            created_productos.append(Producto(id_producto=producto_id, **producto.dict()))
        
        conn.commit()
        return created_productos
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()


@router.post("/codigos/", response_model=Codigo)
def create_codigo(codigo: CodigoCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        query = "INSERT INTO codigo (codigo) VALUES (%s)"
        cursor.execute(query, (codigo.codigo,))
        conn.commit()
        
        codigo_id = cursor.lastrowid
        return Codigo(id_codigo=codigo_id, **codigo.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.get("/codigos/", response_model=List[Codigo])
def list_codigos():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        query = "SELECT * FROM codigo"
        cursor.execute(query)
        codigos = cursor.fetchall()
        return [Codigo(**codigo) for codigo in codigos]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()


@router.post("/tipos/", response_model=Tipo)
def create_tipo(tipo: TipoCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        query = "INSERT INTO tipo (tipo) VALUES (%s)"
        cursor.execute(query, (tipo.tipo,))
        conn.commit()
        
        tipo_id = cursor.lastrowid
        return Tipo(id_tipo=tipo_id, **tipo.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.get("/tipos/", response_model=List[Tipo])
def list_tipos():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        query = "SELECT * FROM tipo"
        cursor.execute(query)
        tipos = cursor.fetchall()
        return [Tipo(**tipo) for tipo in tipos]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.post("/tipos/bulk/", response_model=List[Tipo])
def create_tipos_bulk(tipos: List[TipoCreate]):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        created_tipos = []
        for tipo in tipos:
            query = "INSERT INTO tipo (tipo) VALUES (%s)"
            cursor.execute(query, (tipo.tipo,))
            tipo_id = cursor.lastrowid
            created_tipos.append(Tipo(id_tipo=tipo_id, **tipo.dict()))
        
        conn.commit()
        return created_tipos
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.post("/bodegas/", response_model=Bodega)
def create_bodega(bodega: BodegaCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        query = "INSERT INTO bodega (nombre) VALUES (%s)"
        cursor.execute(query, (bodega.nombre,))
        conn.commit()
        
        bodega_id = cursor.lastrowid
        return Bodega(id_bodega=bodega_id, **bodega.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.get("/bodegas/", response_model=List[Bodega])
def list_bodegas():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        query = "SELECT * FROM bodega"
        cursor.execute(query)
        bodegas = cursor.fetchall()
        return [Bodega(**bodega) for bodega in bodegas]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.post("/bodegas/bulk/", response_model=List[Bodega])
def create_bodegas_bulk(bodegas: List[BodegaCreate]):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        created_bodegas = []
        for bodega in bodegas:
            query = "INSERT INTO bodega (nombre) VALUES (%s)"
            cursor.execute(query, (bodega.nombre,))
            bodega_id = cursor.lastrowid
            created_bodegas.append(Bodega(id_bodega=bodega_id, **bodega.dict()))
        
        conn.commit()
        return created_bodegas
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()


@router.post("/categorias/", response_model=Categoria)
def create_categoria(categoria: CategoriaCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        query = "INSERT INTO categoria (nombre) VALUES (%s)"
        cursor.execute(query, (categoria.nombre,))
        conn.commit()
        
        categoria_id = cursor.lastrowid
        return Categoria(id_categoria=categoria_id, **categoria.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.get("/categorias/", response_model=List[Categoria])
def list_categorias():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        query = "SELECT * FROM categoria"
        cursor.execute(query)
        categorias = cursor.fetchall()
        return [Categoria(**categoria) for categoria in categorias]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.post("/categorias/bulk/", response_model=List[Categoria])
def create_categorias_bulk(categorias: List[CategoriaCreate]):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        created_categorias = []
        for categoria in categorias:
            query = "INSERT INTO categoria (nombre) VALUES (%s)"
            cursor.execute(query, (categoria.nombre,))
            categoria_id = cursor.lastrowid
            created_categorias.append(Categoria(id_categoria=categoria_id, **categoria.dict()))
        
        conn.commit()
        return created_categorias
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()


@router.post("/marcas/", response_model=Marca)
def create_marca(marca: MarcaCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        query = "INSERT INTO marca (nombre) VALUES (%s)"
        cursor.execute(query, (marca.nombre,))
        conn.commit()
        
        marca_id = cursor.lastrowid
        return Marca(id_marca=marca_id, **marca.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.get("/marcas/", response_model=List[Marca])
def list_marcas():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        query = "SELECT * FROM marca"
        cursor.execute(query)
        marcas = cursor.fetchall()
        return [Marca(**marca) for marca in marcas]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.post("/marcas/bulk/", response_model=List[Marca])
def create_marcas_bulk(marcas: List[MarcaCreate]):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        created_marcas = []
        for marca in marcas:
            query = "INSERT INTO marca (nombre) VALUES (%s)"
            cursor.execute(query, (marca.nombre,))
            marca_id = cursor.lastrowid
            created_marcas.append(Marca(id_marca=marca_id, **marca.dict()))
        
        conn.commit()
        return created_marcas
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()


@router.post("/unidades-medida/", response_model=UnidadMedida)
def create_unidad_medida(unidad_medida: UnidadMedidaCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        query = "INSERT INTO unidad_medida (nombre) VALUES (%s)"
        cursor.execute(query, (unidad_medida.nombre,))
        conn.commit()
        
        unidad_medida_id = cursor.lastrowid
        return UnidadMedida(id_unidad_medida=unidad_medida_id, **unidad_medida.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.get("/unidades-medida/", response_model=List[UnidadMedida])
def list_unidades_medida():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        query = "SELECT * FROM unidad_medida"
        cursor.execute(query)
        unidades_medida = cursor.fetchall()
        return [UnidadMedida(**unidad_medida) for unidad_medida in unidades_medida]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.post("/unidades-medida/bulk/", response_model=List[UnidadMedida])
def create_unidades_medida_bulk(unidades_medida: List[UnidadMedidaCreate]):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        created_unidades_medida = []
        for unidad_medida in unidades_medida:
            query = "INSERT INTO unidad_medida (nombre) VALUES (%s)"
            cursor.execute(query, (unidad_medida.nombre,))
            unidad_medida_id = cursor.lastrowid
            created_unidades_medida.append(UnidadMedida(id_unidad_medida=unidad_medida_id, **unidad_medida.dict()))
        
        conn.commit()
        return created_unidades_medida
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()