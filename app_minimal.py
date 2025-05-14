
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Unificación Obras Natstone", layout="wide")
st.title("📁 Unificador de Obras - Natstone")

st.write("Sube los archivos Excel de **Iconstruye** y **Ondac**, y la app los combinará manteniendo las columnas clave.")

# Función para procesar y normalizar cada archivo
def procesar_excel(uploaded_file, fuente):
    df = pd.read_excel(uploaded_file)
    df.columns = df.columns.str.strip()
    
    if fuente == "Iconstruye":
        df = df.rename(columns={
            "Proyecto": "Descripcion",
            "Constructora": "Cliente",
            "Tipo": "Tipo Construcción",
            "Dirección": "Direccion"
        })
        df["Monto Presupuesto"] = None
    else:  # Ondac
        df = df.rename(columns={" Comuna": "Comuna"})
        df["Estado"] = None

    df["Fuente"] = fuente
    columnas_clave = [
        "Direccion", "Tipo Construcción", "Estado", "Monto Presupuesto",
        "Cliente", "Región", "Comuna", "Fuente"
    ]
    return df[columnas_clave]

# Carga de archivos
iconstruye_file = st.file_uploader("📄 Subir archivo Iconstruye", type=["xlsx"], key="iconstruye")
ondac_file = st.file_uploader("📄 Subir archivo Ondac", type=["xlsx"], key="ondac")

dfs = []

if iconstruye_file:
    dfs.append(procesar_excel(iconstruye_file, "Iconstruye"))
if ondac_file:
    dfs.append(procesar_excel(ondac_file, "Ondac"))

if dfs:
    df_combined = pd.concat(dfs, ignore_index=True)

    # Mostrar tabla
    st.success(f"✅ {len(df_combined)} registros combinados")
    st.dataframe(df_combined, use_container_width=True)

    # Descargar resultado
    csv = df_combined.to_csv(index=False).encode("utf-8")
    st.download_button("💾 Descargar Excel combinado", csv, "obras_unificadas.csv", "text/csv")
else:
    st.info("Sube al menos un archivo para comenzar.")
