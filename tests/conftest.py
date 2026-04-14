import os
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
os.environ.setdefault("OAUTH_ENCRYPTION_KEY", "0" * 64)
