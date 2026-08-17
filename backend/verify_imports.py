import sys
import os

def verify():
    print("Verifying backend imports...")
    try:
        import src.main
        import src.services.mastery_service
        import src.routes.media_routes
        import src.services.adaptation_service
        import src.services.mastery_orchestrator
        print("Import check: OK")
    except Exception as e:
        print(f"Import check: FAILED - {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    sys.path.append(os.getcwd())
    verify()
