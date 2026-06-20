import csv
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List

@dataclass
class MetricEntry:
    algorithm: str
    group_name: str
    file_name: str
    original_size: int
    compressed_size: int
    compression_time: float
    decompression_time: float

    @property
    def compression_ratio(self) -> float:
        return self.original_size / self.compressed_size if self.compressed_size > 0 else 0

class MetricsManager:
    def __init__(self):
        self.entries: List[MetricEntry] = []

    def add_entry(self, entry: MetricEntry):
        self.entries.append(entry)

    def get_metrics(self) -> List[MetricEntry]:
        return self.entries

    def write_to_csv(self, output_path: str):
        if not self.entries:
            return

        keys = list(asdict(self.entries[0]).keys()) + ["compression_ratio"]
        with open(output_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            for entry in self.entries:
                data = asdict(entry)
                data["compression_ratio"] = entry.compression_ratio
                writer.writerow(data)
