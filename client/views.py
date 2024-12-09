from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from datetime import datetime
from .forms import AddClientForm
from .models import CLient
from lead.models import Lead

@login_required
def clients_list(request):
    if request.user.is_superuser:
        clients = CLient.objects.all()
    else:
        clients = CLient.objects.filter(created_by=request.user)

    return render(request, 'client/clients_list.html', {
        'clients': clients
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
def clients_edit(request,pk):
    if request.user.is_superuser:
        client = CLient.objects.get(pk=pk)
    else:
        client = CLient.objects.filter(created_by=request.user).get(pk=pk)

    if request.method == 'POST':
        form = AddClientForm(request.POST, instance=client)

        if form.is_valid():
            client = form.save(commit=False)
            client.created_by = request.user
            client.save()

            messages.success(request, 'The client detail was edited.')

            return redirect('clients_list')
    else:
        form = AddClientForm(instance=client)

        

    return render(request, 'client/clients_edit.html', {
        'form':form,
        'client': client,
    })

@login_required
def add_client(request):
    if request.method == 'POST':
        form = AddClientForm(request.POST)

        if form.is_valid():
            client = form.save(commit=False)
            client.created_by = request.user
            client.save()

            messages.success(request, 'The client was added.')

            return redirect('clients_list')
        else:
            print(form.errors)
    else:
         form = AddClientForm()

    return render(request, 'client/add_client.html', {
        'form':form
    })