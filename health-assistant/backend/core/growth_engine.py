"""
Growth monitoring engine.
Uses WHO weight-for-age and MUAC thresholds to classify nutrition status.
Supports SAM / MAM / normal classification per WHO/UNICEF standards.
"""
from datetime import date


# WHO weight-for-age median (kg) by age in months — boys and girls averaged
# Source: WHO Child Growth Standards 2006
WHO_WEIGHT_MEDIAN = {
    0: 3.3, 1: 4.5, 2: 5.6, 3: 6.4, 4: 7.0, 5: 7.5, 6: 7.9,
    7: 8.3, 8: 8.6, 9: 8.9, 10: 9.2, 11: 9.4, 12: 9.6,
    15: 10.3, 18: 10.9, 21: 11.5, 24: 12.0, 30: 13.0,
    36: 14.0, 42: 15.0, 48: 16.0, 54: 17.0, 60: 18.0,
}

# WHO weight-for-age -2 SD (moderate underweight threshold)
WHO_WEIGHT_MINUS2SD = {
    0: 2.5, 1: 3.4, 2: 4.3, 3: 5.0, 4: 5.6, 5: 6.0, 6: 6.4,
    7: 6.7, 8: 7.0, 9: 7.2, 10: 7.5, 11: 7.7, 12: 7.8,
    15: 8.4, 18: 8.9, 21: 9.4, 24: 9.8, 30: 10.5,
    36: 11.2, 42: 12.0, 48: 12.7, 54: 13.5, 60: 14.2,
}

# WHO weight-for-age -3 SD (severe underweight threshold)
WHO_WEIGHT_MINUS3SD = {
    0: 2.1, 1: 2.9, 2: 3.8, 3: 4.4, 4: 4.9, 5: 5.3, 6: 5.7,
    7: 5.9, 8: 6.2, 9: 6.4, 10: 6.6, 11: 6.8, 12: 7.0,
    15: 7.5, 18: 8.0, 21: 8.4, 24: 8.8, 30: 9.4,
    36: 10.0, 42: 10.7, 48: 11.3, 54: 12.0, 60: 12.6,
}


def _interpolate(table: dict, age_months: float) -> float:
    """Linear interpolation between nearest age keys."""
    keys = sorted(table.keys())
    if age_months <= keys[0]:
        return table[keys[0]]
    if age_months >= keys[-1]:
        return table[keys[-1]]
    for i in range(len(keys) - 1):
        lo, hi = keys[i], keys[i + 1]
        if lo <= age_months <= hi:
            frac = (age_months - lo) / (hi - lo)
            return table[lo] + frac * (table[hi] - table[lo])
    return table[keys[-1]]


def classify_muac(muac_cm: float, age_months: float) -> dict:
    """Classify nutrition status by MUAC. For children 6-59 months."""
    if age_months < 6 or age_months > 59:
        return {'status': 'not_applicable', 'color': 'grey',
                'message_en': 'MUAC classification applies to children 6-59 months.'}
    if muac_cm < 11.5:
        return {'status': 'SAM', 'color': 'red',
                'message_en': f'MUAC {muac_cm}cm — SEVERE ACUTE MALNUTRITION. Refer immediately for therapeutic feeding (RUTF).',
                'message_am': f'MUAC {muac_cm}ሴሜ — ከፍተኛ ቀጭነት። ወዲያውኑ ወደ ጤና ጣቢያ ይሂዱ።',
                'message_om': f'MUAC {muac_cm}cm — MALNUTRITION HAMAA. Hatattamaan giddugala fayyaa deemi.',
                'message_ti': f'MUAC {muac_cm}ሴሜ — ከቢድ ቀጭነት። ሕጂ ናብ ጥዕና ጣቢያ ኺድ።',
                'message_so': f'MUAC {muac_cm}cm — MALNUTRITION XOOG AH. Isbitaalka aad u tag.',
                'action_en': 'Refer to health centre for RUTF. Check for oedema and complications.'}
    if muac_cm < 12.5:
        return {'status': 'MAM', 'color': 'yellow',
                'message_en': f'MUAC {muac_cm}cm — MODERATE ACUTE MALNUTRITION. Enrol in supplementary feeding programme.',
                'message_am': f'MUAC {muac_cm}ሴሜ — መካከለኛ ቀጭነት። ወደ ጤና ጣቢያ ይሂዱ።',
                'message_om': f'MUAC {muac_cm}cm — Malnutrition giddugaleessa. Sagantaa nyaata dabalataatti galchi.',
                'message_ti': f'MUAC {muac_cm}ሴሜ — ማእከላይ ቀጭነት። ናብ ጥዕና ጣቢያ ኺድ።',
                'message_so': f'MUAC {muac_cm}cm — Malnutrition dhexdhexaad ah. Barnaamijka cuntada dheeraadka ah ku diiwaangeli.',
                'action_en': 'Enrol in supplementary feeding. Provide RUSF. Follow up in 2 weeks.'}
    return {'status': 'normal', 'color': 'green',
            'message_en': f'MUAC {muac_cm}cm — Normal nutrition status.',
            'message_am': f'MUAC {muac_cm}ሴሜ — መደበኛ የምግብ ሁኔታ።',
            'message_om': f'MUAC {muac_cm}cm — Haala nyaataa idilee.',
            'message_ti': f'MUAC {muac_cm}ሴሜ — ንቡር ናይ ምምጋብ ኩነታት።',
            'message_so': f'MUAC {muac_cm}cm — Xaalada nafaqada caadiga ah.',
            'action_en': 'Continue growth monitoring every month.'}


def classify_weight_for_age(weight_kg: float, age_months: float) -> dict:
    """Classify underweight status using WHO weight-for-age z-scores."""
    minus3 = _interpolate(WHO_WEIGHT_MINUS3SD, age_months)
    minus2 = _interpolate(WHO_WEIGHT_MINUS2SD, age_months)
    median = _interpolate(WHO_WEIGHT_MEDIAN, age_months)
    if weight_kg < minus3:
        return {'status': 'severely_underweight', 'color': 'red',
                'message_en': f'Weight {weight_kg}kg — SEVERELY UNDERWEIGHT. Refer immediately.',
                'message_am': f'ክብደት {weight_kg}ኪሎ — ከፍተኛ ዝቅተኛ ክብደት። ወዲያውኑ ወደ ጤና ጣቢያ ይሂዱ።',
                'message_om': f'Ulfaatina {weight_kg}kg — Ulfaatina gadi aanaa hamaa. Hatattamaan ergi.',
                'message_ti': f'ክብደት {weight_kg}ኪሎ — ከቢድ ዝቅ ዝበለ ክብደት። ሕጂ ናብ ጥዕና ጣቢያ ኺድ።',
                'message_so': f'Miisaanka {weight_kg}kg — Miisaan hooseeya xoog ah. Isbitaalka u dir.',
                'expected_median_kg': round(median, 1)}
    if weight_kg < minus2:
        return {'status': 'underweight', 'color': 'yellow',
                'message_en': f'Weight {weight_kg}kg — UNDERWEIGHT. Nutritional support needed.',
                'message_am': f'ክብደት {weight_kg}ኪሎ — ዝቅተኛ ክብደት። የምግብ ድጋፍ ያስፈልጋል።',
                'message_om': f'Ulfaatina {weight_kg}kg — Ulfaatina gadi aanaa. Gargaarsa nyaataa barbaachisa.',
                'message_ti': f'ክብደት {weight_kg}ኪሎ — ዝቅ ዝበለ ክብደት። ናይ ምምጋብ ሓገዝ የድሊ።',
                'message_so': f'Miisaanka {weight_kg}kg — Miisaan hooseeya. Taageero nafaqo ayaa loo baahan yahay.',
                'expected_median_kg': round(median, 1)}
    return {'status': 'normal_weight', 'color': 'green',
            'message_en': f'Weight {weight_kg}kg — Normal.',
            'message_am': f'ክብደት {weight_kg}ኪሎ — መደበኛ።',
            'message_om': f'Ulfaatina {weight_kg}kg — Idilee.',
            'message_ti': f'ክብደት {weight_kg}ኪሎ — ንቡር።',
            'message_so': f'Miisaanka {weight_kg}kg — Caadi.',
            'expected_median_kg': round(median, 1)}


def assess_growth(weight_kg: float = None, height_cm: float = None,
                  muac_cm: float = None, oedema: bool = False,
                  age_months: float = 0, sex: str = 'unknown') -> dict:
    """Full growth assessment combining MUAC, weight-for-age, and oedema."""
    result = {'age_months': age_months, 'sex': sex, 'assessments': [], 'overall_status': 'normal', 'overall_color': 'green'}

    if oedema:
        result['overall_status'] = 'SAM'
        result['overall_color'] = 'red'
        result['oedema_alert'] = {
            'message_en': 'Bilateral pitting oedema — SEVERE ACUTE MALNUTRITION (Kwashiorkor). Refer immediately.',
            'message_am': 'የሁለቱም እግሮች እብጠት — ከፍተኛ ቀጭነት። ወዲያውኑ ወደ ጤና ጣቢያ ይሂዱ።',
            'message_om': 'Dhiita lama — Malnutrition hamaa. Hatattamaan ergi.',
            'message_ti': 'ናይ ክልቲኡ እግሪ ሕበጥ — ከቢድ ቀጭነት። ሕጂ ናብ ጥዕና ጣቢያ ኺድ።',
            'message_so': 'Barar labada cagood — Malnutrition xoog ah. Isbitaalka aad u tag.',
        }

    if muac_cm is not None:
        muac_result = classify_muac(muac_cm, age_months)
        result['assessments'].append({'type': 'muac', **muac_result})
        if muac_result['status'] == 'SAM':
            result['overall_status'] = 'SAM'
            result['overall_color'] = 'red'
        elif muac_result['status'] == 'MAM' and result['overall_status'] == 'normal':
            result['overall_status'] = 'MAM'
            result['overall_color'] = 'yellow'

    if weight_kg is not None:
        wfa = classify_weight_for_age(weight_kg, age_months)
        result['assessments'].append({'type': 'weight_for_age', **wfa})
        if wfa['status'] == 'severely_underweight' and result['overall_status'] == 'normal':
            result['overall_status'] = 'MAM'
            result['overall_color'] = 'yellow'

    if result['overall_status'] == 'SAM':
        result['recommendation_en'] = 'REFER IMMEDIATELY to health centre for therapeutic feeding (RUTF/F-75/F-100). Do not delay.'
        result['recommendation_am'] = 'ወዲያውኑ ወደ ጤና ጣቢያ ይሂዱ። ህክምና ያስፈልጋል።'
        result['recommendation_om'] = 'HATATTAMAAN giddugala fayyaa deemi. Nyaata yaalaaf (RUTF) barbaachisa.'
        result['recommendation_ti'] = 'ሕጂ ናብ ጥዕና ጣቢያ ኺድ። ሕክምና የድሊ።'
        result['recommendation_so'] = 'HADDA isbitaalka u tag. Cunto daawo ah (RUTF) ayaa loo baahan yahay.'
    elif result['overall_status'] == 'MAM':
        result['recommendation_en'] = 'Enrol in supplementary feeding programme. Follow up in 2 weeks. Improve dietary diversity.'
        result['recommendation_am'] = 'ወደ ጤና ጣቢያ ይሂዱ። ተጨማሪ ምግብ ያስፈልጋል።'
        result['recommendation_om'] = 'Sagantaa nyaata dabalataatti galchi. Torban 2 booda hordofi.'
        result['recommendation_ti'] = 'ናብ ጥዕና ጣቢያ ኺድ። ተወሳኺ ምምጋብ የድሊ።'
        result['recommendation_so'] = 'Barnaamijka cuntada dheeraadka ah ku diiwaangeli. 2 toddobaad kadib soo noqo.'
    else:
        result['recommendation_en'] = 'Continue monthly growth monitoring. Ensure dietary diversity and exclusive breastfeeding if under 6 months.'
        result['recommendation_am'] = 'ወርሃዊ ክብደት መለካት ይቀጥሉ።'
        result['recommendation_om'] = 'Hordoffii guddina ji\'a ji\'aan itti fufi.'
        result['recommendation_ti'] = 'ወርሓዊ ምክትታል ዕቤት ቀጽሎ።'
        result['recommendation_so'] = 'Sii wad kormeerka kobaca bishiiba.'

    return result


def age_months_from_dob(dob: date) -> float:
    """Calculate age in months from date of birth."""
    today = date.today()
    months = (today.year - dob.year) * 12 + (today.month - dob.month)
    days_adjustment = (today.day - dob.day) / 30.0
    return max(0.0, months + days_adjustment)
