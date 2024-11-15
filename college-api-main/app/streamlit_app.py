import streamlit as st
import requests
import pandas as pd


st.set_page_config(page_title="Sistema de Gestión de Productos", layout="wide")


BASE_URL = "http://localhost:8000"


st.title("Sistema de Gestión de Productos")


def get_data(endpoint):
    response = requests.get(f"{BASE_URL}/{endpoint}")
    return response.json() if response.status_code == 200 else []


def create_record(endpoint, data):
    response = requests.post(f"{BASE_URL}/{endpoint}", json=data)
    return response.json() if response.status_code == 200 else None


entidad = st.sidebar.selectbox(
    "Seleccionar Entidad",
    ["Productos", "Códigos", "Tipos", "Bodegas", "Categorías", "Marcas", "Unidades de Medida"]
)


ENTITY_ENDPOINTS = {
    "Productos": "productos",
    "Códigos": "codigos",
    "Tipos": "tipos",
    "Bodegas": "bodegas",
    "Categorías": "categorias",
    "Marcas": "marcas",
    "Unidades de Medida": "unidades-medida"
}


st.header(f"Gestión de {entidad}")


tab1, tab2 = st.tabs(["Ver Registros", "Crear Nuevo"])

with tab1:
    
    endpoint = ENTITY_ENDPOINTS[entidad]
    data = get_data(endpoint)
    
    if data:
        if entidad == "Productos":
            
            codigos = {c["id_codigo"]: c["codigo"] for c in get_data("codigos")}
            tipos = {t["id_tipo"]: t["tipo"] for t in get_data("tipos")}
            bodegas = {b["id_bodega"]: b["nombre"] for b in get_data("bodegas")}
            categorias = {c["id_categoria"]: c["nombre"] for c in get_data("categorias")}
            marcas = {m["id_marca"]: m["nombre"] for m in get_data("marcas")}
            unidades_medida = {u["id_unidad_medida"]: u["nombre"] for u in get_data("unidades-medida")}
            
            
            df = pd.DataFrame(data)
            df['codigo'] = df['codigo_id'].map(codigos)
            df['tipo'] = df['tipo_id'].map(tipos)
            df['bodega'] = df['bodega_id'].map(bodegas)
            df['categoria'] = df['categoria_id'].map(categorias)
            df['marca'] = df['marca_id'].map(marcas)
            df['unidad_medida'] = df['unidad_medida_id'].map(unidades_medida)
            
            
            columns_to_show = {
                'id_producto': 'ID',
                'nombre': 'Nombre',
                'codigo': 'Código',
                'tipo': 'Tipo',
                'categoria': 'Categoría',
                'marca': 'Marca',
                'bodega': 'Bodega',
                'unidad_medida': 'Unidad de Medida',
                'inventario': 'Inventario',
                'precio_venta': 'Precio de Venta',
                'costo': 'Costo'
            }
            
            df = df[columns_to_show.keys()].rename(columns=columns_to_show)
            
            
            col1, col2, col3 = st.columns(3)
            with col1:
                marca_filter = st.multiselect('Filtrar por Marca', options=df['Marca'].unique())
            with col2:
                categoria_filter = st.multiselect('Filtrar por Categoría', options=df['Categoría'].unique())
            with col3:
                bodega_filter = st.multiselect('Filtrar por Bodega', options=df['Bodega'].unique())

            
            if marca_filter:
                df = df[df['Marca'].isin(marca_filter)]
            if categoria_filter:
                df = df[df['Categoría'].isin(categoria_filter)]
            if bodega_filter:
                df = df[df['Bodega'].isin(bodega_filter)]

            
            st.subheader("Estadísticas")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Productos", len(df))
            with col2:
                st.metric("Valor Total Inventario", f"${df['Costo'].sum():,.2f}")
            with col3:
                st.metric("Inventario Total", df['Inventario'].sum())
            with col4:
                st.metric("Valor Venta Total", f"${df['Precio de Venta'].sum():,.2f}")

            
            st.subheader("Análisis")
            col1, col2 = st.columns(2)
            with col1:
                st.bar_chart(df.groupby('Marca')['Inventario'].sum())
                st.caption("Inventario por Marca")
            with col2:
                st.bar_chart(df.groupby('Categoría')['Inventario'].sum())
                st.caption("Inventario por Categoría")

        else:
            df = pd.DataFrame(data)
        
        st.dataframe(df, use_container_width=True)
    else:
        st.warning(f"No hay {entidad.lower()} registrados")

with tab2:

    with st.form(f"crear_{entidad.lower()}_form"):
        st.subheader(f"Crear {entidad[:-1] if entidad.endswith('s') else entidad}")
        
        if entidad == "Productos":
            nombre = st.text_input("Nombre")
            inventario = st.number_input("Inventario", min_value=0)
            precio_venta = st.number_input("Precio de Venta", min_value=0.0)
            costo = st.number_input("Costo", min_value=0.0)
            
           
            codigos = get_data("codigos")
            tipos = get_data("tipos")
            bodegas = get_data("bodegas")
            categorias = get_data("categorias")
            marcas = get_data("marcas")
            unidades_medida = get_data("unidades-medida")

            codigo_id = st.selectbox("Código", 
                options=[c["id_codigo"] for c in codigos],
                format_func=lambda x: next((c["codigo"] for c in codigos if c["id_codigo"] == x), x))
            
            tipo_id = st.selectbox("Tipo", 
                options=[t["id_tipo"] for t in tipos],
                format_func=lambda x: next((t["tipo"] for t in tipos if t["id_tipo"] == x), x))
            
            bodega_id = st.selectbox("Bodega", 
                options=[b["id_bodega"] for b in bodegas],
                format_func=lambda x: next((b["nombre"] for b in bodegas if b["id_bodega"] == x), x))
            
            categoria_id = st.selectbox("Categoría", 
                options=[c["id_categoria"] for c in categorias],
                format_func=lambda x: next((c["nombre"] for c in categorias if c["id_categoria"] == x), x))
            
            marca_id = st.selectbox("Marca", 
                options=[m["id_marca"] for m in marcas],
                format_func=lambda x: next((m["nombre"] for m in marcas if m["id_marca"] == x), x))
            
            unidad_medida_id = st.selectbox("Unidad de Medida", 
                options=[u["id_unidad_medida"] for u in unidades_medida],
                format_func=lambda x: next((u["nombre"] for u in unidades_medida if u["id_unidad_medida"] == x), x))
            
            data = {
                "nombre": nombre,
                "inventario": inventario,
                "precio_venta": precio_venta,
                "costo": costo,
                "codigo_id": codigo_id,
                "tipo_id": tipo_id,
                "bodega_id": bodega_id,
                "categoria_id": categoria_id,
                "marca_id": marca_id,
                "unidad_medida_id": unidad_medida_id
            }
        else:
            if entidad == "Códigos":
                codigo = st.text_input("Código")
                data = {"codigo": codigo}
            elif entidad == "Tipos":
                tipo = st.text_input("Tipo")
                data = {"tipo": tipo}
            else:
                nombre = st.text_input("Nombre")
                data = {"nombre": nombre}

        submitted = st.form_submit_button("Guardar")
        if submitted:
            endpoint = ENTITY_ENDPOINTS[entidad]
            result = create_record(endpoint, data)
            if result:
                st.success(f"{entidad[:-1] if entidad.endswith('s') else entidad} creado exitosamente!")
                st.rerun()
            else:
                st.error("Error al crear el registro")


st.sidebar.markdown("---")
st.sidebar.markdown("### Información")
st.sidebar.info("Sistema de gestión de productos y catálogos")