import streamlit as st

# 1. CONFIGURAÇÃO E MULTIMÉDIA (O que o professor pediu)
st.set_page_config(page_title="LumenÉvora Simulator", page_icon="💡", layout="wide")

# [MULTIMÉDIA: IMAGEM VETORIAL - LOGO]
# Dica: Quando tiveres o teu logo em .svg ou .png, substituis o caminho abaixo
# st.image("logo_vetorial.png", width=100) 

st.title("🏛️ LumenÉvora: Simulador de Eficiência Urbana")

# [MULTIMÉDIA: IMAGEM BITMAP - HEADER]
# Aqui podes pôr uma foto bonita de Évora à noite que vais editar
st.write("---")
st.markdown("### Monitorização de Impacto em Tempo Real")

# 2. SIDEBAR COM CONTROLOS ROBUSTOS (Sugestões do ChatGPT)
st.sidebar.header("⚙️ Parâmetros Técnicos")

n_pontos = st.sidebar.number_input("Número de Pontos de Luz (N)", min_value=1, value=1840, step=1)
p_led = st.sidebar.slider("Potência de cada LED (Watts)", min_value=1, max_value=150, value=50)
custo_kwh = st.sidebar.number_input("Custo da Energia (€/kWh)", min_value=0.01, value=0.20)

st.sidebar.header("⏰ Gestão de Tempo (Sazonalidade)")
 
# 1. O utilizador define a duração total da noite (ex: 9h no Verão, 15h no Inverno)
t_total_noite = st.sidebar.slider("Duração Total da Noite (Horas)", 8, 16, 11)
 
# 2. O utilizador define as horas de Pico (o máximo é o total da noite selecionado)
t_pico = st.sidebar.slider("Horas de Iluminação Máxima (Pico)", 0, t_total_noite, 5)
 
# 3. O sistema calcula o tempo restante para o modo inteligente
t_vazio = t_total_noite - t_pico
 
st.sidebar.info(f"Noite total: {t_total_noite}h | Modo Inteligente: {t_vazio}h")
 
# O t_total para o cálculo de consumo base passa a ser o valor dinâmico da noite
t_total = t_total_noite

st.sidebar.header("🚶 Atividade")
fator_ativacao = st.sidebar.slider("Fator de Movimento (%)", 0, 100, 10) / 100

# 3. LÓGICA DE CÁLCULO
# Consumo Atual (Sem Sensores)
consumo_base = (n_pontos * p_led * t_total) / 1000

# Consumo Proposto (A nossa fórmula mágica)
consumo_pico = (n_pontos * p_led * t_pico) / 1000
consumo_repouso = (n_pontos * (p_led * 0.20) * t_vazio) / 1000
consumo_extra_mov = (n_pontos * (p_led * 0.80) * t_vazio * fator_ativacao) / 1000

consumo_total_novo = consumo_pico + consumo_repouso + consumo_extra_mov

# Resultados de Impacto
poupanca_kwh = consumo_base - consumo_total_novo
poupanca_euros = poupanca_kwh * custo_kwh
co2_evitado = poupanca_kwh * 0.25
percentagem = (poupanca_kwh / consumo_base) * 100 if consumo_base > 0 else 0

# 4. DASHBOARD VISUAL
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Poupança Diária (€)", f"{poupanca_euros:.2f} €")
    st.caption("Baseado no tarifário ERSE 2025")

with col2:
    st.metric("Energia Poupada (kWh)", f"{poupanca_kwh:.1f} kWh")
    st.caption(f"Redução de {percentagem:.1f}%")

with col3:
    st.metric("CO2 Evitado (kg)", f"{co2_evitado:.1f} kg")
    st.caption("Fator APA: 0.25kg/kWh")

st.write("---")
st.success(f"**Estimativa Anual:** Aproximadamente **{poupanca_euros * 365:,.2f} €**")
st.info("💡 *Nota:* Este valor é uma projeção anual baseada na configuração de noite selecionada (cenário médio).")