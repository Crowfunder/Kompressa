import subprocess
import time
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Tuple

class CompressionAlgorithm(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def compress(self, input_path: Path, output_path: Path) -> float:
        """Compresses input_path to output_path. Returns time taken."""
        pass

    @abstractmethod
    def decompress(self, input_path: Path, output_path: Path) -> float:
        """Decompresses input_path to output_path. Returns time taken."""
        pass

class ZstdAlgorithm(CompressionAlgorithm):
    @property
    def name(self) -> str:
        return "zstd"

    def compress(self, input_path: Path, output_path: Path) -> float:
        start = time.perf_counter()
        subprocess.run(["zstd", "-f", str(input_path), "-o", str(output_path)], check=True, capture_output=True)
        return time.perf_counter() - start

    def decompress(self, input_path: Path, output_path: Path) -> float:
        start = time.perf_counter()
        subprocess.run(["zstd", "-d", "-f", str(input_path), "-o", str(output_path)], check=True, capture_output=True)
        return time.perf_counter() - start

class GzipAlgorithm(CompressionAlgorithm):
    @property
    def name(self) -> str:
        return "gzip"

    def compress(self, input_path: Path, output_path: Path) -> float:
        start = time.perf_counter()
        # gzip doesn't have a simple -o for output file without redirection or -c
        with open(output_path, "wb") as f_out:
            subprocess.run(["gzip", "-c", str(input_path)], stdout=f_out, check=True)
        return time.perf_counter() - start

    def decompress(self, input_path: Path, output_path: Path) -> float:
        start = time.perf_counter()
        with open(output_path, "wb") as f_out:
            subprocess.run(["gzip", "-dc", str(input_path)], stdout=f_out, check=True)
        return time.perf_counter() - start

class XzAlgorithm(CompressionAlgorithm):
    @property
    def name(self) -> str:
        return "xz"

    def compress(self, input_path: Path, output_path: Path) -> float:
        start = time.perf_counter()
        subprocess.run(["xz", "-kf", str(input_path), "--stdout"], check=True, stdout=open(output_path, "wb"))
        return time.perf_counter() - start

    def decompress(self, input_path: Path, output_path: Path) -> float:
        start = time.perf_counter()
        subprocess.run(["xz", "-df", str(input_path), "--stdout"], check=True, stdout=open(output_path, "wb"))
        return time.perf_counter() - start

def get_algorithms() -> List[CompressionAlgorithm]:
    return [ZstdAlgorithm(), GzipAlgorithm(), XzAlgorithm()]
