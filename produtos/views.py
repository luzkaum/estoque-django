from django.shortcuts import render, redirect
from .models import Produto
from .forms import ProdutoForm

def listar_produtos(request):
    produtos = Produto.objects.all()
    return render(request, 'produtos/lista.html', {'produtos': produtos})

def criar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_produtos')
    else:
        form = ProdutoForm()
    return render(request, 'produtos/form.html', {'form': form})