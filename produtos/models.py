from django.db import models


class Categoria(models.Model):
    nome = models.CharField('Nome', max_length=80)

    def __str__(self):
        return self.nome

class Produto(models.Model):
    nome = models.CharField('Nome do produto', max_length=120)
    descricao = models.TextField('Descrição', blank=True)
    preco = models.DecimalField('Preço', max_digits = 10, decimal_places=2)
    quantidade = models.PositiveIntegerField('Quantidade em estoque', default=0)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank= True, verbose_name='Categoria')
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)

    def __str__(self):
        return self.nome
    
    class Meta:
        ordering = ['nome']
