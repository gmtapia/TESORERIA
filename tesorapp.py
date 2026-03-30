import streamlit as st
import pandas as pd

# Configuración de la página (Título y Icono)
st.set_page_config(page_title="Tesorería Escolar", page_icon="💰")

st.title("📊 Resumen de Pagos y Cuotas")

# Conexión directa a Google Sheets (Link público o privado)
sheet_url = "https://docs.google.com/spreadsheets/d/1IPwSGCDpPHQKSW6rLvuDQbmQeTdH8TYP1nYxt2Afaqs/edit?gid=1937812936#gid=1937812936/export?format=csv"

# Leer los datos (Como un ClearCollect pero en una línea)
df = pd.read_csv(sheet_url)

# --- PANEL DE FILTROS ---
st.sidebar.header("Filtros")
mes_seleccionado = st.sidebar.selectbox("Seleccionar Mes", df['Mes'].unique())

# --- CÁLCULOS (Variables) ---
total_ingresos = df[df['Mes'] == mes_seleccionado]['Monto'].sum()

# --- MOSTRAR RESULTADOS (UI) ---
col1, col2 = st.columns(2)
col1.metric("Ingresos Totales", f"$ {total_ingresos:,.0f}")
col2.metric("Alumnos Pendientes", "12")

st.divider() # Esta es la línea divisora que buscabas

# Mostrar la tabla de datos
st.subheader(f"Detalle de {mes_seleccionado}")
st.dataframe(df[df['Mes'] == mes_seleccionado], use_container_width=True)
