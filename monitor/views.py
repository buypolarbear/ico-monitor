from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from .serializers import TokenSerializer, VolumeSerializer
from .models import Token, Volume
from .tasks import import_volumes
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from django.http import JsonResponse

class TokenViewSet(viewsets.ModelViewSet):

    queryset = Token.objects.all().order_by('-modified')
    serializer_class = TokenSerializer

class ListVolume(APIView):
    def get(self, request, pk, format=None):
        token = get_object_or_404(Token, id=pk)
        volumes = token.volumes.all()
        serializer = VolumeSerializer(volumes, many=True)
        return Response(serializer.data)

def update_volumes(request, token_id):
    token = Token.objects.get(pk=token_id)
    import_volumes.delay(token_id, token.address)
    return JsonResponse({"status":"ok"})

def index(request):
    tokens = Token.objects.all()
    return render(request, "index.html", {"tokens": tokens})


def token_view(request, contract):
    token = get_object_or_404(Token, address=contract)

    return render(request, "token.html", {"token": token})
