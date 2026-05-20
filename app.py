import streamlit as st
import pandas as pd
import joblib 
from datetime import datetime
from reportlab.pdfgen import canvas

from seguridad import (
    cifrar_dato,
    descifrar_dato
)

# Configuración de la página
st.set_page_config(
    page_title="Mastitis Bovina",
    page_icon="🐮",
    layout="wide"
)

# Sidebar
with st.sidebar:

    st.image(
        "https://cdn-icons-png.flaticon.com/512/1998/1998610.png",
        width=120
    )

    st.title("🐮 Mastitis IA")

    st.markdown("""
    ### Sistema Inteligente Predictivo
    """)

    st.markdown("---")


# Encabezado principal
st.title("🐄 Sistema Predictivo de Mastitis Bovina")

st.subheader("Dashboard interactivo para detección temprana")

st.markdown("---")

# Cargar modelo y columnas
modelo = joblib.load("modelo_predictivo_rf.pkl")
columnas_modelo = joblib.load("columnas_predictivo.pkl")

# Información del animal
with st.container():
    st.header("📋 Información del animal 🐮")

id_vaca = st.text_input(
    "ID de la vaca",
    placeholder="Ejemplo: VACA-001"
)

edad = st.number_input(
    "Edad de la vaca",
    min_value=0,
    max_value=20,
    value=2
)

raza = st.selectbox(
    "Raza",
    ["Holstein", "Jersey", "Cebu", "Otra"]
)

partos = st.number_input(
    "Número de partos",
    min_value=0,
    max_value=15,
    value=1
)

st.markdown("---")

# Producción y ordeña

with st.container():
    st.header("🥛 Producción y Ordeña")

litros_dia = st.slider(
    "Producción de leche (L/día)",
    0.0,
    60.0,
    22.0
)

produccion_promedio = st.slider(
    "Producción promedio habitual (L/día)",
    0.0,
    60.0,
    30.0
)

tipo_ordena = st.selectbox(
    "Tipo de ordeña",
    ["manual", "mecanica"]
)

higiene_ordena = st.selectbox(
    "Higiene durante ordeña",
    ["buena", "regular", "mala"]
)

desinfeccion_pre = st.selectbox(
    "Desinfección pre-ordeña",
    [0, 1],
    format_func=lambda x: "Sí" if x == 1 else "No"
)

desinfeccion_post = st.selectbox(
    "Desinfección post-ordeña",
    [0, 1],
    format_func=lambda x: "Sí" if x == 1 else "No"
)

st.markdown("---")

# Alimentación y Entorno
with st.container():
    st.header("🥬 Alimentación & 🌡️ Entorno")

consumo_alimento = st.slider(
    "Consumo de alimento (kg/día)",
    0.0,
    50.0,
    25.0
)

consumo_agua = st.slider(
    "Consumo de agua (L/día)",
    0.0,
    150.0,
    80.0
)

temperatura_ambiente = st.slider(
    "Temperatura ambiente (°C)",
    0.0,
    50.0,
    28.0
)

humedad = st.slider(
    "Humedad ambiental (%)",
    0,
    100,
    65
)

temperatura_corporal = st.slider(
    "Temperatura corporal (°C)",
    35.0,
    45.0,
    39.5
)

st.markdown("---")

# Captura de síntomas
st.header("🩺 Captura de síntomas")
inflamacion = st.checkbox("Inflamación de ubre")
enrojecimiento = st.checkbox("Enrojecimiento")
dolor = st.checkbox("Dolor al tacto")
fiebre = st.checkbox("Fiebre")
grumos = st.checkbox("Grumos en leche")
cambios_leche = st.checkbox("Cambio en color de la leche")
letargo = st.checkbox("Letargo")
apetito = st.checkbox("Disminución del apetito")

st.markdown("---")

# Botón principal
analizar = st.button(
    "🔍 ANALIZAR RIESGO",
    use_container_width=True
)

st.markdown("---")

# =========================
# GENERAR PDF
# =========================

def generar_pdf(
    id_vaca,
    prediccion,
    probabilidad,
    riesgo
):

    nombre_pdf = (
        f"Reporte_{id_vaca}.pdf"
    )

    c = canvas.Canvas(nombre_pdf)

    c.setFont(
        "Helvetica-Bold",
        18
    )

    c.drawString(
        50,
        800,
        "Reporte Clínico Bovino"
    )

    c.setFont(
        "Helvetica",
        12
    )

    c.drawString(
        50,
        750,
        f"ID vaca: {id_vaca}"
    )

    c.drawString(
        50,
        720,
        f"Clasificación: {prediccion}"
    )

    c.drawString(
        50,
        690,
        f"Probabilidad: {probabilidad:.2f}%"
    )

    c.drawString(
        50,
        660,
        f"Nivel de riesgo: {riesgo}"
    )

    c.drawString(
        50,
        630,
        f"Fecha: {datetime.now()}"
    )

    c.save()

    return nombre_pdf

# Predicción real
if analizar:

    # Variables derivadas

    desviacion_promedio = (
        litros_dia - produccion_promedio
    )

    cambio_porcentual = (
        ((litros_dia - produccion_promedio)
        / (produccion_promedio + 1)) * 100
    )

    # Aproximaciones simples para MVP
    tendencia_3_dias = desviacion_promedio / 3

    variabilidad = abs(desviacion_promedio) * 0.5

    dias_baja = (
        1 if desviacion_promedio < 0 else 0
    )

    # Crear diccionario con entradas
    datos_usuario = {
        "info_animal.edad": edad,
        "info_animal.numero_partos": partos,
        "nutricion.consumo_alimento_kg_dia": consumo_alimento,
        "nutricion.consumo_agua_litros_dia": consumo_agua,
        "manejo.desinfeccion_pre": desinfeccion_pre,
        "manejo.desinfeccion_post": desinfeccion_post,
        "contexto.temperatura_ambiente": temperatura_ambiente,
        "contexto.humedad": humedad,
        "produccion.litros_dia": litros_dia,
        "produccion.desviacion_promedio": desviacion_promedio,
        "produccion.tendencia_3_dias": tendencia_3_dias,
        "produccion.variabilidad": variabilidad,
        "produccion.dias_baja": dias_baja,
        "produccion.cambio_porcentual": cambio_porcentual,
        "fisiologia.temperatura_corporal": temperatura_corporal,
        "info_animal.raza": raza,
        "manejo.tipo_ordena": tipo_ordena,
        "contexto.higiene_ordena": higiene_ordena
    }

    # Crear DataFrame
    df_usuario = pd.DataFrame([datos_usuario])

    # One-hot encoding
    df_usuario = pd.get_dummies(df_usuario)

    # Igualar columnas del modelo
    df_usuario = df_usuario.reindex(
        columns=columnas_modelo,
        fill_value=0
    )

    # Predicción
    prediccion = modelo.predict(df_usuario)[0]

    # Probabilidades
    probabilidades = modelo.predict_proba(df_usuario)[0]
    probabilidad_max = max(probabilidades) * 100

    # Obtener nombres reales de clases
    clases_modelo = modelo.classes_

    # Crear diccionario correcto
    probabilidades_dict = {}

    for clase, prob in zip(
        clases_modelo,
        probabilidades
    ):

        probabilidades_dict[clase] = prob * 100

    # Extraer probabilidades
    prob_saludable = probabilidades_dict.get(
        "saludable",
        0
    )

    prob_clinica = probabilidades_dict.get(
        "clinica",
        0
    )

    prob_subclinica = probabilidades_dict.get(
        "subclinica",
        0
    )

    # CIFRAR RESULTADO

    fecha_actual = datetime.now().strftime(
    "%Y-%m-%d %H:%M"
    )

    texto_resultado = (
    f"ID: {id_vaca} | "
    f"Fecha: {fecha_actual} | "
    f"Predicción: {prediccion} | "
    f"Probabilidad: {probabilidad_max:.2f}%"
    )

    resultado_cifrado = cifrar_dato(
        texto_resultado
    )

    # GUARDAR HISTORIAL

    with open(
        "historial.txt",
        "ab"
    ) as archivo:

        archivo.write(
            resultado_cifrado + b"\n"
        )

    # =========================
    # RESULTADO PRINCIPAL
    # =========================

    st.header("📌 Resultado del análisis")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            label="📈 Probabilidad estimada",
            value=f"{probabilidad_max:.2f}%"
        )

    with col2:

        st.metric(
            label="🩺 Clasificación",
            value=prediccion.capitalize()
        )

    # =========================
    # GRÁFICA PROBABILIDADES
    # =========================

    st.markdown("---")

    st.subheader("📊 Distribución de probabilidades")

    grafica_df = pd.DataFrame({

        "Estado": [
            "Saludable",
            "Clínica",
            "Subclínica"
        ],

        "Probabilidad": [
            prob_saludable,
            prob_clinica,
            prob_subclinica
        ]
    })

    st.bar_chart(
        grafica_df.set_index("Estado")
    )

    # =========================
    # INTERPRETACIÓN CLÍNICA
    # =========================

    st.markdown("---")

    st.subheader("🩺 Interpretación clínica")

    riesgo = ""

    # SALUDABLE
    if prediccion == "saludable":

        st.success("🟢 Estado saludable")

        riesgo = "Bajo"

        st.write(
            """
            La vaca presenta condiciones compatibles
            con un estado saludable.
            """
        )

        st.info(
            "📋 Se recomienda continuar "
            "con monitoreo preventivo."
        )

    # SUBCLÍNICA
    elif prediccion == "subclinica":

        if probabilidad_max <= 60:

            st.warning("🟡 Riesgo moderado")

            riesgo = "Moderado"

        else:

            st.warning("🟠 Riesgo alto")

            riesgo = "Alto"

        st.write(
                """
                La vaca presenta alteraciones compatibles
                con mastitis subclínica.
                """
        )

        st.info(
                "📋 Se recomienda vigilancia "
                "y revisión periódica."
        )

    # CLÍNICA
    else:

        if probabilidad_max <= 85:

            st.error("🔴 Riesgo alto")

            riesgo = "Alto"

        else:

            st.error("🚨 Riesgo crítico")

            riesgo = "Crítico"

        st.write(
            """
            La vaca presenta signos compatibles
            con mastitis clínica.
            """
        )

        st.error(
            "🚨 Atención veterinaria inmediata recomendada."
        )

    # =========================
    # EXPORTAR PDF
    # =========================

    st.markdown("---")

    nombre_pdf = generar_pdf(
        id_vaca,
        prediccion,
        probabilidad_max,
        riesgo
    )

    with open(
        nombre_pdf,
        "rb"
    ) as pdf_file:

        st.download_button(

            label="📄 Descargar reporte PDF",

            data=pdf_file,

            file_name=nombre_pdf,

            mime="application/pdf",

            use_container_width=True
        )

    # =========================
    # RESUMEN VISUAL
    # =========================

    st.markdown("---")

    st.subheader("📈 Resumen clínico")

    conteo_clases = {
        "Saludable": 0,
        "Clínica": 0,
        "Subclínica": 0
    }

    try:

        with open(
            "historial.txt",
            "rb"
        ) as archivo:

            lineas = archivo.readlines()

        for linea in lineas:

            texto = descifrar_dato(
                linea.strip()
            )

            texto_lower = texto.lower()

            if "subclinica" in texto_lower:

                conteo_clases["Subclínica"] += 1

            elif "clinica" in texto_lower:

                conteo_clases["Clínica"] += 1

            elif "saludable" in texto_lower:

                conteo_clases["Saludable"] += 1

        resumen_df = pd.DataFrame({

            "Estado": list(
                conteo_clases.keys()
            ),

            "Cantidad": list(
                conteo_clases.values()
            )
        })

        st.bar_chart(
            resumen_df.set_index("Estado")
        )

    except:
        pass
    

    # HISTORIAL CLÍNICO
    with st.container():
        st.header("📁 Historial clínico")
        st.caption(
        "Historial protegido mediante cifrado AES"
        )

    try:

        with open(
            "historial.txt",
            "rb"
        ) as archivo:

            lineas = archivo.readlines()

        if lineas:

            for linea in reversed(lineas[-10:]):

                linea = linea.strip()

                if linea:

                    texto = descifrar_dato(
                        linea
                    )

                    st.info(texto)

        else:

            st.write(
                "No hay historial disponible."
            )

    except FileNotFoundError:

        st.write(
            "Historial no encontrado."
        )






        