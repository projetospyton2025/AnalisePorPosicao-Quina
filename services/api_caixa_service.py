"""
Serviço para integração com a API da Caixa Econômica Federal - QUINA
"""
import requests
from typing import Optional, Dict
import config
from models.resultado_model import ResultadoModel


class ApiCaixaService:
    """
    Serviço para buscar dados da API da QUINA
    """
    
    def __init__(self):
        """
        Inicializa o serviço com a URL da API
        """
        self.api_url = config.API_QUINA_URL
        self.resultado_model = ResultadoModel()
    
    def buscar_ultimo_concurso(self) -> Optional[Dict]:
        """
        Busca o último concurso da QUINA na API da Caixa
        
        Returns:
            Dicionário com os dados do último concurso ou None em caso de erro
        """
        try:
            response = requests.get(self.api_url, timeout=10)
            response.raise_for_status()
            
            resultado = response.json()
            
            # Valida se tem os campos essenciais
            if 'numero' in resultado and 'listaDezenas' in resultado:
                return resultado
            
            print("Resposta da API não contém campos essenciais")
            return None
            
        except requests.exceptions.RequestException as e:
            print(f"Erro ao buscar último concurso: {e}")
            return None
        except ValueError as e:
            print(f"Erro ao processar JSON da API: {e}")
            return None
    
    def buscar_concurso_especifico(self, numero: int) -> Optional[Dict]:
        """
        Busca um concurso específico da QUINA na API da Caixa
        
        Args:
            numero: Número do concurso a buscar
            
        Returns:
            Dicionário com os dados do concurso ou None em caso de erro
        """
        try:
            url = f"{self.api_url}/{numero}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            resultado = response.json()
            
            # Valida se tem os campos essenciais
            if 'numero' in resultado and 'listaDezenas' in resultado:
                return resultado
            
            print(f"Resposta da API para concurso {numero} não contém campos essenciais")
            return None
            
        except requests.exceptions.RequestException as e:
            print(f"Erro ao buscar concurso {numero}: {e}")
            return None
        except ValueError as e:
            print(f"Erro ao processar JSON da API para concurso {numero}: {e}")
            return None
    
    def atualizar_base_completa(self, atualizar_apenas_novos: bool = True) -> Dict:
        """
        Atualiza a base de dados com concursos da API
        
        Args:
            atualizar_apenas_novos: Se True, busca apenas concursos novos.
                                   Se False, atualiza desde o concurso 1.
        
        Returns:
            Dicionário com estatísticas da atualização:
            - total_processados: Total de concursos processados
            - total_inseridos: Total de concursos inseridos/atualizados
            - total_erros: Total de erros encontrados
            - ultimo_concurso: Número do último concurso processado
        """
        total_processados = 0
        total_inseridos = 0
        total_erros = 0
        
        # Busca o último concurso da API
        ultimo_api = self.buscar_ultimo_concurso()
        if not ultimo_api:
            return {
                'total_processados': 0,
                'total_inseridos': 0,
                'total_erros': 1,
                'ultimo_concurso': None,
                'mensagem': 'Erro ao buscar último concurso da API'
            }
        
        numero_ultimo_api = ultimo_api['numero']
        
        # Define o ponto de início
        if atualizar_apenas_novos:
            ultimo_db = self.resultado_model.buscar_ultimo()
            numero_inicio = ultimo_db['numero'] + 1 if ultimo_db else 1
        else:
            numero_inicio = 1
        
        # Se já está atualizado
        if numero_inicio > numero_ultimo_api:
            return {
                'total_processados': 0,
                'total_inseridos': 0,
                'total_erros': 0,
                'ultimo_concurso': numero_ultimo_api,
                'mensagem': 'Base de dados já está atualizada'
            }
        
        # Atualiza concursos
        print(f"Atualizando concursos de {numero_inicio} até {numero_ultimo_api}...")
        
        for numero in range(numero_inicio, numero_ultimo_api + 1):
            total_processados += 1
            
            # Busca o concurso na API
            resultado = self.buscar_concurso_especifico(numero)
            
            if resultado:
                # Insere no banco de dados
                if self.resultado_model.inserir(resultado):
                    total_inseridos += 1
                    if total_inseridos % 100 == 0:
                        print(f"Processados {total_inseridos} concursos...")
                else:
                    total_erros += 1
            else:
                total_erros += 1
        
        return {
            'total_processados': total_processados,
            'total_inseridos': total_inseridos,
            'total_erros': total_erros,
            'ultimo_concurso': numero_ultimo_api,
            'mensagem': f'Atualização concluída com sucesso'
        }
