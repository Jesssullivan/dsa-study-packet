"""Exercise 3: Rate Limiter

This rate limiter is deployed in a web framework middleware to protect
upstream services. QA reports that under concurrent load, some clients
exceed their rate limit, and occasionally the limiter raises exceptions
during cleanup.

Read the code below, then answer the analysis questions at the bottom.
"""

import time


class RateLimiter:
    """Sliding window rate limiter.

    Allows `max_requests` within a rolling `window_seconds` window per client.
    """

    def __init__(self, max_requests: int, window_seconds: float) -> None:
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        # client_id -> list of request timestamps
        self.requests: dict[str, list[float]] = {}

    def _cleanup(self, client_id: str) -> None:
        """Remove expired timestamps for a client."""
        if client_id not in self.requests:
            return

        now = time.time()
        cutoff = now - self.window_seconds
        timestamps = self.requests[client_id]

        # Remove old entries
        i = 0
        while i < len(timestamps):
            if timestamps[i] < cutoff:
                timestamps.pop(i)
            else:
                i += 1

        # Clean up empty entries
        if len(timestamps) == 0:
            del self.requests[client_id]

    def is_allowed(self, client_id: str) -> bool:
        """Check if a request from client_id should be allowed."""
        self._cleanup(client_id)

        if client_id not in self.requests:
            self.requests[client_id] = [time.time()]
            return True

        if len(self.requests[client_id]) < self.max_requests:
            self.requests[client_id].append(time.time())
            return True

        return False

    def get_remaining(self, client_id: str) -> int:
        """Return how many requests the client has left in the current window."""
        self._cleanup(client_id)
        if client_id not in self.requests:
            return self.max_requests
        return self.max_requests - len(self.requests[client_id])

    def get_retry_after(self, client_id: str) -> float | None:
        """Return seconds until the client can make another request, or None."""
        if client_id not in self.requests:
            return None

        timestamps = self.requests[client_id]
        if len(timestamps) < self.max_requests:
            return None

        oldest = timestamps[0]
        retry_after = oldest + self.window_seconds - time.time()
        return max(0.0, retry_after)

    def reset(self, client_id: str) -> None:
        """Reset rate limit for a client (e.g., after auth upgrade)."""
        if client_id in self.requests:
            del self.requests[client_id]

    def cleanup_all(self) -> None:
        """Periodic cleanup of all expired entries. Called by a background thread."""
        for client_id in self.requests:
            self._cleanup(client_id)


# --- Example middleware usage ---

_limiter = RateLimiter(max_requests=100, window_seconds=60.0)


def rate_limit_middleware(client_id: str) -> dict[str, object]:
    """Returns a response dict. In a real framework, this wraps the handler."""
    if not _limiter.is_allowed(client_id):
        retry_after = _limiter.get_retry_after(client_id)
        return {
            "status": 429,
            "body": "Rate limit exceeded",
            "headers": {"Retry-After": str(retry_after)},
        }

    remaining = _limiter.get_remaining(client_id)
    return {
        "status": 200,
        "body": "OK",
        "headers": {
            "X-RateLimit-Remaining": str(remaining),
            "X-RateLimit-Limit": str(_limiter.max_requests),
        },
    }


# ---------------------------------------------------------------------------
# ANALYSIS QUESTIONS
#
# 1. THREAD SAFETY: `is_allowed` reads and writes `self.requests` without
#    any locking. If two threads call `is_allowed("client-A")` at the
#    same time, what can go wrong? How would you fix it?
#
# 2. CLEANUP BUG: `cleanup_all` iterates over `self.requests` while
#    `_cleanup` can delete entries from it (via `del self.requests[...]`).
#    What exception does this raise? How would you fix it?
#
# 3. CLEANUP PERFORMANCE: `_cleanup` uses `list.pop(i)` which is O(n)
#    for each removal, making the full cleanup O(n^2). Since timestamps
#    are sorted, what's a more efficient approach?
#
# 4. MEMORY: With 100K unique clients, the `requests` dict holds all
#    their timestamps. What's the memory footprint? How would you bound
#    it? (Hint: consider the sliding window counter approach instead.)
#
# 5. TIME HANDLING: The code uses `time.time()` which returns wall-clock
#    time. What happens if the system clock jumps (NTP correction, DST)?
#    What alternative would you use?
#
# 6. RACE CONDITION in `is_allowed`: Between `_cleanup` deleting the key
#    and checking `client_id not in self.requests`, another thread could
#    insert a new entry. Trace through the exact interleaving that allows
#    a client to exceed `max_requests`.
#
# 7. DISTRIBUTED: This implementation is in-process only. If the service
#    runs on 10 pods behind a load balancer, each pod has its own limiter.
#    How would you make this work across pods? (Hint: Redis + Lua script,
#    or a sliding window counter in a shared store.)
# ---------------------------------------------------------------------------
