from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from .models import Produto, Categoria
from .forms import ProdutoForm
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.core.paginator import Paginator

def listar_produtos(request):
    produtos = Produto.objects.all()
    categorias = Categoria.objects.annotate(num_produtos=Count('produto'))
    categoria_id = request.GET.get('categoria')
    if categoria_id:
        produtos = produtos.filter(categoria_id = categoria_id)

    paginator = Paginator(produtos,3)
    numero_pagina = request.GET.get('page')
    pagina = paginator.get_page(numero_pagina)

    return render(request, 'produtos/lista.html', 
    {
        'produtos': pagina,
        'categorias': categorias,
        'categoria_ativa':categoria_id
    })

@staff_member_required
def criar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produto Criado!!')
            return redirect('listar_produtos')
    else:
        form = ProdutoForm()
    return render(request, 'produtos/form.html', {'form': form, 'titulo':'Novo produto'})

@staff_member_required
def editar_produto(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    if request.method == 'POST':
        form = ProdutoForm(request.POST, instance=produto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produto Atualizado!')
            return redirect('listar_produtos')
    else:
        form = ProdutoForm(instance=produto)
    return render(request, 'produtos/form.html', {'form': form, 'titulo':'Editar produto'})        

@staff_member_required
def deletar_produto(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    if request.method == 'POST':
        produto.delete()
        messages.success(request, 'Produto removido.')
        return redirect('listar_produtos')
    return render(request, 'produtos/confirmar_delete.html', {'produto':produto})

def cadastro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Bem-vindo, {user.username}!')
            return redirect('listar_produtos')
    else:
        form = UserCreationForm()
    return render(request, 'produtos/cadastro.html',{'form':form})

@staff_member_required
def relatorio(request):
    produtos = list(Produto.objects.all())

    total_itens = sum(p.quantidade for p in produtos)
    valor_total = sum(p.preco * p.quantidade for p in produtos)
    estoque_baixo = [p for p in produtos if p.quantidade < 20]

    if produtos:
        mais_caro = max(produtos, key=lambda p: p.preco)
    else:
        mais_caro = None
    return render(request, 'produtos/relatorio.html',{
        'total_itens' : total_itens,
        'valor_total' : valor_total,
        'estoque_baixo' : estoque_baixo,
        'mais_caro': mais_caro,
    })

def adicionar_ao_carrinho(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    carrinho = request.session.get('carrinho', {})
    
    chave = str(pk)
    carrinho[chave] = carrinho.get(chave, 0) + 1

    request.session['carrinho'] = carrinho
    messages.success(request, f'{produto.nome} adicionado ao carrinho.')
    return redirect('listar_produtos')

def ver_carrinho(request):
    carrinho = request.session.get('carrinho',{})
    itens = []
    total = 0

    for produto_id, quantidade in carrinho.items():
        produto = get_object_or_404(Produto, pk=produto_id)
        subtotal = produto.preco * quantidade
        total += subtotal
        itens.append({
            'produto': produto,
            'quantidade': quantidade,
            'subtotal': subtotal
        })

    return render(request, 'produtos/carrinho.html', {'itens' : itens, 'total' : total})

def remover_do_carrinho(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    carrinho = request.session.get('carrinho',{})
    chave = str(pk)
    
    if chave in carrinho:
        del carrinho[chave]
        request.session['carrinho'] = carrinho
        messages.success(request, f'{produto.nome} removido do carrinho.')
    return redirect('ver_carrinho')
