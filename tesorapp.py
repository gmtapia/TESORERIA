import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_gsheets import GSheetsConnection

# ==========================================
# 1. CONFIGURACIÓN DE PÁGINA Y ESTILOS
# ==========================================
st.set_page_config(
    page_title="Control Tesorería Kinder C",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed" # Ocultamos la barra lateral por defecto
)

# Estilos CSS personalizados para replicar la estética de las imágenes
st.markdown("""
<style>
    /* Estilo para los títulos */
    .big-title {
        font-size: 32px !important;
        font-weight: bold;
        color: #1A1A1A;
        margin-bottom: 20px;
    }
    .main-header {
        font-size: 28px !important;
        font-weight: bold;
        color: #1A1A1A;
        margin-top: 30px;
        margin-bottom: 20px;
    }
    
    /* Estilo para las tarjetas del menú principal */
    .menu-card {
        background-color: #F0F2F5;
        border-radius: 10px;
        padding: 20px;
        border: 1px solid #E0E0E0;
        cursor: pointer;
        transition: transform 0.2s;
        text-align: center;
        margin-bottom: 20px;
    }
    .menu-card:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .card-title {
        font-size: 20px;
        font-weight: bold;
        color: #1A1A1A;
        margin-top: 10px;
    }
    .card-subtitle {
        font-size: 14px;
        color: #757575;
    }
    .card-icon {
        font-size: 40px;
        color: #7B9D4A; /* Color verde oliva del botón */
    }

    /* Estilo para las métricas del resumen anual */
    .metric-container {
        background-color: #FFFFFF;
        border-radius: 8px;
        padding: 15px;
        border: 1px solid #E0E0E0;
        text-align: center;
    }
    .metric-label {
        font-size: 14px;
        color: #757575;
        text-transform: uppercase;
        font-weight: bold;
    }
    .metric-value {
        font-size: 28px;
        font-weight: bold;
        color: #1A1A1A;
    }

    /* Ocultar elementos de Streamlit por defecto */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Ajuste para los botones */
    .stButton > button {
        background-color: #7B9D4A !important; /* Color verde oliva */
        color: white !important;
        border-radius: 5px !important;
        border: none !important;
        padding: 10px 20px !important;
        font-weight: bold !important;
        width: 100%;
    }
    .stButton > button:hover {
        background-color: #6A8A3F !important;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. CONEXIÓN Y CARGA DE DATOS (GSHEETS)
# ==========================================
# Creamos la conexión (los secretos se configuran en Streamlit Cloud)
conn = st.connection("gsheets", type=GSheetsConnection)

# Función para cargar y limpiar datos
@st.cache_data(ttl=600) # Caché de 10 minutos para no saturar la API
def load_all_data():
    # Cargar las 3 hojas. Nota: 'worksheet' debe coincidir con el nombre exacto de la pestaña
    try:
        df_usuarios = conn.read(worksheet="Usuarios")
        df_pagos = conn.read(worksheet="Pagos")
        df_gastos = conn.read(worksheet="Gastos")
        
        # Validación básica de datos
        # (Aquí podrías agregar validación de tipos, ej: convertir 'Monto' a numérico)
        
        return df_usuarios, df_pagos, df_gastos
    except Exception as e:
        st.error(f"Error al conectar con Google Sheets: {e}")
        return None, None, None

df_usuarios, df_pagos, df_gastos = load_all_data()

# Si no hay datos, detenemos la ejecución
if df_usuarios is None:
    st.stop()

# ==========================================
# 3. LÓGICA DE NAVEGACIÓN Y PANTALLAS
# ==========================================
# Usamos session_state para manejar la pantalla actual
if 'current_screen' not in st.session_state:
    st.session_state['current_screen'] = 'inicio'

# Función para cambiar de pantalla
def navigate_to(screen_name):
    st.session_state['current_screen'] = screen_name
    st.rerun() # Forzamos recarga para ver el cambio

# --- PANTALLA 1: INICIO ---
if st.session_state['current_screen'] == 'inicio':
    # Barra de estado superior (Hora, Iconos) simulada
    st.image("https://raw.githubusercontent.com/streamlit/streamlit/master/docs/static/img/logo-white.png", width=50) # Espaciador
    col_time, col_spacer, col_icons = st.columns([1, 4, 1])
    col_time.write("12:50")
    col_icons.write("📶 🔋")
    
    # Imagen de portada (replicando image_0.png)
    # Aquí puedes usar st.image con la URL de tu imagen o el archivo local
    # st.image("assets/portada.png", use_container_width=True)
    
    # Marcador de posición para la imagen (remplazar por st.image real)
    st.markdown("""
    <div style="background-color: #F0F2F5; height: 250px; border-radius: 10px; display: flex; align-items: center; justify-content: center; margin-bottom: 20px; border: 1px solid #E0E0E0;">
        <span style="font-size: 50px; color: #757575;">📈 💰</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Título principal
    st.markdown('<div class="big-title">CONTROL TESORERÍA<br>KINDER C - SSCC 2026</div>', unsafe_allow_html=True)
    
    # Botón Comenzar
    col_btn_start, col_btn_spacer = st.columns([2, 1])
    if col_btn_start.button("👤 COMENZAR"):
        navigate_to('menu_principal')

# --- PANTALLA 2: MENÚ PRINCIPAL ---
elif st.session_state['current_screen'] == 'menu_principal':
    # Flecha atrás simulada
    st.write("⬅️")
    st.markdown('<div class="main-header">MENÚ PRINCIPAL</div>', unsafe_allow_html=True)
    
    # Grid de tarjetas (replicando image_1.png)
    col1, col2 = st.columns(2)
    
    # Datos para las tarjetas (puedes calcular el número de items reales)
    count_ingresos_mes = df_pagos['Mes'].nunique()
    count_alumnos = df_usuarios['AlumnoID'].nunique()
    
    with col1:
        st.markdown(f"""
        <div class="menu-card">
            <div class="card-icon">📅</div>
            <div class="card-title">INGRESOS<br>MENSUALES</div>
            <div class="card-subtitle">{count_ingresos_mes} items</div>
        </div>
        """, unsafe_allow_html=True)
        # Hacemos la tarjeta clickeable mediante un botón transparente encima
        if st.button("Ver Resumen Anual", key="btn_resumen"):
            navigate_to('resumen_anual')
            
    with col2:
        st.markdown(f"""
        <div class="menu-card">
            <div class="card-icon">👤</div>
            <div class="card-title">DETALLE DE<br>PAGOS ALUMNO</div>
            <div class="card-subtitle">{count_alumnos} items</div>
        </div>
        """, unsafe_allow_html=True)
        # Hacemos la tarjeta clickeable
        if st.button("Ver Detalle Alumno", key="btn_alumno"):
            navigate_to('detalle_alumno')

# --- PANTALLA 3: RESUMEN ANUAL ---
elif st.session_state['current_screen'] == 'resumen_anual':
    # Barra superior (replicando image_2.png)
    col_back, col_title, col_time_r = st.columns([1, 4, 1])
    if col_back.button("⬅️", key="back_resumen"):
        navigate_to('menu_principal')
    col_title.markdown('<div style="text-align: center; color: #7B9D4A; font-weight: bold; margin-top: 10px;">INGRESOS MENSUALES</div>', unsafe_allow_html=True)
    col_time_r.write("12:52")
    
    st.markdown('<div class="main-header">RESUMEN ANUAL</div>', unsafe_allow_html=True)
    
    # --- CÁLCULOS DE MÉTRICAS ---
    # Convertimos montos a numérico por seguridad (asumiendo formato chileno, ej: 90.000)
def clean_monto(monto):
    if pd.isna(monto) or monto == "": 
        return 0
    # Si el valor ya es un número (float o int), lo usamos directamente
    if isinstance(monto, (int, float)):
        return float(monto)
    
    # Si es texto, limpiamos símbolos y puntos de miles
    monto_str = str(monto).replace('$', '').replace('.', '').replace(',', '').strip()
    
    try:
        # Convertimos a float y nos aseguramos de que no sea un número gigante
        return float(monto_str)
    except:
        return 0

    total_ingresos = df_pagos['Monto'].apply(clean_monto).sum()
    total_gastos = df_gastos['Monto'].apply(clean_monto).sum()
    saldo_neto = total_ingresos - total_gastos
    
    # --- MOSTRAR MÉTRICAS ---
    m_col1, m_col2, m_col3 = st.columns(3)
    
    with m_col1:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-label">Ingresos Totales</div>
            <div class="metric-value">$ {total_ingresos:,.0f}.replace(',', '.')</div>
        </div>
        """, unsafe_allow_html=True)
        
    with m_col2:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-label">Gasto Total</div>
            <div class="metric-value">$ {total_gastos:,.0f}.replace(',', '.')</div>
        </div>
        """, unsafe_allow_html=True)
        
    with m_col3:
        # Formato condicional para el saldo negativo (rojo)
        saldo_color = "#1A1A1A" if saldo_neto >= 0 else "#D32F2F"
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-label">Saldo</div>
            <div class="metric-value" style="color: {saldo_color};">$ {saldo_neto:,.0f}.replace(',', '.')</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("---")
    
    # --- SELECTOR DE GRÁFICO (REPLICANDO DROPDOWN) ---
    option = st.selectbox(
        'Seleccionar vista de gráfico:',
        ('Ingresos Mensuales', 'Gastos Mensuales', 'Saldo Acumulado Mensual'),
        label_visibility="collapsed" # Ocultar label para que se parezca más al diseño
    )
    
    # --- LÓGICA DE GRÁFICOS ---
    # Orden de meses para el eje X
    meses_orden = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
    
    if option == 'Ingresos Mensuales':
        # Agrupar ingresos por mes
        df_pagos['MontoNum'] = df_pagos['Monto'].apply(clean_monto)
        df_plot = df_pagos.groupby('Mes')['MontoNum'].sum().reset_index()
        title_graph = "Total Ingresos por Mes"
        y_label = "Monto Ingresado ($)"
        
    elif option == 'Gastos Mensuales':
        # Agrupar gastos por mes
        df_gastos['MontoNum'] = df_gastos['Monto'].apply(clean_monto)
        df_plot = df_gastos.groupby('Mes')['MontoNum'].sum().reset_index()
        title_graph = "Total Gastos por Mes"
        y_label = "Monto Gastado ($)"
        
    else: # Saldo Acumulado Mensual
        # Lógica más compleja: ingresos - gastos por mes + acumulado
        df_pagos['MontoNum'] = df_pagos['Monto'].apply(clean_monto)
        ingresos_mes = df_pagos.groupby('Mes')['MontoNum'].sum()
        
        df_gastos['MontoNum'] = df_gastos['Monto'].apply(clean_monto)
        gastos_mes = df_gastos.groupby('Mes')['MontoNum'].sum()
        
        # Combinar y calcular saldo mensual
        df_combinado = pd.DataFrame(index=meses_orden)
        df_combinado['Ingresos'] = ingresos_mes
        df_combinado['Gastos'] = gastos_mes
        df_combinado = df_combinado.fillna(0)
        df_combinado['SaldoMensual'] = df_combinado['Ingresos'] - df_combinado['Gastos']
        df_combinado['SaldoAcumulado'] = df_combinado['SaldoMensual'].cumsum()
        
        df_plot = df_combinado.reset_index().rename(columns={'index': 'Mes'})
        title_graph = "Saldo Acumulado por Mes"
        y_label = "Saldo ($)"
        df_plot['MontoNum'] = df_plot['SaldoAcumulado'] # Para usar la misma variable de plot

    # --- GENERAR GRÁFICO CON PLOTLY (PARA INTERACTIVIDAD) ---
    # Asegurar orden correcto de meses
    df_plot['Mes'] = pd.Categorical(df_plot['Mes'], categories=meses_orden, ordered=True)
    df_plot = df_plot.sort_values('Mes')
    
    # Color condicional para saldo (verde positivo, rojo negativo)
    if option == 'Saldo Acumulado Mensual':
        df_plot['Color'] = df_plot['MontoNum'].apply(lambda x: '#7B9D4A' if x >= 0 else '#D32F2F')
    else:
        df_plot['Color'] = '#7B9D4A' # Verde oliva por defecto

    fig = px.bar(df_plot, x='Mes', y='MontoNum', title=title_graph,
                 labels={'MontoNum': y_label, 'Mes': 'Mes'},
                 text_auto='.2s') # Mostrar valores sobre las barras
    
    fig.update_traces(marker_color=df_plot['Color'], textposition='outside')
    
    # Ajustes estéticos del gráfico
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_title=None,
        yaxis=dict(
        # Esto le dice a Plotly que use el punto como separador de miles
        tickformat=',.0f', 
        separators=',.', 
        gridcolor='#E0E0E0'
    ),
        title_font=dict(size=18),
        margin=dict(l=20, r=20, t=50, b=20)
    )
    
    # Mostrar gráfico ocupando todo el contenedor
    st.plotly_chart(fig, use_container_width=True)

# --- PANTALLA 4: DETALLE ALUMNO (OPCIONAL, PERO ESTRUCTURADA) ---
elif st.session_state['current_screen'] == 'detalle_alumno':
    # Barra superior
    col_back_a, col_title_a = st.columns([1, 5])
    if col_back_a.button("⬅️", key="back_alumno"):
        navigate_to('menu_principal')
    col_title_a.markdown('<div class="main-header">DETALLE DE PAGOS ALUMNO</div>', unsafe_allow_html=True)
    
    # Selector de alumno
    lista_alumnos = df_usuarios['NombreAlumno'].unique()
    alumno_seleccionado = st.selectbox("Seleccionar Alumno:", lista_alumnos)
    
    # Obtener ID del alumno
    alumno_id = df_usuarios[df_usuarios['NombreAlumno'] == alumno_seleccionado]['AlumnoID'].iloc[0]
    
    # Filtrar pagos del alumno
    def clean_monto(monto):
        if pd.isna(monto): return 0
        return float(str(monto).replace('.', '').replace('$', '').strip())
        
    df_pagos_alumno = df_pagos[df_pagos['AlumnoID'] == alumno_id].copy()
    df_pagos_alumno['MontoNum'] = df_pagos_alumno['Monto'].apply(clean_monto)
    
    # Métricas del alumno
    total_pagado_alumno = df_pagos_alumno['MontoNum'].sum()
    
    st.markdown(f"""
    <div class="metric-container" style="margin-bottom: 20px;">
        <div class="metric-label">Total Pagado por {alumno_seleccionado}</div>
        <div class="metric-value">$ {total_pagado_alumno:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Tabla de detalle
    # Ordenar por mes (puedes necesitar lógica extra para ordenar cronológicamente)
    st.dataframe(df_pagos_alumno[['Mes', 'Concepto', 'Monto']], use_container_width=True, hide_index=True)
