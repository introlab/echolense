_Documentation release: October 5, 2023_

<p align="center">
 <picture>
  <source media="(prefers-color-scheme: dark)" srcset=".github/logo_dark_theme.svg" width="520">
  <img alt="EchoLense" src=".github/logo_light_theme.svg" width="520">
 </picture>
</p>


EchoLense is an open-source acoustic camera made by [IntRoLab](https://introlab.3it.usherbrooke.ca/mediawiki-introlab/index.php/Main_Page). It aims to provide a flexible platform for the scientific community to further research in the field. It can be built with common off-the-shelf components and a 3D printer. This repo contains the STL files to build one as well as assembly instructions. We've also provided 1000 room impulse responses (RIRs) that we measured with the device and you'll find python scripts to measure your own RIRs if necessary.

## Assembly instructions

### Bill of material
|         **Part**         | **Number** |                                              **URL**                                              |
|:------------------------:|:----------:|:-------------------------------------------------------------------------------------------------:|
|    3D printed housing    |      1     |               _See housing folder of this repo_       |
|    Arducam USB camera    |      1     |               https://ca.robotshop.com/products/arducam-8mp-1080p-usb-camera-module      |
| ReSpeaker Mic Array v2.0 |      1     | https://ca.robotshop.com/products/seeedstudio-respeaker-mic-array-v20-far-field-4-pdm-microphones|
|       M2x6mm screws      |      5     |                                                 -                                                 |
|       M3x4mm screws      |      2     |                                                 -                                                 |
| Micro USB to DIP adapter |      1     |          https://www.amazon.ca/Adapter-Female-Connector-Converter-pinboard/dp/B0CDBP341B/         |
|   4-wires ribbon cable   |      1     |                                                 -                                                 |

_We are not affiliated with any of links provided above. Those are just examples of components similar to the ones we used._

### Instructions
1. Remove the camera's native USB connector.
2. Cut the ribbon cable so it has a length of around 90 mm and solder one of its ends to the camera's connector. Solder the other end of the cable to the micro USB to DIP adapter.
4. Using the two M3x4mm screws, secure the micro USB to DIP adapter in the bottom of the housing.
5. Insert the camera in its socket.
6. Place the mic array on top of the bottom part of the housing, place the camera on top of the mic array and secure everything using three M2x6mm screws.
7. Finally, close the housing and secure it using the last M2x6mm screws and the holes on the sides.

## Room impulse responses
