import os
import shutil
from pathlib import Path
from .loader import load_config
from .execution import get_algorithms
from .metrics import MetricsManager, MetricEntry
from .plotter import Plotter

def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=40, fill='█', print_end="\r"):
    """
    Call in a loop to create terminal progress bar
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(" "*100, end=print_end)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=print_end)
    if iteration == total:
        print()

def benchmark_files(group_name: str, files: list, output_dir: Path):
    os.makedirs(output_dir, exist_ok=True)
    tmp_dir = output_dir / "tmp"
    os.makedirs(tmp_dir, exist_ok=True)

    metrics_manager = MetricsManager()
    algorithms = get_algorithms()
    
    total_tasks = len(files) * len(algorithms)
    completed_tasks = 0

    print(f"  Files: {len(files)}, Algorithms: {len(algorithms)}")
    print_progress_bar(0, total_tasks, prefix='  Progress:', suffix='Complete', length=50)

    for file_path in files:
        original_size = file_path.stat().st_size
        if original_size == 0:
            completed_tasks += len(algorithms)
            print_progress_bar(completed_tasks, total_tasks, prefix='  Progress:', suffix='Complete', length=50)
            continue
            
        for algo in algorithms:
            comp_path = tmp_dir / f"{file_path.name}.{algo.name}"
            decomp_path = tmp_dir / f"{file_path.name}.{algo.name}.decomp"

            try:
                comp_time = algo.compress(file_path, comp_path)
                compressed_size = comp_path.stat().st_size
                
                decomp_time = algo.decompress(comp_path, decomp_path)
                
                entry = MetricEntry(
                    algorithm=algo.name,
                    group_name=group_name,
                    file_name=file_path.name,
                    original_size=original_size,
                    compressed_size=compressed_size,
                    compression_time=comp_time,
                    decompression_time=decomp_time
                )
                metrics_manager.add_entry(entry)
                
                if comp_path.exists():
                    comp_path.unlink()
                if decomp_path.exists():
                    decomp_path.unlink()
            except Exception as e:
                print(f"\n  Error benchmarking {file_path.name} with {algo.name}: {e}")
            
            completed_tasks += 1
            print_progress_bar(completed_tasks, total_tasks, prefix='  Progress:', suffix=f'Complete ({algo.name} on {file_path.name})', length=50)

    # Write CSV
    csv_path = output_dir / "metrics.csv"
    metrics_manager.write_to_csv(str(csv_path))

    # Plot
    plotter = Plotter(metrics_manager.get_metrics(), group_name=group_name)
    plotter.plot_all(str(output_dir))

    # Cleanup tmp dir
    shutil.rmtree(tmp_dir)

def run_benchmark(config_path: str, output_root: str):
    # Ensure root output directory exists
    os.makedirs(output_root, exist_ok=True)
    
    groups = load_config(config_path)
    print(f"Starting benchmarks for {len(groups)} groups...")

    for group in groups:
        name = group['name']
        files = group['files']
        print(f"\nProcessing group: {name}")
        
        group_output_dir = Path(output_root) / name
        benchmark_files(name, files, group_output_dir)
    
    print(f"\nAll benchmarks completed. Results saved in {output_root}")
