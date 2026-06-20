# Abstract
Kompressa - A framework that benchmarks compression algorithms and returns data in neat format, as well as gives various plots. For now it will be used for benchmarking zstd against other algorithms.

## Tech details
- Written in python
- Implements 3 compression algorithms by default
- Modular design
- Produces plots that compare data
- Easy definition of experiments


## Components
- Loader: Loads dataset provided from folder path, (use data/silesia as a reference). The module should yield a list of files under the provided folder, that are to be compressed
- Execution: Features definable plugins that implement compression algorithms through executing system binaries (such as "zstd", "zlib", "lzma"). Exposes list of objects that have algorithm name, compress method and decompress method.  
- Metrics: Gathers and organizes metrics related to compression results and algorithms. Should measure: compression and decompression time, compression ratio, initial file size and compressed file size. It should expose methods for reading the metrics as well as write them to csv files
- Plotter: It should read the metrics gathered by Metrics module, and create custom matplotlib plots. Include all relevant plots for compression algorithms, such as compression ratio comparison between algorithms, compression and decompression speed, compression speed vs ratio and some other
- Main: Connects all the components into a single pipeline
- CLI: Command line interface that exposes Main functionality



