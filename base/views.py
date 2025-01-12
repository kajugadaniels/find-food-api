from base.models import *
from base.serializers import *
from django.db.models import Q
from rest_framework import generics, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError

class getCategories(generics.ListAPIView):
    """
    API view to list all categories.
    Supports optional filtering by passing a query parameter 'name' (case-insensitive partial match).
    """
    serializer_class = CategorySerializer

    def get_queryset(self):
        queryset = Category.objects.all()
        name = self.request.query_params.get('name')
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset

    def list(self, request, *args, **kwargs):
        """
        Override list method to include a custom success message.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        response_data = {
            'message': 'Categories retrieved successfully.',
            'data': serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)