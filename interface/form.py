
from django import forms
from django.core.exceptions import ValidationError
from .models import AssetMonitoring
from monitoring.models import Asset, AssetPrice

class AssetMonitoringForm (forms.ModelForm):
    code = forms.ChoiceField()

    class Meta:
        model = AssetMonitoring
        fields = ['lower_limit', 'upper_limit']

    def __init__(self, *args, **kwargs):
        super(AssetMonitoringForm, self).__init__(*args, **kwargs)
        self.fields['code'].choices = [(asset.id, asset.code) for asset in Asset.objects.all()]
        self.fields['lower_limit'].required = False
        self.fields['upper_limit'].required = False

    def clean(self):
        super(AssetMonitoringForm, self).clean()
        asset = Asset.objects.get(id=self.data['code'])
        asset_monitoring = AssetMonitoring.objects.filter(user=self.user, asset=asset)
        price = AssetPrice.objects.filter(asset=asset).order_by('-created_at').first()

        if len(asset_monitoring) > 0:
            raise ValidationError(f'Você já tem esse ativo cadastrado.')
        if self.fields['upper_limit'] and self.fields['upper_limit'] <= price:
            raise ValidationError(f'O limite inferior não pode ser maior que o limite superior.')
        if self.fields['lower_limit'] and self.fields['lower_limit'] >= price:
            raise ValidationError(f'Os limites inferior e superior não podem ser iguais.')

    def save(self):
        asset_monitoring = super(AssetMonitoringForm, self).save(commit=False)
        asset_monitoring.asset = self.asset
        asset_monitoring.user = self.user
        asset_monitoring.save()
