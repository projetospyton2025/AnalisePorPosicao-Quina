# Sistema de Análise por Posição - QUINA

![Logo QUINA](https://i.postimg.cc/G3PvK6cN/quina.png)

Sistema completo de análise estatística e geração de palpites para a loteria **QUINA** da Caixa Econômica Federal, com foco especial em análise por posição de sorteio.

## 🎯 Características da QUINA

- **Números disponíveis**: 01 a 80
- **Números sorteados por concurso**: 5 números
- **Jogo mínimo**: 5 números
- **Jogo máximo**: 15 números
- **Cor principal**: #260184 (roxo/violeta)

## 🚀 Funcionalidades

### 📊 Análises Estatísticas

- **Último Resultado**: Visualização do último concurso realizado
- **Frequência de Números**: Top 20 números mais sorteados historicamente
- **Números Atrasados**: Top 20 números com maior atraso
- **Análise por Posição**: Estatísticas de cada número por posição de sorteio (1ª a 5ª)
- **Análise por Faixa**: Distribuição por faixas de dezenas (01-20, 21-40, 41-60, 61-80)
- **Pares e Ímpares**: Distribuição entre números pares e ímpares
- **Análise por Dígito**: Frequência de cada dígito final (0-9)

### 🎲 Geração de Palpites

Estratégias disponíveis:

1. **Equilibrada**: Mix balanceado de números frequentes e atrasados
2. **Agressiva**: Prioriza números mais frequentes
3. **Conservadora**: Prioriza números mais atrasados
4. **Mista**: Combina múltiplas estratégias
5. **Atrasados**: Foca exclusivamente em números com maior atraso
6. **Por Faixa**: Distribui números proporcionalmente entre as faixas
7. **Por Posição**: Usa análise de frequência por posição de sorteio

### ✅ Conferência de Jogos

- Confira seus palpites com resultados de concursos específicos
- Visualização clara de acertos

## 🛠️ Tecnologias Utilizadas

- **Backend**: Python 3.x, Flask 3.0.0
- **Banco de Dados**: SQLite
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **API**: API oficial da Caixa Econômica Federal

## 📦 Instalação

### Pré-requisitos

- Python 3.7 ou superior
- pip (gerenciador de pacotes Python)

### Passo a Passo

1. Clone o repositório:
```bash
git clone https://github.com/projetospyton2025/AnalisePorPosicao-Quina.git
cd AnalisePorPosicao-Quina
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. (Opcional) Configure variáveis de ambiente:
```bash
cp .env.example .env
# Edite o arquivo .env conforme necessário
```

4. Inicie o servidor:
```bash
python app.py
```

5. Acesse o sistema no navegador:
```
http://localhost:5055
```

## 📖 Como Usar

### 1. Atualizar Base de Dados

Ao abrir o sistema pela primeira vez, clique em **"Atualizar Dados"** na página principal para baixar os resultados históricos da API da Caixa.

### 2. Visualizar Estatísticas

A página principal (`/`) exibe todas as estatísticas calculadas automaticamente a partir dos dados históricos.

### 3. Gerar Palpites

1. Acesse a página **"Gerar Palpites"** (`/palpites`)
2. Selecione a estratégia desejada
3. Escolha a quantidade de números (5-15)
4. Defina quantos jogos gerar (1-100)
5. Clique em **"Gerar Palpites"**

### 4. Conferir Resultados

1. Na página de palpites, role até **"Conferir Palpite"**
2. Digite seus números separados por vírgula
3. Informe o número do concurso
4. Clique em **"Conferir"**

## 🌐 API REST

### Endpoints Disponíveis

#### POST /api/atualizar
Atualiza a base de dados com novos concursos da API da Caixa.

**Resposta:**
```json
{
  "total_processados": 100,
  "total_inseridos": 100,
  "total_erros": 0,
  "ultimo_concurso": 6792,
  "mensagem": "Atualização concluída com sucesso"
}
```

#### GET /api/ultimo-resultado
Retorna o último resultado cadastrado.

**Resposta:**
```json
{
  "numero": 6792,
  "dataApuracao": "05/08/2025",
  "listaDezenas": ["16", "42", "43", "62", "68"],
  "acumulado": true,
  ...
}
```

#### GET /api/resultados?limite=N
Lista resultados com limite opcional.

#### GET /api/resultado/{numero}
Busca um resultado específico por número do concurso.

#### GET /api/estatisticas
Retorna todas as estatísticas calculadas.

**Resposta:**
```json
{
  "total_concursos": 6792,
  "frequencia_numeros": [...],
  "atrasos": [...],
  "pares_impares": {...},
  "por_faixa": [...],
  "por_digito": [...],
  "por_posicao_sorteio": {...}
}
```

#### POST /api/gerar-palpite
Gera palpites usando a estratégia especificada.

**Body:**
```json
{
  "estrategia": "equilibrada",
  "quantidade_numeros": 5,
  "quantidade_jogos": 3
}
```

**Resposta:**
```json
{
  "estrategia": "equilibrada",
  "quantidade_numeros": 5,
  "quantidade_jogos": 3,
  "jogos": [
    [5, 12, 23, 45, 67],
    [8, 15, 28, 39, 71],
    [3, 19, 33, 52, 78]
  ]
}
```

#### POST /api/conferir
Confere um palpite com um resultado.

**Body:**
```json
{
  "numeros": [5, 12, 23, 45, 67],
  "numero_concurso": 6792
}
```

**Resposta:**
```json
{
  "numero_concurso": 6792,
  "numeros_jogo": [5, 12, 23, 45, 67],
  "numeros_sorteados": [16, 42, 43, 62, 68],
  "acertos": [12, 45],
  "quantidade_acertos": 2
}
```

## 📂 Estrutura do Projeto

```
AnalisePorPosicao-Quina/
├── app.py                      # Aplicação Flask principal
├── config.py                   # Configurações e constantes
├── requirements.txt            # Dependências Python
├── .env.example               # Exemplo de variáveis de ambiente
├── .gitignore                 # Arquivos ignorados pelo Git
├── README.md                  # Este arquivo
├── QUICKSTART.md              # Guia rápido de início
├── DOWNLOAD.md                # Guia de download de dados
├── ONDE-ESTAO-ARQUIVOS.md     # Mapa de arquivos do projeto
├── database.db                # Banco de dados SQLite (criado automaticamente)
├── models/
│   ├── __init__.py
│   └── resultado_model.py     # Model para resultados
├── services/
│   ├── __init__.py
│   ├── api_caixa_service.py   # Integração com API da Caixa
│   ├── estatistica_service.py # Cálculos estatísticos
│   └── quina_service.py       # Lógica de palpites
├── routes/
│   ├── __init__.py
│   ├── main_routes.py         # Rotas de páginas HTML
│   └── api_routes.py          # Rotas da API REST
├── static/
│   ├── css/
│   │   └── styles.css         # Estilos CSS
│   └── js/
│       └── scripts.js         # JavaScript interativo
└── templates/
    ├── base.html              # Template base
    ├── index.html             # Página principal
    └── palpites.html          # Página de palpites
```

## 🎨 Identidade Visual

O sistema utiliza a paleta de cores oficial da QUINA, com destaque para o roxo/violeta:

- **Cor Principal**: #260184
- **Gradientes**: Do roxo mais claro (#ede6ff) ao mais escuro (#070019)
- **Logo**: Integrada em todas as páginas

## ⚠️ Avisos Importantes

1. **Dados Reais**: O sistema busca dados reais da API oficial da Caixa Econômica Federal
2. **Apenas para Fins Educacionais**: Este sistema é para fins de estudo e análise estatística
3. **Não Garante Resultados**: Nenhuma estratégia garante ganhos em jogos de loteria
4. **Jogo Responsável**: Jogue com responsabilidade

## 📝 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👥 Autores

- **projetospython2025** - Desenvolvimento inicial

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests.

## 📞 Suporte

Para suporte, abra uma issue no GitHub ou entre em contato através do repositório.

## 🔗 Links Úteis

- [API da Caixa](https://servicebus2.caixa.gov.br/portaldeloterias/api/quina)
- [Sistema Mega-Sena](https://github.com/projetospyton2025/AnalisePorPosicao-MegaSena)
- [Sistema Lotofácil](https://github.com/projetospyton2025/AnalisePorPosicao-Lotofacil)

---

**Desenvolvido com ❤️ para entusiastas da QUINA**
