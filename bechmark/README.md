# Instructions for Running Benchmarks

Follow these steps to run the benchmarking scripts and record the results for analysis:

## Prerequisites

1. **Python Environment**:

   - Ensure Python is installed on your system.
   - Use the virtual environment provided in the project (`myenv`).

2. **Dependencies**:
   - Activate the virtual environment:
     ```bash
     source myenv/bin/activate
     ```
   - Install required packages if not already installed:
     ```bash
     pip install -r requirements.txt
     ```

## Running the Benchmark Script

1. Navigate to the project directory:

   ```bash
   cd /Users/shibi/Documents/College-Projects/Quantum-Watermarking
   ```

2. Run the benchmarking script:

   ```bash
   python benchmark_shamir_vs_quantum.py
   ```

3. Observe the output in the terminal. The script will display the embedding and retrieval times for both the Shamir algorithm and quantum watermarking.

## Recording Results

1. Copy the output from the terminal.
2. Paste the results into a text file or directly into the "Results" section of the conference paper draft.
3. Optionally, save the results in a CSV file for further analysis.

## Visualizing Results

1. Use a tool like Excel, Google Sheets, or Python libraries (e.g., Matplotlib, Seaborn) to create graphs and charts.
2. Suggested visuals:
   - Bar charts comparing embedding and retrieval times.
   - Tables summarizing the metrics for both methods.

## Next Steps

- Analyze the recorded data to identify trends and differences.
- Update the "Results and Discussion" section of the paper with the findings.
- Include visuals to enhance the presentation of the results.
