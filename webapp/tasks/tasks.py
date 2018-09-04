import sys, os, django
sys.path.append('../')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webapp.settings")
django.setup()
from tasks.models import (Organization,
                          BondBuyTransactionByType,
                          BondBuyTransactionByHolding,
                          BondSaleTransactionByType,
                          BondSaleTransactionByHolding,
                          BondNetTransactionByType,
                          BondNetTransactionByHolding,
                          Date,
                          TreasuryBondFutureMarketByTenYears)
import xlrd
from xlrd import xldate
from datetime import date


FILE_PATH = '/Users/vshao/Documents/self/wangzong/stocks_historic_data'
FILE_TREASURY_BOND_FUTURE_PATH ='/Users/vshao/Documents/self/wangzong/treasury_bond_future'

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


def create_bond_record(date, transaction):
    date_list = Date.objects.all()
    if date not in date_list:
        Date(date=date).save()
        for each in ORGANIZATIONS:
            org_id = Organization.objects.all().filter(name=each)[0]
            BondBuyTransactionByType(
                organization=org_id,
                date=date,
                treasury_bond=transaction.get(each)[0][0],
                policy_financial_bond=transaction.get(each)[0][1]).save()
            BondBuyTransactionByHolding(
                organization=org_id,
                date=date,
                one_year=transaction.get(each)[1][0],
                one_to_three_years=transaction.get(each)[1][1]).save()
            BondSaleTransactionByType(
                organization=org_id,
                date=date,
                treasury_bond=transaction.get(each)[2][0],
                policy_financial_bond=transaction.get(each)[2][1]).save()
            BondSaleTransactionByHolding(
                organization=org_id,
                date=date,
                one_year=transaction.get(each)[3][0],
                one_to_three_years=transaction.get(each)[3][1]).save()
            BondNetTransactionByType(
                organization=org_id,
                date=date,
                treasury_bond=transaction.get(each)[4][0],
                policy_financial_bond=transaction.get(each)[4][1]).save()
            BondNetTransactionByHolding(
                organization=org_id,
                date=date,
                one_year=transaction.get(each)[5][0],
                one_to_three_years=transaction.get(each)[5][1]).save()

    pass


def create_treasury_bond_future_market_record_by_10_years(transaction):
    for each in transaction:
        TreasuryBondFutureMarketByTenYears(date=each.get('date'),
                                           security_name= each.get('security_name'),
                                           open_price=each.get('open_price'),
                                           low_price=each.get('low_price'),
                                           high_price=each.get('high_price'),
                                           close_price=each.get('close_price'),
                                           volume=each.get('volume'),
                                           amount=each.get('amount'),
                                           change=each.get('change'),
                                           percent_change=each.get('percent_change'),
                                           open_interest=each.get('open_interest'),
                                           open_interest_change= each.get('open_interest_change')
                                           ).save()


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
                check_value(data_sheet.cell(NET_TRANSACTION_BOND_ROWS[i], 1).value),
                check_value(data_sheet.cell(NET_TRANSACTION_BOND_ROWS[i], 2).value)]
            net_transaction_hoding = [
                check_value(data_sheet.cell(NET_TRANSACTION_HOLDING_ROWS[i], 1).value),
                check_value(data_sheet.cell(NET_TRANSACTION_HOLDING_ROWS[i], 2).value)]
            result = [buy_transaction_bond, buy_transaction_hoding,
                      sale_transaction_bond, sale_transaction_holding,
                      net_transaction_bond, net_transaction_hoding]
            transaction.setdefault(ORGANIZATIONS[i], result)
    return transaction


def parse_xls_file_date(file_name):
    date_str = (file_name.split('.')[0]).split('_')[-1]
    real_date = date(int(date_str[:4]), int(date_str[4:6]), int(date_str[6:]))
    return real_date


def parse_treasury_bond_future_market_by_type(file_name, sec_name):
    output = []
    os.chdir(FILE_TREASURY_BOND_FUTURE_PATH)
    with xlrd.open_workbook(file_name) as workbook:
        data_sheet = workbook.sheets()[0]
        for i in range(4, data_sheet.nrows):
            date_tuple = xldate.xldate_as_tuple(data_sheet.cell(i,0).value,0)
            trade_date = date(date_tuple[0], date_tuple[1], date_tuple[2])
            output_by_day = {'date': trade_date,
                             'security_name': sec_name,
                             'open_price': check_value(data_sheet.cell(i, 2).value),
                             'low_price': check_value(data_sheet.cell(i, 3).value),
                             'high_price': check_value(data_sheet.cell(i, 4).value),
                             'close_price':  check_value(data_sheet.cell(i, 5).value),
                             'volume': check_value(data_sheet.cell(i, 6).value),
                             'amount': check_value(data_sheet.cell(i, 7).value),
                             'change': check_value(data_sheet.cell(i, 8).value),
                             'percent_change': check_value(data_sheet.cell(i, 9).value),
                             'open_interest': check_value(data_sheet.cell(i, 10).value),
                             'open_interest_change': check_value(data_sheet.cell(i, 11).value)
                            }
            output.append(output_by_day)
    return output




def check_value(value):
    if isinstance(value, str):
        return 0
    else:
        return value


if __name__ == "__main__":
    '''
    print('test')
    file_list = get_all_files()
    # file = file_list[1]
    file_candidate = [each for each in file_list if each.endswith('20180530.xls')]
    file = file_candidate[0]
    print(file[0])
    date = parse_xls_file_date(file)
    print(date)
    result = parse_xls_file(file)
    print(result)
    create_bond_record(date, result)


    # print(result)
    for key, value in result.items():
        print('{}:{}'.format(key, value))
        print()
    '''


    print('make treasury bond future market by 10 years')
    result = parse_treasury_bond_future_market_by_type('国债期货行情.xlsx', 'CFFEX10years')
    create_treasury_bond_future_market_record_by_10_years(result)
