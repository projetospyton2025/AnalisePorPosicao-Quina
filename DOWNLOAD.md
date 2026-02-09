# 📥 Guia de Download de Dados - QUINA

Este guia explica como baixar e atualizar os dados históricos da QUINA usando a API oficial da Caixa.

## 🎯 Visão Geral

O sistema oferece **atualização incremental automática**, ou seja:
- Na primeira execução: baixa TODOS os concursos históricos
- Nas próximas: baixa APENAS os novos concursos

## 🚀 Métodos de Atualização

### 1. Via Interface Web (Recomendado)

**Passo a Passo:**

1. Inicie o servidor:
   ```bash
   python app.py
   ```

2. Acesse http://localhost:5055

3. Clique no botão **"🔄 Atualizar Dados"**

4. Aguarde a conclusão:
   - Uma mensagem de progresso aparecerá
   - O tempo depende da quantidade de concursos novos
   - Primeira atualização: pode levar alguns minutos

5. Você verá um resumo:
   ```
   ✅ Atualização concluída!
   
   Processados: 100
   Inseridos: 100
   Erros: 0
   Último concurso: 6792
   ```

### 2. Via API REST

**Usando curl:**
```bash
curl -X POST http://localhost:5055/api/atualizar
```

**Usando Python:**
```python
import requests

response = requests.post('http://localhost:5055/api/atualizar')
resultado = response.json()

print(f"Total processados: {resultado['total_processados']}")
print(f"Total inseridos: {resultado['total_inseridos']}")
print(f"Último concurso: {resultado['ultimo_concurso']}")
```

**Usando JavaScript:**
```javascript
fetch('http://localhost:5055/api/atualizar', {
    method: 'POST'
})
.then(response => response.json())
.then(data => {
    console.log(`Total processados: ${data.total_processados}`);
    console.log(`Total inseridos: ${data.total_inseridos}`);
    console.log(`Último concurso: ${data.ultimo_concurso}`);
});
```

### 3. Via Python Script

Crie um arquivo `atualizar_dados.py`:

```python
#!/usr/bin/env python
"""
Script para atualizar base de dados da QUINA
"""
from services.api_caixa_service import ApiCaixaService

def main():
    print("🎯 Iniciando atualização da base QUINA...")
    
    api_service = ApiCaixaService()
    resultado = api_service.atualizar_base_completa()
    
    print("\n📊 Resultado da Atualização:")
    print(f"  - Total processados: {resultado['total_processados']}")
    print(f"  - Total inseridos: {resultado['total_inseridos']}")
    print(f"  - Total erros: {resultado['total_erros']}")
    print(f"  - Último concurso: {resultado['ultimo_concurso']}")
    print(f"  - Mensagem: {resultado['mensagem']}")
    print("\n✅ Atualização concluída!")

if __name__ == '__main__':
    main()
```

Execute:
```bash
python atualizar_dados.py
```

## 📊 Como Funciona

### Primeira Atualização

Quando você executa pela primeira vez:

1. O sistema verifica que o banco está vazio
2. Busca o último concurso disponível na API
3. Baixa TODOS os concursos do 1 até o último
4. Insere cada concurso no banco de dados
5. Exibe progresso a cada 100 concursos

**Tempo estimado:** 5-15 minutos (depende da conexão e total de concursos)

### Atualizações Subsequentes

Nas próximas execuções:

1. O sistema busca o último concurso no banco local
2. Busca o último concurso disponível na API
3. Baixa APENAS os concursos novos
4. Insere no banco de dados

**Tempo estimado:** Segundos (depende de quantos concursos novos existem)

### Exemplo de Log

```
Atualizando concursos de 1 até 6792...
Processados 100 concursos...
Processados 200 concursos...
Processados 300 concursos...
...
Processados 6700 concursos...
Processados 6792 concursos...
```

## 🔄 Frequência de Atualização

### QUINA - Sorteios

A QUINA tem sorteios:
- **Diariamente** de segunda a sábado
- Aproximadamente **6 sorteios por semana**
- Não há sorteios aos domingos

### Quando Atualizar

Recomendações:

- **Diariamente**: Se você usa o sistema regularmente
- **Semanalmente**: Para análises menos frequentes
- **Antes de gerar palpites**: Para garantir dados atualizados
- **Automaticamente**: Configure um cron job (ver abaixo)

## ⚙️ Atualização Automática

### Linux/Mac (Cron Job)

1. Abra o crontab:
   ```bash
   crontab -e
   ```

2. Adicione uma linha para atualizar diariamente às 22h:
   ```
   0 22 * * * curl -X POST http://localhost:5055/api/atualizar
   ```

3. Ou usando Python:
   ```
   0 22 * * * cd /caminho/para/AnalisePorPosicao-Quina && python atualizar_dados.py
   ```

### Windows (Agendador de Tarefas)

1. Abra o **Agendador de Tarefas**
2. Crie uma nova tarefa básica
3. Configure para executar diariamente
4. Ação: Iniciar programa
5. Programa: `python`
6. Argumentos: `C:\caminho\para\AnalisePorPosicao-Quina\atualizar_dados.py`

### Python (Scheduler)

Crie um arquivo `auto_update.py`:

```python
import schedule
import time
import requests

def atualizar():
    print("🔄 Atualizando base QUINA...")
    try:
        response = requests.post('http://localhost:5055/api/atualizar')
        resultado = response.json()
        print(f"✅ Atualização concluída: {resultado['mensagem']}")
    except Exception as e:
        print(f"❌ Erro na atualização: {e}")

# Atualiza diariamente às 22h
schedule.every().day.at("22:00").do(atualizar)

print("🤖 Agendador iniciado. Atualizações diárias às 22h.")
while True:
    schedule.run_pending()
    time.sleep(60)
```

Execute em background:
```bash
python auto_update.py &
```

## 📈 Monitoramento

### Verificar Status da Base

**Via Interface Web:**
- Acesse http://localhost:5055
- Veja o card "Estatísticas Gerais"
- Mostra o total de concursos cadastrados

**Via API:**
```bash
curl http://localhost:5055/api/estatisticas | jq '.total_concursos'
```

**Via Python:**
```python
from models.resultado_model import ResultadoModel

model = ResultadoModel()
ultimo = model.buscar_ultimo()

if ultimo:
    print(f"Último concurso: {ultimo['numero']}")
    print(f"Data: {ultimo['dataApuracao']}")
else:
    print("Base de dados vazia")
```

### Verificar Último Concurso

```bash
curl http://localhost:5055/api/ultimo-resultado
```

## 🐛 Solução de Problemas

### Erro: Não consegue conectar com a API

**Causas possíveis:**
- Sem conexão com a internet
- API da Caixa temporariamente indisponível
- Firewall bloqueando a conexão

**Soluções:**
1. Verifique sua conexão
2. Tente novamente após alguns minutos
3. Verifique se consegue acessar: https://servicebus2.caixa.gov.br/portaldeloterias/api/quina

### Erro: Timeout na atualização

**Causa:** A API da Caixa pode ser lenta em horários de pico

**Solução:** 
- Tente em outro horário
- A atualização pode ser interrompida e retomada (é incremental)

### Erro: Banco de dados corrompido

**Solução:**
1. Faça backup do banco atual:
   ```bash
   cp database.db database.db.backup
   ```

2. Delete o banco e crie novo:
   ```bash
   rm database.db
   python app.py
   ```

3. Atualize novamente

### Aviso: Muitos erros durante atualização

**Possíveis causas:**
- Concursos específicos não disponíveis na API
- Problemas temporários na API

**Solução:**
- Geralmente não é problema grave
- O sistema pula concursos com erro e continua
- Você pode tentar atualizar novamente depois

## 📊 Estrutura dos Dados

Cada concurso armazena:

- Número do concurso
- Data da apuração
- Lista de dezenas sorteadas
- Ordem do sorteio
- Valores de prêmios
- Informações de ganhadores
- Status de acumulação
- E mais...

**Total de campos:** 23 campos por concurso

**Tamanho estimado:** 
- 1 concurso ≈ 2 KB
- 1000 concursos ≈ 2 MB
- 6000+ concursos ≈ 12 MB

## 🔐 Privacidade e Segurança

- ✅ Todos os dados são públicos (API oficial da Caixa)
- ✅ Nenhuma informação pessoal é coletada
- ✅ Banco de dados armazenado localmente
- ✅ Sem envio de dados para servidores externos

## 📚 Recursos Adicionais

- [README Principal](README.md)
- [Guia Rápido](QUICKSTART.md)
- [Mapa de Arquivos](ONDE-ESTAO-ARQUIVOS.md)
- [API da Caixa](https://servicebus2.caixa.gov.br/portaldeloterias/api/quina)

---

**Mantenha seus dados sempre atualizados! 📥**
