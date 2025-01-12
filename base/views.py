from base.models import *
from base.serializers import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

class getCategories(APIView):
    """
    View to list all categories or filter them if needed in the future.
    """
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class addCategory(APIView):
    """
    View to create a new Category.
    """
    def post(self, request, *args, **kwargs):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class showCategory(APIView):
    """
    View to retrieve a specific Category by slug.
    """
    def get(self, request, slug, *args, **kwargs):
        category = get_object_or_404(Category, slug=slug)
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)

class editCategory(APIView):
    """
    View to update a specific Category by slug.
    """
    def put(self, request, slug, *args, **kwargs):
        category = get_object_or_404(Category, slug=slug)
        serializer = CategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class deleteCategory(APIView):
    """
    View to delete a specific Category by slug.
    """
    def delete(self, request, slug, *args, **kwargs):
        category = get_object_or_404(Category, slug=slug)
        category.delete()
        return Response({'detail': 'Category deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)