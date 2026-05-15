"""Mental Health Screening API views."""
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from core.mental_health_engine import (
    run_mental_health_screen, get_screen_questions, crisis_response
)


@api_view(['GET'])
def mental_health_questions(request):
    """Return PHQ-2 and GAD-2 screening questions in the requested language."""
    language = request.query_params.get('language', 'en')
    return Response(get_screen_questions(language))


@api_view(['POST'])
def mental_health_screen(request):
    """
    Run PHQ-2 + GAD-2 screening.
    Body: { phq2_scores: [int, int], gad2_scores: [int, int], language: str }
    """
    phq2_scores = request.data.get('phq2_scores', [0, 0])
    gad2_scores = request.data.get('gad2_scores', [0, 0])
    language    = request.data.get('language', 'en')

    if len(phq2_scores) < 2 or len(gad2_scores) < 2:
        return Response({'error': 'phq2_scores and gad2_scores must each have 2 values.'},
                        status=status.HTTP_400_BAD_REQUEST)

    result = run_mental_health_screen(phq2_scores, gad2_scores, language)
    return Response(result)


@api_view(['GET'])
def mental_health_crisis(request):
    """Return crisis support message."""
    language = request.query_params.get('language', 'en')
    return Response(crisis_response(language))
