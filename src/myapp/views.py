from django.shortcuts import render

# Create your views here.
def receita(request):
    receitas = Receita.objects.all()
    context = {'receitas': receitas}

    return render(request, 'minha_receitas.html', context)