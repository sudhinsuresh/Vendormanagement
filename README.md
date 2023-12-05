#git clone https://github.com/your_username/vendor-management-api.git

#python -m venv myenv
#myenv\Scripts\activate

#cd VendorManagement  
#pip install -r requirements.txt

#python manage.py makemigrations
#python manage.py migrate

#python manage.py createsuperuser

API Endpoints
----------------
Vendors
-------------
#List/Create Vendors: (GET/POST) /api/vendors
#Retrieve/Update/Delete Vendor: (GET/PUT/DELETE) /api/vendors/{vendor_code}/
Purchase Orders
-----------------
#List/Create Purchase Orders: (GET/POST) /api/purchase_orders
#Retrieve/Delete Purchase Order: (GET/DELETE) /api/purchase_orders/{vendor_code}/
#Vendor Performance Metrics
--------------------------
#Retrieve Vendor Performance Metrics: (GET) /api/vendors/<vendor_id>/performance
