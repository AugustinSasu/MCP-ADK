import sys

from box import Box
import yaml

CONFIG_ABSOLUTE_PATH = '/home/gusti/ASO/ASO-AI/config/config.yml'

try:
    with open(CONFIG_ABSOLUTE_PATH, 'r', encoding='utf8') as ymlfile:
        cfg = Box(yaml.safe_load(ymlfile))
except Exception as e:
    print(f"Error loading config: {e}", file=sys.stderr)
    sys.exit(1)

