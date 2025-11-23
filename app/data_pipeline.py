"""Simplified data pipeline used for integration tests."""

from __future__ import annotations

import itertools
from dataclasses import dataclass
from typing import Iterable, List


@dataclass
class DataRecord:
    id: int
    payload: dict


class DataPipeline:
    def __init__(self):
        self._storage: List[DataRecord] = []
        self._id_counter = itertools.count(1)

    def load(self, rows: Iterable[dict]) -> List[DataRecord]:
        records = [DataRecord(next(self._id_counter), payload=row) for row in rows]
        return records

    def transform(self, records: Iterable[DataRecord]) -> List[DataRecord]:
        transformed = []
        for record in records:
            enriched = {**record.payload, "is_active": record.payload.get("amount", 0) > 0}
            transformed.append(DataRecord(record.id, enriched))
        return transformed

    def persist(self, records: Iterable[DataRecord]) -> None:
        self._storage.extend(records)

    def run(self, rows: Iterable[dict]) -> List[DataRecord]:
        records = self.load(rows)
        transformed = self.transform(records)
        self.persist(transformed)
        return transformed

    @property
    def storage(self) -> List[DataRecord]:
        return list(self._storage)
