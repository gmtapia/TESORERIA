import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_gsheets import GSheetsConnection

# ==========================================
# 1. CONFIGURACIÓN DE PÁGINA Y ESTILOS
# ==========================================
st.set_page_config(
    page_title="Tesorería Kinder C 2026",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Estilos CSS Limpios
st.markdown("""
<style>
    .big-title { font-size: 30px !important; font-weight: bold; color: #1A1A1A; margin-bottom: 20px; text-align: left; }
    .main-header { font-size: 24px !important; font-weight: bold; color: #1A1A1A; margin-bottom: 20px; }
    .menu-card {
        background-color: #F8F9FA; border-radius: 12px; padding: 25px;
        border: 1px solid #E0E0E0; text-align: center; margin-bottom: 10px;
    }
    .card-title { font-size: 18px; font-weight: bold; color: #1A1A1A; margin-top: 10px; }
    .card-icon { font-size: 45px; }
    .metric-container {
        background-color: #FFFFFF; border-radius: 10px; padding: 15px;
        border: 1px solid #E0E0E0; text-align: center;
    }
    .metric-label { font-size: 13px; color: #757575; font-weight: bold; }
    .metric-value { font-size: 24px; font-weight: bold; color: #1A1A1A; }
    .stButton > button {
        background-color: #7B9D4A !important; color: white !important;
        border-radius: 8px !important; width: 100%; font-weight: bold !important;
        border: none !important;
    }
    /* Ocultar elementos innecesarios de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. FUNCIONES DE APOYO
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
    return f"$ {valor:,.0f}".replace(",", ".")

def navigate_to(screen_name):
    """Navegación entre pantallas"""
    st.session_state['current_screen'] = screen_name
    st.rerun()

# ==========================================
# 3. CONEXIÓN Y CARGA
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

# --- PANTALLA: INICIO ---
if st.session_state['current_screen'] == 'inicio':
    # Espacio superior estético
    st.write("") 
    st.markdown('<div style="background-color: #7B9D4A; height: 220px; border-radius: 15px; margin-bottom: 30px; display: flex; align-items: center; justify-content: center; color: white; font-size: 60px;">💰</div>', unsafe_allow_html=True)
    st.markdown('<div class="big-title">CONTROL TESORERÍA<br>KINDER C - SSCC 2026</div>', unsafe_allow_html=True)
    
    if st.button("👤 COMENZAR"):
        navigate_to('menu_principal')

# --- PANTALLA: MENÚ PRINCIPAL ---
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
    
    # Creamos una columna central pequeña para el botón de salir
    _, col_exit, _ = st.columns([1, 2, 1])
    with col_exit:
        if st.button("🚪 SALIR AL INICIO", key="btn_exit"):
            navigate_to('inicio')

# --- PANTALLA: RESUMEN ANUAL ---
elif st.session_state['current_screen'] == 'resumen_anual':
    col_back, col_title = st.columns([1, 4])
    with col_back:
        if st.button("⬅️"): navigate_to('menu_principal')
    
    st.markdown('<div class="main-header">RESUMEN ANUAL DE CAJA</div>', unsafe_allow_html=True)
    
    # 1. Cálculos de Totales
    # Usamos una copia para no alterar los datos originales
    p_temp = df_pagos.copy()
    g_temp = df_gastos.copy()
    
    p_temp['MontoNum'] = p_temp['Monto'].apply(clean_monto)
    g_temp['MontoNum'] = g_temp['Monto'].apply(clean_monto)
    
    ingresos = p_temp['MontoNum'].sum()
    gastos = g_temp['MontoNum'].sum()
    saldo = ingresos - gastos
    
    # 2. Métricas Visuales
    c1, c2, c3 = st.columns(3)
    c1.markdown(f'<div class="metric-container"><div class="metric-label">Ingresos Totales</div><div class="metric-value">{format_chile(ingresos)}</div></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="metric-container"><div class="metric-label">Gasto Total</div><div class="metric-value">{format_chile(gastos)}</div></div>', unsafe_allow_html=True)
    
    color_saldo = "#7B9D4A" if saldo >= 0 else "#D32F2F"
    c3.markdown(f'<div class="metric-container"><div class="metric-label">Saldo Neto</div><div class="metric-value" style="color:{color_saldo}">{format_chile(saldo)}</div></div>', unsafe_allow_html=True)

    st.markdown("---")
    
    # 3. Lógica del Gráfico (Aquí estaba el error del valor 0)
    opcion = st.radio("Seleccionar vista:", ["Ingresos por Mes", "Gastos por Mes"], horizontal=True)
    meses_orden = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
    
    if "Ingresos" in opcion:
        # Agrupamos y reindexamos para asegurar que aparezcan todos los meses
        df_resumen = p_temp.groupby('Mes')['MontoNum'].sum().reset_index()
        titulo_g = "Evolución de Ingresos"
    else:
        df_resumen = g_temp.groupby('Mes')['MontoNum'].sum().reset_index()
        titulo_g = "Evolución de Gastos"

    # Forzamos el orden de los meses para que no salgan desordenados
    df_resumen['Mes'] = pd.Categorical(df_resumen['Mes'], categories=meses_orden, ordered=True)
    df_resumen = df_resumen.sort_values('Mes')

    # 4. Creación del Gráfico Plotly
    fig = px.bar(
        df_resumen, 
        x='Mes', 
        y='MontoNum', 
        text_auto='.2s', 
        title=titulo_g
    )
    
    fig.update_traces(marker_color='#7B9D4A', textposition='outside')
    
    fig.update_layout(
        xaxis_title=None,
        yaxis_title="Monto ($)",
        plot_bgcolor='rgba(0,0,0,0)',
        separators=',.' # Esto arregla el error de formato que tenías antes
    )
    
    fig.update_yaxes(tickformat=',.0f')
    
    st.plotly_chart(fig, use_container_width=True)

# --- PANTALLA: DETALLE ALUMNO ---
elif st.session_state['current_screen'] == 'detalle_alumno':
    if st.button("⬅️ Volver al Menú"): navigate_to('menu_principal')
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
        
        # Mostrar tabla de pagos realizados
        if not pagos_alu.empty:
            st.dataframe(pagos_alu[['Mes', 'Concepto', 'Monto']], use_container_width=True, hide_index=True)
        else:
            st.info("No se registran pagos para este alumno todavía.")
