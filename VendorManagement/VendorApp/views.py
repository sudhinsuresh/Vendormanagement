from django.shortcuts import render
from rest_framework  import generics
from .serializers import VendorSerializer,PurchaseOrderSerializer
from .models import Vendor,PurchaseOrder,HistoricalPerformance
from rest_framework.response import Response
from django.utils import timezone
from rest_framework import status
from django.db.models import Avg, F
from django.db import models
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from datetime import timedelta
class VendorListCreateView(generics.ListCreateAPIView):
    queryset=Vendor.objects.all()
    serializer_class=VendorSerializer


class VendorListCreateDeleteUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset=Vendor.objects.all()
    serializer_class=VendorSerializer


class PurchaseListCreateView(generics.ListCreateAPIView):
    queryset=PurchaseOrder.objects.all()
    serializer_class=PurchaseOrderSerializer

class PurchaseCreateDeleteUpdate(generics.RetrieveDestroyAPIView):
    queryset=PurchaseOrder.objects.all()
    serializer_class=PurchaseOrderSerializer



    


@api_view(['GET'])
def vendor_performance(request, vendor_id):
    vendor = get_object_or_404(Vendor, pk=vendor_id)

    # On-Time Delivery Rate
    completed_orders = vendor.purchaseorder_set.filter(status='completed')
    on_time_deliveries = completed_orders.filter(delivery_date__lte=timezone.now())
    on_time_delivery_rate = (on_time_deliveries.count() / completed_orders.count()) * 100 if completed_orders.count() > 0 else 0.0

    # Quality Rating Average
    completed_orders_with_rating = completed_orders.filter(quality_rating__isnull=False)
    quality_rating_avg = completed_orders_with_rating.aggregate(Avg('quality_rating'))['quality_rating__avg'] or 0.0

    # Average Response Time
    acknowledged_orders = vendor.purchaseorder_set.filter(acknowledgment_date__isnull=False)
    response_times = acknowledged_orders.annotate(
        response_time=models.ExpressionWrapper(
            F('acknowledgment_date') - F('issue_date'),
            output_field=models.DurationField()
        )
    )
    average_response_time_timedelta = response_times.aggregate(Avg('response_time'))['response_time__avg'] or timedelta(seconds=0)
    average_response_time_seconds = average_response_time_timedelta.total_seconds()

    # Fulfilment Rate
    all_orders = vendor.purchaseorder_set.all()
    fulfilled_orders = all_orders.filter(status='completed', issue_date__lte=timezone.now())
    fulfillment_rate = (fulfilled_orders.count() / all_orders.count()) * 100 if all_orders.count() > 0 else 0.0

    performance_data = {
        'on_time_delivery_rate': on_time_delivery_rate,
        'quality_rating_avg': quality_rating_avg,
        'average_response_time': average_response_time_seconds,
        'fulfillment_rate': fulfillment_rate,
    }

    # Create HistoricalPerformance record
    HistoricalPerformance.objects.create(
        vendor=vendor,
        date=timezone.now(),
        on_time_delivery_rate=on_time_delivery_rate,
        quality_rating_avg=quality_rating_avg,
        average_response_time=average_response_time_seconds,
        fulfillment_rate=fulfillment_rate
    )

    return Response(performance_data, status=status.HTTP_200_OK)