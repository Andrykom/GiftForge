#!/usr/bin/env python3
# Тест импортов
import sys
sys.path.insert(0, 'core-api')

print("Testing imports...")

try:
    from app.routers import qr, gift, budget, stats
    print(f"qr type: {type(qr)}")
    print(f"qr: {qr}")
    print(f"Has routes: {hasattr(qr, 'routes')}")
    if hasattr(qr, 'routes'):
        print(f"Routes: {[r.path for r in qr.routes]}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
