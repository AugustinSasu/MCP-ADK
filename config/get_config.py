import sys

from box import Box
import yaml
from pathlib import Path

config_dir = Path(__file__).parent

CONFIG_ABSOLUTE_PATH = config_dir / 'config.yml'

try:
    with open(str(CONFIG_ABSOLUTE_PATH), 'r', encoding='utf8') as ymlfile:
        cfg = Box(yaml.safe_load(ymlfile))
except Exception as e:
    print(f"Error loading config: {e}", file=sys.stderr)
    sys.exit(1)

