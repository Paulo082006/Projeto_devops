import json
import pytest

# As importações que você forneceu
from db import db
from main import app
from models.clientes import Cliente

# Dados de exemplo que serão usados para inserção em testes
CLIENTE_DATA = {
    'nome': 'Novo Cliente Teste', 
    'telefone': '(11) 98765-4321', 
    'endereco': 'Av. Teste, 123'
}


@pytest.fixture
def client():
    """Configura o cliente de teste do Flask e o banco de dados em memória."""
    
    # 1. Configura a aplicação ANTES de qualquer contexto ser criado/utilizado
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:' 
    })

    # 2. Inicializa o cliente de teste
    with app.test_client() as client:
        # 3. Cria o contexto de aplicação para operações de banco de dados
        with app.app_context():
            
            # Cria as tabelas antes de cada teste
            db.create_all() 
        
        # 4. O cliente é retornado para a função de teste
        yield client
            
        # 5. Destrói as tabelas após cada teste (limpeza)
        with app.app_context():
            db.drop_all()

@pytest.fixture
def setup_cliente(client):
    """Fixture auxiliar que insere um cliente e retorna seus dados."""
    response = client.post(
        '/clientes', 
        data=json.dumps(CLIENTE_DATA), 
        content_type='application/json'
    )
    # Retorna o dicionário do cliente criado, incluindo o ID gerado
    return response.get_json()['cliente']




def test_post_clientes_sucesso(client):
    """Testa a criação de um novo cliente (POST)."""
    
    response = client.post(
        '/clientes', 
        data=json.dumps(CLIENTE_DATA), 
        content_type='application/json'
    )
    
    assert response.status_code == 201
    
    response_data = response.get_json()
    
    # Verifica a integridade dos dados retornados
    assert response_data['mensagem'] == 'Cliente criado com sucesso!'
    assert response_data['cliente']['nome'] == CLIENTE_DATA['nome']
    assert 'id' in response_data['cliente']


def test_get_clientes_vazio(client):
    """Testa a listagem de clientes quando o banco está vazio (GET)."""
    response = client.get('/clientes')
    
    assert response.status_code == 200
    response_data = response.get_json()
    
    # Deve retornar uma lista de clientes vazia
    assert response_data['clientes'] == []
    assert response_data['mensagem'] == 'Clientes obtidos com sucesso!'

def test_get_clientes_com_dados(client, setup_cliente):
    """Testa a listagem de clientes com um cliente inserido (GET)."""
    
    # 'setup_cliente' garante que um cliente foi inserido antes da requisição
    response = client.get('/clientes')
    
    assert response.status_code == 200
    response_data = response.get_json()
    
    # Verifica se a lista contém o cliente inserido
    assert len(response_data['clientes']) == 1
    
    cliente_obtido = response_data['clientes'][0]
    assert cliente_obtido['nome'] == CLIENTE_DATA['nome']
    # Garante que o ID e outros campos estão corretos
    assert cliente_obtido['id'] == setup_cliente['id'] 
    
def test_get_cliente_por_id_sucesso(client, setup_cliente):
    """Testa a obtenção de um cliente existente pelo ID (GET /<id>)."""
    
    cliente_id = setup_cliente['id'] 
    response = client.get(f'/clientes/{cliente_id}')
    
    assert response.status_code == 200
    response_data = response.get_json()
    
    assert response_data['mensagem'] == 'Cliente obtido com sucesso!'
    assert response_data['cliente']['id'] == cliente_id
    assert response_data['cliente']['telefone'] == CLIENTE_DATA['telefone']

def test_get_cliente_por_id_nao_encontrado(client):
    """Testa a obtenção de um cliente com ID inexistente (deve retornar 404)."""
    
    id_inexistente = 999 
    response = client.get(f'/clientes/{id_inexistente}')
    
