from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from tasks.serializers import UserSerializer, GroupSerializer

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from rest_framework import request
from tasks.models import (Date,
                          TreasuryBondFutureMarketByTenYears,
                          BondBuyTransactionByHolding,
                          BondBuyTransactionByType,
                          BondSaleTransactionByHolding,
                          BondSaleTransactionByType,
                          BondNetTransactionByHolding,
                          BondNetTransactionByType
                          )
from tasks.serializers import (TreasuryBondFutureMarketByTenYearsSerializer,
                               BondBuyTransactionByHoldingSerializer,
                               BondBuyTransactionByTypeSerializer,
                               BondSaleTransactionByHoldingSerializer,
                               BondSaleTransactionByTypeSerializer,
                               BondNetTransactionByHoldingSerializer,
                               BondNetTransactionByTypeSerializer
                               )

from datetime import date, timedelta

# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allowa users to be viewed oer edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


@csrf_exempt
@api_view(['GET', 'POST'])
def treasury_bond_future_market_by_ten_years_list(request, format=None):
    """
    List all treasury bond future market info,
    or create a new treasury bond future market info
    :param request:
    :return:
    """
    if request.method == 'GET':
        treasury_bond_future_market_by_ten_years = TreasuryBondFutureMarketByTenYears.objects.all()
        serializer = TreasuryBondFutureMarketByTenYearsSerializer(
            treasury_bond_future_market_by_ten_years, many=True)
        # return JsonResponse(serializer.data, safe=False)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = TreasuryBondFutureMarketByTenYearsSerializer(
            data=data)
        if serializer.is_valid():
            serializer.save()
            # return JsonResponse(serializer.data, status=201)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return JsonResponse(serializer.error, status=400)
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)



@csrf_exempt
@api_view(['GET', 'POST', 'DELETE'])
def treasury_bond_future_market_by_ten_years_detail(request, pk, format=None):
    """
    Retrieve, update or delete a treasury bond future market by ten years instance
    :param request:
    :param pk:
    :return:
    """
    try:
        treasury_bond_future_market_by_ten_years = TreasuryBondFutureMarketByTenYears.objects.get(pk=pk)
    except TreasuryBondFutureMarketByTenYears.DoesNotExist:
        # return HttpResponse(status=404)
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TreasuryBondFutureMarketByTenYearsSerializer(treasury_bond_future_market_by_ten_years)
        # return JsonResponse(serializer.data)
        return Response(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = TreasuryBondFutureMarketByTenYearsSerializer(treasury_bond_future_market_by_ten_years,
                                                                  data=data)
        if serializer.is_valid():
            serializer.save()
            # return JsonResponse(serializer.data)
            return Response(serializer.data)
        # return JsonResponse(serializer.error, status=400)
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        treasury_bond_future_market_by_ten_years.delete()
        # return HttpResponse(status=204)
        return Response(status=status.HTTP_204_NO_CONTENT)


class TreasuryBondFutureMarketByTenYearsList(APIView):
    """
    List all treasury bond future market info,
    or create a new treasury bond future market info
    """
    def get(self, request, format=None):
        treasury_bond_future_market_by_ten_years = TreasuryBondFutureMarketByTenYears.objects.all()
        serializer = TreasuryBondFutureMarketByTenYearsSerializer(
            treasury_bond_future_market_by_ten_years, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TreasuryBondFutureMarketByTenYearsSerializer(
            data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)


class TreasuryBondFutureMarketByTenYearsDetail(APIView):
    """
    Retrieve, update or delete a treasury bond future market by ten years instance
    """
    def get_object(self, pk):
        try:
            return TreasuryBondFutureMarketByTenYears.objects.get(pk=pk)
        except TreasuryBondFutureMarketByTenYears.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        treasury_bond_future_market_by_ten_years = self.get_object(pk)
        serializer = TreasuryBondFutureMarketByTenYearsSerializer(
            treasury_bond_future_market_by_ten_years)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        treasury_bond_future_market_by_ten_years = self.get_object(pk)
        serializer = TreasuryBondFutureMarketByTenYearsSerializer(
            treasury_bond_future_market_by_ten_years, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        treasury_bond_future_market_by_ten_years = self.get_object(pk)
        treasury_bond_future_market_by_ten_years.delete()
        return Response(status=status.HTTP_400_BAD_REQUEST)


class TreasuryBondFutureMarketByTenYearsListMixins(mixins.ListModelMixin,
                                                   mixins.CreateModelMixin,
                                                   generics.GenericAPIView):
    """
    List all treasury bond future market info,
    or create a new treasury bond future market info
    """
    queryset = TreasuryBondFutureMarketByTenYears.objects.all()
    serializer_class = TreasuryBondFutureMarketByTenYearsSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class TreasuryBondFutureMarketByTenYearsDetailMixins(mixins.RetrieveModelMixin,
                                                     mixins.UpdateModelMixin,
                                                     mixins.DestroyModelMixin,
                                                     generics.GenericAPIView):
    """
    Retrieve, update or delete a treasury bond future market by ten years instance
    """
    queryset = TreasuryBondFutureMarketByTenYears.objects.all()
    serializer_class = TreasuryBondFutureMarketByTenYearsSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class TreasuryBondFutureMarketByTenYearsListGeneric(generics.ListCreateAPIView):
    """
    List all treasury bond future market info,
    or create a new treasury bond future market info
    """
    queryset = TreasuryBondFutureMarketByTenYears.objects.all()
    serializer_class = TreasuryBondFutureMarketByTenYearsSerializer


class TreasuryBondFutureMarketByTenYearsDetailGeneric(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a treasury bond future market by ten years instance
    """
    queryset = TreasuryBondFutureMarketByTenYears.objects.all()
    serializer_class = TreasuryBondFutureMarketByTenYearsSerializer


class TreasuryBondFutureMarketByTenYearsViewSet(viewsets.ModelViewSet):
    queryset = TreasuryBondFutureMarketByTenYears.objects.all()
    serializer_class = TreasuryBondFutureMarketByTenYearsSerializer

    @action(detail=False, url_path='current', url_name='current')
    def get_current(self, request):
        current_market = TreasuryBondFutureMarketByTenYears.objects.order_by('-date')[:90:-1]
        serializer = self.get_serializer(current_market, many=True)
        return Response(serializer.data)

    @action(methods=['get'],detail=False, url_path='period', url_name='period')
    def get_period(self, request):
        all_data = TreasuryBondFutureMarketByTenYears.objects.order_by(
            'date').values('date')
        all_data_detail = [each.get('date') for each in all_data]
        first_date = all_data[0].get('date')
        last_date = all_data[len(all_data)-1].get('date')
        from_date = request.query_params['from_date']
        from_date = from_date.replace('-', '')
        from_date = date(int(from_date[:4]), int(from_date[4:6]), int(from_date[6:]))
        if from_date not in all_data_detail:
            trade_date = from_date
            while trade_date not in all_data_detail:
                trade_date += timedelta(days=1)
            from_date_index = all_data_detail.index(trade_date)
        else:
            from_date_index = all_data_detail.index(from_date)
        if from_date_index < 30:
            calculate_from_date = first_date
        else:
            calculate_from_date = all_data_detail[from_date_index-30]
        to_date = request.query_params['to_date']
        to_date = to_date.replace('-','')
        to_date = date(int(to_date[:4]), int(to_date[4:6]), int(to_date[6:]))
        if from_date >= first_date and to_date <= last_date:
            period_market = TreasuryBondFutureMarketByTenYears.objects.filter(
                date__range=[calculate_from_date, to_date])
            serializer = self.get_serializer(period_market, many=True)
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class BondBuyTransactionByHoldingViewSet(viewsets.ModelViewSet):
    queryset = BondBuyTransactionByHolding.objects.all()
    serializer_class = BondBuyTransactionByHoldingSerializer

    @action(detail=False, url_path='current', url_name='current')
    def get_current(self, request):
        current_day = Date.objects.order_by('-date')[0].date
        data = self.queryset.filter(date=current_day).order_by('organization_id')
        serializer = self.get_serializer(data, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False, url_path='date', url_name='date')
    def get_date(self, request):
        all_data = Date.objects.order_by('date').values('date')
        first_date = all_data[0].get('date')
        last_date = all_data[len(all_data)-1].get('date')
        input_date = request.query_params['date']
        input_date = input_date.replace('-', '')
        input_date = date(int(input_date[:4]), int(input_date[4:6]),
                          int(input_date[6:]))
        if first_date <= input_date <= last_date:
            data = self.queryset.filter(date=input_date)
            serializer = self.get_serializer(data, many=True)
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class BondBuyTransactionByTypeViewSet(viewsets.ModelViewSet):
    queryset = BondBuyTransactionByType.objects.all()
    serializer_class = BondBuyTransactionByTypeSerializer

    @action(detail=False, url_path='current', url_name='current')
    def get_current(self, request):
        current_day = Date.objects.order_by('-date')[0].date
        data = self.queryset.filter(date=current_day).order_by('organization_id')
        serializer = self.get_serializer(data, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False, url_path='date', url_name='date')
    def get_date(self, request):
        all_data = Date.objects.order_by('date').values('date')
        first_date = all_data[0].get('date')
        last_date = all_data[len(all_data)-1].get('date')
        input_date = request.query_params['date']
        input_date = input_date.replace('-', '')
        input_date = date(int(input_date[:4]), int(input_date[4:6]),
                          int(input_date[6:]))
        if first_date <= input_date <= last_date:
            data = self.queryset.filter(date=input_date)
            serializer = self.get_serializer(data, many=True)
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class BondSaleTransactionByHoldingViewSet(viewsets.ModelViewSet):
    queryset = BondSaleTransactionByHolding.objects.all()
    serializer_class = BondSaleTransactionByHoldingSerializer

    @action(detail=False, url_path='current', url_name='current')
    def get_current(self, request):
        current_day = Date.objects.order_by('-date')[0].date
        data = self.queryset.filter(date=current_day).order_by('organization_id')
        serializer = self.get_serializer(data, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False, url_path='date', url_name='date')
    def get_date(self, request):
        all_data = Date.objects.order_by('date').values('date')
        first_date = all_data[0].get('date')
        last_date = all_data[len(all_data)-1].get('date')
        input_date = request.query_params['date']
        input_date = input_date.replace('-', '')
        input_date = date(int(input_date[:4]), int(input_date[4:6]),
                          int(input_date[6:]))
        if first_date <= input_date <= last_date:
            data = self.queryset.filter(date=input_date)
            serializer = self.get_serializer(data, many=True)
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class BondSaleTransactionByTypeViewSet(viewsets.ModelViewSet):
    queryset = BondSaleTransactionByType.objects.all()
    serializer_class = BondSaleTransactionByTypeSerializer

    @action(detail=False, url_path='current', url_name='current')
    def get_current(self, request):
        current_day = Date.objects.order_by('-date')[0].date
        data = self.queryset.filter(date=current_day).order_by('organization_id')
        serializer = self.get_serializer(data, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False, url_path='date', url_name='date')
    def get_date(self, request):
        all_data = Date.objects.order_by('date').values('date')
        first_date = all_data[0].get('date')
        last_date = all_data[len(all_data)-1].get('date')
        input_date = request.query_params['date']
        input_date = input_date.replace('-', '')
        input_date = date(int(input_date[:4]), int(input_date[4:6]),
                          int(input_date[6:]))
        if first_date <= input_date <= last_date:
            data = self.queryset.filter(date=input_date)
            serializer = self.get_serializer(data, many=True)
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class BondNetTransactionByHoldingViewSet(viewsets.ModelViewSet):
    queryset = BondNetTransactionByHolding.objects.all()
    serializer_class = BondNetTransactionByHoldingSerializer

    @action(detail=False, url_path='current', url_name='current')
    def get_current(self, request):
        current_day = Date.objects.order_by('-date')[0].date
        data = self.queryset.filter(date=current_day).order_by('organization_id')
        serializer = self.get_serializer(data, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False, url_path='date', url_name='date')
    def get_date(self, request):
        all_data = Date.objects.order_by('date').values('date')
        first_date = all_data[0].get('date')
        last_date = all_data[len(all_data)-1].get('date')
        input_date = request.query_params['date']
        input_date = input_date.replace('-', '')
        input_date = date(int(input_date[:4]), int(input_date[4:6]),
                          int(input_date[6:]))
        if first_date <= input_date <= last_date:
            data = self.queryset.filter(date=input_date)
            serializer = self.get_serializer(data, many=True)
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class BondNetTransactionByTypeViewSet(viewsets.ModelViewSet):
    queryset = BondNetTransactionByType.objects.all()
    serializer_class = BondNetTransactionByTypeSerializer

    @action(detail=False, url_path='current', url_name='current')
    def get_current(self, request):
        current_day = Date.objects.order_by('-date')[0].date
        data = self.queryset.filter(date=current_day).order_by('organization_id')
        serializer = self.get_serializer(data, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False, url_path='date', url_name='date')
    def get_date(self, request):
        all_data = Date.objects.order_by('date').values('date')
        first_date = all_data[0].get('date')
        last_date = all_data[len(all_data)-1].get('date')
        input_date = request.query_params['date']
        input_date = input_date.replace('-', '')
        input_date = date(int(input_date[:4]), int(input_date[4:6]),
                          int(input_date[6:]))
        if first_date <= input_date <= last_date:
            data = self.queryset.filter(date=input_date)
            serializer = self.get_serializer(data, many=True)
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)


