"""
Aplicação Flask principal do sistema de análise da QUINA
"""
from flask import Flask
import config
from routes.main_routes import main_bp
from routes.api_routes import api_bp

# Cria a aplicação Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = config.SECRET_KEY

# Registra blueprints
app.register_blueprint(main_bp)
app.register_blueprint(api_bp)

if __name__ == '__main__':
    print(f"🎯 Sistema de Análise QUINA")
    print(f"🌐 Servidor rodando em http://{config.HOST}:{config.PORT}")
    print(f"📊 Acesse o painel de estatísticas em: http://localhost:{config.PORT}/")
    print(f"🎲 Acesse o gerador de palpites em: http://localhost:{config.PORT}/palpites")
    
    app.run(
        host=config.HOST,
        port=config.PORT,
        debug=config.DEBUG
    )
