from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import AddLeadForm
from .models import Lead

@login_required
def leads_list(request):
    leads = Lead.objects.all()

    return render(request, 'lead/leads_list.html', {
        'leads': leads
    })

@login_required
def leads_detail(request, pk):
    lead = Lead.objects.filter(created_by=request.user).get(pk=pk)

    return render(request, 'lead/leads_detail.html', {
        'lead': lead
    })

@login_required
def leads_edit(request, pk):
    leads = Lead.objects.filter(created_by=request.user).get(pk=pk)

    if request.method == 'POST':
        form = AddLeadForm(request.POST, request.FILES ,instance=leads)

        if form.is_valid():
            form.save()

            messages.success(request, 'The contact was edited.')

            return redirect('leads_list')
    else:
        form = AddLeadForm(instance=leads)
    
    return render(request, 'lead/leads_edit.html', {
        'form': form,
        'leads': leads
    })

@login_required
def add_lead(request):
    if request.method == 'POST':
        form = AddLeadForm(request.POST, request.FILES)

        if form.is_valid():
            lead = form.save(commit=False)
            lead.created_by = request.user
            if 'resume' in request.FILES:
                lead.resume = request.FILES['resume']
                print("Resume uploaded:", lead.resume)
            lead.save()

            messages.success(request, 'The contact was added.')

            return redirect('leads_list')
        else:
            print(form.errors)
    else:
        form = AddLeadForm()

    return render(request, 'lead/add_lead.html', {
        'form': form
    })
