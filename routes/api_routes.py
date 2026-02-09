"""
Rotas da API REST para o sistema de análise da QUINA
"""
from flask import Blueprint, jsonify, request
from services.api_caixa_service import ApiCaixaService
from services.estatistica_service import EstatisticaService
from services.quina_service import QuinaService
from models.resultado_model import ResultadoModel

api_bp = Blueprint('api', __name__, url_prefix='/api')

# Inicializa serviços
api_caixa = ApiCaixaService()
estatistica = EstatisticaService()
quina = QuinaService()
resultado_model = ResultadoModel()


@api_bp.route('/atualizar', methods=['POST'])
def atualizar():
    """
    Atualiza a base de dados com novos concursos da API da Caixa
    """
    try:
        resultado = api_caixa.atualizar_base_completa()
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@api_bp.route('/ultimo-resultado', methods=['GET'])
def ultimo_resultado():
    """
    Retorna o último resultado cadastrado
    """
    try:
        resultado = resultado_model.buscar_ultimo()
        if resultado:
            return jsonify(resultado), 200
        else:
            return jsonify({'mensagem': 'Nenhum resultado encontrado'}), 404
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@api_bp.route('/resultados', methods=['GET'])
def listar_resultados():
    """
    Lista resultados com limite opcional
    Query params: limite (int)
    """
    try:
        limite = request.args.get('limite', type=int)
        resultados = resultado_model.buscar_todos(limite=limite)
        return jsonify(resultados), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@api_bp.route('/resultado/<int:numero>', methods=['GET'])
def buscar_resultado(numero):
    """
    Busca um resultado específico por número do concurso
    """
    try:
        resultado = resultado_model.buscar_por_numero(numero)
        if resultado:
            return jsonify(resultado), 200
        else:
            return jsonify({'mensagem': f'Concurso {numero} não encontrado'}), 404
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@api_bp.route('/estatisticas', methods=['GET'])
def obter_estatisticas():
    """
    Retorna estatísticas completas
    """
    try:
        stats = estatistica.calcular_estatisticas_completas()
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@api_bp.route('/gerar-palpite', methods=['POST'])
def gerar_palpite():
    """
    Gera palpites usando estratégia especificada
    Body: {
        "estrategia": "equilibrada",
        "quantidade_numeros": 5,
        "quantidade_jogos": 1
    }
    """
    try:
        dados = request.get_json()
        
        estrategia = dados.get('estrategia', 'equilibrada')
        quantidade_numeros = dados.get('quantidade_numeros', 5)
        quantidade_jogos = dados.get('quantidade_jogos', 1)
        
        resultado = quina.gerar_palpite(
            estrategia=estrategia,
            quantidade_numeros=quantidade_numeros,
            quantidade_jogos=quantidade_jogos
        )
        
        if 'erro' in resultado:
            return jsonify(resultado), 400
        
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@api_bp.route('/conferir', methods=['POST'])
def conferir():
    """
    Confere um palpite com um resultado
    Body: {
        "numeros": [1, 2, 3, 4, 5],
        "numero_concurso": 6792
    }
    """
    try:
        dados = request.get_json()
        
        numeros = dados.get('numeros', [])
        numero_concurso = dados.get('numero_concurso')
        
        if not numeros or not numero_concurso:
            return jsonify({'erro': 'Números e número do concurso são obrigatórios'}), 400
        
        # Busca o resultado do concurso
        resultado = resultado_model.buscar_por_numero(numero_concurso)
        
        if not resultado:
            return jsonify({'erro': f'Concurso {numero_concurso} não encontrado'}), 404
        
        # Converte para inteiros
        numeros_jogo = [int(n) for n in numeros]
        numeros_sorteados = [int(n) for n in resultado['listaDezenas']]
        
        # Verifica acertos
        acertos = set(numeros_jogo).intersection(set(numeros_sorteados))
        
        return jsonify({
            'numero_concurso': numero_concurso,
            'numeros_jogo': sorted(numeros_jogo),
            'numeros_sorteados': sorted(numeros_sorteados),
            'acertos': sorted(list(acertos)),
            'quantidade_acertos': len(acertos)
        }), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500
