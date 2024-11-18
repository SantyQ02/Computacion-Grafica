# goocanvas_util.py
import gi
import time
import logging
from functools import wraps

# Configure logging
logging.basicConfig(level=logging.INFO, format="[%(levelname)s][%(name)s] %(message)s")
logger = logging.getLogger(__name__)


def timer(func):
    """
    Decorator that measures the execution time of a function with high precision.

    Args:
        func (callable): The function to be decorated.

    Returns:
        callable: The wrapped function with timing functionality.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()  # High-resolution timer
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        logger.info(
            f"Function '{func.__name__}' executed in {elapsed_time:.6f} seconds."
        )
        return result

    return wrapper


def setup_goocanvas():
    """
    Sets up the GooCanvas library version.
    """
    try:
        gi.require_version("GooCanvas", "3.0")
    except ValueError:
        try:
            gi.require_version("GooCanvas", "2.0")
        except ValueError:
            raise ImportError("No se encontró ninguna versión compatible de GooCanvas.")
