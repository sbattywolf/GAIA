"""Simple retry helper with exponential backoff.

Provides a `retry` decorator that retries a function on specified exceptions
and supports inspecting an exception attribute `status_code` for HTTP-like
retry decisions (e.g., 429, 5xx).
"""
import time
import functools
from typing import Callable, Iterable, Tuple


class RetryError(Exception):
    pass


def _is_retryable_exc(exc: Exception, retry_statuses: Iterable[int]) -> bool:
    sc = getattr(exc, 'status_code', None)
    if sc is None:
        return True
    try:
        return int(sc) in set(retry_statuses)
    except Exception:
        return False


def retry(max_attempts: int = 3, initial_delay: float = 0.1, backoff: float = 2.0,
          retry_on_exceptions: Tuple[type, ...] = (Exception,), retry_statuses: Iterable[int] = (429, 500, 502, 503, 504)) -> Callable:
    """Return a decorator that retries the wrapped function.

    Parameters:
    - max_attempts: total attempts including first call
    - initial_delay: seconds to wait before first retry
    - backoff: multiplier for exponential backoff
    - retry_on_exceptions: exception types that trigger retry
    - retry_statuses: status codes considered retryable when exception has `status_code`
    """

    def deco(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            delay = initial_delay
            last_exc = None
            while attempt < max_attempts:
                try:
                    return func(*args, **kwargs)
                except retry_on_exceptions as exc:
                    last_exc = exc
                    attempt += 1
                    if attempt >= max_attempts:
                        break
                    # decide whether exception is retryable based on status_code
                    if not _is_retryable_exc(exc, retry_statuses):
                        break
                    time.sleep(delay)
                    delay = delay * backoff
            raise RetryError(f"Failed after {max_attempts} attempts") from last_exc

        return wrapper

    return deco
