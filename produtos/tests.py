from django.test import TestCase
from .models import Produto
from django.contrib.auth.models import User
# Create your tests here.
class ProdutoModelTest(TestCase):
    
    def test_str_retorna_o_nome(self):
        produto=Produto.objects.create(nome='Teclado', preco=100, quantidade=3)
        self.assertEqual(str(produto), 'Teclado')

class ListaProdutosViewTest(TestCase):

    def test_lista_abre_para_qualquer_um(self):
        resposta = self.client.get('/')
        self.assertEqual(resposta.status_code,200)

    def test_linha_mostra_o_produto_cadastrado(self):
        Produto.objects.create(nome='Teclado', preco =100, quantidade=3)
        resposta = self.client.get('/')
        self.assertContains(resposta, 'Teclado')

class PermissaoTest(TestCase):
    
    def test_cliente_nao_pode_criar_produto(self):
        User.objects.create_user(username='cliente', password ='SenhaTeste123')
        self.client.login(username='cliente', password='SenhaTeste123')
        resposta = self.client.get('/novo/')
        self.assertEqual(resposta.status_code, 302)
    
    def test_staff_pode_criar_produto(self):
        User.objects.create_user(username='gerente', password ='SenhaTeste123', is_staff=True)
        self.client.login(username='gerente', password='SenhaTeste123')
        resposta = self.client.get('/novo/')
        self.assertEqual(resposta.status_code, 200)