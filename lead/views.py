from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import AddLeadForm
from .models import Lead

@login_required
def leads_list(request):
   
    leads = Lead.objects.all()

   
    companies = Lead.objects.values_list('company', flat=True).distinct()
    contact_people = Lead.objects.values_list('contact_person', flat=True).distinct()
    regions = Lead.objects.values_list('region', flat=True).distinct()

   
    if 'company' in request.GET:
        leads = leads.filter(company=request.GET['company'])

    if 'contact_person' in request.GET:
        leads = leads.filter(contact_person=request.GET['contact_person'])

    if 'region' in request.GET:
        leads = leads.filter(region=request.GET['region'])

   
    sort_by = request.GET.get('sort_by', 'company')
    leads = leads.order_by(sort_by)

    return render(request, 'lead/leads_list.html', {
        'leads': leads,
        'companies': companies,
        'contact_people': contact_people,
        'regions': regions,
    })


@login_required
def leads_detail(request, pk):
    lead = Lead.objects.filter(created_by=request.user).get(pk=pk)

    return render(request, 'lead/leads_detail.html', {
        'lead': lead
    })

@login_required
def leads_edit(request, id):
    leads = Lead.objects.filter(created_by=request.user).get(id=id)

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
