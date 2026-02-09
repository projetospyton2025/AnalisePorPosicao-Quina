"""
Configurações e constantes do sistema de análise da QUINA
"""
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Configurações do Flask
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'

# Configurações do servidor
HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 5055))

# Configurações do banco de dados
DATABASE_PATH = os.getenv('DATABASE_PATH', 'database.db')

# Configurações da API da Caixa
API_QUINA_URL = os.getenv('API_QUINA_URL', 'https://servicebus2.caixa.gov.br/portaldeloterias/api/quina')

# Constantes da QUINA
MIN_NUMEROS = 1
MAX_NUMEROS = 80
NUMEROS_SORTEADOS = 5
MIN_JOGO = 5
MAX_JOGO = 15

# Identidade Visual da QUINA
COR_PRINCIPAL = '#260184'  # Roxo/Violeta
LOGO_URL = 'https://i.postimg.cc/G3PvK6cN/quina.png'

# Paleta de cores (0% a 100%)
PALETA_CORES = {
    100: '#ffffff',
    95: '#ede6ff',
    90: '#dbcdfe',
    85: '#c9b3fe',
    80: '#b69afe',
    75: '#a481fe',
    70: '#9268fd',
    65: '#804efd',
    60: '#6e35fd',
    55: '#5c1cfd',
    50: '#4903fc',
    45: '#4202e3',
    40: '#3b02ca',
    35: '#3302b1',
    30: '#2c0297',
    26: '#260184',  # Cor principal
    25: '#25017e',
    20: '#1d0165',
    15: '#16014c',
    10: '#0f0132',
    5: '#070019',
    0: '#000000'
}
