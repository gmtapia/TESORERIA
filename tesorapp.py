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

# Estilos CSS - AHORA CON FONDO AZULADO CLARO
st.markdown("""
<style>
    /* FONDO DE LA APP (Azulado Claro) */
    .stApp {
        background-color: #F0F4F8; /* Un azul-grisáceo muy suave y profesional */
    }

    /* ESTILOS DE TEXTO */
    .big-title { font-size: 32px !important; font-weight: bold; color: #1A1A1A; margin-bottom: 5px; text-align: center; }
    .sub-title { font-size: 18px !important; color: #555555; margin-bottom: 30px; text-align: center; font-weight: normal;}
    .main-header { font-size: 24px !important; font-weight: bold; color: #1A1A1A; margin-bottom: 20px; text-align: center;}
    
    /* TARJETAS DEL MENÚ */
    .menu-card {
        background-color: #FFFFFF; border-radius: 12px; padding: 25px;
        border: 1px solid #E0E0E0; text-align: center; margin-bottom: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05); /* Sombra suave */
    }
    .card-title { font-size: 18px; font-weight: bold; color: #1A1A1A; margin-top: 10px; }
    .card-icon { font-size: 45px; }
    
    /* TARJETAS DE MÉTRICAS (Resumen Anual) */
    .metric-container {
        background-color: #FFFFFF; border-radius: 10px; padding: 15px;
        border: 1px solid #E0E0E0; text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .metric-label { font-size: 13px; color: #757575; font-weight: bold; }
    .metric-value { font-size: 24px; font-weight: bold; color: #1A1A1A; }
    
    /* BOTONES STREAMLIT */
    .stButton > button {
        background-color: #7B9D4A !important; color: white !important;
        border-radius: 8px !important; width: 100%; font-weight: bold !important;
        border: none !important; transition: background-color 0.3s;
    }
    .stButton > button:hover {
        background-color: #6A8A3F !important; /* Un tono más oscuro al pasar el mouse */
    }

    /* Botón Secundario (Volver/Salir) */
    div[data-testid="stFormSubmitButton"] > button, 
    .stButton > button[key="btn_back"],
    .stButton > button[key="btn_exit"] {
        background-color: #FFFFFF !important; color: #555555 !important;
        border: 1px solid #CCCCCC !important;
    }
    .stButton > button[key="btn_back"]:hover,
    .stButton > button[key="btn_exit"]:hover {
        background-color: #F0F2F5 !important;
    }

    /* Ocultar elementos de Streamlit */
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

# --- PANTALLA: RESUMEN ANUAL (CON GRÁFICOS CORREGIDOS) ---
elif st.session_state['current_screen'] == 'resumen_anual':
    if st.button("⬅️ Volver", key="btn_back_res"): 
        navigate_to('menu_principal')
    
    st.markdown('<div class="main-header">RESUMEN ANUAL DE CAJA</div>', unsafe_allow_html=True)
    
    # Cálculos y Limpieza
    p_temp = df_pagos.copy()
    g_temp = df_gastos.copy()
    p_temp['MontoNum'] = p_temp['Monto'].apply(clean_monto)
    g_temp['MontoNum'] = g_temp['Monto'].apply(clean_monto)
    
    ingresos = p_temp['MontoNum'].sum()
    gastos = g_temp['MontoNum'].sum()
    saldo = ingresos - gastos
    
    # Métricas
    c1, c2, c3 = st.columns(3)
    c1.markdown(f'<div class="metric-container"><div class="metric-label">Ingresos Totales</div><div class="metric-value">{format_chile(ingresos)}</div></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="metric-container"><div class="metric-label">Gasto Total</div><div class="metric-value">{format_chile(gastos)}</div></div>', unsafe_allow_html=True)
    
    color_saldo = "#7B9D4A" if saldo >= 0 else "#D32F2F"
    c3.markdown(f'<div class="metric-container"><div class="metric-label">Saldo Neto</div><div class="metric-value" style="color:{color_saldo}">{format_chile(saldo)}</div></div>', unsafe_allow_html=True)

    st.markdown("---")
    
    # Gráfico Dinámico - CORREGIDO
    opcion = st.radio("Seleccionar vista:", ["Ingresos por Mes", "Gastos por Mes"], horizontal=True)
    
    # Lista extendida para reconocer meses cortos y largos del Excel
    meses_orden = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic',
                   'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    
    if "Ingresos" in opcion:
        df_resumen = p_temp.groupby('Mes')['MontoNum'].sum().reset_index()
        titulo_g = "Evolución de Ingresos"
        color_barras = '#6B8E23'  # Verde Oliva
    else:
        df_resumen = g_temp.groupby('Mes')['MontoNum'].sum().reset_index()
        titulo_g = "Evolución de Gastos"
        color_barras = '#8B0000'  # Rojo Oscuro

    # Forzamos el orden de los meses y eliminamos filas vacías
    df_resumen['Mes'] = pd.Categorical(df_resumen['Mes'], categories=meses_orden, ordered=True)
    df_resumen = df_resumen.sort_values('Mes').dropna(subset=['Mes'])

    # Creación del Gráfico si hay datos
    if not df_resumen.empty and df_resumen['MontoNum'].sum() > 0:
        fig = px.bar(df_resumen, x='Mes', y='MontoNum', text_auto='.2s', title=titulo_g)
        fig.update_traces(marker_color=color_barras, textposition='outside')
        fig.update_layout(
            xaxis_title=None,
            yaxis_title="Monto ($)",
            plot_bgcolor='rgba(0,0,0,0)',
            separators=',.' 
        )
        fig.update_yaxes(tickformat=',.0f')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning(f"No hay montos registrados para {opcion}. Verifica que la columna 'Mes' en tu Excel coincida con nombres como 'Mar' o 'Marzo'.")

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
