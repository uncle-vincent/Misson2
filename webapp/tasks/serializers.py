from django.contrib.auth.models import User, Group
from rest_framework import serializers
from tasks.models import (Organization,
                          TreasuryBondFutureMarketByTenYears,
                          BondBuyTransactionByHolding,
                          BondBuyTransactionByType,
                          BondSaleTransactionByHolding,
                          BondSaleTransactionByType,
                          BondNetTransactionByHolding,
                          BondNetTransactionByType)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class TreasuryBondFutureMarketByTenYearsSerializerOld(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    date = serializers.DateField(required=True)
    security_name = serializers.CharField(required=True)
    open_price = serializers.FloatField()
    low_price = serializers.FloatField()
    high_price = serializers.FloatField()
    close_price = serializers.FloatField()
    volume = serializers.FloatField()
    amount = serializers.FloatField()
    change = serializers.FloatField()
    percent_change = serializers.FloatField()
    open_interest = serializers.FloatField()
    open_interest_change = serializers.FloatField()

    def create(self, validate_data):
        """
        Create and return a new `TreasuryBondFutureMarketByTenYearsSerializer`,
        given the validated data.
        :param validate_data:
        :return:
        """
        return TreasuryBondFutureMarketByTenYears.objects.create(**validate_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `TreasuryBondFutureMarketByTenYearsSerializer` instance,
        given the validated data.
        :param instance:
        :param validated_data:
        :return:
        """
        instance.date = validated_data.get('date', instance.date)
        instance.security_name = validated_data.get('security_name', instance.security_name)
        instance.open_price = validated_data.get('open_price', instance.open_price)
        instance.low_price = validated_data.get('low_price', instance.low_price)
        instance.high_price = validated_data.get('high_price', instance.high_price)
        instance.close_price = validated_data.get('close_price', instance.close_price)
        instance.volume = validated_data.get('volume', instance.volume)
        instance.amount = validated_data.get('amount', instance.amount)
        instance.change = validated_data.get('change', instance.change)
        instance.percent_change = validated_data.get('percent_change', instance.percent_change)
        instance.open_interest = validated_data.get('open_interest', instance.open_interest)
        instance.open_interest_change = validated_data.get('open_interest_change', instance.open_interest_change)
        instance.save()
        return instance


class TreasuryBondFutureMarketByTenYearsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TreasuryBondFutureMarketByTenYears
        fields = ('id', 'date', 'open_price', 'low_price', 'high_price', 'close_price',
                  'volume', 'amount', 'change', 'percent_change', 'open_interest', 'open_interest_change')


class BondBuyTransactionByHoldingSerializer(serializers.HyperlinkedModelSerializer):
    organization_name = serializers.CharField(source='organization.name')

    class Meta:
        model = BondBuyTransactionByHolding
        fields = ('id', 'date', 'organization_name', 'one_year', 'one_to_three_years')


class BondBuyTransactionByTypeSerializer(serializers.HyperlinkedModelSerializer):
    organization_name = serializers.CharField(source='organization.name')

    class Meta:
        model = BondBuyTransactionByType
        fields = ('id', 'date', 'organization_name', 'policy_financial_bond', 'treasury_bond')


class BondSaleTransactionByHoldingSerializer(serializers.HyperlinkedModelSerializer):
    organization_name = serializers.CharField(source='organization.name')

    class Meta:
        model = BondSaleTransactionByHolding
        fields = ('id', 'date', 'organization_name', 'one_year', 'one_to_three_years')


class BondSaleTransactionByTypeSerializer(serializers.HyperlinkedModelSerializer):
    organization_name = serializers.CharField(source='organization.name')

    class Meta:
        model = BondSaleTransactionByType
        fields = ('id', 'date', 'organization_name', 'policy_financial_bond', 'treasury_bond')


class BondNetTransactionByHoldingSerializer(serializers.HyperlinkedModelSerializer):
    organization_name = serializers.CharField(source='organization.name')

    class Meta:
        model = BondSaleTransactionByHolding
        fields = ('id', 'date', 'organization_name', 'one_year', 'one_to_three_years')


class BondNetTransactionByTypeSerializer(serializers.HyperlinkedModelSerializer):
    organization_name = serializers.CharField(source='organization.name')

    class Meta:
        model = BondSaleTransactionByType
        fields = ('id', 'date', 'organization_name', 'policy_financial_bond', 'treasury_bond')
