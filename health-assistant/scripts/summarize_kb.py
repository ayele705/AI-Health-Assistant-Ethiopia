import json, os
path = os.path.join(os.path.dirname(__file__), '..', 'data', 'knowledge_base.json')
d = json.load(open(path, encoding='utf-8'))
conditions = d.get('conditions', [])
tips = d.get('health_tips', [])
cats = {}
urgencies = {}
for c in conditions:
    cats[c.get('category','?')] = cats.get(c.get('category','?'), 0) + 1
    urgencies[c.get('urgency','?')] = urgencies.get(c.get('urgency','?'), 0) + 1
print("=== Knowledge Base Summary ===")
print("Total conditions:", len(conditions))
print("Total health tips:", len(tips))
print("Categories:")
for k,v in sorted(cats.items()):
    print(f"  {k}: {v}")
print("Urgency levels:")
for k,v in sorted(urgencies.items()):
    print(f"  {k}: {v}")
print("Condition IDs:")
for c in conditions:
    print(f"  {c['id']} - {c['name_en']}")
