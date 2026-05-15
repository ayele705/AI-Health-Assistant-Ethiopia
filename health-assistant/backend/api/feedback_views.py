"""Feedback & Rating API views."""
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import FeedbackRating
from django.db.models import Avg, Count
from .validators import (
    ValidationError, validate_request,
    sanitize_optional_text, validate_language, validate_rating,
)


@api_view(['POST'])
@validate_request
def submit_feedback_rating(request):
    """
    Submit a feedback rating.
    Body: { session_id, rating (1-5), helpful (bool), comment, language, feature_used }
    """
    rating       = validate_rating(request.data.get('rating'))
    session_id   = sanitize_optional_text(request.data.get('session_id', ''), field='session_id', max_length=100)
    comment      = sanitize_optional_text(request.data.get('comment', ''), field='comment', max_length=500)
    language     = validate_language(request.data.get('language', 'en'))
    feature_used = sanitize_optional_text(request.data.get('feature_used', ''), field='feature_used', max_length=50)
    helpful      = bool(request.data.get('helpful', True))

    fb = FeedbackRating.objects.create(
        session_id=session_id,
        rating=rating,
        helpful=helpful,
        comment=comment,
        language=language,
        feature_used=feature_used,
    )
    return Response({'id': fb.id, 'rating': fb.rating, 'message': 'Thank you for your feedback!'},
                    status=status.HTTP_201_CREATED)


@api_view(['GET'])
@validate_request
def feedback_stats(request):
    """
    Aggregate feedback statistics.
    Query params: feature_used (optional), days (default 30)
    """
    from datetime import timedelta
    from django.utils import timezone
    from django.db.models import Q

    try:
        days = int(request.query_params.get('days', 30))
        if days < 1 or days > 365:
            raise ValidationError('days must be between 1 and 365.', field='days')
    except (ValueError, TypeError):
        raise ValidationError('days must be a whole number.', field='days')

    since = timezone.now() - timedelta(days=days)
    qs = FeedbackRating.objects.filter(created_at__gte=since)

    if request.query_params.get('feature_used'):
        qs = qs.filter(feature_used=request.query_params['feature_used'])

    agg = qs.aggregate(
        avg_rating=Avg('rating'),
        total=Count('id'),
        helpful_count=Count('id', filter=Q(helpful=True)),
    )

    by_feature = list(
        FeedbackRating.objects.filter(created_at__gte=since)
        .values('feature_used')
        .annotate(avg=Avg('rating'), count=Count('id'))
        .order_by('-count')
    )

    by_rating = list(
        qs.values('rating').annotate(count=Count('id')).order_by('rating')
    )

    return Response({
        'period_days': days,
        'total_ratings': agg['total'] or 0,
        'average_rating': round(agg['avg_rating'] or 0, 2),
        'helpful_count': agg['helpful_count'] or 0,
        'by_feature': by_feature,
        'by_rating': by_rating,
    })
