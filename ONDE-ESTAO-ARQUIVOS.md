# 🗺️ Onde Estão os Arquivos - QUINA

Guia completo da estrutura de arquivos e responsabilidades de cada componente do sistema.

## 📁 Estrutura Completa

```
AnalisePorPosicao-Quina/
│
├── 📄 app.py                          # Aplicação Flask principal
├── ⚙️ config.py                       # Configurações e constantes
├── 📋 requirements.txt                # Dependências Python
├── 🔐 .env.example                    # Exemplo de variáveis de ambiente
├── 🚫 .gitignore                      # Arquivos ignorados pelo Git
├── 📖 README.md                       # Documentação principal
├── 🚀 QUICKSTART.md                   # Guia rápido de início
├── 📥 DOWNLOAD.md                     # Guia de download de dados
├── 🗺️ ONDE-ESTAO-ARQUIVOS.md         # Este arquivo
├── 💾 database.db                     # Banco de dados SQLite (criado automaticamente)
│
├── 📂 models/                         # Camada de Dados
│   ├── __init__.py
│   └── resultado_model.py             # Model para gerenciar resultados
│
├── 📂 services/                       # Camada de Serviços/Negócios
│   ├── __init__.py
│   ├── api_caixa_service.py           # Integração com API da Caixa
│   ├── estatistica_service.py         # Cálculos estatísticos
│   └── quina_service.py               # Lógica de geração de palpites
│
├── 📂 routes/                         # Camada de Rotas/Controle
│   ├── __init__.py
│   ├── main_routes.py                 # Rotas para páginas HTML
│   └── api_routes.py                  # Rotas da API REST
│
├── 📂 static/                         # Arquivos Estáticos
│   ├── 📂 css/
│   │   └── styles.css                 # Estilos CSS da aplicação
│   └── 📂 js/
│       └── scripts.js                 # JavaScript interativo
│
└── 📂 templates/                      # Templates HTML
    ├── base.html                      # Template base (header, footer, nav)
    ├── index.html                     # Página principal (estatísticas)
    └── palpites.html                  # Página de geração de palpites
```

## 📄 Descrição Detalhada dos Arquivos

### 🎯 Raiz do Projeto

#### `app.py`
**O que faz:** Ponto de entrada da aplicação Flask
- Inicializa o servidor Flask
- Registra os blueprints de rotas
- Configura a aplicação
- **Porta:** 5055 (diferente de outros sistemas)

**Responsabilidades:**
- ✅ Criar instância do Flask
- ✅ Registrar rotas principais e API
- ✅ Iniciar servidor na porta correta
- ✅ Exibir mensagens de boas-vindas

**Quando modificar:**
- Adicionar novos blueprints
- Configurar middlewares
- Alterar configurações do servidor

---

#### `config.py`
**O que faz:** Centraliza todas as configurações do sistema

**Contém:**
- ⚙️ Configurações do Flask (SECRET_KEY, DEBUG)
- 🌐 Configurações do servidor (HOST, PORT)
- 💾 Configurações do banco de dados
- 🔗 URL da API da Caixa
- 🎯 Constantes da QUINA (MIN_NUMEROS, MAX_NUMEROS, etc.)
- 🎨 Paleta de cores (#260184 e variações)
- 🖼️ URL da logo

**Quando modificar:**
- Alterar porta do servidor
- Modificar constantes da loteria
- Ajustar cores do sistema

---

#### `requirements.txt`
**O que faz:** Lista todas as dependências Python

**Pacotes:**
```
Flask==3.0.0        # Framework web
requests==2.31.0    # Cliente HTTP para API
python-dotenv==1.0.0 # Gerenciador de variáveis de ambiente
```

**Quando modificar:**
- Adicionar novas dependências
- Atualizar versões de pacotes

---

#### `.env.example`
**O que faz:** Template para configurações sensíveis

**Uso:**
```bash
cp .env.example .env
# Edite .env com suas configurações
```

**Quando modificar:**
- Adicionar novas variáveis de ambiente

---

#### `.gitignore`
**O que faz:** Define arquivos que o Git deve ignorar

**Ignora:**
- `__pycache__/` - Cache do Python
- `*.pyc` - Bytecode Python
- `.env` - Variáveis de ambiente sensíveis
- `database.db` - Banco de dados local
- `*.log` - Arquivos de log

---

### 📂 models/ - Camada de Dados

#### `resultado_model.py`
**O que faz:** Gerencia a persistência de dados no SQLite

**Responsabilidades:**
- 💾 Criar tabela de resultados
- ➕ Inserir/atualizar resultados
- 🔍 Buscar resultados (último, todos, por número)
- 🔄 Converter dados entre JSON e SQLite

**Métodos principais:**
- `__init__()` - Inicializa e cria tabela
- `inserir(resultado)` - Insere/atualiza um resultado
- `buscar_ultimo()` - Retorna último concurso
- `buscar_todos(limite)` - Lista todos os resultados
- `buscar_por_numero(numero)` - Busca concurso específico

**Schema do banco:**
23 campos incluindo:
- numero (PRIMARY KEY)
- listaDezenas (JSON)
- dezenasSorteadasOrdemSorteio (JSON)
- dataApuracao
- acumulado
- E mais...

**Quando modificar:**
- Adicionar novos campos
- Criar novos índices
- Adicionar novos métodos de busca

---

### 📂 services/ - Camada de Negócios

#### `api_caixa_service.py`
**O que faz:** Integração com a API oficial da Caixa

**Responsabilidades:**
- 🌐 Fazer requisições HTTP para a API
- 📥 Baixar concursos (último, específico, completo)
- ✅ Validar respostas da API
- 🔄 Atualização incremental de dados

**Métodos principais:**
- `buscar_ultimo_concurso()` - GET /quina
- `buscar_concurso_especifico(numero)` - GET /quina/{numero}
- `atualizar_base_completa()` - Atualiza base incremental

**URL da API:**
```
https://servicebus2.caixa.gov.br/portaldeloterias/api/quina
```

**Quando modificar:**
- Adicionar tratamento de novos campos da API
- Melhorar tratamento de erros
- Otimizar velocidade de download

---

#### `estatistica_service.py`
**O que faz:** Calcula todas as estatísticas dos resultados

**Responsabilidades:**
- 📊 Calcular frequência de números
- ⏰ Calcular atrasos
- ⚖️ Distribuição pares/ímpares
- 📍 Análise por posição de sorteio
- 📊 Análise por faixa de dezenas
- 🔢 Análise por dígito final

**Métodos principais:**
- `calcular_estatisticas_completas()` - Todas as estatísticas
- `calcular_frequencia_numeros()` - Top números frequentes
- `calcular_atrasos()` - Números atrasados
- `calcular_por_posicao_sorteio()` - **Análise diferencial**
- `calcular_pares_impares()` - Distribuição par/ímpar
- `calcular_por_faixa()` - Análise por faixas
- `calcular_por_digito()` - Frequência por dígito

**Destaque - Análise Posicional:**
```python
# Retorna quais números aparecem mais em cada posição (1ª a 5ª)
posicoes = {
    'posicao_1': {'top_numeros': [...]},
    'posicao_2': {'top_numeros': [...]},
    ...
}
```

**Quando modificar:**
- Adicionar novas estatísticas
- Otimizar cálculos
- Adicionar cache

---

#### `quina_service.py`
**O que faz:** Gera palpites usando diferentes estratégias

**Responsabilidades:**
- 🎲 Gerar palpites inteligentes
- 🎯 Implementar múltiplas estratégias
- ✅ Validar parâmetros de entrada

**Estratégias implementadas:**

1. **Equilibrada** (`_estrategia_equilibrada`)
   - Mix 50/50 de frequentes e atrasados

2. **Agressiva** (`_estrategia_agressiva`)
   - Prioriza top 30 mais frequentes

3. **Conservadora** (`_estrategia_conservadora`)
   - Prioriza top 30 mais atrasados

4. **Mista** (`_estrategia_mista`)
   - Divide em 3 grupos: frequentes, atrasados, médios

5. **Atrasados** (`_estrategia_atrasados`)
   - Foca exclusivamente nos mais atrasados

6. **Por Faixa** (`_estrategia_por_faixa`)
   - Distribui entre faixas (01-20, 21-40, 41-60, 61-80)

7. **Por Posição** (`_estrategia_por_posicao`)
   - Usa análise posicional do sorteio

**Quando modificar:**
- Adicionar novas estratégias
- Melhorar algoritmos existentes
- Ajustar pesos e proporções

---

### 📂 routes/ - Camada de Controle

#### `main_routes.py`
**O que faz:** Rotas para páginas HTML

**Rotas:**
- `GET /` → `index.html` (Estatísticas)
- `GET /palpites` → `palpites.html` (Gerar palpites)

**Quando modificar:**
- Adicionar novas páginas
- Passar dados para templates

---

#### `api_routes.py`
**O que faz:** API REST para acesso programático

**Endpoints:**

| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/api/atualizar` | Atualiza base de dados |
| GET | `/api/ultimo-resultado` | Último resultado |
| GET | `/api/resultados?limite=N` | Lista resultados |
| GET | `/api/resultado/<numero>` | Busca concurso específico |
| GET | `/api/estatisticas` | Todas estatísticas |
| POST | `/api/gerar-palpite` | Gera palpites |
| POST | `/api/conferir` | Confere palpite |

**Quando modificar:**
- Adicionar novos endpoints
- Melhorar validações
- Adicionar rate limiting

---

### 📂 static/ - Arquivos Estáticos

#### `static/css/styles.css`
**O que faz:** Todos os estilos visuais do sistema

**Inclui:**
- 🎨 Variáveis CSS com cores da QUINA
- 📱 Design responsivo
- 🎭 Animações (pulse, spin)
- 🃏 Estilos de cards e números
- 📊 Estilos de tabelas e gráficos

**Cores principais:**
```css
--cor-principal: #260184;      /* Roxo QUINA */
--cor-principal-hover: #3302b1;
--cor-clara: #ede6ff;
--cor-media: #9268fd;
```

**Quando modificar:**
- Ajustar cores e espaçamentos
- Adicionar novos componentes
- Melhorar responsividade

---

#### `static/js/scripts.js`
**O que faz:** Interatividade e integração com a API

**Funções principais:**

| Função | Responsabilidade |
|--------|------------------|
| `carregarUltimoResultado()` | Busca e exibe último concurso |
| `carregarEstatisticas()` | Carrega todas estatísticas |
| `atualizarDados()` | Chama API de atualização |
| `gerarPalpites()` | Gera palpites via API |
| `conferirPalpite()` | Confere jogo com resultado |
| `renderizar*()` | Funções para renderizar dados |

**Quando modificar:**
- Adicionar novas interações
- Melhorar visualizações
- Adicionar validações client-side

---

### 📂 templates/ - Templates HTML

#### `base.html`
**O que faz:** Template base herdado por todas as páginas

**Inclui:**
- 🎯 Header com logo QUINA
- 📝 Navegação principal
- 👣 Footer
- 🔗 Links para CSS e JS

**Blocos Jinja2:**
- `{% block title %}` - Título da página
- `{% block content %}` - Conteúdo principal
- `{% block scripts %}` - Scripts adicionais

---

#### `index.html`
**O que faz:** Página principal com estatísticas

**Seções:**
1. 🎯 Último Concurso
2. 📊 Estatísticas Gerais
3. 🔥 Números Mais Frequentes
4. ⏰ Números Mais Atrasados
5. 📍 Análise por Posição
6. 📊 Análise por Faixa
7. ⚖️ Distribuição Pares/Ímpares
8. 🔢 Análise por Dígito

---

#### `palpites.html`
**O que faz:** Página de geração e conferência de palpites

**Seções:**
1. 🎲 Gerador de Palpites
   - Formulário com estratégias
   - Exibição de jogos gerados
2. 🔍 Conferir Palpite
   - Input de números
   - Resultado da conferência
3. ℹ️ Informações sobre Estratégias

---

## 🔄 Fluxo de Dados

### 1. Atualização de Dados
```
API Caixa → api_caixa_service → resultado_model → database.db
```

### 2. Exibição de Estatísticas
```
database.db → resultado_model → estatistica_service → API REST → Frontend
```

### 3. Geração de Palpites
```
Frontend → API REST → quina_service → estatistica_service → resultado_model → database.db
```

## 🎯 Arquivos por Funcionalidade

### 📥 Download de Dados
- `services/api_caixa_service.py`
- `models/resultado_model.py`
- `routes/api_routes.py` (endpoint /atualizar)

### 📊 Estatísticas
- `services/estatistica_service.py`
- `routes/api_routes.py` (endpoint /estatisticas)
- `templates/index.html`
- `static/js/scripts.js` (funções renderizar*)

### 🎲 Palpites
- `services/quina_service.py`
- `routes/api_routes.py` (endpoint /gerar-palpite)
- `templates/palpites.html`
- `static/js/scripts.js` (gerarPalpites)

### 🎨 Interface Visual
- `static/css/styles.css`
- `templates/base.html`
- `templates/*.html`
- `static/js/scripts.js`

## 📝 Convenções de Código

### Python
- **PEP 8**: Seguir guia de estilo Python
- **Docstrings**: Todas as funções documentadas
- **Type hints**: Usar quando apropriado
- **Nomes**: snake_case para funções e variáveis

### JavaScript
- **ES6+**: Usar recursos modernos
- **Async/Await**: Para chamadas de API
- **Funções**: Nomes descritivos em camelCase
- **Comentários**: Explicar lógica complexa

### HTML/CSS
- **Semântico**: Usar tags HTML apropriadas
- **BEM**: Nomenclatura de classes (opcional)
- **Responsivo**: Mobile-first
- **Acessibilidade**: Alt text, ARIA labels

## 🚀 Próximos Passos

Após entender a estrutura:

1. ✅ Leia o [README Principal](README.md)
2. 🚀 Siga o [QUICKSTART](QUICKSTART.md)
3. 📥 Configure o [DOWNLOAD](DOWNLOAD.md)
4. 💻 Explore o código fonte

---

**Estrutura clara, código organizado! 🗺️**
