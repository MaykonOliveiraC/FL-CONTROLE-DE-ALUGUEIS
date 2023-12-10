from django.shortcuts import render, redirect
from .models import Immobile, ImmobileImage    
from myapp.forms import ClientForm, ImmobileForm,RegisterLocationForm

def list_location(request):
    immobiles = Immobile.objects.filter(is_locate=False)
    context = {
        'immobiles': immobiles
    }
    return render(request, 'list-location.html', context)


def form_client(request):
    form = ClientForm() 
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list-location')   
    return render(request, 'form-client.html', {'form': form})

def form_immobile(request):
    form = ImmobileForm()
    if request.method == 'POST':
        form = ImmobileForm(request.POST, request.FILES)
        if form.is_valid():
            immobile = form.save()
            files = request.FILES.getlist('immobile') ## pega todas as imagens
            if files:
                for f in files:
                    ImmobileImage.objects.create( # cria instance para imagens
                        immobile=immobile, 
                        image=f)
            return redirect('list-location')  
    return render(request, 'form-immobile.html', {'form': form})

def form_location(request, id):
    get_locate = Immobile.objects.get(id=id) ## pega objeto
    form = RegisterLocationForm()  
    if request.method == 'POST':
        form = RegisterLocationForm(request.POST)
        if form.is_valid():
            location_form = form.save(commit=False)
            location_form.immobile = get_locate ## salva id do imovel 
            location_form.save() 

            immo = Immobile.objects.get(id=id)
            immo.is_locate = True ## passa ser True
            immo.save() ## muda status do imovel para "Alugado"
            return redirect('list-location') # Retorna para lista
    context = {'form': form, 'location': get_locate}
    return render(request, 'form-location.html', context)



def reports(request): ## Relatórios   
    immobile = Immobile.objects.all()  
    return render(request, 'reports.html', {'immobiles':immobile})