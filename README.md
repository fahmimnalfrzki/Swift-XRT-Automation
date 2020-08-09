# Autonomous Swift-XRT Data Reduction Script

This autonomous scripts were built in Python 3.6
This automation script system is an updated version and this is built for my bachelor thesis work. Also, this was used by several projects that are my research with my supervisor and it was presented on South Asia Astronomy Network Meeting 2019 in NUS, Singapore, Ultraluminous X-ray Sources research group, Master thesis of an ITB master student, and other bachelor theses.

Swift-XRT

Swift mission or The Neil Gehrels Swift Observatory is one of the X-ray Astronomy satellite mission. It was launched at 17:16 GMT on 20th November 2004. It managed by NASA Goddard Space Flight Center and operated by Penn State University. It is carrying three telescopes which are BAT (Burst Alert Telescope - Gamma ray wavelenght), XRT (X-ray Telescope - X-ray wavelength), and UVOT (Ultraviolet - Optical Telescope - UV and Optic wavelength). 

The aim of this scripts are to perform data reduction of X-ray sources which are from X-ray binaries from raw Swift-XRT data (it can be accessed on https://heasarc.gsfc.nasa.gov/cgi-bin/W3Browse/w3browse.pl) to the data that ready to analyze. Since XRT consists of several modes, I only perform data reduction from Photon-Counting mode (PC) and Windowed Timing mode (WT). This scripts will recognize which data is from PC and WT mode automatically. This scripts are used for studies of X-ray binaries which have black hole or neutron star as the object compact and Ultraluminous X-ray Sources which are presumed as X-ray radiation source from an accretion disk around Intermediate-Mass Black Hole.

The data reduction was performed on Heasoft 6.26.1 and XSPEC 12.10.1f. Therefore, this automation should be run on Linux terminal and do not forget to run Heasoft previously.

This system consist of two main features which are obj.txt file and swiftotomasi folder.
obj.txt file consists list of object that want to be studied and swiftotomasi folder consists of the python script files.

In swiftotomasi folder there are python files which are:
Main Scripts:
- main.py |
This script wraps other main scripts. In general, this script will call calb.py,extrct.py,calb.py,and reduc.py. Before running those scripts, main.py will read obj.txt and find coordinate of the objects that listed on obj.txt using Astropy package automatically on Vizier, but if the source cannot be found on Vizier and other astronomical catalog, you can provide the coordinate on obj.txt.

- calb.py |
This script is used to perform data calibration using Xrtpipeline task on Heasoft 6.26.1. The output will be po_cl.evt file and it is copied to each obsid event folder.
- extrct.py |
This script performs image and spectra (source and background) extraction using xselect task.
- reduc.py |
This script performs spectra reduction. The reduction includes expomap creation, arf file creation, and group the spectra and other reduction files. Also, this script copies the rmf file from CALDB to each obsid event folder.
- function.py |
This script performs region files creation, and define the Heasoft file caller.


Additional Scripts:
- object.py |
This script is used to make obj.txt
- xspec_fit.py |
This script performs spectral fitting using Xspec. The output is .xcm file of each obsid
- xcm_ambildata.py |
This script catches spectral fitting parameters from .xcm file and store them into an Excel file including fitting model parameters and their error, reduced Chi-squared value, count rate value and its error, flux values and their error.
- HR_ULX.py |
This script is used for extract hardness ration parameters of ULX from .xcm file
- fakeitswift.py |
This script extracts hard color and soft color values for building a color-color diagram model.
- datproc.py |
This script plots color-color diagram model based on the output of fakeitswift.py

**Disclaimer**
This automation scripts are still under improvement. However, you can use it for your project that the same purpose. If you want to use it or ask further information about the scripts, you can contact me on email: fahmimn21@gmail.com. Any suggestion and critics are welcome!

