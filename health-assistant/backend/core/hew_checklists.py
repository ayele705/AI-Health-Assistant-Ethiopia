"""
HEW (Health Extension Worker) home visit checklists.
Based on Ethiopia FMOH Health Extension Programme guidelines.
"""

CHECKLISTS = {
    'newborn': {
        'title_en': 'Newborn Care Checklist (0-28 days)',
        'title_am': 'የጨቅላ ህጻን እንክብካቤ ዝርዝር (0-28 ቀናት)',
        'items': [
            {'id': 'breathing_ok',      'question_en': 'Is the baby breathing normally (no grunting or fast breathing)?',   'question_am': 'ህጻኑ በደንብ ይተነፍሳል?',          'critical': True},
            {'id': 'temperature_ok',    'question_en': 'Is the baby warm (not cold to touch)?',                             'question_am': 'ህጻኑ ሞቅ ያለ ነው?',              'critical': True},
            {'id': 'breastfeeding',     'question_en': 'Is the baby breastfeeding well (at least 8 times/day)?',            'question_am': 'ህጻኑ ጡት ይጠባል?',              'critical': True},
            {'id': 'cord_clean',        'question_en': 'Is the umbilical cord clean and dry (no redness or pus)?',          'question_am': 'የእምብርት ቁርጥ ንጹህ ነው?',       'critical': True},
            {'id': 'jaundice_check',    'question_en': 'Is there yellowing of skin or eyes (jaundice)?',                    'question_am': 'ቢጫ ቆዳ ወይም ዓይን አለ?',         'critical': True},
            {'id': 'bcg_given',         'question_en': 'Has BCG and OPV birth dose been given?',                            'question_am': 'BCG እና OPV ክትባት ተሰጥቷል?',    'critical': False},
            {'id': 'mother_wellbeing',  'question_en': 'Is the mother well (no fever, no heavy bleeding)?',                 'question_am': 'እናቲቱ ጤናማ ናት?',             'critical': True},
            {'id': 'kangaroo_care',     'question_en': 'Is kangaroo mother care being practiced for low birth weight baby?','question_am': 'ዝቅተኛ ክብደት ህጻን ካንጋሩ እናት ክንክን ይደረጋል?', 'critical': False},
            {'id': 'birth_registered',  'question_en': 'Has the birth been registered?',                                    'question_am': 'ልደቱ ተመዝግቧል?',              'critical': False},
        ]
    },
    'sick_child': {
        'title_en': 'Sick Child Assessment (IMCI)',
        'title_am': 'የታመመ ህጻን ምዘና (IMCI)',
        'items': [
            {'id': 'danger_signs',      'question_en': 'Any general danger signs? (unable to drink, vomiting everything, convulsions, lethargic)', 'question_am': 'አደጋ ምልክቶች አሉ?', 'critical': True},
            {'id': 'cough_breathing',   'question_en': 'Does the child have cough or difficulty breathing?',                'question_am': 'ሳል ወይም የመተንፈስ ችግር አለ?',    'critical': True},
            {'id': 'diarrhea',          'question_en': 'Does the child have diarrhea? (how many days, blood in stool?)',    'question_am': 'ተቅማጥ አለ?',                  'critical': True},
            {'id': 'fever',             'question_en': 'Does the child have fever? (how many days, malaria risk area?)',    'question_am': 'ትኩሳት አለ?',                  'critical': True},
            {'id': 'ear_problem',       'question_en': 'Does the child have ear pain or discharge?',                        'question_am': 'የጆሮ ህመም ወይም ፈሳሽ አለ?',      'critical': False},
            {'id': 'nutrition_check',   'question_en': 'Check MUAC and look for oedema',                                   'question_am': 'MUAC ይለኩ እና እብጠት ይፈትሹ',    'critical': True},
            {'id': 'vaccination_check', 'question_en': 'Is the child up to date with vaccinations?',                       'question_am': 'ክትባቶች ወቅቱን ጠብቀዋል?',        'critical': False},
            {'id': 'vitamin_a',         'question_en': 'Has the child received Vitamin A in the last 6 months?',           'question_am': 'ቫይታሚን ኤ ባለፉት 6 ወር ተሰጥቷል?', 'critical': False},
        ]
    },
    'postnatal': {
        'title_en': 'Postnatal Care Checklist (0-6 weeks after delivery)',
        'title_am': 'ከወሊድ በኋላ እንክብካቤ ዝርዝር',
        'items': [
            {'id': 'bleeding_check',    'question_en': 'Is there heavy vaginal bleeding (more than normal lochia)?',        'question_am': 'ከፍተኛ ደም መፍሰስ አለ?',          'critical': True},
            {'id': 'fever_check',       'question_en': 'Does the mother have fever (above 38°C)?',                          'question_am': 'ትኩሳት አለ?',                  'critical': True},
            {'id': 'wound_check',       'question_en': 'Is the perineal wound or C-section wound healing well?',            'question_am': 'ቁስሉ ጥሩ ሆኖ ይድናል?',          'critical': True},
            {'id': 'breastfeeding_ok',  'question_en': 'Is the mother breastfeeding exclusively?',                          'question_am': 'ብቻ ጡት ታጠባለች?',             'critical': False},
            {'id': 'family_planning',   'question_en': 'Has family planning been discussed and method chosen?',             'question_am': 'የቤተሰብ ምጣኔ ተወያይቷል?',        'critical': False},
            {'id': 'iron_folic',        'question_en': 'Is the mother taking iron and folic acid supplements?',             'question_am': 'ብረት እና ፎሊክ አሲድ ትወስዳለች?',   'critical': False},
            {'id': 'mental_health',     'question_en': 'Does the mother show signs of postpartum depression (sadness, not bonding with baby)?', 'question_am': 'ከወሊድ በኋላ ድብርት ምልክቶች?', 'critical': True},
            {'id': 'newborn_check',     'question_en': 'Is the newborn feeding well and gaining weight?',                   'question_am': 'ህጻኑ ጥሩ ይጠባል እና ክብደት ያገኛል?', 'critical': True},
        ]
    },
    'antenatal': {
        'title_en': 'Antenatal Home Visit Checklist',
        'title_am': 'ቅድመ ወሊድ የቤት ጉብኝት ዝርዝር',
        'items': [
            {'id': 'danger_signs',      'question_en': 'Any danger signs? (bleeding, severe headache, blurred vision, convulsions, no fetal movement)', 'question_am': 'አደጋ ምልክቶች?', 'critical': True},
            {'id': 'bp_check',          'question_en': 'Blood pressure measured (flag if ≥140/90)?',                        'question_am': 'የደም ግፊት ተለክቷል?',            'critical': True},
            {'id': 'iron_folic',        'question_en': 'Is the mother taking iron and folic acid daily?',                   'question_am': 'ብረት እና ፎሊክ አሲድ ትወስዳለች?',   'critical': False},
            {'id': 'facility_delivery', 'question_en': 'Has the mother planned to deliver at a health facility?',           'question_am': 'ወደ ጤና ጣቢያ ለመሄድ አቅዳለች?',    'critical': False},
            {'id': 'birth_plan',        'question_en': 'Does the mother have a birth plan (transport, money, companion)?',  'question_am': 'የወሊድ እቅድ አላት?',             'critical': False},
            {'id': 'tt_vaccine',        'question_en': 'Has the mother received TT vaccine (2 doses)?',                     'question_am': 'TT ክትባት ተሰጥቷታል?',           'critical': False},
            {'id': 'hiv_tested',        'question_en': 'Has the mother been tested for HIV during this pregnancy?',         'question_am': 'ለኤች አይ ቪ ተመርምራለች?',        'critical': False},
            {'id': 'malaria_net',       'question_en': 'Does the mother sleep under an insecticide-treated bed net?',       'question_am': 'ፀረ-ነፍሳት አልጋ መረብ ትጠቀማለች?',  'critical': False},
        ]
    },
    'nutrition': {
        'title_en': 'Nutrition Home Visit Checklist',
        'title_am': 'የምግብ ሁኔታ የቤት ጉብኝት ዝርዝር',
        'items': [
            {'id': 'muac_measured',     'question_en': 'MUAC measured for all children 6-59 months?',                      'question_am': 'MUAC ለሁሉም 6-59 ወር ህጻናት ተለክቷል?', 'critical': True},
            {'id': 'oedema_check',      'question_en': 'Checked for bilateral pitting oedema?',                            'question_am': 'የሁለቱም እግሮች እብጠት ተፈትሿል?',   'critical': True},
            {'id': 'breastfeeding',     'question_en': 'Infants under 6 months exclusively breastfed?',                    'question_am': 'ከ6 ወር በታች ህጻናት ብቻ ጡት ይጠባሉ?', 'critical': False},
            {'id': 'complementary',     'question_en': 'Children 6-24 months receiving appropriate complementary foods?',  'question_am': 'ተጨማሪ ምግብ ይሰጣቸዋል?',          'critical': False},
            {'id': 'vitamin_a',         'question_en': 'All children 6-59 months received Vitamin A in last 6 months?',    'question_am': 'ቫይታሚን ኤ ተሰጥቷቸዋል?',          'critical': False},
            {'id': 'deworming',         'question_en': 'Children 12-59 months dewormed in last 6 months?',                 'question_am': 'ትሎች ህክምና ተሰጥቷቸዋል?',         'critical': False},
            {'id': 'iodized_salt',      'question_en': 'Is the household using iodized salt?',                             'question_am': 'አዮዲን ጨው ይጠቀማሉ?',            'critical': False},
            {'id': 'rutf_enrolled',     'question_en': 'SAM children enrolled in therapeutic feeding programme?',          'question_am': 'SAM ህጻናት ህክምና ፕሮግራም ገብተዋል?', 'critical': True},
        ]
    },
}


def get_checklist(visit_type: str, language: str = 'en') -> dict:
    cl = CHECKLISTS.get(visit_type)
    if not cl:
        return {}
    title_key = f'title_{language}' if language in ('am', 'ti') else 'title_en'
    q_key = f'question_{language}' if language in ('am', 'ti') else 'question_en'
    return {
        'visit_type': visit_type,
        'title': cl.get(title_key, cl['title_en']),
        'items': [{'id': item['id'], 'question': item.get(q_key, item['question_en']), 'critical': item['critical']} for item in cl['items']],
    }


def get_all_checklist_types() -> list:
    return [{'id': k, 'title_en': v['title_en'], 'title_am': v.get('title_am', v['title_en'])} for k, v in CHECKLISTS.items()]
