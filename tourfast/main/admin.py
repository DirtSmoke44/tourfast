from django.contrib import admin
from .models import Country, Clients, Hotel, Tour, Booking, Buyer, Contracts, Transaction

admin.site.register(Country)
admin.site.register(Clients)
admin.site.register(Hotel)
admin.site.register(Tour)
admin.site.register(Booking)
admin.site.register(Buyer)
admin.site.register(Contracts)
admin.site.register(Transaction)


