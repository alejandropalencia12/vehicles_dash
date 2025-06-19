import streamlit as st
import pandas as pd
import plotly.express as px

# Encabezado de la aplicación
st.header("Aplicación de análisis de vehículos")

# Cargar los datos
car_data = pd.read_csv('vehicles_us.csv')

# Mostrar los primeros datos para verificar
st.subheader("Vista previa del conjunto de datos")
st.dataframe(car_data.head())

# Botón para crear histograma
hist_button = st.button('Construir histograma')

if hist_button:
    st.write('Creación de un histograma para la columna odómetro')
    fig = px.histogram(car_data, x="odometer")
    st.plotly_chart(fig, use_container_width=True)

# Botón para crear gráfico de dispersión
scatter_button = st.button('Construir gráfico de dispersión')

if scatter_button:
    st.write('Creación de un gráfico de dispersión entre odómetro y precio')
    fig2 = px.scatter(car_data, x="odometer", y="price")
    st.plotly_chart(fig2, use_container_width=True)

# Vehicle types by model con filtro de tipo
st.subheader("Tipos de vehículo por modelo")
vehicle_types = sorted(car_data['type'].dropna().unique().tolist())
selected_type = st.selectbox("Selecciona el tipo de vehículo", options=[
                             "Todos"] + vehicle_types)

if selected_type == "Todos":
    df_filtered = car_data
else:
    df_filtered = car_data[car_data['type'] == selected_type]

fig3 = px.bar(
    df_filtered.groupby('model')['type'].count().reset_index(name='count'),
    x='model', y='count',
    title='Tipos de vehículo por modelo'
)
st.plotly_chart(fig3, use_container_width=True)

# Histograma condición vs año del modelo
st.subheader("Histograma de condición vs año del modelo")
conditions = sorted(car_data['condition'].dropna().unique().tolist())
selected_condition = st.selectbox(
    "Selecciona condición", options=["Todos"] + conditions)

if selected_condition == "Todos":
    df_cond = car_data
else:
    df_cond = car_data[car_data['condition'] == selected_condition]

fig4 = px.histogram(
    df_cond, x="model_year", color="condition",
    title="Histograma de condición vs año del modelo",
    barmode='group'
)
st.plotly_chart(fig4, use_container_width=True)

# Comparar precios entre modelos
st.subheader("Comparar distribución de precios entre modelos")

# Mostrar los modelos
all_models = sorted(car_data['model'].dropna().unique())
model1 = st.selectbox("Selecciona modelo 1", options=all_models, index=0)
model2 = st.selectbox("Selecciona modelo 2", options=all_models, index=1)

normalize_hist = st.checkbox("Normalizar histograma")

df_model1 = car_data[car_data['model'] == model1]
df_model2 = car_data[car_data['model'] == model2]

fig5 = px.histogram(
    pd.concat([df_model1.assign(model=model1),
              df_model2.assign(model=model2)]),
    x='price', color='model',
    barmode='overlay',
    histnorm='probability' if normalize_hist else '',
    nbins=40,
    title=f'Distribución de precios: {model1} vs {model2}'
)
st.plotly_chart(fig5, use_container_width=True)


st.subheader("Vista completa de los datos")
st.dataframe(car_data)



# Cargar los datos
car_data = pd.read_csv('vehicles_us.csv')

# Filtrar los modelos de carros desde el año 2010
car_data_modern = car_data[car_data['model_year'] >= 2010]

# Agrupar los datos por año
gp_by_year = car_data_modern.groupby('model_year')['model'].size().reset_index()

# Título principal
st.header('Modelos más recientes')

# Botón para construir gráfico de modelos por año
bar_button = st.button('Construir un diagrama de barras para los modelos de carros')

if bar_button:
    st.write('Creación de diagrama de barras para visualizar la cantidad de modelos de carros que se producen cada año')
    # Crear gráfico de barras con color azul uniforme
    fig1 = px.bar(
        gp_by_year,
        x='model_year',
        y='model',
        labels={'model_year': 'Año', 'model': 'Cantidad de carros'},
        color_discrete_sequence=['#1f77b4']  # Azul oscuro
    )
    st.plotly_chart(fig1, use_container_width=True)

# Botón para construir gráfico de condiciones por tipo de carro
bar_button2 = st.button('Construir un diagrama de barras de las condiciones de cada tipo de carro')

# Agrupar por tipo de carro y condición
gp_by_type = car_data_modern.groupby(['type', 'condition'])['model'].size().reset_index()

if bar_button2:
    st.write('Creación de diagrama de barras para visualizar las condiciones de cada tipo de carro')
    fig2 = px.bar(
        gp_by_type,
        x='type',
        y='model',
        labels={'type': 'Tipo de carro', 'model': 'Cantidad de carros'},
        color='condition',  # Se colorea por condición
        color_discrete_sequence=px.colors.qualitative.Set2  # Puedes cambiar esta paleta
    )
    st.plotly_chart(fig2, use_container_width=True)

# Checkbox para crear diagrama de dispersión
build_dispersion_diagram = st.checkbox('Construir un diagrama de dispersión de precio y kilometraje')

if build_dispersion_diagram:
    st.write('Creación de diagrama de dispersión para ver la relación entre precio y kilometraje')
    fig3 = px.scatter(
        car_data_modern,
        x="odometer",
        y="price",
        labels={"odometer": "Kilometraje", "price": "Precio"},
        color_discrete_sequence=['#2ca02c']  # Verde, si quieres darle color
    )
    st.plotly_chart(fig3, use_container_width=True)
