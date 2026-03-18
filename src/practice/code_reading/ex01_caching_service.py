"""Exercise 1: Caching Service

You've been asked to review this caching service that sits between a web API
and multiple upstream data providers. Users report that the service becomes
slow and eventually unresponsive under load.

Read the code below, then answer the analysis questions at the bottom.
"""

import json
import time
import urllib.request
from typing import Any


class CacheEntry:
    def __init__(self, value: Any, fetched_at: float) -> None:
        self.value = value
        self.fetched_at = fetched_at


class DataProviderClient:
    """Fetches data from an external REST API."""

    def __init__(self, base_url: str) -> None:
        self.base_url = base_url

    def get_item(self, item_id: str) -> dict[str, Any]:
        """Fetch a single item by ID. ~200ms per call."""
        url = f"{self.base_url}/items/{item_id}"
        with urllib.request.urlopen(url, timeout=10) as resp:
            return json.loads(resp.read().decode())

    def get_items_bulk(self, item_ids: list[str]) -> list[dict[str, Any]]:
        """Bulk endpoint exists but is unused."""
        url = f"{self.base_url}/items/bulk"
        payload = json.dumps({"ids": item_ids}).encode()
        req = urllib.request.Request(url, data=payload, method="POST")
        req.add_header("Content-Type", "application/json")
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())


class CachingService:
    def __init__(self, provider: DataProviderClient) -> None:
        self.provider = provider
        self.cache: dict[str, CacheEntry] = {}
        self.stats = {"hits": 0, "misses": 0}

    def get_item(self, item_id: str) -> dict[str, Any]:
        """Get a single item, using cache if available."""
        if item_id in self.cache:
            self.stats["hits"] += 1
            return self.cache[item_id].value

        self.stats["misses"] += 1
        result = self.provider.get_item(item_id)
        self.cache[item_id] = CacheEntry(result, time.time())
        return result

    def get_items(self, item_ids: list[str]) -> list[dict[str, Any]]:
        """Get multiple items. Called frequently with 50-200 IDs."""
        results = []
        for item_id in item_ids:
            result = self.get_item(item_id)
            results.append(result)
        return results

    def get_dashboard_data(self, user_id: str) -> dict[str, Any]:
        """Build a dashboard view for a user.
        Called on every page load (~500 req/min at peak).
        """
        # Get user's saved items
        user_profile = self.provider.get_item(f"user:{user_id}")
        saved_ids = user_profile.get("saved_items", [])

        # Fetch each saved item
        items = self.get_items(saved_ids)

        # Fetch category info for each item
        categories: dict[str, dict[str, Any]] = {}
        for item in items:
            cat_id = item.get("category_id", "")
            if cat_id:
                cat_data = self.provider.get_item(f"category:{cat_id}")
                categories[cat_id] = cat_data

        # Build summary string
        summary = ""
        for item in items:
            summary = summary + f"- {item['name']}: ${item['price']:.2f}\n"

        return {
            "user": user_profile,
            "items": items,
            "categories": categories,
            "summary": summary,
            "generated_at": time.time(),
        }

    def invalidate(self, item_id: str) -> None:
        """Remove an item from cache."""
        if item_id in self.cache:
            del self.cache[item_id]

    def get_stats(self) -> dict[str, Any]:
        return {
            **self.stats,
            "cache_size": len(self.cache),
            "hit_rate": (
                self.stats["hits"] / (self.stats["hits"] + self.stats["misses"])
                if (self.stats["hits"] + self.stats["misses"]) > 0
                else 0.0
            ),
        }


# ---------------------------------------------------------------------------
# ANALYSIS QUESTIONS
#
# 1. PERFORMANCE: The `get_items` method is called with 50-200 IDs.
#    What is the time complexity? How would you fix it?
#
# 2. N+1 PATTERN: In `get_dashboard_data`, how many network calls are made
#    if a user has 30 saved items across 10 categories? How would you reduce
#    this?
#
# 3. MEMORY: The cache grows without bound. What happens after the service
#    runs for days ingesting diverse item IDs? What eviction strategy would
#    you add and why?
#
# 4. STALE DATA: Cache entries never expire. What problems does this cause?
#    How would you add TTL-based expiration?
#
# 5. STRING BUILDING: The summary construction in `get_dashboard_data` uses
#    repeated string concatenation. Why is this inefficient in Python?
#    What's the idiomatic alternative?
#
# 6. CONCURRENCY: If this service runs in a multi-threaded server, what
#    race conditions exist? How would you make it thread-safe?
#
# 7. OVERALL: Rank the top 3 issues by severity and propose fixes for each.
# ---------------------------------------------------------------------------
