# src/algorithm.py
# Manual min-heap implementation + top-k and anomaly detection
import math

class MinHeap:
    def __init__(self):
        self.data = []

    def _parent(self, i): return (i - 1) // 2
    def _left(self, i): return 2 * i + 1
    def _right(self, i): return 2 * i + 2

    def push(self, val):
        # val: (key_value, key_id) where key_value is the heap ordering (count)
        self.data.append(val)
        self._sift_up(len(self.data) - 1)

    def pop(self):
        if not self.data:
            return None
        top = self.data[0]
        last = self.data.pop()
        if self.data:
            self.data[0] = last
            self._sift_down(0)
        return top

    def peek(self):
        return self.data[0] if self.data else None

    def __len__(self):
        return len(self.data)

    def _sift_up(self, i):
        while i > 0:
            p = self._parent(i)
            if self.data[p][0] <= self.data[i][0]:
                break
            self.data[p], self.data[i] = self.data[i], self.data[p]
            i = p

    def _sift_down(self, i):
        n = len(self.data)
        while True:
            l = self._left(i)
            r = self._right(i)
            smallest = i
            if l < n and self.data[l][0] < self.data[smallest][0]:
                smallest = l
            if r < n and self.data[r][0] < self.data[smallest][0]:
                smallest = r
            if smallest == i:
                break
            self.data[i], self.data[smallest] = self.data[smallest], self.data[i]
            i = smallest

def top_k_from_iterable(iterable_counts, k=10):
    """
    iterable_counts: iterable of (key, count) pairs
    returns list of (key, count) sorted descending by count
    """
    heap = MinHeap()
    for key, count in iterable_counts:
        item = (count, key)
        if len(heap) < k:
            heap.push(item)
        else:
            if count > heap.peek()[0]:
                heap.pop()
                heap.push(item)
    out = []
    while len(heap):
        c, key = heap.pop()
        out.append((key, c))
    out.reverse()
    return out

def compute_mean_std(values):
    # manual mean + std (two-pass)
    n = 0
    total = 0.0
    for v in values:
        n += 1
        total += v
    if n == 0:
        return None, None
    mean = total / n
    var_sum = 0.0
    for v in values:
        var_sum += (v - mean) ** 2
    variance = var_sum / n
    std = math.sqrt(variance)
    return mean, std

def detect_fare_per_km_outliers(trip_iterable, multiplier=3.0):
    """
    trip_iterable: iterable of dict-like objects with 'fare_per_km' and optional trip identifiers
    returns list of outlier items
    """
    values = []
    for t in trip_iterable:
        v = t.get("fare_per_km")
        if v is not None:
            values.append(v)
    mean, std = compute_mean_std(values)
    if mean is None:
        return []
    threshold_high = mean + multiplier * std
    threshold_low = mean - multiplier * std
    outliers = []
    for t in trip_iterable:
        v = t.get("fare_per_km")
        if v is None:
            continue
        if v > threshold_high or v < threshold_low:
            outliers.append(t)
    return outliers
