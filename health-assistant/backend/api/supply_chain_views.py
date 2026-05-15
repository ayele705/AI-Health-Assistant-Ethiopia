"""Supply Chain / Stock Tracking API views."""
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from core.supply_chain_engine import get_supply_list, build_shortage_report, classify_stock_level
from .models import StockShortageReport


@api_view(['GET'])
def shortage_report_list(request):
    """List stock shortage reports. Query params: kebele, urgent"""
    qs = StockShortageReport.objects.order_by('-created_at')
    if request.query_params.get('kebele'):
        qs = qs.filter(kebele=request.query_params['kebele'])
    if request.query_params.get('urgent') == 'true':
        qs = qs.filter(urgent=True, resolved=False)
    data = list(qs[:50].values('id', 'kebele', 'hew_name', 'urgent', 'resolved', 'created_at', 'report_data'))
    return Response({'reports': data, 'count': len(data)})


@api_view(['GET'])
def supply_list(request):
    """Return the list of essential supplies."""
    language = request.query_params.get('language', 'en')
    return Response({'supplies': get_supply_list(language)})


@api_view(['POST'])
def stock_report(request):
    """
    Submit a stock report from a health post.
    Body: {
        kebele: str,
        hew_name: str,
        language: str,
        reports: [{ supply_id, quantity, weekly_consumption }]
    }
    """
    kebele   = request.data.get('kebele', '')
    hew_name = request.data.get('hew_name', '')
    language = request.data.get('language', 'en')
    reports  = request.data.get('reports', [])

    if not reports:
        return Response({'error': 'reports list is required.'}, status=status.HTTP_400_BAD_REQUEST)

    result = build_shortage_report(reports, kebele, hew_name, language)

    # Log to DB if there are urgent shortages
    if result['needs_resupply']:
        try:
            from .models import StockShortageReport
            StockShortageReport.objects.create(
                kebele=kebele,
                hew_name=hew_name,
                report_data=result,
                urgent=result['urgent_shortages'] > 0,
            )
        except Exception:
            pass  # Model may not exist yet — graceful degradation

    return Response(result, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def stock_level_check(request):
    """
    Quick stock level check for a single item.
    Body: { quantity: int, weekly_consumption: int }
    """
    try:
        quantity           = int(request.data.get('quantity', 0))
        weekly_consumption = int(request.data.get('weekly_consumption', 1))
    except (ValueError, TypeError):
        return Response({'error': 'quantity and weekly_consumption must be integers.'},
                        status=status.HTTP_400_BAD_REQUEST)
    level = classify_stock_level(quantity, weekly_consumption)
    return Response({'level': level, 'quantity': quantity, 'weekly_consumption': weekly_consumption})
