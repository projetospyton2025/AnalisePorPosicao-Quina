"""
Serviço para cálculos estatísticos dos resultados da QUINA
"""
from typing import Dict, List, Tuple
from collections import Counter, defaultdict
import config
from models.resultado_model import ResultadoModel


class EstatisticaService:
    """
    Serviço para calcular estatísticas dos resultados da QUINA
    """
    
    def __init__(self):
        """
        Inicializa o serviço
        """
        self.resultado_model = ResultadoModel()
    
    def calcular_estatisticas_completas(self) -> Dict:
        """
        Calcula todas as estatísticas disponíveis
        
        Returns:
            Dicionário com todas as estatísticas
        """
        return {
            'total_concursos': self._contar_concursos(),
            'frequencia_numeros': self.calcular_frequencia_numeros(),
            'atrasos': self.calcular_atrasos(),
            'pares_impares': self.calcular_pares_impares(),
            'por_faixa': self.calcular_por_faixa(),
            'por_digito': self.calcular_por_digito(),
            'por_posicao_sorteio': self.calcular_por_posicao_sorteio()
        }
    
    def calcular_frequencia_numeros(self) -> List[Dict]:
        """
        Calcula a frequência de cada número (01-80)
        
        Returns:
            Lista de dicionários com número e frequência, ordenados por frequência
        """
        resultados = self.resultado_model.buscar_todos()
        
        if not resultados:
            return []
        
        # Conta frequência de cada número
        frequencias = Counter()
        for resultado in resultados:
            if resultado.get('listaDezenas'):
                for numero in resultado['listaDezenas']:
                    frequencias[int(numero)] += 1
        
        # Formata resultado
        frequencia_list = [
            {
                'numero': numero,
                'frequencia': freq,
                'percentual': round((freq / len(resultados)) * 100, 2)
            }
            for numero, freq in frequencias.items()
        ]
        
        # Ordena por frequência (decrescente) e depois por número
        frequencia_list.sort(key=lambda x: (-x['frequencia'], x['numero']))
        
        return frequencia_list
    
    def calcular_atrasos(self) -> List[Dict]:
        """
        Calcula o atraso de cada número (concursos desde última aparição)
        
        Returns:
            Lista de dicionários com número e atraso, ordenados por atraso
        """
        resultados = self.resultado_model.buscar_todos()
        
        if not resultados:
            return []
        
        # Inicializa atrasos para todos os números (1-80)
        ultima_aparicao = {num: -1 for num in range(1, 81)}
        
        # Percorre resultados do mais recente ao mais antigo
        for idx, resultado in enumerate(resultados):
            if resultado.get('listaDezenas'):
                for numero in resultado['listaDezenas']:
                    num_int = int(numero)
                    if ultima_aparicao[num_int] == -1:
                        ultima_aparicao[num_int] = idx
        
        # Calcula atraso (números que nunca apareceram terão atraso = total de concursos)
        total_concursos = len(resultados)
        atrasos = [
            {
                'numero': numero,
                'atraso': ultima_aparicao[numero] if ultima_aparicao[numero] != -1 else total_concursos
            }
            for numero in range(1, 81)
        ]
        
        # Ordena por atraso (decrescente)
        atrasos.sort(key=lambda x: (-x['atraso'], x['numero']))
        
        return atrasos
    
    def calcular_pares_impares(self) -> Dict:
        """
        Calcula a distribuição de números pares e ímpares
        
        Returns:
            Dicionário com estatísticas de pares e ímpares
        """
        resultados = self.resultado_model.buscar_todos()
        
        if not resultados:
            return {'pares': 0, 'impares': 0, 'total': 0}
        
        total_pares = 0
        total_impares = 0
        
        for resultado in resultados:
            if resultado.get('listaDezenas'):
                for numero in resultado['listaDezenas']:
                    if int(numero) % 2 == 0:
                        total_pares += 1
                    else:
                        total_impares += 1
        
        total = total_pares + total_impares
        
        return {
            'pares': total_pares,
            'impares': total_impares,
            'total': total,
            'percentual_pares': round((total_pares / total) * 100, 2) if total > 0 else 0,
            'percentual_impares': round((total_impares / total) * 100, 2) if total > 0 else 0
        }
    
    def calcular_por_faixa(self) -> List[Dict]:
        """
        Calcula a frequência de números por faixa de dezenas
        Faixas: 01-20, 21-40, 41-60, 61-80
        
        Returns:
            Lista de dicionários com informações de cada faixa
        """
        resultados = self.resultado_model.buscar_todos()
        
        if not resultados:
            return []
        
        faixas = {
            '01-20': 0,
            '21-40': 0,
            '41-60': 0,
            '61-80': 0
        }
        
        for resultado in resultados:
            if resultado.get('listaDezenas'):
                for numero in resultado['listaDezenas']:
                    num_int = int(numero)
                    if 1 <= num_int <= 20:
                        faixas['01-20'] += 1
                    elif 21 <= num_int <= 40:
                        faixas['21-40'] += 1
                    elif 41 <= num_int <= 60:
                        faixas['41-60'] += 1
                    elif 61 <= num_int <= 80:
                        faixas['61-80'] += 1
        
        total = sum(faixas.values())
        
        return [
            {
                'faixa': faixa,
                'quantidade': qtd,
                'percentual': round((qtd / total) * 100, 2) if total > 0 else 0
            }
            for faixa, qtd in faixas.items()
        ]
    
    def calcular_por_digito(self) -> List[Dict]:
        """
        Calcula a frequência por dígito final (0-9)
        
        Returns:
            Lista de dicionários com frequência de cada dígito
        """
        resultados = self.resultado_model.buscar_todos()
        
        if not resultados:
            return []
        
        digitos = Counter()
        
        for resultado in resultados:
            if resultado.get('listaDezenas'):
                for numero in resultado['listaDezenas']:
                    digito = int(numero) % 10
                    digitos[digito] += 1
        
        total = sum(digitos.values())
        
        return [
            {
                'digito': digito,
                'quantidade': digitos[digito],
                'percentual': round((digitos[digito] / total) * 100, 2) if total > 0 else 0
            }
            for digito in range(10)
        ]
    
    def calcular_por_posicao_sorteio(self) -> Dict:
        """
        Calcula quais números aparecem mais em cada posição do sorteio (1ª a 5ª)
        
        Returns:
            Dicionário com estatísticas por posição
        """
        resultados = self.resultado_model.buscar_todos()
        
        if not resultados:
            return {}
        
        # Inicializa contadores para cada posição
        posicoes = {
            1: Counter(),
            2: Counter(),
            3: Counter(),
            4: Counter(),
            5: Counter()
        }
        
        # Conta frequência por posição
        for resultado in resultados:
            ordem_sorteio = resultado.get('dezenasSorteadasOrdemSorteio')
            if ordem_sorteio and len(ordem_sorteio) == 5:
                for idx, numero in enumerate(ordem_sorteio, start=1):
                    posicoes[idx][int(numero)] += 1
        
        # Formata resultado
        resultado_formatado = {}
        for posicao, counter in posicoes.items():
            # Top 10 números mais frequentes nesta posição
            top_numeros = [
                {
                    'numero': numero,
                    'frequencia': freq
                }
                for numero, freq in counter.most_common(10)
            ]
            
            resultado_formatado[f'posicao_{posicao}'] = {
                'posicao': posicao,
                'top_numeros': top_numeros,
                'total_sorteios': sum(counter.values())
            }
        
        return resultado_formatado
    
    def _contar_concursos(self) -> int:
        """
        Conta o total de concursos cadastrados
        
        Returns:
            Total de concursos
        """
        resultados = self.resultado_model.buscar_todos()
        return len(resultados)
