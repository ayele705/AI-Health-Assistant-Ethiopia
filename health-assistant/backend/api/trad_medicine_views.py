"""Traditional Medicine Knowledge Base API views."""
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from core.trad_medicine_engine import search_remedies, get_remedy_by_id, check_interactions


@api_view(['GET'])
def trad_medicine_search(request):
    q    = request.query_params.get('q', '').strip()
    lang = request.query_params.get('language', 'en')
    if not q:
        return Response({'error': 'Query parameter q is required.'}, status=status.HTTP_400_BAD_REQUEST)
    results = search_remedies(q, lang)
    return Response({'remedies': results, 'count': len(results), 'query': q})


@api_view(['GET'])
def trad_medicine_detail(request, remedy_id):
    lang   = request.query_params.get('language', 'en')
    remedy = get_remedy_by_id(remedy_id, lang)
    if not remedy:
        return Response({'error': 'Remedy not found.'}, status=status.HTTP_404_NOT_FOUND)
    return Response(remedy)


@api_view(['POST'])
def check_interactions(request):
    remedies     = request.data.get('remedies', [])
    medications  = request.data.get('medications', [])
    lang         = request.data.get('language', 'en')
    if not remedies:
        return Response({'error': 'remedies list is required.'}, status=status.HTTP_400_BAD_REQUEST)
    result = check_interactions(remedies, medications, lang)
    return Response(result)
