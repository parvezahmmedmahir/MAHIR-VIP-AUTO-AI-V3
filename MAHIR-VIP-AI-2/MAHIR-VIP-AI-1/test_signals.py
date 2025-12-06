from quotex_api import api
import json

api.connect()

print("\n=== TESTING SIGNAL GENERATION (10 signals) ===\n")

results = []
for i in range(10):
    signal = api.get_signal()
    results.append(signal)
    data = signal['data']
    print(f"{i+1}. {data['pair']}: {data['direction']} - {data['confidence']} ({data['strategy']})")

call_count = sum(1 for r in results if r['data']['direction'] == 'CALL')
put_count = sum(1 for r in results if r['data']['direction'] == 'PUT')

print(f"\n📊 DISTRIBUTION:")
print(f"   CALL signals: {call_count}")
print(f"   PUT signals: {put_count}")

if call_count == 0 or put_count == 0:
    print("\n⚠️ WARNING: One-sided signals detected! System needs fixing!")
else:
    print("\n✅ Signal distribution looks balanced!")
