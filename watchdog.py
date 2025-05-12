import logging
import traceback
from datetime import datetime
from typing import Callable

def setup_logging(log_file: str):
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s"
    )

def pulse(pulse_path: str = "pulse.txt"):
    with open(pulse_path, "w") as f:
        f.write(f"ALIVE {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

def run_with_watchdog(
    bot_func: Callable[[], None],
    log_file: str="crawler.log",
    pulse_file: str="pulse.txt"
    )-> None:
    setup_logging(log_file)
    logging.info("Bot started")
    pulse(pulse_file)
    try:
        bot_func()
        logging.info("Bot finished successfully")
    except Exception as e:
        error_msg = traceback.format_exc()
        logging.error(f"Bot crashe with error: {e}")
        logging.debug(f"Full traceback::\n{error_msg}")
        pulse(pulse_file)
