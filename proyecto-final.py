import streamlit as st
import pandas as pd
import plotly.express as px

# Carga de datos
def load_data():
    df = pd.read_csv('salario_minimo.csv')
    return df

def main():
    # Título principal
    st.title('Análisis de Salarios Mínimos y Costo de Vida')
    st.subheader('Mauricio Artunduaga Conde')
    
    # Párrafo introductorio
    st.markdown("""
    Este análisis compara el salario mínimo de Colombia con otros países de América Latina, Norteamérica, Europa y Oceanía.
    Es un esfuerzo por entender mejor las diferencias en los costos de vida y los salarios en distintas regiones del mundo.
    """)
    
    # Enlace a LinkedIn
    st.markdown("""
    🌐 Conecta conmigo en [LinkedIn](https://www.linkedin.com/in/mauricio-artunduaga-23935b106?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app)
    """)
    
    # Cargar datos
    df = load_data()
    
    # Sidebar para filtros
    st.sidebar.header('Filtros')
    region_filter = st.sidebar.multiselect(
        'Seleccionar Región',
        options=df['Region'].unique(),
        default=df['Region'].unique()
    )
    
    # Filtrar dataframe
    df_filtered = df[df['Region'].isin(region_filter)]
    
    # Mostrar datos
    st.header("Datos por País:")
    st.dataframe(df_filtered)
    
    # Análisis de Salarios
    st.header("Análisis de Salarios Mínimos")
    
    # Gráfico de barras de salarios por país
    fig_salarios = px.bar(
        df_filtered,
        x='Pais',
        y='Salario Minimo',
        color='Region',
        title='Salarios Mínimos por País',
        labels={'Salario Minimo': 'Salario Mínimo (Moneda Local)'}
    )
    st.plotly_chart(fig_salarios)
    
    # Análisis de Costos
    st.header("Análisis de Costos")
    
    # Selector de país para análisis detallado
    pais_seleccionado = st.selectbox('Seleccionar País para Análisis Detallado', df_filtered['Pais'])
    
    # Datos del país seleccionado
    datos_pais = df_filtered[df_filtered['Pais'] == pais_seleccionado].iloc[0]
    
    # Crear gráfico de pie para distribución de gastos
    datos_gastos = {
        'Categoría': ['Alquiler', 'Alimentación', 'Servicios', 'Internet', 'Transporte', 'Entretenimiento'],
        'Monto': [
            datos_pais['Alquiler Accesible'],
            datos_pais['Alimentacion'],
            datos_pais['Servicios Publicos'],
            datos_pais['Internet'],
            datos_pais['Transporte'],
            datos_pais['Entretenimiento Basico']
        ]
    }
    
    df_gastos = pd.DataFrame(datos_gastos)
    fig_gastos = px.pie(
        df_gastos,
        values='Monto',
        names='Categoría',
        title=f'Distribución de Gastos en {pais_seleccionado}'
    )
    st.plotly_chart(fig_gastos)
    
    # Métricas importantes
    col1, col2, col3 = st.columns(3)
    with col1:
        total_gastos = df_gastos['Monto'].sum()
        st.metric(
            label="Total Gastos Mensuales",
            value=f"{total_gastos:.2f} {datos_pais['Moneda']}"
        )
    with col2:
        salario = datos_pais['Salario Minimo']
        st.metric(
            label="Salario Mínimo",
            value=f"{salario:.2f} {datos_pais['Moneda']}"
        )
    with col3:
        balance = salario - total_gastos
        st.metric(
            label="Balance",
            value=f"{balance:.2f} {datos_pais['Moneda']}"
        )

if __name__ == '__main__':
    main()
