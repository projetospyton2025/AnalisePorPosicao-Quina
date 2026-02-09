"""
Rotas para páginas HTML do sistema de análise da QUINA
"""
from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """
    Página principal com estatísticas e análises
    """
    return render_template('index.html')


@main_bp.route('/palpites')
def palpites():
    """
    Página de geração de palpites
    """
    return render_template('palpites.html')
