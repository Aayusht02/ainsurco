from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Associate
from .forms import AssociateForm
from django.contrib.auth.models import Group

def is_cofounder(user):
    return user.groups.filter(name="Co-Founders").exists()

def some_view(request):
    is_cofounder = request.user.groups.filter(name="Co-Founders").exists()
    return render(request, 'core/base.html', {'is_cofounder': is_cofounder})


@user_passes_test(is_cofounder, login_url='/')  
@login_required
def associate_list(request):
    associates = Associate.objects.all()

   
    companies = Associate.objects.values_list('company_name', flat=True).distinct()
    contact_people = Associate.objects.values_list('contact_person', flat=True).distinct()
    specializations = Associate.objects.values_list('specialization', flat=True).distinct()
    skill_set = Associate.objects.values_list('skills', flat=True).distinct()

    
   
    if 'company_name' in request.GET:
        associates = associates.filter(company=request.GET['company_name'])

    if 'contact_person' in request.GET:
        associates = associates.filter(contact_person=request.GET['contact_person'])

    if 'specialization' in request.GET:
        associates = associates.filter(specialization=request.GET['specialization'])

    if 'skills' in request.GET:
        associates = associates.filter(skills=request.GET['skills'])


    
    sort_by = request.GET.get('sort_by', 'company_name')
    associates = associates.order_by(sort_by)

    return render(request, 'associate_list/associate_list.html', {
        'associates': associates,
        'companies': companies,
        'contact_people': contact_people,
        'specializations': specializations,
        'skill_set': skill_set,
    })
    
@login_required
def add_associate(request):
    if request.method == 'POST':
        form = AssociateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('associate_list')
    else:
        form = AssociateForm()
    return render(request, 'associate_list/add_associate.html', {'form': form})
