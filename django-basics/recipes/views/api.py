from rest_framework.decorators import api_view
from rest_framework.response import Response
from recipes.models import Recipe,Tag
from recipes.serializes import RecipeSerializer,TagSerializer
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from recipes.permissions import IsOwner
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from rest_framework import status

class RecipeApiPagination(PageNumberPagination):
    page_size = 5
    def get_next_link(self):
            url = super().get_next_link()
            if url:
                return url.replace('http://', 'https://')
            return None
        
    def get_previous_link(self):
        url = super().get_previous_link()
        if url:
            return url.replace('http://','https://')
        return None
    

class RecipeApi(ModelViewSet):
    queryset = Recipe.objects.get_recipes_publhised()
    serializer_class = RecipeSerializer
    pagination_class = RecipeApiPagination
    permission_classes = [IsAuthenticatedOrReadOnly,]
    http_method_names = [
        'get','options','head','delete','patch','post'
    ]
    def get_queryset(self):
        query_set = super().get_queryset()
        category_id = self.request.query_params.get("category_id",'')
        if category_id != '' and category_id.isnumeric():
            query_set = query_set.filter(
                category_id = category_id
            )
        return query_set
    
    def get_object(self):
        pk = self.kwargs.get("pk",'')
        print("get object")

        obj = get_object_or_404(
            self.get_queryset(),
            pk=pk
        )
        self.check_object_permissions(self.request,obj=obj)
        return obj
    
    def partial_update(self, request: HttpRequest, *args, **kwargs):

        recipe = self.get_object()
        serializer = RecipeSerializer(
            instance=recipe,
            data=request.data,
            many=False,
            context={'request':request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data
        )
    
    def get_permissions(self):
        if self.request.method in ['PATCH','DELETE']:
            return [IsOwner(),]

        if self.request.method == "POST":
            return [IsOwner(),IsAuthenticatedOrReadOnly(),]
            
        return super().get_permissions()
    
    #post
    def create(self, request:HttpRequest, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    


@api_view()
def tag(request,pk):
    tag = get_object_or_404(
        Tag.objects.all(),
        pk=pk
    )
    serializer = TagSerializer(tag)
    return Response(serializer.data)
