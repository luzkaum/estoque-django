from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from .models import Produto, Categoria
from .forms import ProdutoForm
from django.db.models import Count
from django.contrib.auth.decorators import login_required


def listar_produtos(request):
    produtos = Produto.objects.all()
    categorias = Categoria.objects.annotate(num_produtos=Count('produto'))
    categoria_id = request.GET.get('categoria')
    if categoria_id:
        produtos = produtos.filter(categoria_id = categoria_id)
    return render(request, 'produtos/lista.html', 
    {
        'produtos': produtos,
        'categorias': categorias,
        'categoria_ativa':categoria_id
    })

@login_required
def criar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_produtos')
    else:
        form = ProdutoForm()
    return render(request, 'produtos/form.html', {'form': form, 'titulo':'Novo produto'})

@login_required
def editar_produto(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    if request.method == 'POST':
        form = ProdutoForm(request.POST, instance=produto)
        if form.is_valid():
            form.save()
            return redirect('listar_produtos')
    else:
        form = ProdutoForm(instance=produto)
    return render(request, 'produtos/form.html', {'form': form, 'titulo':'Editar produto'})        

@login_required
def deletar_produto(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    if request.method == 'POST':
        produto.delete()
        return redirect('listar_produtos')
    return render(request, 'produtos/confirmar_delete.html', {'produto':produto})
