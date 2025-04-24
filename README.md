# Write MODTRAN tp5 file
Here are personal codes for generating .tp5 files, which are the necessary inputs of [MODerate resolution atmospheric TRANsmission (MODTRAN)](http://modtran.spectral.com/).

Descriptions of files:
* create_cards.py: creation of CARD 1-5 in MODTRAN .tp5 file
* read_profiles.py: read atmospheric profiles (such as tempearture and moisture), then feed into CARD 2C
* read_outputs.py: read the target variables from MODTRAN output files (e.g., .tp7 and .flx)
* main.ipynb: an example

---
If our code is helpful to your research, please cite the most relevant of our previous publications, where appropriate:
```
[1] Zhang H, Tang B H, Li Z L. A practical two-step framework for all-sky land surface temperature estimation[J]. Remote Sensing of Environment, 2024, 303: 113991.
[2] Zhang H, Hu T, Tang B H, et al. Deep learning coupled with split window and temperature-emissivity separation (DL-SW-TES) method improves clear-sky high-resolution land surface temperature estimation[J]. ISPRS Journal of Photogrammetry and Remote Sensing, 2025, 225: 1-18.
[3] Zhang H, Hu T, Tang B H, et al. Revisit of the Temperature and Emissivity Separation Algorithm (TES) towards Model Refinement[J]. IEEE Transactions on Geoscience and Remote Sensing, 2025.
[4] Zhang H, Tang B H. Retrieval of daytime surface upward longwave radiation under all-sky conditions with remote sensing and meteorological reanalysis data[J]. IEEE Transactions on Geoscience and Remote Sensing, 2022, 60: 1-13.
```