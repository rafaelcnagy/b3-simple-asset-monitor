from locale import currency
from wsgiref import headers
from interface.models import AssetMonitoring
from simple_asset_monitor.settings import API_KEY
from .models import Asset, AssetPrice

import aiohttp
import asyncio
import datetime
from parsel import Selector


class API:
    def __init__(self):
        self.thread_size = 30
        self.obtained_assets = dict()
        self.headers = {
            'Host': 'api.hgbrasil.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0',
            'Accept': 'application/json',
            'Alt-Used': 'api.hgbrasil.com',
            'Connection': 'keep-alive',
        }
        self.initialize_data()

    def initialize_data(self):
        if API_KEY is None:
            raise Exception("API KEY não cadastrada")
        print(f'{datetime.datetime.now()} - Procurando novas ações...')
        # Get codes on DB
        all_saved_codes = [item[0] for item in Asset.objects.all().values_list('code')]
        # Get codes on WEB (self.all_asset_codes)
        asyncio.run(self.get_asset_codes())
        
        remaining_codes = [code for code in self.all_asset_codes if code not in all_saved_codes]

        self.get_new_assets(remaining_codes)
        print(f'{datetime.datetime.now()} - Busca por novas ações encerrada.')

    def get_new_assets(self, remaining_codes):
        for index in range(0, len(remaining_codes), self.thread_size):
            self.obtained_assets = dict()
            asyncio.run(self.call_multiple_requests(remaining_codes[index:index + self.thread_size]))
            self.save_new_assets()

    async def call_multiple_requests(self, codes):
        coros = [self.get_new_asset(code) for code in codes]
        await asyncio.gather(*coros)
            
    async def get_asset_codes(self):
        url = 'https://console.hgbrasil.com/documentation/finance/symbols'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                sel = Selector(await response.text())
                codes = sel.xpath('//div[@class="card"]//ul//li/code[@class="highlighter-rouge"]/text()').extract()
                self.all_asset_codes = codes

    async def get_new_asset(self, code):
        url = 'https://api.hgbrasil.com/finance/stock_price'
        params = {
            'key': API_KEY,
            'symbol': code,
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params, headers=self.headers) as response:
                    response.raise_for_status()
                    json = await response.json()
                    asset = json['results'][code]
                    self.obtained_assets[code] = asset
        except Exception as e:
            print(f'Erro ao buscar dados da ação {code}: {e}')

    def save_new_assets(self):
        for code in self.obtained_assets:
            asset = self.obtained_assets[code]
            try:
                asset_obj = Asset.objects.create(
                    code = asset['symbol'],
                    name = asset['name'],
                    company_name = asset['company_name'],
                    document = asset['document'],
                    description = asset['description'],
                    website = asset['website'],
                    region = asset['region'],
                    market_time_open = datetime.time(int(asset['market_time']['open'].split(':')[0]), int(asset['market_time']['open'].split(':')[1])),
                    market_time_close = datetime.time(int(asset['market_time']['close'].split(':')[0]), int(asset['market_time']['close'].split(':')[1])),
                    market_time_timezone = int(asset['market_time']['timezone']),
                    market_cap = asset['market_cap'] if 'market_cap' in asset else None,
                )
                AssetPrice.objects.create(
                    asset = asset_obj,
                    price = float(asset['price']),
                    currency = asset['currency'],
                    change_percent = asset['currency'],
                )
                print(f'Ação criada: "{code}"')
            except Exception as e:
                raise Exception(f'Erro ao salvar ação {code}: {e}')

    def update_data(self):
        print(f'{datetime.datetime.now()} - Atualizando valores das ações...')
        assets_monitoring = AssetMonitoring.objects.all()
        assets_id_list = assets_monitoring.values_list('asset').distinct()[:4]
        assets_codes = [item.code for item in Asset.objects.filter(id__in=assets_id_list)]
        self.update_assets(assets_codes)
        print(f'{datetime.datetime.now()} - Atualização encerrada.')


    def update_assets(self, assets_codes):
        for index in range(0, len(assets_codes), self.thread_size):
            self.updated_assets = dict()
            asyncio.run(self.call_multiple_requests(assets_codes[index:index + self.thread_size]))
            self.save_updated_assets()

    def save_updated_assets(self):
        for code in self.obtained_assets:
            asset = self.obtained_assets[code]
            try:
                asset_obj = Asset.objects.get(code = code)
                AssetPrice.objects.create(
                    asset = asset_obj,
                    price = float(asset['price']),
                    currency = asset['currency'],
                    change_percent = asset['change_percent'],
                )
                print(f'Preço da ação atualizado: "{code}"')
            except Exception as e:
                raise Exception(f'Erro ao salvar ação {code}: {e}')
