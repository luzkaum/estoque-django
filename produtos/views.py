from django.shortcuts import render, redirect, get_object_or_404
from .models import Produto, Categoria
from .forms import ProdutoForm

def listar_produtos(request):
    produtos = Produto.objects.all()
    categorias= Categoria.objects.all()
    categoria_id = request.GET.get('categoria')
    if categoria_id:
        produtos = produtos.filter(categoria_id = categoria_id)
    return render(request, 'produtos/lista.html', 
    {
        'produtos': produtos,
        'categorias': categorias,
        'categoria_ativa':categoria_id
    })

def criar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_produtos')
    else:
        form = ProdutoForm()
    return render(request, 'produtos/form.html', {'form': form, 'titulo':'Novo produto'})

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
   
def deletar_produto(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    if request.method == 'POST':
        produto.delete()
        return redirect('listar_produtos')
    return render(request, 'produtos/confirmar_delete.html', {'produto':produto})
