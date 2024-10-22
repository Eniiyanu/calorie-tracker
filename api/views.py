from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Meal
from .serializers import MealSerializer
from .permissions import IsOwnerOrAdmin

class MealViewSet(viewsets.ModelViewSet):
    serializer_class = MealSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Meal.objects.all()
        return Meal.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
