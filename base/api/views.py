import imp
from tokenize import group
from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Group
from .serializers import GroupSerializer

@api_view(['GET'])
def get_routes(request):
    routes = [
        'GET /api',
        'GET /api/groups',
        'GET /api/groups/:id'
    ]
    return Response(routes)

@api_view(['GET']) 
def get_groups(request):
    groups = Group.objects.all()
    serializer = GroupSerializer(groups, many=True)
    return Response(serializer.data)

@api_view(['GET']) 
def get_group(request, pk):
    group = Group.objects.get(id=pk)
    serializer = GroupSerializer(group, many=False)
    return Response(serializer.data)