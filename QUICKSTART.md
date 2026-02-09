# 🚀 Guia Rápido - Sistema QUINA

Comece a usar o Sistema de Análise da QUINA em minutos!

## ⚡ Instalação Rápida

### 1. Clone o Repositório
```bash
git clone https://github.com/projetospyton2025/AnalisePorPosicao-Quina.git
cd AnalisePorPosicao-Quina
```

### 2. Instale as Dependências
```bash
pip install -r requirements.txt
```

### 3. Inicie o Servidor
```bash
python app.py
```

Você verá:
```
🎯 Sistema de Análise QUINA
🌐 Servidor rodando em http://0.0.0.0:5055
📊 Acesse o painel de estatísticas em: http://localhost:5055/
🎲 Acesse o gerador de palpites em: http://localhost:5055/palpites
```

## 🎯 Primeiros Passos

### 1. Atualizar Base de Dados

**Via Interface Web:**
1. Acesse http://localhost:5055
2. Clique no botão **"Atualizar Dados"**
3. Aguarde o download dos concursos históricos

**Via API (curl):**
```bash
curl -X POST http://localhost:5055/api/atualizar
```

**Via API (Python):**
```python
import requests
response = requests.post('http://localhost:5055/api/atualizar')
print(response.json())
```

### 2. Visualizar Estatísticas

Acesse: http://localhost:5055

Você verá:
- ✅ Último resultado
- 📊 Estatísticas gerais
- 🔥 Números mais frequentes
- ⏰ Números mais atrasados
- 📍 Análise por posição
- E muito mais!

### 3. Gerar Palpites

**Via Interface Web:**
1. Acesse http://localhost:5055/palpites
2. Escolha a estratégia
3. Defina quantidade de números (5-15)
4. Defina quantidade de jogos (1-100)
5. Clique em **"Gerar Palpites"**

**Via API:**
```bash
curl -X POST http://localhost:5055/api/gerar-palpite \
  -H "Content-Type: application/json" \
  -d '{
    "estrategia": "equilibrada",
    "quantidade_numeros": 5,
    "quantidade_jogos": 3
  }'
```

## 🎲 Estratégias Disponíveis

| Estratégia | Descrição |
|------------|-----------|
| `equilibrada` | Mix de frequentes e atrasados (Recomendada) |
| `agressiva` | Prioriza números frequentes |
| `conservadora` | Prioriza números atrasados |
| `mista` | Combina múltiplas estratégias |
| `atrasados` | Foco em números com maior atraso |
| `por_faixa` | Distribui por faixas de dezenas |
| `por_posicao` | Usa análise posicional |

## 📋 Comandos Úteis

### Buscar Último Resultado
```bash
curl http://localhost:5055/api/ultimo-resultado
```

### Listar Últimos 10 Resultados
```bash
curl http://localhost:5055/api/resultados?limite=10
```

### Buscar Concurso Específico
```bash
curl http://localhost:5055/api/resultado/6792
```

### Obter Todas as Estatísticas
```bash
curl http://localhost:5055/api/estatisticas
```

### Conferir Palpite
```bash
curl -X POST http://localhost:5055/api/conferir \
  -H "Content-Type: application/json" \
  -d '{
    "numeros": [5, 12, 23, 45, 67],
    "numero_concurso": 6792
  }'
```

## 🐍 Exemplo em Python

```python
import requests

# URL base da API
BASE_URL = 'http://localhost:5055/api'

# Atualizar base de dados
def atualizar_dados():
    response = requests.post(f'{BASE_URL}/atualizar')
    return response.json()

# Gerar palpite
def gerar_palpite(estrategia='equilibrada', numeros=5, jogos=1):
    data = {
        'estrategia': estrategia,
        'quantidade_numeros': numeros,
        'quantidade_jogos': jogos
    }
    response = requests.post(f'{BASE_URL}/gerar-palpite', json=data)
    return response.json()

# Obter estatísticas
def obter_estatisticas():
    response = requests.get(f'{BASE_URL}/estatisticas')
    return response.json()

# Exemplo de uso
if __name__ == '__main__':
    # Gera 3 jogos usando estratégia equilibrada
    resultado = gerar_palpite('equilibrada', 5, 3)
    
    print("Palpites gerados:")
    for i, jogo in enumerate(resultado['jogos'], 1):
        print(f"Jogo {i}: {jogo}")
```

## 🔧 Configuração Avançada

### Variáveis de Ambiente

Copie o arquivo de exemplo:
```bash
cp .env.example .env
```

Edite o arquivo `.env`:
```
SECRET_KEY=sua-chave-secreta-aqui
DEBUG=True
HOST=0.0.0.0
PORT=5055
DATABASE_PATH=database.db
API_QUINA_URL=https://servicebus2.caixa.gov.br/portaldeloterias/api/quina
```

### Porta Personalizada

Para rodar em outra porta:
```bash
# No arquivo .env
PORT=8080
```

Ou diretamente no código (app.py):
```python
app.run(host='0.0.0.0', port=8080, debug=True)
```

## 📊 Primeira Atualização

Na primeira execução, recomendamos:

1. Iniciar com poucos concursos para testar:
   - A API pode levar alguns minutos para buscar todos os concursos históricos
   - O sistema busca incrementalmente apenas os novos concursos

2. Monitorar o progresso:
   - O sistema exibe mensagens no console durante a atualização
   - A cada 100 concursos, uma mensagem de progresso é exibida

3. Verificar a base de dados:
   - O arquivo `database.db` será criado automaticamente
   - Contém todos os dados históricos da QUINA

## ❓ Solução de Problemas

### Erro: Módulo não encontrado
```bash
pip install -r requirements.txt
```

### Erro: Porta em uso
Mude a porta no arquivo `.env` ou use:
```bash
# Linux/Mac
lsof -ti:5055 | xargs kill -9

# Windows
netstat -ano | findstr :5055
taskkill /PID <PID> /F
```

### Erro ao conectar com a API
- Verifique sua conexão com a internet
- A API da Caixa pode estar temporariamente indisponível
- Tente novamente após alguns minutos

## 📚 Próximos Passos

1. ✅ Explore a [documentação completa](README.md)
2. 📥 Leia o [guia de download de dados](DOWNLOAD.md)
3. 🗺️ Veja o [mapa de arquivos](ONDE-ESTAO-ARQUIVOS.md)

## 🆘 Precisa de Ajuda?

- 📖 Consulte a [documentação completa](README.md)
- 🐛 Reporte bugs no [GitHub Issues](https://github.com/projetospyton2025/AnalisePorPosicao-Quina/issues)

---

**Pronto para começar! 🎯**
