import functools
import inspect
from typing import Callable, Any, Dict
from logger import setup_logging


log = setup_logging()


def get_bound_arguments(func: Callable, args: tuple, kwargs: dict) -> Dict[str, Any]:
    signature = inspect.signature(func)
    bound = signature.bind(*args, **kwargs)
    bound.apply_defaults()

    return bound.arguments


def logging_middleware(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        params = get_bound_arguments(func, args, kwargs)
        params_str = " | ".join(f"{k}={v}" for k, v in sorted(params.items()))

        log.info(f"CALL: {func.__name__} | {params_str}")

        try:
            result = func(*args, **kwargs)
            log.info(f"SUCCESS: {func.__name__} | {params_str} | result={result}")
            return result
        except (ValueError, KeyError) as e:
            log.error(
                f"ERROR: {func.__name__} | {params_str} | "
                f"error_type={type(e).__name__} | error_message={str(e)}"
            )
            raise
        except Exception as e:
            log.error(
                f"UNEXPECTED_ERROR: {func.__name__} | {params_str} | "
                f"error_type={type(e).__name__} | error_message={str(e)}"
            )
            raise

    return wrapper
