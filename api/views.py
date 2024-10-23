from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from .services.nutritionix import NutritionixService
from datetime import datetime

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)

    def get_permissions(self):
        if self.action == 'create':
            return []
        return [IsAuthenticated()]

    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['put'])
    def update_calories_goal(self, request):
        profile = request.user.profile
        profile.daily_calorie_goal = request.data.get('daily_calorie_goal', 2000)
        profile.save()
        return Response({'status': 'calories goal updated'})

class MealViewSet(viewsets.ModelViewSet):
    serializer_class = MealSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['date', 'within_goal']
    ordering_fields = ['date', 'time', 'calories']
    ordering = ['-date', '-time']

    def get_queryset(self):
        if self.request.user.is_staff:
            return Meal.objects.all()
        return Meal.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        nutritionix = NutritionixService()
        calories = serializer.validated_data.get('calories')
        
        if not calories:
            description = serializer.validated_data.get('description')
            calories = nutritionix.get_calories(description)

        # Calculate if within daily goal
        date = serializer.validated_data.get('date')
        daily_meals = Meal.objects.filter(
            user=self.request.user,
            date=date
        )
        daily_total = sum(meal.calories or 0 for meal in daily_meals)
        within_goal = (daily_total + (calories or 0)) <= self.request.user.profile.daily_calorie_goal

        serializer.save(
            user=self.request.user,
            calories=calories,
            within_goal=within_goal
        )