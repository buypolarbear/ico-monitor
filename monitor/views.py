from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from.serializers import TokenSerializer
from .models import Token


class TokenViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Token.objects.all().order_by('-modified')
    serializer_class = TokenSerializer


def index(request):
    tokens = Token.objects.all()
    return render(request, "index.html", {"tokens": tokens})


def token_view(request, contract):
    token_info = get_object_or_404(Token, contract=contract)
    return render(request, "token.html", {"token_info": token_info})
