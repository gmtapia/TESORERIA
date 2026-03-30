import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_gsheets import GSheetsConnection

# ==========================================
# 1. CONFIGURACIÓN DE PÁGINA Y ESTILOS
# ==========================================
st.set_page_config(
    page_title="Tesorería Kinder C 2026 - SSCC",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Estilos CSS - RECUPERADAS LAS TARJETAS DEL MENÚ Y VISIBILIDAD MÓVIL
st.markdown("""
<style>
    /* 1. FONDO GLOBAL AZULADO CLARO */
    .stApp {
        background-color: #F0F4F8;
    }

    /* 2. FORZAR COLOR DE TEXTO OSCURO EN TODO EL DOCUMENTO (Visibilidad Móvil) */
    html, body, [data-testid="stWidgetLabel"], .stText, p, h1, h2, h3 {
        color: #1A1A1A !important;
    }

    /* 3. TÍTULOS ESPECÍFICOS */
    .big-title { font-size: 28px !important; font-weight: bold; color: #1A1A1A !important; text-align: center; margin-bottom: 5px; }
    .sub-title { font-size: 16px !important; color: #444444 !important; text-align: center; margin-bottom: 20px; font-weight: normal; }
    .main-header { font-size: 22px !important; font-weight: bold; color: #1A1A1A !important; text-align: center; margin-bottom: 15px;}

    /* 4. --- RECUPERACIÓN DE TARJETAS DEL MENÚ PRINCIPAL --- */
    .menu-card {
        background-color: #FFFFFF !important; /* Fondo blanco sólido */
        border-radius: 12px; 
        padding: 20px;
        border: 1px solid #D1D5DB; /* Borde gris suave pero visible */
        text-align: center; 
        margin-bottom: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.08); /* Sombra suave para efecto flotante */
    }
    .card-title { 
        font-size: 18px !important; 
        font-weight: bold !important; 
        color: #1A1A1A !important; /* Texto negro */
        margin-top: 10px; 
    }
    .card-icon { font-size: 45px; }

    /* 5. TARJETAS DE MÉTRICAS (Resumen Anual) */
    .metric-container {
        background-color: #FFFFFF; 
        border-radius: 10px; 
        padding: 12px;
        border: 1px solid #D0D7DE; 
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .metric-label { font-size: 12px; color: #555555 !important; font-weight: bold; }
    .metric-value { font-size: 22px; font-weight: bold; color: #1A1A1A !important; }

    /* 6. BOTONES (Generales y Menú) */
    .stButton > button {
        background-color: #7B9D4A !important; 
        color: white !important;
        border-radius: 8px !important; 
        width: 100%; 
        font-weight: bold !important;
        border: none !important;
        height: 45px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Botón de Salir (Menú Principal) */
    .stButton > button[key="btn_exit"] {
        background-color: #FFFFFF !important;
        color: #555555 !important;
        border: 1px solid #D1D5DB !important;
    }

    /* 7. OCULTAR ELEMENTOS STREAMLIT */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. FUNCIONES DE APOYO (REVISADAS)
# ==========================================
def clean_monto(monto):
    """Limpia montos evitando el error del cero adicional"""
    if pd.isna(monto) or monto == "":
        return 0.0
    if isinstance(monto, (int, float)):
        return float(monto)
    monto_str = str(monto).replace('$', '').replace('.', '').replace(',', '').strip()
    try:
        return float(monto_str)
    except:
        return 0.0

def format_chile(valor):
    """Formatea número a moneda chilena: $ 90.000"""
    if valor is None: valor = 0
    return f"$ {valor:,.0f}".replace(",", ".")

def navigate_to(screen_name):
    """Navegación entre pantallas"""
    st.session_state['current_screen'] = screen_name
    st.rerun()

# ==========================================
# 3. CONEXIÓN Y CARGA (REVISADAS)
# ==========================================
if 'current_screen' not in st.session_state:
    st.session_state['current_screen'] = 'inicio'

conn = st.connection("gsheets", type=GSheetsConnection)

@st.cache_data(ttl=600)
def load_data():
    try:
        u = conn.read(worksheet="Usuarios")
        p = conn.read(worksheet="Pagos")
        g = conn.read(worksheet="Gastos")
        return u, p, g
    except Exception as e:
        st.error(f"Error al conectar con Google Sheets: {e}")
        return None, None, None

df_usuarios, df_pagos, df_gastos = load_data()

# ==========================================
# 4. LÓGICA DE PANTALLAS
# ==========================================

# --- PANTALLA: INICIO (PERSONALIZADA CON LOUGO Y FONDO) ---
if st.session_state['current_screen'] == 'inicio':
    # Banner superior más estético
    st.markdown('<div style="background-color: #7B9D4A; height: 250px; border-radius: 15px; margin-bottom: 30px; display: flex; align-items: center; justify-content: center; color: white; font-size: 80px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">💰</div>', unsafe_allow_html=True)
    
    # Texto de bienvenida centrado
    st.markdown('<div class="big-title">CONTROL TESORERÍA</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Kinder C - SSCC Alameda<br>Año Escolar 2026</div>', unsafe_allow_html=True)
    
    st.write("") # Espacio
    
    # Botón centrado
    _, col_btn, _ = st.columns([1, 2, 1])
    with col_btn:
        if st.button("👥 INGRESAR AL SISTEMA", key="btn_start"):
            navigate_to('menu_principal')

# --- PANTALLA: MENÚ PRINCIPAL (CON BOTÓN VOLVER A INICIO) ---
elif st.session_state['current_screen'] == 'menu_principal':
    st.markdown('<div class="main-header">MENÚ PRINCIPAL</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="menu-card"><div class="card-icon">📊</div><div class="card-title">RESUMEN<br>ANUAL</div></div>', unsafe_allow_html=True)
        if st.button("Ver Resumen", key="btn_res"): 
            navigate_to('resumen_anual')
            
    with col2:
        st.markdown('<div class="menu-card"><div class="card-icon">👨‍👩‍👧</div><div class="card-title">DETALLE POR<br>ALUMNO</div></div>', unsafe_allow_html=True)
        if st.button("Ver Alumno", key="btn_alu"): 
            navigate_to('detalle_alumno')

    # --- NUEVO BOTÓN PARA VOLVER AL INICIO ---
    st.write("") # Espacio en blanco
    st.write("")
    
    # Columna central para el botón de salir
    _, col_exit, _ = st.columns([1, 2, 1])
    with col_exit:
        if st.button("🚪 VOLVER A BIENVENIDA", key="btn_exit"):
            navigate_to('inicio')

# --- PANTALLA: RESUMEN ANUAL (CORRECCIÓN DE MESES Y AGRUPACIÓN) ---
elif st.session_state['current_screen'] == 'resumen_anual':
    if st.button("⬅️ Volver", key="btn_back_res"): 
        navigate_to('menu_principal')
    
    st.markdown('<div class="main-header">RESUMEN ANUAL DE CAJA</div>', unsafe_allow_html=True)
    
    # 1. Preparación de Datos y Estandarización de Meses
    p_temp = df_pagos.copy()
    g_temp = df_gastos.copy()
    
    # Diccionario para convertir abreviaturas a nombres completos si es necesario
    mapa_meses = {
        'Ene': 'Enero', 'Feb': 'Febrero', 'Mar': 'Marzo', 'Abr': 'Abril', 
        'May': 'Mayo', 'Jun': 'Junio', 'Jul': 'Julio', 'Ago': 'Agosto', 
        'Sep': 'Septiembre', 'Oct': 'Octubre', 'Nov': 'Noviembre', 'Dic': 'Diciembre'
    }

    def normalizar_mes(mes):
        if pd.isna(mes): return "Sin Mes"
        m = str(mes).strip().capitalize()[:3] # Tomamos las primeras 3 letras
        return mapa_meses.get(m, m) # Si es 'Mar', devuelve 'Marzo'

    p_temp['MesFull'] = p_temp['Mes'].apply(normalizar_mes)
    g_temp['MesFull'] = g_temp['Mes'].apply(normalizar_mes)
    p_temp['MontoNum'] = p_temp['Monto'].apply(clean_monto)
    g_temp['MontoNum'] = g_temp['Monto'].apply(clean_monto)
    
    ingresos = p_temp['MontoNum'].sum()
    gastos = g_temp['MontoNum'].sum()
    saldo = ingresos - gastos
    
    # 2. Métricas
    c1, c2, c3 = st.columns(3)
    c1.markdown(f'<div class="metric-container"><div class="metric-label">Ingresos</div><div class="metric-value">{format_chile(ingresos)}</div></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="metric-container"><div class="metric-label">Gastos</div><div class="metric-value">{format_chile(gastos)}</div></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="metric-container"><div class="metric-label">Saldo</div><div class="metric-value" style="color:{"green" if saldo>=0 else "red"}">{format_chile(saldo)}</div></div>', unsafe_allow_html=True)

    st.markdown("---")
    
    # 3. Lógica de Gráfico (Eje X completo)
    opcion = st.radio("Seleccionar vista:", ["Ingresos por Mes", "Gastos por Mes"], horizontal=True)
    meses_cl = ['Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    
    if "Ingresos" in opcion:
        # Agrupamos por el mes normalizado y reindexamos para que no falte ninguno
        resumen_grafico = p_temp.groupby('MesFull')['MontoNum'].sum().reindex(meses_cl, fill_value=0).reset_index()
        color_barras = '#6B8E23'
        # Agrupación para la tabla
        df_agrupado = p_temp.groupby(['MesFull', 'Concepto'])['MontoNum'].sum().reset_index()
    else:
        resumen_grafico = g_temp.groupby('MesFull')['MontoNum'].sum().reindex(meses_cl, fill_value=0).reset_index()
        color_barras = '#8B0000'
        df_agrupado = g_temp.groupby(['MesFull', 'Concepto'])['MontoNum'].sum().reset_index()

    # 4. Mostrar Gráfico (ESTÁTICO Y SIN ZOOM)
    resumen_grafico['MesFull'] = pd.Categorical(resumen_grafico['MesFull'], categories=meses_cl, ordered=True)
    fig = px.bar(resumen_grafico, x='MesFull', y='MontoNum', text_auto='.2s')
    fig.update_traces(marker_color=color_barras, textposition='outside')
    
    fig.update_layout(
        xaxis_title=None, 
        yaxis_title="Monto ($)", 
        plot_bgcolor='rgba(0,0,0,0)', 
        separators=',.',
        # --- AJUSTES DE FIJACIÓN ---
        dragmode=False, # Desactiva el arrastre
        xaxis=dict(fixedrange=True), # Bloquea zoom en eje X
        yaxis=dict(fixedrange=True, tickformat=',.0f') # Bloquea zoom en eje Y
    )
    
    # Renderizar el gráfico ocultando la barra de herramientas superior
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    # 5. Tabla Resumen Agrupada
    st.write("### 📝 Resumen de Movimientos por Concepto")
    df_agrupado = df_agrupado[df_agrupado['MontoNum'] > 0].copy()
    if not df_agrupado.empty:
        df_agrupado['MesFull'] = pd.Categorical(df_agrupado['MesFull'], categories=meses_cl, ordered=True)
        df_agrupado = df_agrupado.sort_values(['MesFull', 'Concepto'])
        df_agrupado['Monto'] = df_agrupado['MontoNum'].apply(format_chile)
        # Renombramos MesFull a Mes para la vista final
        st.dataframe(df_agrupado.rename(columns={'MesFull': 'Mes'})[['Mes', 'Concepto', 'Monto']], 
                     use_container_width=True, hide_index=True)
    else:
        st.info("No hay movimientos registrados.")

# Grafico Pie para Cumplimiento Cuotas Mensuales
st.markdown("---")
    st.write("### 📈 Cumplimiento de Cuotas Mensuales")
    
    # 1. Selector de Mes para el cumplimiento
    mes_sel = st.selectbox("Seleccione el mes para verificar cumplimiento:", meses_cl, index=0)
    
    # 2. Cálculo de cumplimiento: Buscamos pagos de $10.000 con concepto "CUOTAS 2026"
    # Filtramos por el mes seleccionado y el concepto específico
    pagos_mes = p_temp[
        (p_temp['MesFull'] == mes_sel) & 
        (p_temp['Concepto'].str.contains("CUOTAS 2026", case=False, na=False)) &
        (p_temp['MontoNum'] >= 10000)
    ]
    
    alumnos_pagados = len(pagos_mes['AlumnoID'].unique())
    alumnos_pendientes = max(0, 25 - alumnos_pagados)
    
    # 3. Crear DataFrame para el gráfico Pie
    df_pie = pd.DataFrame({
        "Estado": ["Pagado", "Pendiente"],
        "Cantidad": [alumnos_pagados, alumnos_pendientes]
    })
    
    # 4. Generar Gráfico Pie
    fig_pie = px.pie(
        df_pie, 
        values='Cantidad', 
        names='Estado',
        color='Estado',
        color_discrete_map={'Pagado': '#7B9D4A', 'Pendiente': '#D32F2F'}, # Verde Oliva y Rojo
        hole=0.4, # Efecto Donut para que se vea más moderno
        title=f"Cumplimiento Cuotas - {mes_sel}"
    )
    
    fig_pie.update_traces(textinfo='percent+label', pull=[0.1, 0])
    
    fig_pie.update_layout(
        showlegend=True,
        dragmode=False,
        # Bloqueamos interacciones para celular
        xaxis=dict(fixedrange=True),
        yaxis=dict(fixedrange=True)
    )
    
    # Renderizar con el mismo bloqueo de zoom que el anterior
    st.plotly_chart(fig_pie, use_container_width=True, config={'displayModeBar': False})
    
    # Métrica rápida debajo del Pie
    st.info(f"**Resumen {mes_sel}:** {alumnos_pagados} alumnos al día de un total de 25.")

# --- PANTALLA: DETALLE ALUMNO ---
elif st.session_state['current_screen'] == 'detalle_alumno':
    if st.button("⬅️ Volver", key="btn_back_alu"): 
        navigate_to('menu_principal')
    st.markdown('<div class="main-header">DETALLE POR ALUMNO</div>', unsafe_allow_html=True)
    
    if df_usuarios is not None:
        lista_nombres = sorted(df_usuarios['NombreAlumno'].unique())
        nombre_sel = st.selectbox("Seleccione el nombre del alumno:", lista_nombres)
        
        # Obtener ID
        id_alu = df_usuarios[df_usuarios['NombreAlumno'] == nombre_sel]['AlumnoID'].iloc[0]
        
        # Filtrar Pagos
        pagos_alu = df_pagos[df_pagos['AlumnoID'] == id_alu].copy()
        pagos_alu['MontoNum'] = pagos_alu['Monto'].apply(clean_monto)
        total_alu = pagos_alu['MontoNum'].sum()
        
        st.markdown(f"""
            <div class="metric-container" style="background-color: #F1F8E9; border-color: #7B9D4A;">
                <div class="metric-label">Total acumulado por {nombre_sel}</div>
                <div class="metric-value" style="color: #33691E;">{format_chile(total_alu)}</div>
            </div>
            <br>
        """, unsafe_allow_html=True)
        
        if not pagos_alu.empty:
            st.dataframe(pagos_alu[['Mes', 'Concepto', 'Monto']], use_container_width=True, hide_index=True)
        else:
            st.info("No se registran pagos para este alumno todavía.")
