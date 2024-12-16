from rest_framework.decorators import api_view
from rest_framework.response import Response
from recipes.models import Recipe,Tag
from recipes.serializes import RecipeSerializer,TagSerializer
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

class RecipeApiPagination(PageNumberPagination):
    page_size = 10
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
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        query_set = super().get_queryset()
        category_id = self.request.query_params.get("category_id",'')
        if category_id != '' and category_id.isnumeric():
            query_set = query_set.filter(
                category_id = category_id
            )
        return query_set
    
    
    


@api_view()
def tag(request,pk):
    tag = get_object_or_404(
        Tag.objects.all(),
        pk=pk
    )
    serializer = TagSerializer(tag)
    return Response(serializer.data)
