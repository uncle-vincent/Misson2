from django.db import models

# Create your models here.


class Organization(models.Model):
    organization_id = models.IntegerField(unique=True, primary_key=True)
    name = models.CharField(max_length=256)

    def __str__(self):
        return 'Organization - {}'.format(self.name)


class BondBuyTransactionByType(models.Model):
    organization = models.ForeignKey('Organization',
                                     on_delete=models.CASCADE,
                                     related_name='bond_buy_type')
    date = models.DateField()
    treasury_bond = models.FloatField()
    policy_financial_bond = models.FloatField()


class BondBuyTransactionByHolding(models.Model):
    organization = models.ForeignKey('Organization',
                                     on_delete=models.CASCADE,
                                     related_name='bond_buy_holding')
    date = models.DateField()
    one_year = models.FloatField()
    one_to_three_years = models.FloatField()


class BondSaleTransactionByType(models.Model):
    organization = models.ForeignKey('Organization',
                                     on_delete=models.CASCADE,
                                     related_name='bond_sale_type')
    date = models.DateField()
    treasury_bond = models.FloatField()
    policy_financial_bond = models.FloatField()


class BondSaleTransactionByHolding(models.Model):
    organization = models.ForeignKey('Organization',
                                     on_delete=models.CASCADE,
                                     related_name='bond_sale_holding')
    date = models.DateField()
    one_year = models.FloatField()
    one_to_three_years = models.FloatField()


class BondNetTransactionByType(models.Model):
    organization = models.ForeignKey('Organization',
                                     on_delete=models.CASCADE,
                                     related_name='bond_net_type')
    date = models.DateField()
    treasury_bond = models.FloatField()
    policy_financial_bond = models.FloatField()


class BondNetTransactionByHolding(models.Model):
    organization = models.ForeignKey('Organization',
                                     on_delete=models.CASCADE,
                                     related_name='bond_net_holding')
    date = models.DateField()
    one_year = models.FloatField()
    one_to_three_years = models.FloatField()


class Date(models.Model):
    date = models.DateField(unique=True)


class TreasuryBondFutureMarketByTenYears(models.Model):
    date = models.DateField()
    security_name = models.CharField(max_length=256)
    open_price = models.FloatField()
    low_price = models.FloatField()
    high_price = models.FloatField()
    close_price = models.FloatField()
    volume = models.FloatField()
    amount = models.IntegerField()
    change = models.FloatField()
    percent_change = models.FloatField()
    open_interest = models.FloatField()
    open_interest_change = models.FloatField()
