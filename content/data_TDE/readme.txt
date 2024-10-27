
# Data_TDE Database

This folder contains the simulation results and related data for various configurations of cosmic ray and neutrino spectra, generated from astrophysical models. The data is organized in `.npy` format files, allowing easy loading and analysis using Python.

## Directory Structure

```
data_TDE/
│
├── energy_CR.npy               # Energy array used in cosmic ray spectrum calculations
├── energy_nu.npy               # Energy array used in neutrino spectrum calculations
│
├── dsg_<parameters>_<injected>_<group>.npy   # Spectrum data for DSG model
├── fdr_<parameters>_<injected>_<group>.npy   # Spectrum data for FDR model
├── aalc_<parameters>_<injected>_<group>.npy  # Spectrum data for AALC model
│
└── (many files with similar naming patterns)
```

### Naming Convention for Spectrum Files

Each file in the database follows a specific naming convention to indicate its model, configuration parameters, and spectrum type:

```
<model>_<radius>_<rigidity_max>_<B_value>_<input_spec>_<group>.npy
```

- **model**: Indicates the astrophysical model used. Possible values:
  - `dsg` for DSG model
  - `fdr` for FDR model
  - `aalc` for AALC model
- **radius**, **rigidity_max**, **B_value**: Indices representing configuration parameters.
- **input_spec**: Specifies the injected input spectrum configuration.
- **group**: Represents the atomic group or category used in the spectrum calculation:
  - `"1_1"`, `"2_4"`, `"5_14"`, `"15_28"`, `"29_56"` for specific atomic groups.
  - `"CR"` for cosmic ray spectra.
  - `"nu_source"` and `"nu_cosmo"` for source and cosmogenic neutrino spectra, respectively.

### Example Filenames

- `dsg_0_2_3_1_15_28.npy`: Spectrum data for the DSG model with radius=0, rigidity_max=2, B_value=3, input_spec=1, and atomic group 15–28.
- `aalc_1_3_5_2_CR.npy`: Cosmic ray spectrum data for the AALC model with radius=1, rigidity_max=3, B_value=5, input_spec=2.

## Contents of Each File

- **`energy_CR.npy`**: The energy array corresponding to all cosmic ray (`CR`) spectra.
- **`energy_nu.npy`**: The energy array for all neutrino (`nu_source` and `nu_cosmo`) spectra.
- **`<model>_<parameters>_<group>.npy` files**: Contain spectrum data as a numpy array, structured based on the configuration parameters and group.

## Usage

You can load these `.npy` files in Python using `numpy.load()`:

```python
import numpy as np

# Load energy array for cosmic rays
energy_CR = np.load("data_TDE/energy_CR.npy")

# Load specific spectrum data
spectrum_dsg = np.load("data_TDE/dsg_0_2_3_1_15_28.npy")
```

### Example Analysis Script

Here’s a quick example of plotting a spectrum:

```python
import matplotlib.pyplot as plt
import numpy as np

energy_CR = np.load("data_TDE/energy_CR.npy")
spectrum_dsg = np.load("data_TDE/dsg_0_2_3_1_15_28.npy")

plt.loglog(energy_CR, spectrum_dsg)
plt.xlabel("Energy")
plt.ylabel("Spectrum")
plt.title("DSG Model Spectrum for Group 15-28")
plt.show()
```

## Notes

- Ensure that the `data_TDE` folder and its contents are in the same directory as your Python scripts, or provide the full path.
- These spectra can be used for further astrophysical analyses and visualizations.
- If additional models or configurations are added, ensure they follow the same naming conventions for consistency.
