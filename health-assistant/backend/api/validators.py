"""
validators.py — Comprehensive input validation for the AI Health Assistant API.

All validation functions raise ValidationError on failure.
Use the @validate_request decorator to automatically catch and return 400 responses.
"""

import re
import html
import functools
from datetime import date, datetime
from rest_framework.response import Response
from rest_framework import status


# ─────────────────────────────────────────────────────────────────────────────
# Custom Exception
# ─────────────────────────────────────────────────────────────────────────────

class ValidationError(Exception):
    """Raised when any input validation fails."""
    def __init__(self, message, field=None):
        self.message = message
        self.field = field
        super().__init__(message)


# ─────────────────────────────────────────────────────────────────────────────
# Decorator: auto-catch ValidationError and return HTTP 400
# ─────────────────────────────────────────────────────────────────────────────

def validate_request(func):
    """
    Decorator for API view functions.
    Catches ValidationError and returns a structured 400 Bad Request response
    so every endpoint does not need its own try/except block.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValidationError as exc:
            body = {'error': exc.message}
            if exc.field:
                body['field'] = exc.field
            return Response(body, status=status.HTTP_400_BAD_REQUEST)
        except (ValueError, TypeError) as exc:
            return Response(
                {'error': f'Invalid data format: {exc}'},
                status=status.HTTP_400_BAD_REQUEST,
            )
    return wrapper


# ─────────────────────────────────────────────────────────────────────────────
# Text / String Sanitization
# ─────────────────────────────────────────────────────────────────────────────

def sanitize_text(value, field='text', max_length=1000):
    """
    Strip leading/trailing whitespace, escape HTML entities, and enforce a
    maximum length.  Returns the cleaned string.
    Raises ValidationError if the value is empty after stripping.
    """
    if value is None:
        raise ValidationError(f'{field} is required.', field=field)
    cleaned = html.escape(str(value).strip())
    if not cleaned:
        raise ValidationError(f'{field} must not be empty.', field=field)
    if len(cleaned) > max_length:
        raise ValidationError(
            f'{field} must not exceed {max_length} characters (got {len(cleaned)}).',
            field=field,
        )
    return cleaned


def sanitize_optional_text(value, field='text', max_length=500, default=''):
    """
    Like sanitize_text but returns a default value instead of raising when
    the input is empty or None.
    """
    if value is None:
        return default
    cleaned = html.escape(str(value).strip())
    if len(cleaned) > max_length:
        raise ValidationError(
            f'{field} must not exceed {max_length} characters.',
            field=field,
        )
    return cleaned or default


# ─────────────────────────────────────────────────────────────────────────────
# Language
# ─────────────────────────────────────────────────────────────────────────────

SUPPORTED_LANGUAGES = {'en', 'am', 'ti', 'om'}
def validate_language(value, field='language', default='en'):
    """
    Validate that the language code is one of the supported values.
    Returns the validated code, or the default if value is empty/None.
    """
    if not value:
        return default
    code = str(value).strip().lower()
    if code not in SUPPORTED_LANGUAGES:
        raise ValidationError(
            f'Unsupported language "{code}". Supported: {", ".join(sorted(SUPPORTED_LANGUAGES))}.',
            field=field,
        )
    return code


# ─────────────────────────────────────────────────────────────────────────────
# Age
# ─────────────────────────────────────────────────────────────────────────────

def validate_age(value, field='age', min_age=0, max_age=120, default=25):
    """
    Validate that age is an integer between min_age and max_age.
    Returns the integer age, or the default if value is empty/None.
    """
    if value is None or value == '':
        return default
    try:
        age = int(value)
    except (ValueError, TypeError):
        raise ValidationError(f'{field} must be a whole number.', field=field)
    if age < min_age or age > max_age:
        raise ValidationError(
            f'{field} must be between {min_age} and {max_age} (got {age}).',
            field=field,
        )
    return age


# ─────────────────────────────────────────────────────────────────────────────
# Sex / Gender
# ─────────────────────────────────────────────────────────────────────────────

VALID_SEX_VALUES = {'male', 'female', 'unknown'}

def validate_sex(value, field='sex', default='unknown'):
    """
    Validate that sex is one of: male, female, unknown.
    Returns the validated value, or the default if empty/None.
    """
    if not value:
        return default
    val = str(value).strip().lower()
    if val not in VALID_SEX_VALUES:
        raise ValidationError(
            f'{field} must be one of: {", ".join(sorted(VALID_SEX_VALUES))}.',
            field=field,
        )
    return val


# ─────────────────────────────────────────────────────────────────────────────
# Phone Number (Ethiopian format)
# ─────────────────────────────────────────────────────────────────────────────

# Accepts: +251XXXXXXXXX  |  0XXXXXXXXX  |  9XXXXXXXX  (9 digits after country/0 prefix)
_PHONE_RE = re.compile(r'^(\+251|0)?[79]\d{8}$')

def validate_phone(value, field='phone', required=False):
    """
    Validate an Ethiopian phone number.
    Normalises to +251XXXXXXXXX format.
    If required=True, raises when value is empty.
    If required=False, returns '' when value is empty.
    """
    if not value:
        if required:
            raise ValidationError(f'{field} is required.', field=field)
        return ''
    digits = re.sub(r'\s+', '', str(value).strip())
    if not _PHONE_RE.match(digits):
        raise ValidationError(
            f'{field} must be a valid Ethiopian phone number '
            '(e.g. +251912345678 or 0912345678).',
            field=field,
        )
    # Normalise
    if digits.startswith('+251'):
        return digits
    if digits.startswith('0'):
        return '+251' + digits[1:]
    return '+251' + digits


# ─────────────────────────────────────────────────────────────────────────────
# Dates
# ─────────────────────────────────────────────────────────────────────────────

def validate_date_string(value, field='date', allow_future=True, allow_past=True,
                          required=True, default=None):
    """
    Parse and validate a date string in YYYY-MM-DD format.
    Returns a datetime.date object, or default if value is empty and not required.
    """
    if not value:
        if required:
            raise ValidationError(f'{field} is required (YYYY-MM-DD).', field=field)
        return default or date.today()
    try:
        parsed = datetime.strptime(str(value).strip(), '%Y-%m-%d').date()
    except ValueError:
        raise ValidationError(
            f'{field} must be in YYYY-MM-DD format (e.g. 2024-06-15).',
            field=field,
        )
    today = date.today()
    if not allow_future and parsed > today:
        raise ValidationError(f'{field} cannot be a future date.', field=field)
    if not allow_past and parsed < today:
        raise ValidationError(f'{field} cannot be a past date.', field=field)
    return parsed


def validate_past_date(value, field='date', required=True):
    """Convenience wrapper: date must be today or in the past."""
    return validate_date_string(value, field=field, allow_future=False, required=required)


def validate_future_date(value, field='date', required=True):
    """Convenience wrapper: date must be today or in the future."""
    return validate_date_string(value, field=field, allow_past=False, required=required)


# ─────────────────────────────────────────────────────────────────────────────
# Symptoms List
# ─────────────────────────────────────────────────────────────────────────────

def validate_symptoms(value, field='symptoms', min_count=1, max_count=30):
    """
    Validate that symptoms is a non-empty list of non-empty strings.
    Each symptom string is sanitised and length-checked.
    """
    if not value:
        raise ValidationError(
            f'Provide at least {min_count} symptom(s).',
            field=field,
        )
    if not isinstance(value, list):
        raise ValidationError(f'{field} must be a list.', field=field)
    if len(value) < min_count:
        raise ValidationError(
            f'Provide at least {min_count} symptom(s).',
            field=field,
        )
    if len(value) > max_count:
        raise ValidationError(
            f'Too many symptoms — maximum is {max_count}.',
            field=field,
        )
    cleaned = []
    for i, sym in enumerate(value):
        if not isinstance(sym, str) or not sym.strip():
            raise ValidationError(
                f'Symptom at index {i} must be a non-empty string.',
                field=field,
            )
        cleaned.append(html.escape(sym.strip()[:100]))
    return cleaned


# ─────────────────────────────────────────────────────────────────────────────
# Medical Measurements
# ─────────────────────────────────────────────────────────────────────────────

def validate_weight(value, field='weight_kg', required=False):
    """Validate weight in kilograms (0.3 – 500 kg)."""
    if value is None or value == '':
        if required:
            raise ValidationError(f'{field} is required.', field=field)
        return None
    try:
        w = float(value)
    except (ValueError, TypeError):
        raise ValidationError(f'{field} must be a number.', field=field)
    if w < 0.3 or w > 500:
        raise ValidationError(
            f'{field} must be between 0.3 and 500 kg (got {w}).',
            field=field,
        )
    return round(w, 2)


def validate_height(value, field='height_cm', required=False):
    """Validate height in centimetres (20 – 250 cm)."""
    if value is None or value == '':
        if required:
            raise ValidationError(f'{field} is required.', field=field)
        return None
    try:
        h = float(value)
    except (ValueError, TypeError):
        raise ValidationError(f'{field} must be a number.', field=field)
    if h < 20 or h > 250:
        raise ValidationError(
            f'{field} must be between 20 and 250 cm (got {h}).',
            field=field,
        )
    return round(h, 1)


def validate_muac(value, field='muac_cm', required=False):
    """Validate mid-upper arm circumference in centimetres (5 – 50 cm)."""
    if value is None or value == '':
        if required:
            raise ValidationError(f'{field} is required.', field=field)
        return None
    try:
        m = float(value)
    except (ValueError, TypeError):
        raise ValidationError(f'{field} must be a number.', field=field)
    if m < 5 or m > 50:
        raise ValidationError(
            f'{field} must be between 5 and 50 cm (got {m}).',
            field=field,
        )
    return round(m, 1)


def validate_blood_pressure(systolic, diastolic,
                             sys_field='bp_systolic', dia_field='bp_diastolic',
                             required=False):
    """
    Validate systolic (50–300 mmHg) and diastolic (30–200 mmHg) blood pressure.
    Returns (systolic_int, diastolic_int) or (None, None) if both are absent.
    """
    if systolic is None and diastolic is None:
        if required:
            raise ValidationError('Blood pressure (bp_systolic and bp_diastolic) is required.')
        return None, None

    if systolic is None or diastolic is None:
        raise ValidationError(
            'Both bp_systolic and bp_diastolic must be provided together.'
        )
    try:
        sys_val = int(systolic)
        dia_val = int(diastolic)
    except (ValueError, TypeError):
        raise ValidationError('Blood pressure values must be whole numbers.')

    if sys_val < 50 or sys_val > 300:
        raise ValidationError(
            f'{sys_field} must be between 50 and 300 mmHg (got {sys_val}).',
            field=sys_field,
        )
    if dia_val < 30 or dia_val > 200:
        raise ValidationError(
            f'{dia_field} must be between 30 and 200 mmHg (got {dia_val}).',
            field=dia_field,
        )
    if dia_val >= sys_val:
        raise ValidationError(
            'Diastolic pressure must be lower than systolic pressure.',
            field=dia_field,
        )
    return sys_val, dia_val


def validate_glucose(value, field='glucose_mgdl', required=False):
    """Validate blood glucose in mg/dL (10 – 1000)."""
    if value is None or value == '':
        if required:
            raise ValidationError(f'{field} is required.', field=field)
        return None
    try:
        g = float(value)
    except (ValueError, TypeError):
        raise ValidationError(f'{field} must be a number.', field=field)
    if g < 10 or g > 1000:
        raise ValidationError(
            f'{field} must be between 10 and 1000 mg/dL (got {g}).',
            field=field,
        )
    return round(g, 1)


# ─────────────────────────────────────────────────────────────────────────────
# GPS Coordinates
# ─────────────────────────────────────────────────────────────────────────────

def validate_coordinates(lat_value, lon_value,
                          lat_field='lat', lon_field='lon'):
    """
    Validate latitude (-90 to 90) and longitude (-180 to 180).
    Ethiopia bounding box is roughly lat 3–15, lon 33–48 — a soft warning is
    included in the error message but values outside Ethiopia are still accepted
    to support diaspora users.
    Returns (float lat, float lon).
    """
    try:
        lat = float(lat_value)
    except (ValueError, TypeError):
        raise ValidationError(
            f'{lat_field} must be a numeric latitude value.',
            field=lat_field,
        )
    try:
        lon = float(lon_value)
    except (ValueError, TypeError):
        raise ValidationError(
            f'{lon_field} must be a numeric longitude value.',
            field=lon_field,
        )
    if lat < -90 or lat > 90:
        raise ValidationError(
            f'{lat_field} must be between -90 and 90 (got {lat}).',
            field=lat_field,
        )
    if lon < -180 or lon > 180:
        raise ValidationError(
            f'{lon_field} must be between -180 and 180 (got {lon}).',
            field=lon_field,
        )
    return lat, lon


# ─────────────────────────────────────────────────────────────────────────────
# Urgency Level
# ─────────────────────────────────────────────────────────────────────────────

VALID_URGENCY_LEVELS = {
    'emergency', 'urgent', 'routine', 'self_care', 'unknown', ''
}

def validate_urgency(value, field='urgency_level', default='self_care'):
    """Validate urgency level string. Returns default if empty."""
    if not value:
        return default
    val = str(value).strip().lower()
    if val not in VALID_URGENCY_LEVELS:
        raise ValidationError(
            f'{field} must be one of: emergency, urgent, routine, self_care.',
            field=field,
        )
    return val


# ─────────────────────────────────────────────────────────────────────────────
# Numeric Range (generic)
# ─────────────────────────────────────────────────────────────────────────────

def validate_positive_integer(value, field='value', min_val=1, max_val=9999,
                               required=False, default=None):
    """Validate a positive integer within a given range."""
    if value is None or value == '':
        if required:
            raise ValidationError(f'{field} is required.', field=field)
        return default
    try:
        n = int(value)
    except (ValueError, TypeError):
        raise ValidationError(f'{field} must be a whole number.', field=field)
    if n < min_val or n > max_val:
        raise ValidationError(
            f'{field} must be between {min_val} and {max_val} (got {n}).',
            field=field,
        )
    return n


# ─────────────────────────────────────────────────────────────────────────────
# Required Field Helper
# ─────────────────────────────────────────────────────────────────────────────

def require_fields(data, fields):
    """
    Check that all field names in `fields` are present and non-empty in `data`.
    Raises ValidationError for the first missing field found.
    """
    for field in fields:
        if not data.get(field):
            raise ValidationError(f'{field} is required.', field=field)


# ─────────────────────────────────────────────────────────────────────────────
# Rating (1–5)
# ─────────────────────────────────────────────────────────────────────────────

def validate_rating(value, field='rating'):
    """Validate a 1–5 star rating."""
    try:
        r = int(value)
    except (ValueError, TypeError):
        raise ValidationError(f'{field} must be a number between 1 and 5.', field=field)
    if r < 1 or r > 5:
        raise ValidationError(f'{field} must be between 1 and 5 (got {r}).', field=field)
    return r


# ─────────────────────────────────────────────────────────────────────────────
# Gestational / Age in Months
# ─────────────────────────────────────────────────────────────────────────────

def validate_age_months(value, field='age_months', required=False, default=0.0):
    """Validate child age in months (0 – 60 months = 0 – 5 years)."""
    if value is None or value == '':
        if required:
            raise ValidationError(f'{field} is required.', field=field)
        return default
    try:
        m = float(value)
    except (ValueError, TypeError):
        raise ValidationError(f'{field} must be a number.', field=field)
    if m < 0 or m > 60:
        raise ValidationError(
            f'{field} must be between 0 and 60 months (got {m}).',
            field=field,
        )
    return round(m, 1)


# ─────────────────────────────────────────────────────────────────────────────
# Condition Type (chronic disease)
# ─────────────────────────────────────────────────────────────────────────────

VALID_CONDITIONS = {'hypertension', 'diabetes'}

def validate_condition(value, field='condition'):
    """Validate chronic disease condition type."""
    if not value:
        raise ValidationError(f'{field} is required.', field=field)
    val = str(value).strip().lower()
    if val not in VALID_CONDITIONS:
        raise ValidationError(
            f'{field} must be one of: {", ".join(sorted(VALID_CONDITIONS))}.',
            field=field,
        )
    return val


# ─────────────────────────────────────────────────────────────────────────────
# Visit Type (HEW checklist)
# ─────────────────────────────────────────────────────────────────────────────

VALID_VISIT_TYPES = {
    'newborn', 'sick_child', 'postnatal', 'antenatal', 'family_planning', 'nutrition'
}

def validate_visit_type(value, field='visit_type'):
    """Validate HEW checklist visit type."""
    if not value:
        raise ValidationError(f'{field} is required.', field=field)
    val = str(value).strip().lower()
    if val not in VALID_VISIT_TYPES:
        raise ValidationError(
            f'{field} must be one of: {", ".join(sorted(VALID_VISIT_TYPES))}.',
            field=field,
        )
    return val


# ─────────────────────────────────────────────────────────────────────────────
# Reminder Time of Day
# ─────────────────────────────────────────────────────────────────────────────

VALID_TIMES_OF_DAY = {'morning', 'afternoon', 'evening'}

def validate_time_of_day(value, field='time_of_day', default='morning'):
    """Validate medication reminder time of day."""
    if not value:
        return default
    val = str(value).strip().lower()
    if val not in VALID_TIMES_OF_DAY:
        raise ValidationError(
            f'{field} must be one of: morning, afternoon, evening.',
            field=field,
        )
    return val
