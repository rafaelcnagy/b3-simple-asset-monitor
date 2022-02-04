from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .models import AssetMonitoring
from monitoring.models import Asset
from .form import AssetMonitoringForm
from django.contrib import messages

@login_required
def view_list(request):
    user = request.user
    assets = AssetMonitoring.objects.filter(user=user).order_by('-created_at')
    return render(request, 'interface/view_list.html', {'assets': assets})

@login_required
def update(request, id):
    asset_monitoring = AssetMonitoring.objects.get(id=id)        
    if request.method == 'POST':
        upper_limit = request.POST.get('upper_limit', None)
        lower_limit = request.POST.get('lower_limit', None)
        asset_monitoring.upper_limit = float(upper_limit.replace(',', '.'))
        asset_monitoring.lower_limit = float(lower_limit.replace(',', '.'))
        asset_monitoring.save()
        request.session['form_message'] = "Ativo atualizado com sucesso!"
        return redirect('view_list')
    else:
        return render(request, "interface/update.html", {'asset': asset_monitoring})

@login_required
def register(request):
    if request.method == 'POST':
        form = AssetMonitoringForm(request.POST)
        form.user = request.user
        if form.is_valid():
            form.asset = Asset.objects.get(id=form.data['code'])
            form.save()
            request.session['form_message'] = "Ativo adicionado com sucesso!"
            return redirect('view_list')
        else:
            for form_error in form.errors.values():
                messages.error(request, form_error)
    else:
        form = AssetMonitoringForm()
    
    return render(request, 'interface/register.html', {'form': form})

