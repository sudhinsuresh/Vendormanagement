
from django.urls import path
# from .views import (VendorListCreateView)
from VendorApp import views
urlpatterns = [

    #vendor--get,post,put,delele
    path('api/vendors',views.VendorListCreateView.as_view(),name="CreatevenderListView"),
    path('api/vendors/<int:pk>/',views.VendorListCreateDeleteUpdate.as_view(),name="VendorUpdateDelete"),

    #purchase-get,post,ut,delete
    path('api/purchase_orders',views.PurchaseListCreateView.as_view(),name="CreatePurchaseOrder"),
    path('api/purchase_orders/<int:pk>/',views.VendorListCreateDeleteUpdate.as_view(),name="PurchaseUpdatedelete"),

    #vendor-performanceVendorPerformanceView
    path('api/vendors/<int:vendor_id>/performance',views.vendor_performance,name="VendorperformaceView")
    
    
]