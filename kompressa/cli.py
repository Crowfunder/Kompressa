import argparse
import sys
from .main import run_benchmark

logo = """
▖▖                 
▙▘▛▌▛▛▌▛▌▛▘█▌▛▘▛▘▀▌
▌▌▙▌▌▌▌▙▌▌ ▙▖▄▌▄▌█▌
       ▌           
"""
def main():
    parser = argparse.ArgumentParser(description="Kompressa - Compression Algorithm Benchmarking Framework")
    parser.add_argument("config", help="Path to the YAML configuration file")
    parser.add_argument("--output", "-o", default="results", help="Directory to save results (default: results)")

    args = parser.parse_args()

    try:
        print(logo)
        run_benchmark(args.config, args.output)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
