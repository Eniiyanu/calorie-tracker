from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Meal, UserProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(user=user)
        return user

class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = '__all__'
        read_only_fields = ('user', 'within_goal')

# api/views.py
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