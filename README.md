# MapAnt France scripts

All the scripts used for the processing of LiDAR data to make [mapant.fr](http://mapant.fr/).

<!-- TABLE OF CONTENTS -->
## Table of Contents
<details open="open">
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

Inspired by [mapant.fi](http://mapant.fi), [mapant.no](http://mapant.no), [omap.nz](http://omap.nz), and recently [mapant.es](http://mapant.es) and [mapant.ch](https://mapant.ch/), this website is a first attempt (as far as I know) to generate an orienteering map from a large amount of LiDAR data in France. This pilot project was made with *[territoire français du Grand Genève](https://www.data.gouv.fr/fr/datasets/carroyage-des-dalles-des-points-lidar-2014-territoire-francais-grand-geneve/)* LiDAR data from 2014, and the *[BD TOPO](https://geoservices.ign.fr/documentation/diffusion/telechargement-donnees-libres.html#bd-topo)* database from the [French Geographic Institute](https://www.ign.fr/). I also used [OpenStreetMap](https://www.openstreetmap.org) data for residential areas. This project was a way to get used with the *LiDAR to map server* workflow, while waiting for the [full coverage of France](https://www.ign.fr/institut/nos-activites/lidar-hd-une-couverture-nationale-dici-2025).

This repository contains the source code of the [mapant.fr](http://mapant.fr/) website. To see the scripts that I wrote to generate the maps from the LiDAR data and made the tile pyramid, visit the [MapAnt scripts](https://github.com/NicoRio42/mapant-scripts) repository.

This repository contains all the scripts used for the processing of LiDAR data. Below are all the steps of the workflow:
- downloading the files with lidar_download
- thining and indexing the files with lidar_thin_index
- generating PNG files with [karttapullautin](http://www.routegadget.net/karttapullautin/)
- sorting the PNG files with lidar_sort
- generating the tile pyramid for the web portal with pullautin_to_tiles

To see the source code of [mapant.fr](http://mapant.fr/) website, visit [MapAnt France website](https://github.com/NicoRio42/mapant-website)

### Built With

* [LAStools](https://rapidlasso.com/LAStools/)
* [karttapullautin](http://www.routegadget.net/karttapullautin/)
* [Pillow](https://pillow.readthedocs.io/en/stable/)


<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

Upgrade pip
```sh
pip install --upgrade pip
```
Download virtualenv
```sh
pip install virtualenv --upgrade
```
Set up a virtual environment
```sh
python -m virtualenv env
```
Activate the virtual environment
```sh
env\Scripts\activate.bat
```

### Installation

Clone the repo
```sh
git clone https://github.com/NicoRio42/mapant-scripts.git
```
Install requirements
```sh
pip install requirements.txt
```


<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/NicoRio42/mapant-scripts/issues) for a list of proposed features (and known issues).



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

Nicolas Rio - nicolas.rio42@gmail.com

Project Link: [https://github.com/NicoRio42/mapant-scripts](https://github.com/NicoRio42/mapant-scripts)