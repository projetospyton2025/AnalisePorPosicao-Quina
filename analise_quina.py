#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Análise de resultados da Quina por posição

Este script analisa os resultados históricos da loteria Quina,
focando na distribuição de números em cada posição do sorteio.
"""

from collections import Counter
from typing import List, Dict


class AnalisadorQuina:
    """Classe para análise de resultados da Quina por posição."""
    
    def __init__(self):
        """Inicializa o analisador."""
        self.resultados = []
        
    def adicionar_resultado(self, numeros: List[int]):
        """
        Adiciona um resultado de sorteio.
        
        Args:
            numeros: Lista com 5 números sorteados (ordenados)
        """
        if len(numeros) != 5:
            raise ValueError("Quina tem exatamente 5 números")
        
        if not all(1 <= n <= 80 for n in numeros):
            raise ValueError("Números devem estar entre 1 e 80")
        
        self.resultados.append(sorted(numeros))
    
    def analisar_por_posicao(self) -> Dict[int, Counter]:
        """
        Analisa a frequência de números em cada posição.
        
        Returns:
            Dicionário com a contagem de números por posição (0-4)
        """
        analise = {i: Counter() for i in range(5)}
        
        for resultado in self.resultados:
            for posicao, numero in enumerate(resultado):
                analise[posicao][numero] += 1
        
        return analise
    
    def numeros_mais_frequentes(self, posicao: int, top: int = 10) -> List[tuple]:
        """
        Retorna os números mais frequentes em uma posição.
        
        Args:
            posicao: Posição a analisar (0-4)
            top: Quantidade de números a retornar
            
        Returns:
            Lista de tuplas (numero, frequencia)
        """
        if not 0 <= posicao < 5:
            raise ValueError("Posição deve estar entre 0 e 4")
        
        analise = self.analisar_por_posicao()
        return analise[posicao].most_common(top)
    
    def estatisticas_resumo(self) -> Dict:
        """
        Gera estatísticas resumidas dos resultados.
        
        Returns:
            Dicionário com estatísticas gerais
        """
        if not self.resultados:
            return {"total_sorteios": 0}
        
        todos_numeros = [n for resultado in self.resultados for n in resultado]
        
        return {
            "total_sorteios": len(self.resultados),
            "numeros_unicos": len(set(todos_numeros)),
            "numero_mais_comum": Counter(todos_numeros).most_common(1)[0] if todos_numeros else None,
            "numero_menos_comum": Counter(todos_numeros).most_common()[-1] if todos_numeros else None,
        }


def exemplo_uso():
    """Demonstra o uso básico do analisador."""
    print("=" * 60)
    print("AnalisePorPosicao-Quina")
    print("=" * 60)
    print()
    print("✅ SIM, POSSO TRABALHAR POR AQUI!")
    print()
    print("Este é um exemplo de uso do analisador de Quina.")
    print("-" * 60)
    
    # Cria analisador
    analisador = AnalisadorQuina()
    
    # Adiciona alguns resultados de exemplo
    resultados_exemplo = [
        [5, 12, 23, 45, 67],
        [3, 15, 28, 44, 70],
        [7, 18, 23, 50, 75],
        [2, 12, 30, 45, 68],
        [8, 20, 25, 48, 72],
    ]
    
    for resultado in resultados_exemplo:
        analisador.adicionar_resultado(resultado)
    
    # Mostra estatísticas
    print(f"\nTotal de sorteios analisados: {len(analisador.resultados)}")
    print("\nNúmeros mais frequentes por posição:")
    
    for posicao in range(5):
        print(f"\n{posicao + 1}ª Posição:")
        frequentes = analisador.numeros_mais_frequentes(posicao, top=3)
        for numero, freq in frequentes:
            print(f"  Número {numero:2d}: {freq} vez(es)")
    
    print("\n" + "=" * 60)
    print("Projeto configurado e funcionando!")
    print("=" * 60)


if __name__ == "__main__":
    exemplo_uso()
