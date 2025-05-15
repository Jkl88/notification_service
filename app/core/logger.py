from loguru import logger
import sys
from pathlib import Path

log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

log_format = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | {message}"

logger.remove()
logger.add(sys.stdout, level="INFO", format=log_format)
logger.add(log_dir / "app.log", level="INFO", rotation="1 week", retention="4 weeks", encoding="utf-8", format=log_format)
