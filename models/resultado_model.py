"""
Model para gerenciar os resultados da QUINA no banco de dados SQLite
"""
import sqlite3
import json
from typing import Dict, List, Optional
import config


class ResultadoModel:
    """
    Classe para gerenciar os resultados da QUINA no banco de dados
    """
    
    def __init__(self, db_path: str = None):
        """
        Inicializa o model com o caminho do banco de dados
        
        Args:
            db_path: Caminho do banco de dados SQLite
        """
        self.db_path = db_path or config.DATABASE_PATH
        self._criar_tabela()
    
    def _criar_tabela(self):
        """
        Cria a tabela de resultados se não existir
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS resultados (
                    numero INTEGER PRIMARY KEY,
                    acumulado BOOLEAN,
                    dataApuracao TEXT,
                    dataProximoConcurso TEXT,
                    dezenasSorteadasOrdemSorteio TEXT,
                    exibirDetalhamentoPorCidade BOOLEAN,
                    indicadorConcursoEspecial INTEGER,
                    listaDezenas TEXT,
                    listaDezenasSegundoSorteio TEXT,
                    listaMunicipioUFGanhadores TEXT,
                    listaRateioPremio TEXT,
                    localSorteio TEXT,
                    nomeMunicipioUFSorteio TEXT,
                    numeroConcursoAnterior INTEGER,
                    numeroConcursoFinal_0_5 INTEGER,
                    numeroConcursoProximo INTEGER,
                    numeroJogo INTEGER,
                    tipoJogo TEXT,
                    valorArrecadado REAL,
                    valorAcumuladoConcurso_0_5 REAL,
                    valorAcumuladoConcursoEspecial REAL,
                    valorAcumuladoProximoConcurso REAL,
                    valorEstimadoProximoConcurso REAL
                )
            """)
            conn.commit()
    
    def inserir(self, resultado: Dict) -> bool:
        """
        Insere ou atualiza um resultado no banco de dados
        
        Args:
            resultado: Dicionário com os dados do resultado da API
            
        Returns:
            True se inseriu/atualizou com sucesso, False caso contrário
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Converte listas e dicts para JSON
                dezenas_ordem = json.dumps(resultado.get('dezenasSorteadasOrdemSorteio', []))
                lista_dezenas = json.dumps(resultado.get('listaDezenas', []))
                lista_dezenas_segundo = json.dumps(resultado.get('listaDezenasSegundoSorteio'))
                lista_municipios = json.dumps(resultado.get('listaMunicipioUFGanhadores', []))
                lista_rateio = json.dumps(resultado.get('listaRateioPremio', []))
                
                cursor.execute("""
                    INSERT OR REPLACE INTO resultados (
                        numero, acumulado, dataApuracao, dataProximoConcurso,
                        dezenasSorteadasOrdemSorteio, exibirDetalhamentoPorCidade,
                        indicadorConcursoEspecial, listaDezenas, listaDezenasSegundoSorteio,
                        listaMunicipioUFGanhadores, listaRateioPremio, localSorteio,
                        nomeMunicipioUFSorteio, numeroConcursoAnterior, numeroConcursoFinal_0_5,
                        numeroConcursoProximo, numeroJogo, tipoJogo, valorArrecadado,
                        valorAcumuladoConcurso_0_5, valorAcumuladoConcursoEspecial,
                        valorAcumuladoProximoConcurso, valorEstimadoProximoConcurso
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    resultado.get('numero'),
                    resultado.get('acumulado'),
                    resultado.get('dataApuracao'),
                    resultado.get('dataProximoConcurso'),
                    dezenas_ordem,
                    resultado.get('exibirDetalhamentoPorCidade'),
                    resultado.get('indicadorConcursoEspecial'),
                    lista_dezenas,
                    lista_dezenas_segundo,
                    lista_municipios,
                    lista_rateio,
                    resultado.get('localSorteio'),
                    resultado.get('nomeMunicipioUFSorteio'),
                    resultado.get('numeroConcursoAnterior'),
                    resultado.get('numeroConcursoFinal_0_5'),
                    resultado.get('numeroConcursoProximo'),
                    resultado.get('numeroJogo'),
                    resultado.get('tipoJogo'),
                    resultado.get('valorArrecadado'),
                    resultado.get('valorAcumuladoConcurso_0_5'),
                    resultado.get('valorAcumuladoConcursoEspecial'),
                    resultado.get('valorAcumuladoProximoConcurso'),
                    resultado.get('valorEstimadoProximoConcurso')
                ))
                conn.commit()
                return True
        except Exception as e:
            print(f"Erro ao inserir resultado: {e}")
            return False
    
    def buscar_ultimo(self) -> Optional[Dict]:
        """
        Busca o último resultado cadastrado
        
        Returns:
            Dicionário com o último resultado ou None se não houver resultados
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM resultados ORDER BY numero DESC LIMIT 1")
                row = cursor.fetchone()
                
                if row:
                    return self._row_to_dict(row)
                return None
        except Exception as e:
            print(f"Erro ao buscar último resultado: {e}")
            return None
    
    def buscar_todos(self, limite: Optional[int] = None) -> List[Dict]:
        """
        Busca todos os resultados, opcionalmente limitando a quantidade
        
        Args:
            limite: Número máximo de resultados a retornar
            
        Returns:
            Lista de dicionários com os resultados
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                if limite:
                    cursor.execute(
                        "SELECT * FROM resultados ORDER BY numero DESC LIMIT ?",
                        (limite,)
                    )
                else:
                    cursor.execute("SELECT * FROM resultados ORDER BY numero DESC")
                
                rows = cursor.fetchall()
                return [self._row_to_dict(row) for row in rows]
        except Exception as e:
            print(f"Erro ao buscar todos os resultados: {e}")
            return []
    
    def buscar_por_numero(self, numero: int) -> Optional[Dict]:
        """
        Busca um resultado específico por número do concurso
        
        Args:
            numero: Número do concurso
            
        Returns:
            Dicionário com o resultado ou None se não encontrado
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM resultados WHERE numero = ?", (numero,))
                row = cursor.fetchone()
                
                if row:
                    return self._row_to_dict(row)
                return None
        except Exception as e:
            print(f"Erro ao buscar resultado por número: {e}")
            return None
    
    def _row_to_dict(self, row: sqlite3.Row) -> Dict:
        """
        Converte uma linha do banco de dados para dicionário
        
        Args:
            row: Linha do banco de dados
            
        Returns:
            Dicionário com os dados do resultado
        """
        resultado = dict(row)
        
        # Converte campos JSON de volta para listas/dicts
        if resultado.get('dezenasSorteadasOrdemSorteio'):
            resultado['dezenasSorteadasOrdemSorteio'] = json.loads(
                resultado['dezenasSorteadasOrdemSorteio']
            )
        
        if resultado.get('listaDezenas'):
            resultado['listaDezenas'] = json.loads(resultado['listaDezenas'])
        
        if resultado.get('listaDezenasSegundoSorteio'):
            resultado['listaDezenasSegundoSorteio'] = json.loads(
                resultado['listaDezenasSegundoSorteio']
            )
        
        if resultado.get('listaMunicipioUFGanhadores'):
            resultado['listaMunicipioUFGanhadores'] = json.loads(
                resultado['listaMunicipioUFGanhadores']
            )
        
        if resultado.get('listaRateioPremio'):
            resultado['listaRateioPremio'] = json.loads(resultado['listaRateioPremio'])
        
        return resultado
