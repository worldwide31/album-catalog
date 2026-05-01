import json
import time
import urllib.request
from collections import Counter

URL = "http://localhost:8080/health"
REQUESTS = 30

instances = Counter()

for index in range(REQUESTS):
    with urllib.request.urlopen(URL, timeout=5) as response:
        data = json.loads(response.read().decode("utf-8"))
        instance = data.get("instance", "unknown")
        instances[instance] += 1
        print(f"{index + 1:02d}: instance={instance}, version={data.get('version')}, env={data.get('environment')}")
    time.sleep(0.1)

print("\nРаспределение запросов между экземплярами:")
for instance, count in instances.items():
    print(f"{instance}: {count}")
