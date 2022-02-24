from django.core.mail import send_mail
from interface.models import AssetMonitoring
from .models import AssetPrice

from simple_asset_monitor.settings import EMAIL_HOST_USER


def mail_trigger(asset):
    all_monitoring = AssetMonitoring.objects.filter(asset=asset)

    for monitoring in all_monitoring:
        prices = AssetPrice.objects.filter(asset=monitoring.asset).order_by('-created_at')[:2]
        if len(prices) <= 1 or prices[0].price == prices[1].price:
            continue
        if prices[0].price <= monitoring.lower_limit:
            mail_to_buy(monitoring, prices[0])
        elif prices[0].price >= monitoring.upper_limit:
            mail_to_sell(monitoring, prices[0])

def mail_to_buy(monitoring, price):
    user = monitoring.user
    send_mail(
        f'Oportunidade de compra de ativo {monitoring.asset.code}',
        f'''Olá {user.first_name},

        Encontramos uma oportunidade de compra de um ativo monitorado por você.
        O ativo em questão é o {monitoring.asset.code}, que está com o valor R${price.price}, abaixo do limite inferior de R${monitoring.lower_limit} que você determinou.
        Essa informação foi constatada por nosso software em {price.created_at}.
        Confira as informações e, se quiser, efetue sua transação.

        Atenciosamente,
        Simple Asset Monitor
        ''',
        EMAIL_HOST_USER,
        [user.email],
        fail_silently=False,
        )
    print(f'Alertando oportunidade de compra de {monitoring.asset.code} para {user.first_name}')

def mail_to_sell(monitoring, price):
    user = monitoring.user
    send_mail(
        f'Oportunidade de venda de ativo {monitoring.asset.code}',
        f'''Olá {user.first_name},

        Encontramos uma oportunidade de venda de um ativo monitorado por você.
        O ativo em questão é o {monitoring.asset.code}, que está com o valor R${price.price}, acima do limite superior de R${monitoring.upper_limit} que você determinou.
        Essa informação foi constatada por nosso software em {price.created_at}.
        Confira as informações e, se quiser, efetue sua transação.

        Atenciosamente,
        Simple Asset Monitor
        ''',
        EMAIL_HOST_USER,
        [user.email],
        fail_silently=False,
        )
    print(f'Alertando oportunidade de venda de {monitoring.asset.code} para {user.first_name}')
