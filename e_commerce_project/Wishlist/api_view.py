from .serializers import WishlistSerializer
from .models import Wishlist
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated



class WishlistView(viewsets.ModelViewSet):
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        user = self.request.user
        return Wishlist.objects.filter(user=user)
        
        