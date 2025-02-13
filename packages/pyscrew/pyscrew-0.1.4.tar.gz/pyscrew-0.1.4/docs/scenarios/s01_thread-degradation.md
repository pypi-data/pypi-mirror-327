# Screw Driving Dataset - s01_thread-degradation

<!-- Dataset Information -->
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.14855576.svg)](https://zenodo.org/uploads/14855576)
[![Dataset Size](https://img.shields.io/badge/Dataset_Size-5000_samples-blue)](https://github.com/nikolaiwest/pyscrew)

<!-- Version Information -->
[![Version](https://img.shields.io/badge/Version-v1.2.0-blue)](https://github.com/nikolaiwest/pyscrew)
[![Updated](https://img.shields.io/badge/Updated-2025/02/12-blue)](https://github.com/nikolaiwest/pyscrew)

<!-- Publication Information -->
[![Paper](https://img.shields.io/badge/DOI-10.24251%2FHICSS.2024.126-green)](https://hdl.handle.net/10125/106504)
[![ResearchGate](https://img.shields.io/badge/ResearchGate-00CCBB?logo=ResearchGate&logoColor=white)](https://www.researchgate.net/publication/379822823_A_Comparative_Study_of_Machine_Learning_Approaches_for_Anomaly_Detection_in_Industrial_Screw_Driving_Data)

## Table of Contents
- [Overview](#overview)
- [Quick Start](#quick-start)
- [Dataset Structure](#dataset-structure)
- [Experimental Setup](#experimental-setup)
- [Dataset Statistics](#dataset-statistics)
- [Usage Guidelines](#usage-guidelines)
- [Citations](#citations)
- [Repository](#repository)
- [Acknowledgments](#acknowledgments)
- [License](#license)

## Overview
This dataset examines thread degradation in plastic materials through repeated fastening operations.
It was generated using an automatic screwing station from EV motor control unit assembly.
It captures the progressive wear of plastic threads over multiple fastening cycles, providing insights into material degradation patterns and failure prediction.

Collection Date: Sept. 2022

## Quick Start

```python
from pyscrew import get_data

# Load and prepare the data (returns a dictionary)
data = get_data(scenario_name="s01_thread-degradation")

# Access measurements and labels
x_values = data["torque values"] # Available: torque, angle, time, gradient, step, class
y_values = data["class values"]
```

## Dataset Structure

The dataset consists of three primary components:

1. `/json` directory: Contains 5,000 individual JSON files of unprocessed screw driving operations, each recording the complete measurement data of a single screwing process.
2. `labels.csv`: A metadata file that collects key information from each operation (e.g. for classification). More Details are displayed in the table below.
3. `README.md`: This readme-file providing stand-alone context for the dataset.

### Labels File Structure

The `labels.csv` contains seven columns:

| Column             | Type    | Description                                                      |
|--------------------|---------|------------------------------------------------------------------|
| run_id             | int     | Unique cycle number as recorded by the screw station             |
| file_name          | string  | Name of corresponding JSON file with the measurements            |
| class_value        | integer | Specifies the [respective class](#classification-labels-classes) |
| result_value       | string  | Operation outcome (OK/NOK) as determined by the station          |
| workpiece_id       | string  | Unique workpiece identifier (14-digit) as data matrix code       |
| workpiece_usage    | integer | Previous operations count (0-24): number of screw runs           |
| workpiece_location | integer | Screw position (0: left, 1: right)                               |

### Classification Labels (Classes)

| Value  | Name      | Amount | Description                                                   |
|--------|-----------|--------|---------------------------------------------------------------|
| 0      | Baseline  | 5000   | No additional manipulations, only wear down from repeated use |


### JSON File Structure
Each JSON file represents a complete screw driving operation with the following structure:

#### System Configuration
- `format`: Data format specification
- `node id`: System identifier
- `hardware`: Hardware model (e.g., "CS351")
- `sw version`: Software version
- `MCE factor`: Measurement calibration factor
- `max. speed`: Maximum speed capability
- `nominal torque`: System's nominal torque setting

#### Operation Parameters
- `prg name`: Program name used for the operation
- `prg date`: Program creation/modification date
- `cycle`: Operation cycle number
- `date`: Timestamp of the operation
- `id code`: Work piece identifier (14-digit DMC)
- `torque unit`: Unit of measurement for torque (Nm)
- `total time`: Total operation duration (seconds)
- `tool serial`: Tool identifier

#### Tightening Steps
Each operation consists of four tightening steps:
1. Finding
2. Thread forming
3. Pre-tightening
4. Final tightening (1.4 Nm)

Each step contains:
- `step type`: Type of tightening step
- `name`: Step identifier
- `speed`: Angular velocity (degrees/minute)
- `result`: Step outcome (OK/NOK)
- `tightening functions`: Array of control parameters including:
  - Target values (`nom`)
  - Actual values (`act`)
  - Thresholds and limits

#### Time Series Data
Each step includes detailed measurement graphs containing:
- `angle values`: Rotation angle in degrees
- `torque values`: Applied torque in Nm
- `gradient values`: Rate of change
- `time values`: Timestamp for each measurement (seconds)
- Additional monitoring values (`torqueRed`, `angleRed`)

## Data Processing

The dataset is provided raw and underwent no additional preprocessing steps.

## Experimental Setup

### Equipment
- Automatic screwing station (EV motor control unit assembly)
- Delta PT 40x12 screws (thermoplastic-optimized)
- Target torque: 1.4 Nm (range: 1.2-1.6 Nm)
- Thermoplastic housing components

### Test Protocol
- Each workpiece uniquely identified via DMC
- Two test locations per workpiece (left/right)
- Maximum 25 cycles per location
- 100 unique workpieces
- 5,000 total operations
- Natural wear progression (no artificial errors)

## Dataset Statistics

### Sample Distribution
- Sample Metrics:
  - Total operations: 5,000
  - Unique workpieces: 100
  - Operations per workpiece: 50 (25 cycles × 2 sides)
- Quality Distribution:
  - Normal (OK): 4,089 (81.78%)
  - Anomalous (NOK): 911 (18.22%)

### Distribution by Class

| Value  | Name      | Samples | #OK  | #NOK | %OK   | %NOK  |
|--------|-----------|---------|------|------|-------|-------|
| 0      | Baseline  | 5000    | 4089 |  911 | 81.78 | 18.22 |


### Collection Timeline

**September 2022**
- Sep 5-7: Initial data collection (1,200 samples)
- Sep 8-9: Extended collection (1,150 samples)
- Sep 12-14: Further testing (1,400 samples)
- Sep 16: Final collection phase (1,250 samples)

### Data Quality
- Sampling frequency: 833.33 Hz
- Missing values: 4.45%
- Data completeness: 95.55%

### Key Characteristics
- Natural degradation progression
- Initial anomaly rate: 1.5% (from second connection)
- Peak anomaly rate: 41% (final cycle)
- Complete lifecycle coverage
- Dual independent test locations

## Usage Guidelines

### Data Access
Recommended approaches:
- Either via JSON library for operation data and Pandas/CSV readers for labels file
- Or via our custom `PyScrew` Python package (available in [this repository](https://github.com/nikolaiwest/pyscrew))

### Analysis Suggestions
- Torque-angle relationship evolution
- Degradation pattern analysis
- Location-based comparison
- Cycle-based failure probability
- Torque requirement trends
- Maximum rotation analysis

## Citations
If using this dataset, please cite:
- West, N., & Deuse, J. (2024). A Comparative Study of Machine Learning Approaches for Anomaly Detection in Industrial Screw Driving Data. Proceedings of the 57th Hawaii International Conference on System Sciences (HICSS), 1050-1059. https://hdl.handle.net/10125/106504


## Repository
Issues and questions: https://github.com/nikolaiwest/pyscrew

## Acknowledgments

These datasets were collected and prepared by:
- [RIF Institute for Research and Transfer e.V.](https://www.rif-ev.de/)
- [Technical University Dortmund](https://www.tu-dortmund.de/), [Institute for Production Systems](https://ips.mb.tu-dortmund.de/)
- Feel free to contact us directly for further questions: [Nikolai West (nikolai.west@tu-dortmund.de)](nikolai.west@tu-dortmund.de)

The preparation and provision of the research was supported by:

| Organization | Role | Logo |
|-------------|------|------|
| German Ministry of Education and Research (BMBF) | Funding | <img src="https://vdivde-it.de/system/files/styles/vdivde_logo_vdivde_desktop_1_5x/private/image/BMBF_englisch.jpg?itok=6FdVWG45" alt="BMBF logo" height="150"> |
| European Union's "NextGenerationEU" | Funding | <img src="https://www.bundesfinanzministerium.de/Content/DE/Bilder/Logos/nextgenerationeu.jpg?__blob=square&v=1" alt="NextGenerationEU logo" height="150"> |
| VDIVDE | Program Support | <img src="https://vdivde-it.de/themes/custom/vdivde/images/vdi-vde-it_og-image.png" alt="Projekttraeger VDIVDE logo" height="150"> |

This research is part of the funding program ["Data competencies for early career researchers"](https://www.bmbf.de/DE/Forschung/Wissenschaftssystem/Forschungsdaten/DatenkompetenzenInDerWissenschaft/datenkompetenzeninderwissenschaft_node.html). 

More information regarding the research project is available our [project homepage](https://prodata-projekt.de/).

## License

**MIT License**


Permission is hereby granted, free of charge, to any person obtaining a copy of this dataset and associated documentation files, to deal in the dataset without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the dataset, and to permit persons to whom the dataset is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the dataset.

THE DATASET IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE DATASET OR THE USE OR OTHER DEALINGS IN THE DATASET.

*Copyright (c) 2025 Nikolai West @ RIF/IPS*