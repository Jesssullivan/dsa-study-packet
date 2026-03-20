"""Tests for LRU Cache."""

import pytest

from algo.linked_lists.lru_cache import LRUCache, LRUCacheManual


class TestLRUCache:
    def test_basic_get_put(self) -> None:
        cache = LRUCache(2)
        cache.put(1, 1)
        cache.put(2, 2)
        assert cache.get(1) == 1
        cache.put(3, 3)  # evicts key 2
        assert cache.get(2) == -1

    def test_update_existing_key(self) -> None:
        cache = LRUCache(2)
        cache.put(1, 1)
        cache.put(2, 2)
        cache.put(1, 10)  # update key 1
        assert cache.get(1) == 10
        cache.put(3, 3)  # evicts key 2 (not 1, since 1 was just updated)
        assert cache.get(2) == -1
        assert cache.get(1) == 10

    def test_get_missing_key(self) -> None:
        cache = LRUCache(1)
        assert cache.get(99) == -1

    def test_capacity_one(self) -> None:
        cache = LRUCache(1)
        cache.put(1, 1)
        cache.put(2, 2)  # evicts key 1
        assert cache.get(1) == -1
        assert cache.get(2) == 2

    def test_eviction_order(self) -> None:
        cache = LRUCache(3)
        cache.put(1, 1)
        cache.put(2, 2)
        cache.put(3, 3)
        cache.get(1)  # 1 is now most recently used
        cache.put(4, 4)  # evicts key 2 (least recently used)
        assert cache.get(2) == -1
        assert cache.get(1) == 1
        assert cache.get(3) == 3
        assert cache.get(4) == 4

    def test_zero_capacity_raises(self) -> None:
        with pytest.raises(ValueError):
            LRUCache(0)


class TestLRUCacheManual:
    def test_basic_get_put(self) -> None:
        cache = LRUCacheManual(2)
        cache.put(1, 1)
        cache.put(2, 2)
        assert cache.get(1) == 1
        cache.put(3, 3)  # evicts key 2
        assert cache.get(2) == -1

    def test_update_existing_key(self) -> None:
        cache = LRUCacheManual(2)
        cache.put(1, 1)
        cache.put(2, 2)
        cache.put(1, 10)
        assert cache.get(1) == 10
        cache.put(3, 3)  # evicts key 2
        assert cache.get(2) == -1
        assert cache.get(1) == 10

    def test_get_missing_key(self) -> None:
        cache = LRUCacheManual(1)
        assert cache.get(99) == -1

    def test_capacity_one(self) -> None:
        cache = LRUCacheManual(1)
        cache.put(1, 1)
        cache.put(2, 2)
        assert cache.get(1) == -1
        assert cache.get(2) == 2

    def test_eviction_order(self) -> None:
        cache = LRUCacheManual(3)
        cache.put(1, 1)
        cache.put(2, 2)
        cache.put(3, 3)
        cache.get(1)
        cache.put(4, 4)  # evicts key 2
        assert cache.get(2) == -1
        assert cache.get(1) == 1
        assert cache.get(3) == 3
        assert cache.get(4) == 4

    def test_zero_capacity_raises(self) -> None:
        with pytest.raises(ValueError):
            LRUCacheManual(0)
