"""
Serviço para geração de palpites para a QUINA
"""
import random
from typing import List, Dict
import config
from services.estatistica_service import EstatisticaService


class QuinaService:
    """
    Serviço para gerar palpites da QUINA usando diferentes estratégias
    """
    
    def __init__(self):
        """
        Inicializa o serviço
        """
        self.estatistica_service = EstatisticaService()
    
    def gerar_palpite(
        self,
        estrategia: str = 'equilibrada',
        quantidade_numeros: int = 5,
        quantidade_jogos: int = 1
    ) -> Dict:
        """
        Gera palpites usando a estratégia especificada
        
        Args:
            estrategia: Tipo de estratégia (equilibrada, agressiva, conservadora, 
                       mista, atrasados, por_faixa, por_posicao)
            quantidade_numeros: Quantidade de números por jogo (5-15)
            quantidade_jogos: Quantidade de jogos a gerar (1-100)
            
        Returns:
            Dicionário com os palpites gerados e informações da estratégia
        """
        # Validações
        if quantidade_numeros < config.MIN_JOGO or quantidade_numeros > config.MAX_JOGO:
            return {
                'erro': f'Quantidade de números deve ser entre {config.MIN_JOGO} e {config.MAX_JOGO}'
            }
        
        if quantidade_jogos < 1 or quantidade_jogos > 100:
            return {
                'erro': 'Quantidade de jogos deve ser entre 1 e 100'
            }
        
        # Mapeia estratégias para métodos
        estrategias = {
            'equilibrada': self._estrategia_equilibrada,
            'agressiva': self._estrategia_agressiva,
            'conservadora': self._estrategia_conservadora,
            'mista': self._estrategia_mista,
            'atrasados': self._estrategia_atrasados,
            'por_faixa': self._estrategia_por_faixa,
            'por_posicao': self._estrategia_por_posicao
        }
        
        if estrategia not in estrategias:
            return {
                'erro': f'Estratégia inválida. Opções: {", ".join(estrategias.keys())}'
            }
        
        # Gera os jogos
        metodo = estrategias[estrategia]
        jogos = []
        
        for _ in range(quantidade_jogos):
            numeros = metodo(quantidade_numeros)
            jogos.append(sorted(numeros))
        
        return {
            'estrategia': estrategia,
            'quantidade_numeros': quantidade_numeros,
            'quantidade_jogos': quantidade_jogos,
            'jogos': jogos
        }
    
    def _estrategia_equilibrada(self, quantidade: int) -> List[int]:
        """
        Estratégia equilibrada: mix de números frequentes e atrasados
        
        Args:
            quantidade: Quantidade de números a gerar
            
        Returns:
            Lista de números
        """
        frequencias = self.estatistica_service.calcular_frequencia_numeros()
        atrasos = self.estatistica_service.calcular_atrasos()
        
        if not frequencias or not atrasos:
            # Fallback: números aleatórios
            return random.sample(range(1, 81), quantidade)
        
        # Pega metade dos mais frequentes e metade dos mais atrasados
        metade = quantidade // 2
        outra_metade = quantidade - metade
        
        frequentes = [f['numero'] for f in frequencias[:20]]
        atrasados_list = [a['numero'] for a in atrasos[:20]]
        
        numeros = []
        numeros.extend(random.sample(frequentes, min(metade, len(frequentes))))
        
        # Pega atrasados que não estão nos frequentes
        atrasados_disponiveis = [n for n in atrasados_list if n not in numeros]
        numeros.extend(random.sample(
            atrasados_disponiveis,
            min(outra_metade, len(atrasados_disponiveis))
        ))
        
        # Completa se necessário
        while len(numeros) < quantidade:
            num = random.randint(1, 80)
            if num not in numeros:
                numeros.append(num)
        
        return numeros[:quantidade]
    
    def _estrategia_agressiva(self, quantidade: int) -> List[int]:
        """
        Estratégia agressiva: prioriza números mais frequentes
        
        Args:
            quantidade: Quantidade de números a gerar
            
        Returns:
            Lista de números
        """
        frequencias = self.estatistica_service.calcular_frequencia_numeros()
        
        if not frequencias:
            return random.sample(range(1, 81), quantidade)
        
        # Pega dos 30 mais frequentes
        top_frequentes = [f['numero'] for f in frequencias[:30]]
        return random.sample(top_frequentes, min(quantidade, len(top_frequentes)))
    
    def _estrategia_conservadora(self, quantidade: int) -> List[int]:
        """
        Estratégia conservadora: prioriza números mais atrasados
        
        Args:
            quantidade: Quantidade de números a gerar
            
        Returns:
            Lista de números
        """
        atrasos = self.estatistica_service.calcular_atrasos()
        
        if not atrasos:
            return random.sample(range(1, 81), quantidade)
        
        # Pega dos 30 mais atrasados
        top_atrasados = [a['numero'] for a in atrasos[:30]]
        return random.sample(top_atrasados, min(quantidade, len(top_atrasados)))
    
    def _estrategia_mista(self, quantidade: int) -> List[int]:
        """
        Estratégia mista: combina múltiplas estratégias
        
        Args:
            quantidade: Quantidade de números a gerar
            
        Returns:
            Lista de números
        """
        frequencias = self.estatistica_service.calcular_frequencia_numeros()
        atrasos = self.estatistica_service.calcular_atrasos()
        
        if not frequencias or not atrasos:
            return random.sample(range(1, 81), quantidade)
        
        # Divide em 3 grupos
        grupo1 = quantidade // 3
        grupo2 = quantidade // 3
        grupo3 = quantidade - grupo1 - grupo2
        
        frequentes = [f['numero'] for f in frequencias[:15]]
        atrasados_list = [a['numero'] for a in atrasos[:15]]
        medios = [f['numero'] for f in frequencias[15:45]]
        
        numeros = []
        numeros.extend(random.sample(frequentes, min(grupo1, len(frequentes))))
        
        atrasados_disponiveis = [n for n in atrasados_list if n not in numeros]
        numeros.extend(random.sample(
            atrasados_disponiveis,
            min(grupo2, len(atrasados_disponiveis))
        ))
        
        medios_disponiveis = [n for n in medios if n not in numeros]
        numeros.extend(random.sample(
            medios_disponiveis,
            min(grupo3, len(medios_disponiveis))
        ))
        
        # Completa se necessário
        while len(numeros) < quantidade:
            num = random.randint(1, 80)
            if num not in numeros:
                numeros.append(num)
        
        return numeros[:quantidade]
    
    def _estrategia_atrasados(self, quantidade: int) -> List[int]:
        """
        Estratégia focada em números com maior atraso
        
        Args:
            quantidade: Quantidade de números a gerar
            
        Returns:
            Lista de números
        """
        atrasos = self.estatistica_service.calcular_atrasos()
        
        if not atrasos:
            return random.sample(range(1, 81), quantidade)
        
        # Pega os mais atrasados
        mais_atrasados = [a['numero'] for a in atrasos[:quantidade]]
        return mais_atrasados
    
    def _estrategia_por_faixa(self, quantidade: int) -> List[int]:
        """
        Estratégia que distribui números por faixas de dezenas
        Faixas: 01-20, 21-40, 41-60, 61-80
        
        Args:
            quantidade: Quantidade de números a gerar
            
        Returns:
            Lista de números
        """
        # Distribui proporcionalmente entre as 4 faixas
        faixas = [
            list(range(1, 21)),    # 01-20
            list(range(21, 41)),   # 21-40
            list(range(41, 61)),   # 41-60
            list(range(61, 81))    # 61-80
        ]
        
        numeros = []
        por_faixa = quantidade // 4
        resto = quantidade % 4
        
        for idx, faixa in enumerate(faixas):
            qtd = por_faixa + (1 if idx < resto else 0)
            numeros.extend(random.sample(faixa, min(qtd, len(faixa))))
        
        # Se não conseguiu preencher, completa aleatoriamente
        while len(numeros) < quantidade:
            num = random.randint(1, 80)
            if num not in numeros:
                numeros.append(num)
        
        return numeros[:quantidade]
    
    def _estrategia_por_posicao(self, quantidade: int) -> List[int]:
        """
        Estratégia baseada na análise posicional do sorteio
        
        Args:
            quantidade: Quantidade de números a gerar
            
        Returns:
            Lista de números
        """
        posicoes = self.estatistica_service.calcular_por_posicao_sorteio()
        
        if not posicoes or len(posicoes) < 5:
            return random.sample(range(1, 81), quantidade)
        
        numeros = []
        
        # Para jogos de 5 números, pega 1 de cada posição
        if quantidade == 5:
            for i in range(1, 6):
                pos_key = f'posicao_{i}'
                if pos_key in posicoes and posicoes[pos_key]['top_numeros']:
                    top = posicoes[pos_key]['top_numeros']
                    # Escolhe aleatoriamente entre os top 5 desta posição
                    candidatos = [n['numero'] for n in top[:5]]
                    num = random.choice(candidatos)
                    if num not in numeros:
                        numeros.append(num)
        else:
            # Para outros tamanhos, distribui proporcionalmente
            por_posicao = quantidade // 5
            resto = quantidade % 5
            
            for i in range(1, 6):
                pos_key = f'posicao_{i}'
                if pos_key in posicoes and posicoes[pos_key]['top_numeros']:
                    qtd = por_posicao + (1 if i <= resto else 0)
                    top = posicoes[pos_key]['top_numeros']
                    candidatos = [n['numero'] for n in top[:10] if n['numero'] not in numeros]
                    
                    qtd_disponivel = min(qtd, len(candidatos))
                    numeros.extend(random.sample(candidatos, qtd_disponivel))
        
        # Completa se necessário
        while len(numeros) < quantidade:
            num = random.randint(1, 80)
            if num not in numeros:
                numeros.append(num)
        
        return numeros[:quantidade]
