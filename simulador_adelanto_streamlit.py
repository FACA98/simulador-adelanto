
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

def calcular_adelanto(monto_credito, tasa_mensual, cuota_mensual, adelanto, cuota_adelanto):
    saldo = monto_credito
    cuota_numero = 0
    interes_total = 0
    while saldo > 0 and cuota_numero < 1000:
        cuota_numero += 1
        interes = saldo * tasa_mensual
        capital = cuota_mensual - interes
        saldo -= capital
        interes_total += interes
        if cuota_numero == cuota_adelanto:
            saldo -= adelanto
    return cuota_numero, interes_total

# Parámetros del préstamo
monto_credito = 70798.97
tasa_anual = 0.0632
tasa_mensual = (1 + tasa_anual) ** (1 / 12) - 1
cuota_mensual = 431.21
cuotas_originales = 360

st.set_page_config(page_title="Simulador de Adelanto de Capital", layout="centered")
st.title("💰 Simulador de Adelanto de Capital")
st.markdown("Calculá cómo impacta adelantar capital sobre tu crédito hipotecario.")

# Inputs
adelanto_usuario = st.number_input("🔢 Ingresá el monto de capital a adelantar ($)", min_value=0.0, value=1000.0, step=500.0)
cuota_adelanto = st.number_input("📅 En qué cuota vas a hacer el adelanto", min_value=1, max_value=cuotas_originales, value=10)

if st.button("Calcular"):
    cuotas_base, interes_base = calcular_adelanto(monto_credito, tasa_mensual, cuota_mensual, 0, 0)
    cuotas_nuevas, interes_nuevo = calcular_adelanto(monto_credito, tasa_mensual, cuota_mensual, adelanto_usuario, int(cuota_adelanto))

    st.subheader("📊 Resultados del Adelanto Puntual")
    st.markdown(f'''
    - **Cuotas originales**: {cuotas_base}  
    - **Cuotas luego del adelanto**: {cuotas_nuevas}  
    - **Cuotas ahorradas**: {cuotas_base - cuotas_nuevas}  
    - **Interés sin adelanto**: ${interes_base:,.2f}  
    - **Interés con adelanto**: ${interes_nuevo:,.2f}  
    - **Ahorro en intereses**: ${interes_base - interes_nuevo:,.2f}
    ''')

    st.subheader(f"📈 Simulación incremental en la cuota {cuota_adelanto}")
    adelantos = list(range(1000, 41000, 1000))
    cuotas_ahorradas_acumuladas = []
    interes_ahorrado = []
    eficiencia = []

    for adelanto in adelantos:
        cuotas_sim, interes_sim = calcular_adelanto(monto_credito, tasa_mensual, cuota_mensual, adelanto, int(cuota_adelanto))
        ahorro_cuotas = cuotas_base - cuotas_sim
        ahorro_interes = interes_base - interes_sim
        cuotas_ahorradas_acumuladas.append(ahorro_cuotas)
        interes_ahorrado.append(ahorro_interes)
        eficiencia.append(round(ahorro_interes / adelanto, 4))

    cuotas_marginales = [cuotas_ahorradas_acumuladas[0]]
    for i in range(1, len(cuotas_ahorradas_acumuladas)):
        cuotas_marginales.append(cuotas_ahorradas_acumuladas[i] - cuotas_ahorradas_acumuladas[i - 1])

    # Mostrar tabla de simulación incremental
    df_resultados = pd.DataFrame({
        "Adelanto ($)": adelantos,
        "Equiv. Cuotas": [round(a / cuota_mensual, 2) for a in adelantos],
        "Cuotas Nuevas": [cuotas_base - ah + cuotas_base - (cuotas_base - ah) for ah in cuotas_ahorradas_acumuladas],
        "Cuotas Ahorradas": cuotas_ahorradas_acumuladas,
        "Interés Ahorrado ($)": [round(i, 2) for i in interes_ahorrado],
        "Eficiencia ($ Interés / $ Adelanto)": eficiencia
    })

    st.dataframe(df_resultados.style.format({
        "Adelanto ($)": "{:,.0f}",
        "Equiv. Cuotas": "{:.2f}",
        "Cuotas Nuevas": "{:.0f}",
        "Cuotas Ahorradas": "{:.0f}",
        "Interés Ahorrado ($)": "${:,.2f}",
        "Eficiencia ($ Interés / $ Adelanto)": "{:.4f}"
    }))

    # Gráfico 1: Interés ahorrado + cuotas marginales
    fig, ax1 = plt.subplots(figsize=(10, 5))
    ax1.set_xlabel("Monto Adelantado ($)")
    ax1.set_ylabel("Interés Ahorrado ($)", color='tab:blue')
    line1, = ax1.plot(adelantos, interes_ahorrado, marker='o', color='tab:blue', label='Interés Ahorrado')
    ax1.tick_params(axis='y', labelcolor='tab:blue')

    ax2 = ax1.twinx()
    ax2.set_ylabel("Cuotas Marginales", color='tab:green')
    line2, = ax2.plot(adelantos, cuotas_marginales, marker='s', color='tab:green', label='Cuotas Marginales')
    ax2.tick_params(axis='y', labelcolor='tab:green')

    fig.tight_layout()
    ax1.set_title("Impacto del Adelanto: Interés Ahorrado vs Cuotas Marginales")
    st.pyplot(fig)

    # Gráfico 2: Eficiencia
    fig2, ax3 = plt.subplots(figsize=(10, 5))
    ax3.plot(adelantos, eficiencia, marker='^', color='purple', label='Eficiencia')
    ax3.set_xlabel("Monto Adelantado ($)")
    ax3.set_ylabel("Eficiencia ($ interés / $ adelantado)")
    ax3.set_title("Evolución de la Eficiencia del Adelanto")
    ax3.grid(True)
    st.pyplot(fig2)
