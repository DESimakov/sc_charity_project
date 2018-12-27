from web3 import Web3, HTTPProvider
import json

class CharityShop():
    def __init__(self):
        self.avail_ids = None
        self._load()
        
    def _load(self):
        with open('erc.json', 'r') as outfile:
            ERC20_ABI = json.load(outfile)

        infura_provider = HTTPProvider('https://ropsten.infura.io')
        web3 = Web3([infura_provider])
        self.erc20 = web3.eth.contract(address='0x615936924B49eE87DaE5ff8ef141310a45084eA4', abi=ERC20_ABI)

    def _get_all_id(self):
        i = 0
        ids = []
        while True:
            try:
                ids_i = self.erc20.functions.goods_ids(i).call()
                ids.append(ids_i)
                i += 1
            except:
                break
        return ids

    def _get_avail(self, ids):
        avail = []
        for ids_i in ids:
            status = self.erc20.functions.get_good_stats(ids_i).call()
            if status == 0:
                avail.append(ids_i)
        return avail
    
    def _get_inf(self, ids):
        inform = {}
        for ids_i in ids:
            name = self.erc20.functions.get_good_name(ids_i).call()
            discr = self.erc20.functions.get_good_discr(ids_i).call()
            price = self.erc20.functions.get_good_prices(ids_i).call()
            inform[ids_i] = {'Название': name, 'Описание товара': discr, 'Цена': price}
        return inform
    
    def get_balance(self):
        balance = self.erc20.functions.value().call()
        print('Всего совершенно пожертвований: {} wei.'.format(balance))
    
    def get_information(self):
        self.all_ids = self._get_all_id()
        print('Число товаров: {}.'.format(len(self.all_ids)))
        self.avail_ids = self._get_avail(self.all_ids)
        print('Число доступных товаров: {}.'.format(len(self.avail_ids) if self.avail_ids is not None else 0))
        
        if self.avail_ids is None:
            self.inform = None
        else:
            self.inform = self._get_inf(self.avail_ids)
        
    def print_results(self, max_price=1e9):
        if self.inform is None:
            print('В данный момент все изделия проданы. Возвращайтесь в ближайшее время!')
        else:
            k = 0
            for key, value in self.inform.items():
                if self.inform[key]['Цена'] <= max_price:
                    print('Название товара: {}'.format(self.inform[key]['Название']))
                    print('Описание товара: {}'.format(self.inform[key]['Описание товара']))
                    print('Цена товара: {}'.format(self.inform[key]['Цена']))
                    print('Id товара: {}'.format(key))
                    print('\t')
                    k += 1

            if k == 0:
                print('Ни один из товаров не удовлетворяет условиям поиска.')
                       