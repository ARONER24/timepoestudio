import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Configuración de la página
st.set_page_config(page_title="Explorador de Datos Pro", layout="wide")

st.title("📊 Analizador de Correlación de Datos")
st.write("Sube tu archivo CSV para explorar sus datos y analizar cómo se relacionan sus variables.")

# 1. Cargador de archivos
uploaded_file = st.file_uploader("Selecciona un archivo CSV", type=["csv"])

if uploaded_file is not None:
    try:
        # Leer el archivo con Pandas
        df = pd.read_csv(uploaded_file)
        
        # Mensaje de éxito
        st.success("¡Archivo cargado correctamente!")
        
        # 2. Mostrar df.head()
        st.subheader("👀 Vista previa de los datos (df.head())")
        st.dataframe(df.head())
        
        # Filtrar solo columnas numéricas para la correlación
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
        
        if len(numeric_cols) < 2:
            st.warning("⚠️ El dataset necesita tener al menos 2 columnas numéricas para calcular una correlación.")
        else:
            st.write("---")
            st.subheader("🔥 Diagrama de Correlación Dinámico")
            
            # 3. Selección de columnas por el usuario
            selected_cols = st.multiselect(
                "Selecciona las columnas numéricas que deseas incluir en el análisis:",
                options=numeric_cols,
                default=numeric_cols[:min(5, len(numeric_cols))] # Selecciona por defecto hasta las primeras 5
            )
            
            if len(selected_cols) >= 2:
                # Calcular la matriz de correlación
                corr_matrix = df[selected_cols].corr()
                
                # Crear el gráfico con Seaborn y Matplotlib
                fig, ax = plt.subplots(figsize=(8, 6))
                sns.heatmap(
                    corr_matrix, 
                    annot=True, 
                    cmap="coolwarm", 
                    fmt=".2f", 
                    linewidths=0.5, 
                    ax=ax,
                    vmin=-1, 
                    vmax=1
                )
                plt.title("Matriz de Correlación")
                
                # Mostrar el gráfico en Streamlit
                st.pyplot(fig)
            else:
                st.info("💡 Por favor, selecciona al menos 2 columnas para generar el mapa de calor.")
                
    except Exception as e:
        st.error(f"Hubo un error al procesar el archivo: {e}")
else:
    st.info("📥 Esperando que subas un archivo CSV...")
