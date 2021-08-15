# Medoid-HLS-Compositing

https://bharathk113.github.io

![GitHub stars](https://img.shields.io/github/stars/bharathk113/Medoid-HLS-Compositing)
![GitHub forks](https://img.shields.io/github/forks/bharathk113/Medoid-HLS-Compositing)
[![Maintenance](https://img.shields.io/badge/maintained-yes-green.svg)](https://github.com/bharathk113/Medoid-HLS-Compositing/commits/master)
[![Ask Me Anything !](https://img.shields.io/badge/ask%20me-linkedin-1abc9c.svg)](https://www.linkedin.com/in/bharathk113/)
[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

:star: Star me on GitHub — it helps!

## Introduction to Data 📋
Harmonized Landsat and Sentinel (HLS) [1] project by NASA was initiated to generate surface reflectance data acquired from both Landsat OLI and Sentinel-2 MSI sensors.  The products from this project are cloud corrected, cloud shadow masked with better spatial co-registration, common gridding with illumination and view angle normalization and bandpass adjustment. Atmospheric correction is also applied to the data. For more technical details on the products from this project please visit Harmonized Landsat Sentinel-2 (nasa.gov)

The harmonized term means the products from both the sensors are radiometrically, spectrally, and geometrically corrected to generate a seamless HLS product that is stackable in time series and perform any analysis. These products can also be the building blocks of "data cube" which provides a unique advantage of observing any pixel every 2-3 days in some parts of the world.

## Time composite generation 📋
The multi-temporal and harmonized multi-sensor data can be utilized to prepare composite images that can be representative of the specific time period. This implementation is based on an article [3] that uses medoids for compositing. Since medoid is just a multi-dimensional median the composited image shall be robust to extreme values and hence cloud-free and shadow-free in most cases. Further, the advantage of using HLS data sets in this is the availability of data from different sensors increase the probability of obtaining a better and seamless composite image.

Since the data helps in reducing the probability of missing data, noise and other contaminations, the data can be used in a multitude of applications such as understanding the seasonal variations in crops, reliable monitoring of crop growth, etc.

This technique is slightly different to the median reducer used on the earth engine. The median reducer on earth engine “returns a multi-band Image, each pixel of which is the median of all unmasked pixels in the ImageCollection at that pixel location. Specifically, the reducer has been repeated for each band of the input imagery, meaning that the median is computed independently in each band. Note that the band names have the name of the reducer appended: ‘B1_median’, ‘B2_median’, etc.”[2]. Since each pixel is a median from all the bands there is a very good chance for the final pixel to be having a reflectance value from different dates and hence a not suitable candidate of analyzing any spectral characteristics.

The technique implemented here doesn’t compute the median for individual bands separately but considers the pixel (all the bands included) as a point in n-dimensional space. For every pixel along with the time series, an n-dimensional point is generated. The medoid of those pixels is the pixel that has the lowest sum of the distances from all other pixels in that n-d space. Since all the bands of the medoid are from a single image in time series data, meaning the resultant pixel can be spectrally analyzed meaningfully.

This technique [3] is applied to Landsat TM/ETM+ data and was published in 2013. The same has been implemented for HLS data in python here. This is still a development version and users are advised to report any bugs or issues with the implementation.

Link to the repo on Github: [Medoid-HLS-Compositing](https://github.com/bharathk113/Medoid-HLS-Compositing)

References
1. Martin Claverie, Junchang Ju, Jeffrey G. Masek, Jennifer L. Dungan, Eric F. Vermote, Jean-Claude Roger, Sergii V. Skakun, Christopher Justice, The Harmonized Landsat and Sentinel-2 surface reflectance data set, Remote Sensing of Environment, Volume 219, 2018, Pages 145-161, ISSN 0034-4257, https://doi.org/10.1016/j.rse.2018.09.002. (https://www.sciencedirect.com/science/article/pii/S0034425718304139)

2. ImageCollection Reductions | Google Earth Engine | Google Developers. (n.d.). Retrieved August 13, 2021, from https://developers.google.com/earth-engine/guides/reducers_image_collection

3. Flood, N. (2013). Seasonal Composite Landsat TM/ETM+ Images Using the Medoid (a Multi-Dimensional Median). Remote Sensing 2013, Vol. 5, Pages 6481-6500, 5(12), 6481–6500. https://doi.org/10.3390/RS5126481


## Running the Script 📦
- Download the repository
- Download the sample HLS images from [google drive](https://drive.google.com/drive/folders/1IvfuO6wsUnuJ9cDRo15OB4ffSNJoxHKe?usp=sharing) or from [HLS Sentinel](https://lpdaac.usgs.gov/products/hlss30v015/) and [HLS Landsat](https://lpdaac.usgs.gov/products/hlsl30v015/)
- Extract the files into folder named subset and run the code

## Required Python Packages 🛠️
* [<b>GDAL</b>](https://gdal.org/) - For reading and writing geospatial datasets.
* [<b>Numpy</b>](https://numpy.org/) - For all other computations.
* glob, os, and math

## Contributing 💡
#### Step 1

- **Option 1**
    - 🍴 Fork this repo!

- **Option 2**
    - 👯 Clone this repo to your local machine.


#### Step 2

- **Make changes to the code** 🔨🔨🔨

#### Step 3

- 🔃 Create a new pull request.

## License 📄
This project is licensed under the MIT License - see the [LICENSE.md](./LICENSE) file for details.
