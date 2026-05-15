"""Nutrition Counseling API views."""
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from core.nutrition_engine import (
    get_iycf_guidance, get_micronutrient_guidance,
    get_therapeutic_feeding_protocol, assess_nutrition_risk
)


@api_view(['GET'])
def iycf_guidance(request):
    """
    Return IYCF guidance for a child's age.
    Query params: age_months (int), language
    """
    try:
        age_months = int(request.query_params.get('age_months', 0))
    except ValueError:
        return Response({'error': 'age_months must be an integer.'}, status=status.HTTP_400_BAD_REQUEST)
    language = request.query_params.get('language', 'en')
    return Response(get_iycf_guidance(age_months, language))


@api_view(['GET'])
def micronutrient_guidance_view(request):
    """
    Return guidance for a micronutrient deficiency.
    Query params: deficiency (iron_deficiency|vitamin_a_deficiency|zinc_deficiency), language
    """
    deficiency = request.query_params.get('deficiency', '')
    language   = request.query_params.get('language', 'en')
    if not deficiency:
        return Response({'error': 'deficiency parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)
    result = get_micronutrient_guidance(deficiency, language)
    if not result:
        return Response({'error': 'Deficiency type not found.'}, status=status.HTTP_404_NOT_FOUND)
    return Response(result)


@api_view(['GET'])
def therapeutic_feeding_view(request):
    """
    Return therapeutic feeding protocol.
    Query params: status (SAM|MAM), language
    """
    nutrition_status = request.query_params.get('status', '').upper()
    language         = request.query_params.get('language', 'en')
    if nutrition_status not in ('SAM', 'MAM'):
        return Response({'error': 'status must be SAM or MAM.'}, status=status.HTTP_400_BAD_REQUEST)
    return Response(get_therapeutic_feeding_protocol(nutrition_status, language))


@api_view(['POST'])
def nutrition_risk_assess(request):
    """
    Quick nutrition risk assessment.
    Body: { age_months, muac_cm (optional), breastfed (optional), language }
    """
    try:
        age_months = int(request.data.get('age_months', 0))
    except ValueError:
        return Response({'error': 'age_months must be an integer.'}, status=status.HTTP_400_BAD_REQUEST)

    muac_cm   = request.data.get('muac_cm')
    breastfed = request.data.get('breastfed')
    language  = request.data.get('language', 'en')

    result = assess_nutrition_risk(
        age_months=age_months,
        muac_cm=float(muac_cm) if muac_cm is not None else None,
        breastfed=breastfed,
        language=language,
    )
    return Response(result)
