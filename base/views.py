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

class deleteCategory(generics.DestroyAPIView):
    """
    API view to delete a category identified by its slug.
    """
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    queryset = Category.objects.all()

    def destroy(self, request, *args, **kwargs):
        """
        Override destroy method to return a custom success message.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'message': 'Category deleted successfully.'}, status=status.HTTP_200_OK)

class getPlaces(generics.ListAPIView):
    """
    API view to list all places.
    Supports optional filtering by query parameters such as:
    - province (exact match, case-insensitive)
    - district (exact match, case-insensitive)
    - category (using the category's slug)
    - search (searches in address and description)
    """
    serializer_class = PlaceSerializer

    def get_queryset(self):
        queryset = Place.objects.all()
        province = self.request.query_params.get('province')
        district = self.request.query_params.get('district')
        category = self.request.query_params.get('category')
        search = self.request.query_params.get('search')

        if province:
            queryset = queryset.filter(province__iexact=province)
        if district:
            queryset = queryset.filter(district__iexact=district)
        if category:
            queryset = queryset.filter(category__slug=category)
        if search:
            queryset = queryset.filter(
                Q(address__icontains=search) | Q(description__icontains=search)
            )
        return queryset

    def list(self, request, *args, **kwargs):
        """
        Override list method to include a custom success message.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        response_data = {
            'message': 'Places retrieved successfully.',
            'data': serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)

class addPlace(generics.CreateAPIView):
    """
    API view to add a new place.
    The model's save() method handles the creation of an associated User if needed.
    """
    serializer_class = PlaceSerializer
    queryset = Place.objects.all()

    def create(self, request, *args, **kwargs):
        """
        Override create method to handle errors and return a custom success message on place creation.
        """
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
        except ValidationError as ve:
            return Response(
                {'message': 'Error creating place.', 'errors': ve.detail},
                status=status.HTTP_400_BAD_REQUEST
            )

        response_data = {
            'message': 'Place created successfully.',
            'data': serializer.data
        }
        return Response(response_data, status=status.HTTP_201_CREATED)

class showPlace(generics.RetrieveAPIView):
    """
    API view to retrieve a single place by the slug of its associated User.
    """
    serializer_class = PlaceSerializer
    lookup_field = 'user__slug'
    queryset = Place.objects.all()

    def get_object(self):
        """
        Retrieve a Place instance based on the slug of its associated user.
        """
        slug = self.kwargs.get('slug')
        obj = get_object_or_404(Place, user__slug=slug)
        return obj

    def retrieve(self, request, *args, **kwargs):
        """
        Override retrieve method to return a custom success message.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        response_data = {
            'message': 'Place retrieved successfully.',
            'data': serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)

class editPlace(generics.UpdateAPIView):
    """
    API view to update an existing place using the slug of the associated User.
    """
    serializer_class = PlaceSerializer
    lookup_field = 'user__slug'
    queryset = Place.objects.all()

    def get_object(self):
        """
        Retrieve a Place instance based on the user's slug.
        """
        slug = self.kwargs.get('slug')
        obj = get_object_or_404(Place, user__slug=slug)
        return obj

    def update(self, request, *args, **kwargs):
        """
        Override update method to handle errors and return a custom success message.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
        except ValidationError as ve:
            return Response(
                {'message': 'Error updating place.', 'errors': ve.detail},
                status=status.HTTP_400_BAD_REQUEST
            )
        response_data = {
            'message': 'Place updated successfully.',
            'data': serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)