from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .searchConfig import searchEngine


class SearchView(APIView):

    def get(self, request, format=None, **kwargs):
        keywords = request.query_params.get('keywords', None)
        new2old = request.query_params.get('new2old', True)
        new2old = False if new2old == "false" else True
        exclude = request.query_params.get('exclude', None)
        
        keywords = keywords.split(",")
        query_results = searchEngine.search(keywords, new2old, exclude)
        return Response(query_results, status=status.HTTP_200_OK)
