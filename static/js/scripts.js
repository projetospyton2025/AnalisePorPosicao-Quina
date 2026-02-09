// JavaScript para o Sistema de Análise da QUINA

// Função para formatar número com zeros à esquerda
function formatarNumero(numero) {
    return numero.toString().padStart(2, '0');
}

// Função para criar elemento de número
function criarElementoNumero(numero) {
    const div = document.createElement('div');
    div.className = 'numero';
    div.textContent = formatarNumero(numero);
    return div;
}

// Função para mostrar mensagem de alerta
function mostrarAlerta(mensagem, tipo = 'info') {
    const alertClass = tipo === 'error' ? 'alert-error' : 
                      tipo === 'success' ? 'alert-success' : 'alert-info';
    
    return `<div class="alert ${alertClass}">${mensagem}</div>`;
}

// Carrega o último resultado
async function carregarUltimoResultado() {
    try {
        const response = await fetch('/api/ultimo-resultado');
        const data = await response.json();
        
        const container = document.getElementById('ultimo-resultado');
        
        if (response.ok && data.numero) {
            const dezenas = data.listaDezenas.map(n => parseInt(n));
            
            container.innerHTML = `
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 2rem;">
                    <div>
                        <h3 style="color: var(--cor-principal); margin-bottom: 0.5rem;">
                            Concurso ${data.numero}
                        </h3>
                        <p style="color: #666;">${data.dataApuracao}</p>
                        ${data.acumulado ? '<p style="color: red; font-weight: bold;">ACUMULADO!</p>' : ''}
                    </div>
                    <div class="numeros-container">
                        ${dezenas.map(n => `<div class="numero sorteado">${formatarNumero(n)}</div>`).join('')}
                    </div>
                </div>
            `;
        } else {
            container.innerHTML = mostrarAlerta('Nenhum resultado encontrado. Clique em "Atualizar Dados" para carregar.', 'info');
        }
    } catch (error) {
        console.error('Erro ao carregar último resultado:', error);
        document.getElementById('ultimo-resultado').innerHTML = 
            mostrarAlerta('Erro ao carregar último resultado.', 'error');
    }
}

// Carrega todas as estatísticas
async function carregarEstatisticas() {
    try {
        const response = await fetch('/api/estatisticas');
        const data = await response.json();
        
        if (response.ok) {
            renderizarEstatisticasGerais(data);
            renderizarNumerosFrequentes(data.frequencia_numeros);
            renderizarNumerosAtrasados(data.atrasos);
            renderizarAnalisePosicao(data.por_posicao_sorteio);
            renderizarAnaliseFaixa(data.por_faixa);
            renderizarParesImpares(data.pares_impares);
            renderizarAnaliseDigito(data.por_digito);
        } else {
            console.error('Erro ao carregar estatísticas');
        }
    } catch (error) {
        console.error('Erro ao carregar estatísticas:', error);
    }
}

// Renderiza estatísticas gerais
function renderizarEstatisticasGerais(data) {
    const container = document.getElementById('estatisticas-gerais');
    
    container.innerHTML = `
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value">${data.total_concursos}</div>
                <div class="stat-label">Total de Concursos</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">80</div>
                <div class="stat-label">Números Disponíveis</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">5</div>
                <div class="stat-label">Números Sorteados</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${data.total_concursos * 5}</div>
                <div class="stat-label">Total de Sorteios</div>
            </div>
        </div>
    `;
}

// Renderiza números mais frequentes
function renderizarNumerosFrequentes(frequencias) {
    const container = document.getElementById('numeros-frequentes');
    const top20 = frequencias.slice(0, 20);
    
    let html = '<table><thead><tr><th>Posição</th><th>Número</th><th>Frequência</th><th>Percentual</th></tr></thead><tbody>';
    
    top20.forEach((item, index) => {
        html += `
            <tr>
                <td>${index + 1}º</td>
                <td><div class="numero" style="display: inline-flex;">${formatarNumero(item.numero)}</div></td>
                <td>${item.frequencia} vezes</td>
                <td>${item.percentual}%</td>
            </tr>
        `;
    });
    
    html += '</tbody></table>';
    container.innerHTML = html;
}

// Renderiza números mais atrasados
function renderizarNumerosAtrasados(atrasos) {
    const container = document.getElementById('numeros-atrasados');
    const top20 = atrasos.slice(0, 20);
    
    let html = '<table><thead><tr><th>Posição</th><th>Número</th><th>Atraso</th></tr></thead><tbody>';
    
    top20.forEach((item, index) => {
        html += `
            <tr>
                <td>${index + 1}º</td>
                <td><div class="numero" style="display: inline-flex;">${formatarNumero(item.numero)}</div></td>
                <td>${item.atraso} concursos</td>
            </tr>
        `;
    });
    
    html += '</tbody></table>';
    container.innerHTML = html;
}

// Renderiza análise por posição
function renderizarAnalisePosicao(posicoes) {
    const container = document.getElementById('analise-posicao');
    
    let html = '<div class="posicao-grid">';
    
    for (let i = 1; i <= 5; i++) {
        const posKey = `posicao_${i}`;
        if (posicoes[posKey]) {
            const pos = posicoes[posKey];
            const top5 = pos.top_numeros.slice(0, 5);
            
            html += `
                <div class="posicao-card">
                    <div class="posicao-titulo">${i}ª Posição</div>
                    <div style="margin-top: 0.5rem;">
                        ${top5.map(n => `
                            <div style="display: flex; justify-content: space-between; margin-bottom: 0.25rem;">
                                <span>${formatarNumero(n.numero)}</span>
                                <span>${n.frequencia}x</span>
                            </div>
                        `).join('')}
                    </div>
                </div>
            `;
        }
    }
    
    html += '</div>';
    container.innerHTML = html;
}

// Renderiza análise por faixa
function renderizarAnaliseFaixa(faixas) {
    const container = document.getElementById('analise-faixa');
    
    let html = '<div class="stats-grid">';
    
    faixas.forEach(faixa => {
        html += `
            <div class="stat-card">
                <div class="stat-value">${faixa.quantidade}</div>
                <div class="stat-label">Faixa ${faixa.faixa}</div>
                <div class="stat-label" style="font-size: 0.9rem;">${faixa.percentual}%</div>
            </div>
        `;
    });
    
    html += '</div>';
    container.innerHTML = html;
}

// Renderiza distribuição pares/ímpares
function renderizarParesImpares(dados) {
    const container = document.getElementById('pares-impares');
    
    container.innerHTML = `
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value">${dados.pares}</div>
                <div class="stat-label">Números Pares</div>
                <div class="stat-label" style="font-size: 0.9rem;">${dados.percentual_pares}%</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${dados.impares}</div>
                <div class="stat-label">Números Ímpares</div>
                <div class="stat-label" style="font-size: 0.9rem;">${dados.percentual_impares}%</div>
            </div>
        </div>
    `;
}

// Renderiza análise por dígito
function renderizarAnaliseDigito(digitos) {
    const container = document.getElementById('analise-digito');
    
    let html = '<div class="stats-grid" style="grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));">';
    
    digitos.forEach(dig => {
        html += `
            <div class="stat-card">
                <div class="stat-value">${dig.digito}</div>
                <div class="stat-label">${dig.quantidade} vezes</div>
                <div class="stat-label" style="font-size: 0.9rem;">${dig.percentual}%</div>
            </div>
        `;
    });
    
    html += '</div>';
    container.innerHTML = html;
}

// Atualiza dados da API
async function atualizarDados() {
    const btn = event.target;
    btn.disabled = true;
    btn.innerHTML = '⏳ Atualizando...';
    
    try {
        const response = await fetch('/api/atualizar', {
            method: 'POST'
        });
        
        const data = await response.json();
        
        if (response.ok) {
            alert(`✅ Atualização concluída!\n\nProcessados: ${data.total_processados}\nInseridos: ${data.total_inseridos}\nErros: ${data.total_erros}\nÚltimo concurso: ${data.ultimo_concurso}`);
            
            // Recarrega os dados
            carregarUltimoResultado();
            carregarEstatisticas();
        } else {
            alert('❌ Erro ao atualizar dados: ' + (data.erro || data.mensagem));
        }
    } catch (error) {
        console.error('Erro ao atualizar:', error);
        alert('❌ Erro ao atualizar dados. Verifique sua conexão.');
    } finally {
        btn.disabled = false;
        btn.innerHTML = '🔄 Atualizar Dados';
    }
}

// Gera palpites
async function gerarPalpites(event) {
    event.preventDefault();
    
    const estrategia = document.getElementById('estrategia').value;
    const quantidade_numeros = parseInt(document.getElementById('quantidade_numeros').value);
    const quantidade_jogos = parseInt(document.getElementById('quantidade_jogos').value);
    
    const container = document.getElementById('resultado-palpites');
    container.innerHTML = '<div class="loading"><div class="spinner"></div><p>Gerando palpites...</p></div>';
    
    try {
        const response = await fetch('/api/gerar-palpite', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                estrategia,
                quantidade_numeros,
                quantidade_jogos
            })
        });
        
        const data = await response.json();
        
        if (response.ok && data.jogos) {
            let html = `
                <div class="alert alert-success">
                    ✨ ${data.quantidade_jogos} palpite(s) gerado(s) com sucesso usando estratégia <strong>${data.estrategia}</strong>!
                </div>
            `;
            
            data.jogos.forEach((jogo, index) => {
                html += `
                    <div class="palpite-card">
                        <div class="palpite-titulo">Jogo ${index + 1}</div>
                        <div class="numeros-container">
                            ${jogo.map(n => `<div class="numero">${formatarNumero(n)}</div>`).join('')}
                        </div>
                    </div>
                `;
            });
            
            container.innerHTML = html;
        } else {
            container.innerHTML = mostrarAlerta(data.erro || 'Erro ao gerar palpites.', 'error');
        }
    } catch (error) {
        console.error('Erro ao gerar palpites:', error);
        container.innerHTML = mostrarAlerta('Erro ao gerar palpites. Verifique sua conexão.', 'error');
    }
}

// Confere palpite
async function conferirPalpite(event) {
    event.preventDefault();
    
    const numerosStr = document.getElementById('numeros_conferir').value;
    const numero_concurso = parseInt(document.getElementById('numero_concurso').value);
    
    // Converte string para array de números
    const numeros = numerosStr.split(',').map(n => parseInt(n.trim())).filter(n => !isNaN(n));
    
    if (numeros.length < 5) {
        alert('❌ Digite pelo menos 5 números válidos!');
        return;
    }
    
    const container = document.getElementById('resultado-conferencia');
    container.innerHTML = '<div class="loading"><div class="spinner"></div><p>Conferindo...</p></div>';
    
    try {
        const response = await fetch('/api/conferir', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                numeros,
                numero_concurso
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            let html = `
                <div class="alert ${data.quantidade_acertos >= 3 ? 'alert-success' : 'alert-info'}">
                    ${data.quantidade_acertos >= 5 ? '🎉' : data.quantidade_acertos >= 4 ? '🎊' : data.quantidade_acertos >= 3 ? '👏' : ''}
                    <strong>${data.quantidade_acertos} acerto(s)</strong> no concurso ${data.numero_concurso}
                </div>
                <div class="palpite-card">
                    <div class="palpite-titulo">Seus Números</div>
                    <div class="numeros-container">
                        ${data.numeros_jogo.map(n => `<div class="numero">${formatarNumero(n)}</div>`).join('')}
                    </div>
                </div>
                <div class="palpite-card">
                    <div class="palpite-titulo">Números Sorteados</div>
                    <div class="numeros-container">
                        ${data.numeros_sorteados.map(n => `<div class="numero sorteado">${formatarNumero(n)}</div>`).join('')}
                    </div>
                </div>
            `;
            
            if (data.acertos.length > 0) {
                html += `
                    <div class="palpite-card">
                        <div class="palpite-titulo">Acertos</div>
                        <div class="numeros-container">
                            ${data.acertos.map(n => `<div class="numero" style="background: #28a745;">${formatarNumero(n)}</div>`).join('')}
                        </div>
                    </div>
                `;
            }
            
            container.innerHTML = html;
        } else {
            container.innerHTML = mostrarAlerta(data.erro || 'Erro ao conferir palpite.', 'error');
        }
    } catch (error) {
        console.error('Erro ao conferir:', error);
        container.innerHTML = mostrarAlerta('Erro ao conferir palpite. Verifique sua conexão.', 'error');
    }
}
