# 📚 Revisão: os arquivos de um app Django

Guia de bolso dos arquivos que ficam dentro de um app (a pasta `produtos/`).
Feito com exemplos do **seu próprio projeto de estoque**. Consulte sempre que precisar!

---

## 🗺️ Visão geral (o mapa)

| Arquivo | Em uma frase | Você mexe muito? |
|---|---|---|
| `models.py` | Define a **estrutura dos dados** (as tabelas) | ✅ Sim |
| `views.py` | A **lógica** de cada página (busca dados, decide o que fazer) | ✅ Sim |
| `urls.py` | Liga **endereços** (URLs) às views | ✅ Sim |
| `forms.py` | Cria **formulários** (a partir dos models) | ✅ Sim |
| `admin.py` | Registra models no **painel /admin** | 🔸 Às vezes |
| `apps.py` | **Configuração** do app | ❌ Quase nunca |
| `tests.py` | **Testes automáticos** do seu código | 🔸 Quando quiser testar |

> A arquitetura do Django se chama **MTV**: **M**odel (dados) → **V**iew (lógica) → **T**emplate (visual).

---

## 1. `models.py` — a estrutura dos dados 🗄️

**Pra que serve:** definir **o que** o sistema guarda. Cada classe vira uma **tabela** no banco; cada atributo, uma **coluna**.

**No seu projeto:**
```python
class Produto(models.Model):
    nome = models.CharField('Nome do produto', max_length=120)
    preco = models.DecimalField('Preço', max_digits=10, decimal_places=2)
    quantidade = models.PositiveIntegerField('Quantidade em estoque', default=0)
    categoria = models.ForeignKey('Categoria', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nome
```

- Cada `Field` é o **tipo** da coluna (`CharField` = texto, `DecimalField` = decimal...).
- `ForeignKey` = **relacionamento** entre tabelas (o JOIN do SQL).
- `__str__` = como o objeto **aparece escrito** (a "etiqueta").

**Analogia:** é a **planta baixa** das suas planilhas/tabelas, escrita em Python.

> ⚠️ Mudou o `models.py`? Rode `makemigrations` + `migrate` pra aplicar no banco.

---

## 2. `views.py` — a lógica (o cérebro) 🧠

**Pra que serve:** cada função (view) **recebe um pedido** (request), **busca dados** e **devolve** uma página (ou um redirect).

**No seu projeto:**
```python
def listar_produtos(request):
    produtos = Produto.objects.all()          # busca no banco (ORM)
    return render(request, 'produtos/lista.html', {'produtos': produtos})
```

- `Produto.objects.all()` / `.filter()` = buscar dados **sem escrever SQL** (isso é o **ORM**).
- `render(...)` = juntar template + dados e devolver a página.
- `redirect(...)` = mandar pra outra página.
- `@login_required` (decorator) = só deixa entrar quem está logado.

**Analogia:** o **cozinheiro** — pega os ingredientes (dados) e monta o prato (a página).

---

## 3. `urls.py` — os endereços (o roteiro) 🧭

**Pra que serve:** dizer **qual view** roda pra **cada endereço** (URL).

**No seu projeto:**
```python
urlpatterns = [
    path('', views.listar_produtos, name='listar_produtos'),
    path('novo/', views.criar_produto, name='criar_produto'),
    path('<int:pk>/editar/', views.editar_produto, name='editar_produto'),
]
```

- `path('endereço/', views.qualView, name='apelido')`
- `<int:pk>` = parte variável (pega um número da URL, ex.: `/5/editar/`).
- `name='...'` = **apelido** usado nos templates com `{% url 'apelido' %}` (nunca escreva o endereço na mão!).

**Analogia:** a **lista de ramais** — "endereço X → toca na view Y".

---

## 4. `forms.py` — os formulários 📝

**Pra que serve:** criar formulários (campos + validação). O `ModelForm` gera tudo **a partir de um model**.

**No seu projeto:**
```python
class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'descricao', 'preco', 'quantidade', 'categoria']
```

- `ModelForm` = formulário automático baseado num model (campos + validação de graça).
- `class Meta` = configurações (qual model, quais campos).
- No template, `{{ form.as_p }}` desenha os campos sozinho.

**Analogia:** um **molde de formulário** que o Django preenche olhando o seu model.

---

## 5. `admin.py` — o painel administrativo 🛠️

**Pra que serve:** "apresentar" seus models ao **painel /admin** (aquele pronto do Django), pra gerenciar dados sem criar telas.

**No seu projeto:**
```python
from .models import Produto, Categoria

admin.site.register(Produto)
admin.site.register(Categoria)
```

- Depois de registrar, o model aparece em `http://127.0.0.1:8000/admin/`.
- Dá pra customizar (colunas, busca, filtros) com uma classe `ModelAdmin`.

**Analogia:** um **painel de controle** pronto pros bastidores do sistema.

---

## 6. `apps.py` — configuração do app ⚙️

**Pra que serve:** guardar **configurações** do app. É **gerado automaticamente** e você quase **nunca** mexe.

**No seu projeto (gerado sozinho):**
```python
class ProdutosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'produtos'
```

- `name = 'produtos'` = o nome do app.
- É por causa dele que você escreveu `'produtos'` no `INSTALLED_APPS`.

**Analogia:** a **ficha de identidade** do app. Fica lá quietinho.

---

## 7. `tests.py` — testes automáticos ✅

**Pra que serve:** escrever **testes** que verificam sozinhos se seu código funciona. Você ainda **não usou**, mas é muito útil quando o projeto cresce.

**Exemplo (como seria):**
```python
from django.test import TestCase
from .models import Produto

class ProdutoTest(TestCase):
    def test_criar_produto(self):
        p = Produto.objects.create(nome='Teste', preco=10, quantidade=5)
        self.assertEqual(p.nome, 'Teste')
```

- Roda com: `python manage.py test`
- Em vez de você abrir o navegador e testar na mão toda vez, o teste faz isso **sozinho**.

> 💡 Curiosidade: aqueles testes que EU rodei pra conferir seu CRUD (criar/editar/apagar) usavam essa mesma ideia — o "cliente de teste" do Django. É isso que mora aqui.

**Analogia:** um **inspetor de qualidade** que confere seu código automaticamente.

---

## 🎬 Como tudo se conecta (a viagem de um clique)

Quando alguém abre a lista de produtos:
```
Navegador pede "/"
      ↓
urls.py     → acha o path('') → chama a view listar_produtos
      ↓
views.py    → busca no banco (usando o models.py) via ORM
      ↓
models.py   → devolve os dados da tabela
      ↓
template    → o lista.html monta o visual com os dados
      ↓
Navegador recebe a página pronta ✅
```

E o `forms.py`, `admin.py` entram quando você **cria/edita** dados; o `tests.py`, quando você quer **verificar** que tudo funciona.

---

## 🧠 Resumo de uma linha cada
- **models** = os dados (tabelas)
- **views** = a lógica (o que fazer)
- **urls** = os endereços (por onde chega)
- **forms** = os formulários (entrada de dados)
- **admin** = o painel de bastidores
- **apps** = a config do app (não mexe)
- **tests** = os testes automáticos

Bons estudos, Lucas! 🚀
