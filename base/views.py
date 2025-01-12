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

class addCategory(generics.CreateAPIView):
    """
    API view to create a new category.
    """
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def create(self, request, *args, **kwargs):
        """
        Override create method to return a custom success message on category creation.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        response_data = {
            'message': 'Category created successfully.',
            'data': serializer.data
        }
        return Response(response_data, status=status.HTTP_201_CREATED)

class showCategory(generics.RetrieveAPIView):
    """
    API view to retrieve a single category by its slug.
    """
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    queryset = Category.objects.all()

    def retrieve(self, request, *args, **kwargs):
        """
        Override retrieve method to add a custom success message.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        response_data = {
            'message': 'Category retrieved successfully.',
            'data': serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)

class editCategory(generics.UpdateAPIView):
    """
    API view to update an existing category by its slug.
    """
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    queryset = Category.objects.all()

    def update(self, request, *args, **kwargs):
        """
        Override update method to return a custom success message.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        response_data = {
            'message': 'Category updated successfully.',
            'data': serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)