import yfinance as yf
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from matplotlib.widgets import Dropdown

def obter_dados_acao(ticker):
    """Obtém os dados históricos de uma ação."""
    try:
        acao = yf.Ticker(ticker + ".SA")
        historico = acao.history(period="1y")
        historico["Variacao"] = historico["Close"].pct_change()
        return historico
    except Exception as e:
        print(f"Erro ao obter dados de {ticker}: {e}")
        return None

def prever_acao(historico, dias_previsao=5):
    """Faz a previsão dos preços da ação."""
    modelo = LinearRegression()
    dias = range(len(historico))
    modelo.fit(pd.DataFrame(dias), historico["Close"])
    ultimos_dias = range(len(historico), len(historico) + dias_previsao)
    previsoes = modelo.predict(pd.DataFrame(ultimos_dias))
    return previsoes

def atualizar_grafico(ticker):
    """Atualiza o gráfico principal com os dados da ação selecionada."""
    historico = obter_dados_acao(ticker)
    if historico is not None:
        previsoes = prever_acao(historico)
        ax.clear()  # Limpa o gráfico anterior
        ax.plot(historico["Close"], label="Preço Histórico", linewidth=2)
        ax.plot(range(len(historico), len(historico) + 5), previsoes, label="Previsão", color="red", linestyle="--", linewidth=2)
        ax.set_title(f"Previsão de {ticker} (1 Ano)", fontsize=16)
        ax.set_xlabel("Dias", fontsize=12)
        ax.set_ylabel("Preço (R$)", fontsize=12)
        ax.legend(fontsize=10)
        ax.grid(True, linestyle="--", alpha=0.5)
        plt.draw()  # Redesenha o gráfico

# Lista de ações
acoes = ["PETR4", "VALE3", "ITUB4", "BBDC4", "ABEV3", "WEGE3", "GGBR4", "JBSS3", "RENT3", "EQTL3"]

# Configuração do gráfico
plt.style.use("dark_background")
fig, ax = plt.subplots(figsize=(12, 6))
plt.subplots_adjust(top=0.8)  # Ajusta o espaço para o menu

# Menu suspenso
menu_ax = plt.axes([0.1, 0.9, 0.8, 0.05])  # Posição do menu
menu = Dropdown(menu_ax, "Ações", acoes)
menu.on_changed(atualizar_grafico)

# Exibe o gráfico inicial com a primeira ação
atualizar_grafico(acoes[0])
plt.show()