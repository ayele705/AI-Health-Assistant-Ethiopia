import urllib.request, urllib.parse, json

query = '[out:json][timeout:15];(node["amenity"~"hospital|clinic|health_post|doctors"](around:10000,12.6030,37.4521);way["amenity"~"hospital|clinic|health_post|doctors"](around:10000,12.6030,37.4521);node["healthcare"](around:10000,12.6030,37.4521););out center tags;'

data = urllib.parse.urlencode({'data': query}).encode()
req = urllib.request.Request('https://overpass.kumi.systems/api/interpreter', data=data, headers={'User-Agent':'HealthAssistant/1.0'})
with urllib.request.urlopen(req, timeout=20) as r:
    result = json.loads(r.read())
elements = result.get('elements', [])
print(f'Found {len(elements)} facilities near Gondar:')
for e in elements[:15]:
    tags = e.get('tags', {})
    name = tags.get('name') or tags.get('name:en', 'unnamed')
    print(f'  - {name} [{tags.get("amenity", tags.get("healthcare","?"))}]')
