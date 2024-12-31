from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from datetime import datetime
from .forms import AddClientForm
from .models import CLient
from lead.models import Lead
from django.http import JsonResponse

@login_required
def clients_list(request):
    clients = CLient.objects.all()

   
    companies = CLient.objects.values_list('company', flat=True).distinct()
    contact_people = CLient.objects.values_list('contact_person', flat=True).distinct()
    consultants = CLient.objects.values_list('lead_consultant', flat=True).distinct()
    priorities = CLient.objects.values_list('priority', flat=True).distinct()
    deliverable_types = CLient.objects.values_list('deliverable_type', flat=True).distinct()
    statuses = CLient.objects.values_list('status', flat=True).distinct()

   
    if 'company' in request.GET:
        clients = clients.filter(company=request.GET['company'])
    if 'contact_person' in request.GET:
        clients = clients.filter(contact_person=request.GET['contact_person'])
    if 'lead_consultant' in request.GET:
        clients = clients.filter(lead_consultant=request.GET['lead_consultant'])
    if 'priority' in request.GET:
        clients = clients.filter(priority=request.GET['priority'])
    if 'deliverable_type' in request.GET:
        clients = clients.filter(deliverable_type=request.GET['deliverable_type'])
    if 'status' in request.GET:
        clients = clients.filter(status=request.GET['status'])

    
    sort_by = request.GET.get('sort_by', 'company')
    clients = clients.order_by(sort_by)

    return render(request, 'client/clients_list.html', {
        'clients': clients,
        'companies': companies,
        'contact_people': contact_people,
        'consultants': consultants,
        'priorities': priorities,
        'deliverable_types': deliverable_types,
        'statuses': statuses,
    })

@login_required
def clients_detail(request, pk):
    if request.user.is_superuser:
        client = CLient.objects.get(pk=pk)
    else:
        client = CLient.objects.filter(created_by=request.user).get(pk=pk)

    return render(request, 'client/clients_detail.html', {
        'client': client
    })

@login_required
def clients_edit(request, pk):
    client = get_object_or_404(CLient, pk=pk)
    selected_company = request.GET.get('company', client.company)  

    if request.method == 'POST':
        form = AddClientForm(request.POST, instance=client, selected_company=request.POST.get('company'))
        if form.is_valid():
            form.save()
            messages.success(request, 'The client was updated.')
            return redirect('clients_list')
        else:
            print("Form errors:", form.errors)
    else:
        form = AddClientForm(instance=client, selected_company=selected_company)

    return render(request, 'client/clients_edit.html', {'form': form, 'client': client})


@login_required
def add_client(request):
    selected_company = request.GET.get('company', None)  

    if request.method == 'POST':
        
        form = AddClientForm(request.POST, selected_company=request.POST.get('company'))
        if form.is_valid():
            client = form.save(commit=False)
            client.created_by = request.user
            client.save()
            messages.success(request, 'The client was added.')
            return redirect('clients_list')
        else:
            print("Form errors:", form.errors)
    else:
        form = AddClientForm(selected_company=selected_company)

    return render(request, 'client/add_client.html', {'form': form})



@login_required
def clients_edit(request, pk):
    client = get_object_or_404(CLient, pk=pk)
    selected_company = request.GET.get('company', client.company)

    if request.method == 'POST':
        form = AddClientForm(request.POST, instance=client, selected_company=request.POST.get('company'))
        if form.is_valid():
            form.save()
            messages.success(request, 'The client was updated.')
            return redirect('clients_list')
        else:
            print(form.errors)
    else:
        form = AddClientForm(instance=client, selected_company=selected_company)

    return render(request, 'client/clients_edit.html', {'form': form, 'client': client})

@login_required
def add_client(request):
    selected_company = request.GET.get('company', None)

    if request.method == 'POST':
        form = AddClientForm(request.POST, selected_company=request.POST.get('company'))
        if form.is_valid():
            client = form.save(commit=False)
            client.created_by = request.user
            client.save()
            messages.success(request, 'The client was added.')
            return redirect('clients_list')
        else:
            print(form.errors)
    else:
        form = AddClientForm(selected_company=selected_company)

    return render(request, 'client/add_client.html', {'form': form})
