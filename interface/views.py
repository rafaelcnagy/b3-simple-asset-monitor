from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .models import AssetMonitoring
from monitoring.models import Asset, AssetPrice
from .form import AssetMonitoringForm
from django.contrib import messages

@login_required
def view_list(request):
    user = request.user
    assets = AssetMonitoring.objects.filter(user=user).order_by('-created_at')
    assets_prices = AssetPrice.objects.filter(asset__in=[asset_monitoring.asset for asset_monitoring in assets]).order_by('-created_at')
    for asset in assets:
        asset.prices = [asset_price for asset_price in assets_prices if asset_price.asset == asset.asset]

    return render(request, 'interface/view_list.html', {'assets': assets})

@login_required
def update(request, id):
    def check_interval(upper_limit, lower_limit, price):
        if upper_limit is not None and upper_limit != '':
            asset_monitoring.upper_limit = float(upper_limit.replace(',', '.'))
            if asset_monitoring.upper_limit < price or asset_monitoring.upper_limit <= 0:
                return False
        else:
            asset_monitoring.upper_limit = None

        if lower_limit is not None and lower_limit != '':
            asset_monitoring.lower_limit = float(lower_limit.replace(',', '.'))
            if asset_monitoring.lower_limit > price or asset_monitoring.lower_limit <= 0:
                return False
        else:
            asset_monitoring.lower_limit = None
        
        return True

    asset_monitoring = AssetMonitoring.objects.get(id=id)
    asset_monitoring.prices = AssetPrice.objects.filter(asset=asset_monitoring.asset).order_by('-created_at')

    if request.method == 'POST':
        upper_limit = request.POST.get('upper_limit', None)
        lower_limit = request.POST.get('lower_limit', None)
        if check_interval(upper_limit, lower_limit, asset_monitoring.prices[0].price):
            asset_monitoring.save()
            request.session['form_message'] = "Ativo atualizado com sucesso!"
            return redirect('view_list')
        else:
            messages.error(request, 'Valor inválido')
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

    