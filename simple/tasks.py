import xlrd
import os
from datetime import date

FILE_PATH = '/Users/vshao/Documents/self/wangzong/stocks_historic_data'

ORGANIZATIONS = ['Large Commercial Banks/Policy Banks',
                 'Joint Stock Commercial Banks',
                 'Urban Commercial Banks',
                 'Rural financial institutions',
                 'Securities companies and products',
                 'The insurance companies and products',
                 'Fund companies and products',
                 'Trust companies and products',
                 'Wealth management products',
                 'Foreign institutions',
                 'Others']

BUSINESS_BY_TYPE = {1: 'Treasury Bond', 2: 'Policy Financial Bond'}
BUSINESS_BY_HOLDING = {1: 'one year', 2: 'one to three years'}
BUY_TRANSACTION_BOND_ROWS = [each for each in range(5, 16)]
BUY_TRANSACTION_HOLDING_ROWS = [each for each in range(21, 32)]
SALE_TRANSACTION_BOND_ROWS = [each for each in range(37, 48)]
SALE_TRANSACTION_HOLDING_ROWS = [each for each in range(53, 64)]
NET_TRANSACTION_BOND_ROWS = [each for each in range(69, 80)]
NET_TRANSACTION_HOLDING_ROWS = [each for each in range(85, 96)]



def create_bond_record(file_name):
    pass


def get_all_files():
    os.chdir(FILE_PATH)
    files = os.listdir(FILE_PATH)
    return files


def parse_xls_file(file_name):
    transaction = {}
    with xlrd.open_workbook(file_name) as workbook:
        data_sheet = workbook.sheets()[0]
        for i in range(len(ORGANIZATIONS)):
            buy_transaction_bond = [
                check_value(data_sheet.cell(BUY_TRANSACTION_BOND_ROWS[i], 1).value),
                check_value(data_sheet.cell(BUY_TRANSACTION_BOND_ROWS[i], 2).value)]
            buy_transaction_hoding = [
                check_value(data_sheet.cell(BUY_TRANSACTION_HOLDING_ROWS[i], 1).value),
                check_value(data_sheet.cell(BUY_TRANSACTION_HOLDING_ROWS[i], 2).value)]
            sale_transaction_bond = [
                check_value(data_sheet.cell(SALE_TRANSACTION_BOND_ROWS[i], 1).value),
                check_value(data_sheet.cell(SALE_TRANSACTION_BOND_ROWS[i], 2).value)]
            sale_transaction_holding = [
                check_value(data_sheet.cell(SALE_TRANSACTION_HOLDING_ROWS[i], 1).value),
                check_value(data_sheet.cell(SALE_TRANSACTION_HOLDING_ROWS[i], 2).value)]
            net_transaction_bond = [
                check_value(data_sheet.cell(SALE_TRANSACTION_HOLDING_ROWS[i], 1).value),
                check_value(data_sheet.cell(SALE_TRANSACTION_HOLDING_ROWS[i], 2).value)]
            net_transaction_hoding = [
                check_value(data_sheet.cell(SALE_TRANSACTION_HOLDING_ROWS[i], 1).value),
                check_value(data_sheet.cell(SALE_TRANSACTION_HOLDING_ROWS[i], 2).value)]
            result = [buy_transaction_bond, buy_transaction_hoding,
                      sale_transaction_bond, sale_transaction_holding,
                      net_transaction_bond, net_transaction_hoding]
            transaction.setdefault(ORGANIZATIONS[i], result)
    return transaction


def parse_xls_file_date(file_name):
    date_str = (file_name.split('.')[0]).split('_')[-1]
    real_date = date(int(date_str[:4]), int(date_str[4:6]), int(date_str[6:]))
    return real_date


def check_value(value):
    if isinstance(value, str):
        return 0
    else:
        return value


if __name__ == '__main__':
    file_list = get_all_files()
    file = file_list[2]
    print(file)
    print(parse_xls_file_date(file))
    result = parse_xls_file(file)
    #print(result)
    for key, value in result.items():
        print('{}:{}'.format(key, value))
        print()

