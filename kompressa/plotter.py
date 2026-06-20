import matplotlib.pyplot as plt
import numpy as np
from typing import List
from .metrics import MetricEntry

class Plotter:
    def __init__(self, metrics: List[MetricEntry], group_name: str = ""):
        self.metrics = metrics
        self.group_name = group_name

    def plot_all(self, output_dir: str):
        self.plot_compression_ratio(output_dir)
        self.plot_compression_speed(output_dir)
        self.plot_decompression_speed(output_dir)
        self.plot_speed_vs_ratio(output_dir)
        self.plot_size_vs_ratio(output_dir)
        self.plot_distributions(output_dir)

    def _add_subtitle(self):
        if self.group_name:
            plt.suptitle(f"Group: {self.group_name}", fontsize=10, color='gray')

    def plot_size_vs_ratio(self, output_dir: str):
        plt.figure(figsize=(10, 6))
        self._add_subtitle()
        algorithms = sorted(list(set(m.algorithm for m in self.metrics)))
        
        for alg in algorithms:
            alg_metrics = [m for m in self.metrics if m.algorithm == alg]
            sizes = [m.original_size / 1024 / 1024 for m in alg_metrics]
            ratios = [m.compression_ratio for m in alg_metrics]
            plt.scatter(sizes, ratios, label=alg, alpha=0.6)

        plt.xlabel('Initial File Size (MB)')
        plt.ylabel('Compression Ratio')
        plt.title('Initial File Size vs Compression Ratio')
        plt.legend()
        plt.savefig(f"{output_dir}/size_vs_ratio.png")
        plt.close()

    def plot_distributions(self, output_dir: str):
        algorithms = sorted(list(set(m.algorithm for m in self.metrics)))
        
        # Plot distribution for Ratio
        plt.figure(figsize=(10, 6))
        self._add_subtitle()
        for alg in algorithms:
            ratios = [m.compression_ratio for m in self.metrics if m.algorithm == alg]
            plt.hist(ratios, alpha=0.5, label=alg, bins=15)
        plt.xlabel('Compression Ratio')
        plt.ylabel('Frequency')
        plt.title('Distribution of Compression Ratios')
        plt.legend()
        plt.savefig(f"{output_dir}/dist_ratio.png")
        plt.close()

        # Plot distribution for Compression Speed
        plt.figure(figsize=(10, 6))
        self._add_subtitle()
        for alg in algorithms:
            speeds = [(m.original_size / 1024 / 1024) / m.compression_time for m in self.metrics if m.algorithm == alg]
            plt.hist(speeds, alpha=0.5, label=alg, bins=15)
        plt.xlabel('Compression Speed (MB/s)')
        plt.ylabel('Frequency')
        plt.title('Distribution of Compression Speeds')
        plt.legend()
        plt.savefig(f"{output_dir}/dist_comp_speed.png")
        plt.close()

        # Plot distribution for Decompression Speed
        plt.figure(figsize=(10, 6))
        self._add_subtitle()
        for alg in algorithms:
            speeds = [(m.original_size / 1024 / 1024) / m.decompression_time for m in self.metrics if m.algorithm == alg]
            plt.hist(speeds, alpha=0.5, label=alg, bins=15)
        plt.xlabel('Decompression Speed (MB/s)')
        plt.ylabel('Frequency')
        plt.title('Distribution of Decompression Speeds')
        plt.legend()
        plt.savefig(f"{output_dir}/dist_decomp_speed.png")
        plt.close()

        # Plot distribution for Initial Size
        plt.figure(figsize=(10, 6))
        self._add_subtitle()
        initial_sizes = [m.original_size / 1024 / 1024 for m in self.metrics if m.algorithm == algorithms[0]]
        plt.hist(initial_sizes, alpha=0.7, color='grey', bins=15)
        plt.xlabel('Initial File Size (MB)')
        plt.ylabel('Frequency')
        plt.title('Distribution of Initial File Sizes')
        plt.savefig(f"{output_dir}/dist_initial_size.png")
        plt.close()

        # Plot distribution for Compressed Size
        plt.figure(figsize=(10, 6))
        self._add_subtitle()
        for alg in algorithms:
            comp_sizes = [m.compressed_size / 1024 / 1024 for m in self.metrics if m.algorithm == alg]
            plt.hist(comp_sizes, alpha=0.5, label=alg, bins=15)
        plt.xlabel('Compressed File Size (MB)')
        plt.ylabel('Frequency')
        plt.title('Distribution of Compressed File Sizes')
        plt.legend()
        plt.savefig(f"{output_dir}/dist_compressed_size.png")
        plt.close()

        # Plot distribution for Compression Time
        plt.figure(figsize=(10, 6))
        self._add_subtitle()
        for alg in algorithms:
            times = [m.compression_time for m in self.metrics if m.algorithm == alg]
            plt.hist(times, alpha=0.5, label=alg, bins=15)
        plt.xlabel('Compression Time (s)')
        plt.ylabel('Frequency')
        plt.title('Distribution of Compression Times')
        plt.legend()
        plt.savefig(f"{output_dir}/dist_comp_time.png")
        plt.close()

        # Plot distribution for Decompression Time
        plt.figure(figsize=(10, 6))
        self._add_subtitle()
        for alg in algorithms:
            times = [m.decompression_time for m in self.metrics if m.algorithm == alg]
            plt.hist(times, alpha=0.5, label=alg, bins=15)
        plt.xlabel('Decompression Time (s)')
        plt.ylabel('Frequency')
        plt.title('Distribution of Decompression Times')
        plt.legend()
        plt.savefig(f"{output_dir}/dist_decomp_time.png")
        plt.close()

    def plot_compression_ratio(self, output_dir: str):
        plt.figure(figsize=(10, 6))
        self._add_subtitle()
        algorithms = sorted(list(set(m.algorithm for m in self.metrics)))
        ratios = [np.mean([m.compression_ratio for m in self.metrics if m.algorithm == alg]) for alg in algorithms]
        
        plt.bar(algorithms, ratios, color='skyblue')
        plt.xlabel('Algorithm')
        plt.ylabel('Average Compression Ratio')
        plt.title('Average Compression Ratio by Algorithm')
        plt.savefig(f"{output_dir}/compression_ratio.png")
        plt.close()

    def plot_compression_speed(self, output_dir: str):
        plt.figure(figsize=(10, 6))
        self._add_subtitle()
        algorithms = sorted(list(set(m.algorithm for m in self.metrics)))
        # Speed in MB/s
        speeds = [np.mean([(m.original_size / 1024 / 1024) / m.compression_time for m in self.metrics if m.algorithm == alg]) for alg in algorithms]
        
        plt.bar(algorithms, speeds, color='salmon')
        plt.xlabel('Algorithm')
        plt.ylabel('Average Compression Speed (MB/s)')
        plt.title('Average Compression Speed by Algorithm')
        plt.savefig(f"{output_dir}/compression_speed.png")
        plt.close()

    def plot_decompression_speed(self, output_dir: str):
        plt.figure(figsize=(10, 6))
        self._add_subtitle()
        algorithms = sorted(list(set(m.algorithm for m in self.metrics)))
        # Speed in MB/s
        speeds = [np.mean([(m.original_size / 1024 / 1024) / m.decompression_time for m in self.metrics if m.algorithm == alg]) for alg in algorithms]
        
        plt.bar(algorithms, speeds, color='lightgreen')
        plt.xlabel('Algorithm')
        plt.ylabel('Average Decompression Speed (MB/s)')
        plt.title('Average Decompression Speed by Algorithm')
        plt.savefig(f"{output_dir}/decompression_speed.png")
        plt.close()

    def plot_speed_vs_ratio(self, output_dir: str):
        plt.figure(figsize=(10, 6))
        self._add_subtitle()
        algorithms = sorted(list(set(m.algorithm for m in self.metrics)))
        
        for alg in algorithms:
            alg_metrics = [m for m in self.metrics if m.algorithm == alg]
            ratios = [m.compression_ratio for m in alg_metrics]
            speeds = [(m.original_size / 1024 / 1024) / m.compression_time for m in alg_metrics]
            plt.scatter(ratios, speeds, label=alg, alpha=0.6)

        plt.xlabel('Compression Ratio')
        plt.ylabel('Compression Speed (MB/s)')
        plt.title('Compression Speed vs Ratio')
        plt.legend()
        plt.savefig(f"{output_dir}/speed_vs_ratio.png")
        plt.close()
