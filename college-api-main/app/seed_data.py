import random
from faker import Faker
import mysql.connector
from database import get_db_connection

fake = Faker()

def seed_database():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Datos para códigos
        codigos = [
            "PRD-001", "PRD-002", "PRD-003", "PRD-004", "PRD-005",
            "PRD-006", "PRD-007", "PRD-008", "PRD-009", "PRD-010"
        ]
        for codigo in codigos:
            cursor.execute("INSERT INTO codigo (codigo) VALUES (%s)", (codigo,))
        
        # Datos para tipos
        tipos = [
            "Electrónico", "Ropa", "Alimentos", "Bebidas", "Limpieza",
            "Herramientas", "Juguetes", "Deportes", "Hogar", "Oficina"
        ]
        for tipo in tipos:
            cursor.execute("INSERT INTO tipo (tipo) VALUES (%s)", (tipo,))
        
        # Datos para bodegas
        bodegas = [
            "Bodega Principal", "Bodega Norte", "Bodega Sur", "Almacén Central",
            "Depósito Este", "Depósito Oeste", "Almacén Secundario"
        ]
        for bodega in bodegas:
            cursor.execute("INSERT INTO bodega (nombre) VALUES (%s)", (bodega,))
        
        # Datos para categorías
        categorias = [
            "Premium", "Básico", "Lujo", "Económico", "Gama Alta",
            "Gama Media", "Gama Baja", "Importado", "Nacional"
        ]
        for categoria in categorias:
            cursor.execute("INSERT INTO categoria (nombre) VALUES (%s)", (categoria,))
        
        # Datos para marcas
        marcas = [
            "TechPro", "FashionStyle", "FoodMaster", "CleanMax", "ToolKing",
            "ToyWorld", "SportMaster", "HomePlus", "OfficePro", "ElectroTech"
        ]
        for marca in marcas:
            cursor.execute("INSERT INTO marca (nombre) VALUES (%s)", (marca,))
        
        # Datos para unidades de medida
        unidades_medida = [
            "Unidad", "Kilogramo", "Litro", "Metro", "Caja",
            "Paquete", "Docena", "Par", "Gramo", "Pieza"
        ]
        for unidad in unidades_medida:
            cursor.execute("INSERT INTO unidad_medida (nombre) VALUES (%s)", (unidad,))
        
        # Generar productos aleatorios
        for _ in range(50):  # Generará 50 productos
            nombre = fake.product_name()
            inventario = random.randint(0, 1000)
            precio_venta = round(random.uniform(10.0, 1000.0), 2)
            costo = round(precio_venta * 0.7, 2)  # Costo es 70% del precio de venta
            codigo_id = random.randint(1, len(codigos))
            tipo_id = random.randint(1, len(tipos))
            bodega_id = random.randint(1, len(bodegas))
            categoria_id = random.randint(1, len(categorias))
            marca_id = random.randint(1, len(marcas))
            unidad_medida_id = random.randint(1, len(unidades_medida))
            
            query = """
            INSERT INTO productos (nombre, inventario, precio_venta, costo, 
                                 codigo_id, tipo_id, bodega_id, categoria_id, 
                                 marca_id, unidad_medida_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (nombre, inventario, precio_venta, costo, codigo_id, 
                     tipo_id, bodega_id, categoria_id, marca_id, unidad_medida_id)
            cursor.execute(query, values)
        
        conn.commit()
        print("¡Datos sintéticos generados exitosamente!")
        
    except Exception as e:
        conn.rollback()
        print(f"Error al generar datos: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    
    seed_database()