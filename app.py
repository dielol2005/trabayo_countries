import streamlit as st
import requests
import pandas as pd

# Función para obtener los datos de la API
@st.cache
def fetch_countries_data():
    url = "https://restcountries.com/v3.1/all"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        countries = []
        for country in data:
            countries.append({
                "Nombre": country.get("name", {}).get("common", "Desconocido"),
                "Región": country.get("region", "Desconocida"),
                "Población": country.get("population", 0),
                "Área (km²)": country.get("area", 0),
                "Fronteras": len(country.get("borders", [])),
                "Idiomas": len(country.get("languages", {}).keys()),
                "Zonas Horarias": len(country.get("timezones", []))
            })
        return pd.DataFrame(countries)
    else:
        st.error(f"Error al conectar con la API. Código de estado: {response.status_code}")
        return pd.DataFrame()

# Título de la aplicación
st.title("Visualización de Datos: REST Countries API")

# Cargar los datos
st.subheader("Cargando datos...")
data = fetch_countries_data()

# Mostrar los datos originales
st.subheader("Datos Originales")
if not data.empty:
    st.dataframe(data)

    # Interacción: Filtrar por región
    st.subheader("Filtrar por Región")
    regiones = data["Región"].dropna().unique()
    region_seleccionada = st.selectbox("Selecciona una región:", ["Todas"] + list(regiones))
    if region_seleccionada != "Todas":
        data = data[data["Región"] == region_seleccionada]

    # Interacción: Ordenar por columna
    st.subheader("Ordenar por Columna")
    columna = st.selectbox("Selecciona una columna para ordenar:", data.columns)
    orden = st.radio("Orden:", ["Ascendente", "Descendente"])
    data = data.sort_values(by=columna, ascending=(orden == "Ascendente"))

    # Mostrar datos filtrados y ordenados
    st.write("Datos Filtrados y Ordenados:")
    st.dataframe(data)

    # Descarga de datos
    st.download_button(
        label="Descargar Datos Filtrados",
        data=data.to_csv(index=False).encode("utf-8"),
        file_name="datos_filtrados.csv",
        mime="text/csv"
    )
else:
    st.write("No se encontraron datos para mostrar.")
