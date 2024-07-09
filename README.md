# bladeRF_SDR
## purpose: to use BladeRF as SDR for the RAN system
- follow https://github.com/srsran/srsRAN_Project/discussions/222



<!-- toc -->

- [installation](#installation)
  * [1. SoapySDR](#1-soapysdr)
    + [Sources](#sources)
    + [Steps](#steps)
  * [2. SoapyBladeRF](#2-soapybladerf)
    + [Sources:](#sources)
    + [2.1. libBladeRF](#21-libbladerf)
    + [2.2 install SoapyBladeRF](#22-install-soapybladerf)
  * [3. SoapyUHD](#3-soapyuhd)
    + [Sources](#sources-1)
    + [3.1 UHD](#31-uhd)
    + [3.2 SoapyUHD](#32-soapyuhd)
  * [3. open5GS](#3-open5gs)
  * [4. srsRAN_Project](#4-srsran_project)

<!-- tocstop -->

## installation
from: https://github.com/srsran/srsRAN_Project/discussions/222

### 1. SoapySDR
#### Sources
from: https://github.com/pothosware/SoapySDR/wiki <br>

can download from package but we will build on source
- download from package: https://github.com/pothosware/PothosCore/wiki/Downloads#ubuntu-packages
- built from source: https://github.com/pothosware/SoapySDR/wiki/BuildGuide#ubuntu


#### Steps 
- install dependencies
```
sudo apt-get install cmake g++ libpython3-dev python3-numpy swig
```
- get from source code
```
git clone https://github.com/pothosware/SoapySDR.git
cd SoapySDR
```
- [future] next time update exisitng checkout
```
cd SoapySDR
git pull origin master
```
- build and install
```
mkdir build
cd build
```
- [intermittent] Install ccache (for fast re-compilation) - see: https://github.com/pchat-imm/o-ran-e2-kpm/wiki/USRP 

- continue on build and install
```
cmake ..
make -j`nproc`
sudo make install -j`nproc`
sudo ldconfig #needed on debian systems
SoapySDRUtil --info
```
- [future] rebuild after pulling from git
```
cd build

make -j4
sudo make install

# Repeat on project that depend on SoapySDR
```

### 2. SoapyBladeRF
#### Sources:
from: https://github.com/pothosware/SoapyBladeRF <br>

dependencies
- SoapySDR: https://github.com/pothosware/SoapySDR/wiki
- libBladeRF: https://github.com/nuand/bladeRF

#### 2.1. libBladeRF
from: https://github.com/nuand/bladeRF
1. clone
```
git clone https://github.com/Nuand/bladeRF.git
```
2. fetch latest FPGA images (https://www.nuand.com/fpga_images/)
3. fetch latest firmware image (https://www.nuand.com/fx3_images/)
4. build and install `libbladeRF` and `bladeRF-cli`
from: https://github.com/Nuand/bladeRF/tree/master/host
dependencies
- [libusb](https://libusb.info/)
- [CMake](https://cmake.org/)

build
```
cd bladeRF
mkdir -p build
cmake [options] ../
make
sudo make install
sudo ldconfig
```
note: choose `[option]` from the site (https://github.com/Nuand/bladeRF/tree/master/host)

5. attach bladeRF to the fastest USB port
6. check device with `bladeRF-cli -p` 
```
bladeRF-cli -p
  Description:    Nuand bladeRF 2.0
  Backend:        libusb
  Serial:         6685e220048b4304b28eb62a5e1a5c78
  USB Bus:        4
  USB Address:    2
```
7. view additional info via `bladeRF-cli -e info -e version`
```
bladeRF-cli -e info -e version

  Board:                    Nuand bladeRF 2.0 (bladerf2)
  Serial #:                 6685e220048b4304b28eb62a5e1a5c78
  VCTCXO DAC calibration:   0x1e03
  FPGA size:                49 KLE
  FPGA loaded:              yes
  Flash size:               32 Mbit
  USB bus:                  4
  USB address:              2
  USB speed:                SuperSpeed
  Backend:                  libusb
  Instance:                 0


  bladeRF-cli version:        1.9.0-git-b40cd829
  libbladeRF version:         2.5.0-git-b40cd829

  Firmware version:           2.4.0-git-a3d5c55f
  FPGA version:               0.15.0 (configured from SPI flash)
```

#### 2.2 install SoapyBladeRF
building SoapyBladeRF
```
git clone https://github.com/pothosware/SoapyBladeRF.git
cd SoapyBladeRF
mkdir build
cd build
cmake ..
make
sudo make install
```
detect blade RF
```
SoapySDRUtil --probe="driver=bladerf"
```

### 3. SoapyUHD
#### Sources
from: https://github.com/pothosware/SoapyUHD <br>

dependencies
- SoapySDR - https://github.com/pothosware/SoapySDR/wiki
- UHD - https://github.com/pothosware/SoapyUHD/wiki
- boost libraries - http://www.boost.org/

#### 3.1 UHD
from: https://files.ettus.com/manual/page_build_guide.html

- setting up dependencies on Ubuntu
```
sudo apt-get install autoconf automake build-essential ccache cmake cpufrequtils doxygen ethtool \
g++ git inetutils-tools libboost-all-dev libncurses5 libncurses5-dev libusb-1.0-0 libusb-1.0-0-dev \
libusb-dev python3-dev python3-mako python3-numpy python3-requests python3-scipy python3-setuptools \
python3-ruamel.yaml 
```
- getting source code
```
git clone https://github.com/EttusResearch/uhd.git
```
- generate Makefiles with CMake
```
cd uhd/host
mkdir build
cd build
cmake ../
```
- if success, then `make`
```
make
make test # optional
sudo make installl
```
setup library path
```
sudo ldconfig
```

#### 3.2 SoapyUHD
build and install
```
git clone https://github.com/pothosware/SoapyUHD.git
cd SoapyUHD
mkdir build
cd build
cmake ..
make
sudo make install
```
check soapy devices in uhd
```
uhd_find_devices 

[INFO] [UHD] linux; GNU C++ version 10.5.0; Boost_107400; UHD_4.7.0.0-0-ga5ed1872
--------------------------------------------------
-- UHD Device 0
--------------------------------------------------
Device Address:
    serial: 6685e220048b4304b28eb62a5e1a5c78
    backend: libusb
    device: 0x04:0x02
    driver: bladerf
    instance: 0
    label: BladeRF #0 [6685e220..5e1a5c78]
    type: soapy
```

### 3. open5GS
from: https://open5gs.org/open5gs/docs/guide/02-building-open5gs-from-sources/

- install `open5GS`
- config to `sample.yaml`
- config and get `open5GS webui`



using binaries provided by Ettus
```
sudo add-apt-repository ppa:ettusresearch/uhd
sudo apt-get update
sudo apt-get install libuhd-dev uhd-host
```

### 4. srsRAN_Project
from: https://docs.srsran.com/projects/project/en/latest/user_manuals/source/installation.html#build-tools-and-dependencies
- install dependencies
```
sudo apt-get install cmake make gcc g++ pkg-config libfftw3-dev libmbedtls-dev libsctp-dev libyaml-cpp-dev libgtest-dev
```
- install Ccache
- install backward-cpp (https://github.com/bombela/backward-cpp)
- build `srsRAN_Project`
```
git clone https://github.com/srsRAN/srsRAN_Project.git
cd srsRAN_Project
mkdir build
cd build
cmake ../
make -j $(nproc)
make test -j $(nproc)
sudo make install
```

## Config
### 1. Config bladeRF to be able to use as gNB
1. Remove the reference to `time_source` in `srsRAN_Project/lib/radio/uhd/radio_uhd_device.h:254`
```
#if UHD_VERSION < 3140099
    return safe_execution([this, &sync_src, &clock_src]() {
      // std::vector<std::string> time_sources = usrp->get_time_sources(0);
      // if (std::find(time_sources.begin(), time_sources.end(), sync_src) == time_sources.end()) {
        // on_error("Invalid time source {}. Supported: {}", sync_src, span<const std::string>(time_sources));
        // return;
      // }
      std::vector<std::string> clock_sources = usrp->get_clock_sources(0);
      if (std::find(clock_sources.begin(), clock_sources.end(), clock_src) == clock_sources.end()) {
        on_error("Invalid clock source {}. Supported: {}", clock_src, span<const std::string>(clock_sources));
        return;
      }

      // usrp->set_time_source(sync_src);
      usrp->set_clock_source(clock_src);
    });
```

2. Set the tx buffer timeout (`TRANSMIT_TIMEOUT_S`) to 0 in `srsRAN_Project/lib/radio/uhd/radio_uhd_tx_stream.h:44`
```
static constexpr double TRANSMIT_TIMEOUT_S = 0;
```

3. Set the rx buffer timeout (`RECEIVE_TIMEOUT_S`) to 0 in `
srsRAN_Project/lib/radio/uhd/radio_uhd_rx_stream.h:40`
```
static constexpr double RECEIVE_TIMEOUT_S = 0;
```
4. then build `srsRAN_Project` again

5. change `bladerf_set_gain_stage` to `bladerf_set_gain`. Then build `SoapyBladeRF` again
```
void bladeRF_SoapySDR::setGain(const int direction, const size_t channel, const std::string &name, const double value)
{
    // int ret = bladerf_set_gain_stage(_dev, _toch(direction, channel), name.c_str(), bladerf_gain(std::round(value)));
    ret = bladerf_set_gain(_dev, _toch(direction, channel), bladerf_gain(std::round(value)));
```
### 2. gNB 
```
amf:
  addr: 127.0.0.2                                               # The address or hostname of the AMF.
  bind_addr: 127.0.0.1                                            # A local IP that the gNB binds to for traffic from the AMF.

cu_cp:
  inactivity_timer: 7200

ru_sdr:
  device_driver: uhd                                            # The RF driver name.
  # device_args: type=bladeRF
  # clock: internal                                                       # Specify the clock source used by the RF.
  # sync: internal                                                        # Specify the sync source used by the RF.
  srate: 23.04                                                  # RF sample rate might need to be adjusted according to selected bandwidth.
  # srate: 30.72
  # srate: 46.08
  otw_format: sc12
  # tx_gain: 20                                                  # Transmit gain of the RF might need to adjusted to the given situation.
  # tx_gain: 70
  tx_gain: 89
  # rx_gain: 15                                                   # Receive gain of the RF might need to adjusted to the given situation.
  rx_gain: 60

cell_cfg:
  dl_arfcn: 627340                                                # ARFCN of the downlink carrier (center frequency).
  band: 78                                                        # The NR band.
  channel_bandwidth_MHz: 20                                       # @1mm- Bandwith in MHz. Number of PRBs will be automatically derived.
  # channel_bandwidth_MHz: 40
  common_scs: 30                                                  # Subcarrier spacing in kHz used for data.
  plmn: "90170"                                                   # PLMN broadcasted by the gNB.
  tac: 7                                                          # Tracking area code (needs to match the core configuration).
  pci: 1                                                          # Physical cell ID.

# pdsch:
     # mcs_table: qam256            # @1mm - Use QAM256 MCS table in downlink

log:
  filename: /tmp/gnb.log                                          # Path of the log file.
  all_level: debug                                             # Logging level applied to all layers.

pcap:
  mac_enable: true                                               # Set to true to enable MAC-layer PCAPs.
  mac_filename: /tmp/gnb_mac.pcap                                 # Path where the MAC PCAP is stored.
  ngap_enable: true                                              # Set to true to enable NGAP PCAPs.
  ngap_filename: /tmp/gnb_ngap.pcap                               # Path where the NGAP PCAP is stored.
  
metrics:
    enable_json_metrics: true       # Enable reporting metrics in JSON format
    addr: 172.19.1.4                # Metrics-server IP
    port: 55555                     # Metrics-server Port
```

## Result
### 1. gnb in bladerf
```
sudo ./gnb -c gnb_fllay3.yml 

--== srsRAN gNB (commit 4cf7513e9) ==--


The PRACH detector will not meet the performance requirements with the configuration {Format B4, ZCZ 0, SCS 30kHz, Rx ports 1}.
Lower PHY in quad executor mode.
N2: Connection to AMF on 127.0.0.2:38412 completed
Cell pci=1, bw=20 MHz, 1T1R, dl_arfcn=627340 (n78), dl_freq=3410.1 MHz, dl_ssb_arfcn=626976, ul_freq=3410.1 MHz

Available radio types: uhd.
[INFO] [UHD] linux; GNU C++ version 10.5.0; Boost_107400; UHD_4.7.0.0-0-ga5ed1872
[INFO] [LOGGING] Fastpath logging disabled at runtime.
[DEBUG] [MPMD] Discovering MPM devices on port 49600
[DEBUG] [MPMD] Discovering MPM devices on port 49600
[DEBUG] [MPMD] Discovering MPM devices on port 49600
[DEBUG] [MPMD] Discovering MPM devices on port 49600
[DEBUG] [MPMD] Discovering MPM devices on port 49600
[DEBUG] [MPMD] Discovering MPM devices on port 49600
No device type given, found device with address 'backend=libusb,device=0x04:0x02,driver=bladerf,instance=0,label=BladeRF #0 [6685e220..5e1a5c78],serial=6685e220048b4304b28eb62a5e1a5c78,type=soapy'
Making USRP object with args 'type=soapy'
[INFO] [UHDSoapyDevice] bladerf_open_with_devinfo()
[INFO] [UHDSoapyDevice] bladerf_get_serial() = 6685e220048b4304b28eb62a5e1a5c78
[INFO] [UHDSoapyDevice] setSampleRate(Rx, 0, 4.000000 MHz), actual = 4.000000 MHz
[INFO] [UHDSoapyDevice] setSampleRate(Tx, 0, 4.000000 MHz), actual = 4.000000 MHz
[INFO] [UHDSoapyDevice] setSampleRate(Tx, 0, 23.040000 MHz), actual = 23.040000 MHz
[INFO] [UHDSoapyDevice] setSampleRate(Tx, 1, 23.040000 MHz), actual = 23.040000 MHz
[INFO] [UHDSoapyDevice] setSampleRate(Rx, 0, 23.040000 MHz), actual = 23.040000 MHz
[INFO] [UHDSoapyDevice] setSampleRate(Rx, 1, 23.040000 MHz), actual = 23.040000 MHz
Error: setting gain for transmitter 0. Tx gain (i.e., 89.0 dB) is out-of-range. Range is [-89.75000762939453, 0.0] dB in steps of 0.25 dB.
```
### 2. Speedtest
from mobile phone that connect to the CPE (the UE)
<img src = "https://github.com/pchat-imm/bladeRF_SDR/assets/40858099/a755d358-9446-49b5-9671-cffdc2a63fc3" width="60%" height="auto"> <br>

- gnb trace
```
          |--------------------DL---------------------|-------------------------UL------------------------------
 pci rnti | cqi  ri  mcs  brate   ok  nok  (%)  dl_bs | pusch  rsrp  mcs  brate   ok  nok  (%)    bsr     ta  phr
   1 4602 |  15 1.0    0      0    0    0   0%      0 |   n/a   n/a    0      0    0    0   0%      0    97n   -1
   1 4602 |  15 1.0   27    32k   17    0   0%      0 |   2.4   ovl    6    40k    7    0   0%      0      0    1
   1 4602 |  15 1.0   27   754k  137    2   1%      0 |   3.8   ovl    9   323k   61    3   4%      0    89n    1
   1 4602 |  15 1.0   27   1.2M  134    3   2%      0 |   3.3   ovl    7   420k   77    2   2%      0      0    1
   1 4602 |  15 1.0   27   378k   65    4   5%      0 |   3.0   ovl    6   186k   37    0   0%      0    24n    1
   1 4602 |  15 1.0   26   138k   62    2   3%      0 |   3.5   ovl    7   338k   62    0   0%      0    89n    2
   1 4602 |  15 1.0   26    53k   16    0   0%      0 |   2.4   ovl    6    47k    9    0   0%      0   113n    0
   1 4602 |  15 1.0   26   400k   94    2   2%     65 |   2.7   ovl    6   241k   43    0   0%      0      0    1
   1 4602 |  15 1.0   26   3.6M  245    3   1%      0 |   3.4   ovl    7   535k   96    1   1%      0    97n    0
   1 4602 |  15 1.0   26   889k  158    2   1%      0 |   3.2   ovl    7   559k  107    0   0%      0   113n    0
   1 4602 |  15 1.0   26   877k  127    1   0%      0 |   3.0   ovl    7   277k   51    0   0%      0      0    0

          |--------------------DL---------------------|-------------------------UL------------------------------
 pci rnti | cqi  ri  mcs  brate   ok  nok  (%)  dl_bs | pusch  rsrp  mcs  brate   ok  nok  (%)    bsr     ta  phr
   1 4602 |  15 1.0   26   2.8M  246    1   0%      0 |   4.3   ovl    9   327k   73    5   6%    535   105n    6
   1 4602 |  15 1.0   26   2.0M  173    0   0%      0 |   3.4   ovl    7   333k   67    0   0%      0   105n    0
   1 4602 |  15 1.0   27   205k   63    1   1%      0 |   2.7   ovl    6   146k   28    0   0%      0    65n    0
   1 4602 |  15 1.0   27    48k   45    0   0%     58 |   2.5   ovl    6   136k   26    0   0%      0    89n    0
   1 4602 |  15 1.0   27   5.9M  282    1   0%      0 |   3.9   ovl    8   302k   56    0   0%  1.04k      0    0
   1 4602 |  15 1.0   27    16M  618    0   0%      0 |   4.4   ovl    8   639k  122    8   6%  1.04k      0    0
   1 4602 |  15 1.0   28   9.8M  431    0   0%  4.62k |   3.9   ovl    7   783k  174   11   5%  2.81k   105n   -1
   1 4602 |  15 1.0   28    10M  445    0   0%      0 |   4.4   ovl    7   599k  144   15   9%  3.91k    81n   -1
   1 4602 |  15 1.0   28    13M  523    0   0%      0 |   4.5   ovl    6   533k  150    8   5%     10      0    0
   1 4602 |  15 1.0   28    11M  439    0   0%      0 |   4.6   ovl    7   469k  154   19  10%     74    89n    0
   1 4602 |  15 1.0   28    10M  463    0   0%      0 |   4.2   ovl    5   501k  178   10   5%      0    89n   -1

          |--------------------DL---------------------|-------------------------UL------------------------------
 pci rnti | cqi  ri  mcs  brate   ok  nok  (%)  dl_bs | pusch  rsrp  mcs  brate   ok  nok  (%)    bsr     ta  phr
   1 4602 |  15 1.0   28    12M  485    0   0%      0 |   4.0   ovl    4   390k  137    4   2%      0      0   -1
   1 4602 |  15 1.0   28    12M  515    0   0%      0 |   3.6   ovl    4   637k  212    0   0%      0   105n    0
   1 4602 |  15 1.0   28    13M  514    0   0%      0 |   3.9   ovl    4   582k  190    1   0%    745   113n   -1
   1 4602 |  15 1.0   27   4.6M  239    2   0%      0 |   3.9  -0.0    4   405k  135    5   3%      0      0    0
   1 4602 |  15 1.0   27    23k   26    0   0%      0 |   2.5   ovl    3    49k   17    0   0%      0    48n   -1
   1 4602 |  15 1.0   27   104k  106    0   0%      0 |  10.6  -1.1    9   1.4M  183    5   2%  77.3k    40n   -1
   1 4602 |  15 1.0   27   311k  317    0   0%    129 |  12.9  -1.9   13   4.8M  509   76  12%   300k    65n    0
   1 4602 |  15 1.0   27   196k  223    1   0%      0 |   3.0   ovl    4   1.9M  600    0   0%   300k    89n    0
   1 4602 |  15 1.0   27   292k  320    0   0%      0 |  11.3  -0.7   12   4.9M  544   56   9%   300k    56n    0
   1 4602 |  15 1.0   27   255k  251    4   1%      0 |  12.8  -2.1   14   4.5M  490  110  18%   300k    97n   -1
   1 4602 |  15 1.0   27   146k  169    0   0%      0 |   2.9   ovl    4   1.9M  600    0   0%   300k    89n    0

          |--------------------DL---------------------|-------------------------UL------------------------------
 pci rnti | cqi  ri  mcs  brate   ok  nok  (%)  dl_bs | pusch  rsrp  mcs  brate   ok  nok  (%)    bsr     ta  phr
   1 4602 |  15 1.0   27   366k  303    0   0%      0 |  14.8  -2.0   14   6.4M  561   39   6%   300k    81n   -1
   1 4602 |  15 1.0   27   285k  196    1   0%      0 |  11.1  -1.5   13   3.9M  481  119  19%   300k    97n    2
   1 4602 |  15 1.0   27   143k  198    0   0%      0 |   3.2   ovl    4   1.9M  600    0   0%   300k    97n    2
   1 4602 |  15 1.0   27   466k  384    2   0%      0 |  14.1  -1.3   15   6.1M  544   56   9%   300k    81n    0
   1 4602 |  15 1.0   27   251k  215    2   0%      0 |   9.4  -1.3   11   3.3M  488  112  18%   300k    65n   -1
   1 4602 |  15 1.0   27   159k  196    0   0%      0 |   4.4  -0.1    6   2.2M  569   31   5%   566k    89n    1
   1 4602 |  15 1.0   27   577k  436    1   0%     58 |  15.9  -2.2   15   7.0M  567   33   5%   300k    48n    1
   1 4602 |  15 1.0   27   264k  200    0   0%      0 |   7.8  -0.9   10   2.6M  482  118  19%   300k   113n    2
   1 4602 |  15 1.0   27   228k  205    1   0%      0 |   6.2  -0.2    7   2.5M  544   56   9%   300k    48n    0
   1 4602 |  15 1.0   27   785k  487    2   0%      0 |  14.3  -1.6   14   6.7M  565   18   3%  7.59k    40n    0
   1 4602 |  15 1.0   27   439k  124    4   3%      0 |   3.9   ovl    4   441k  132    0   0%      0      0   -2

          |--------------------DL---------------------|-------------------------UL------------------------------
 pci rnti | cqi  ri  mcs  brate   ok  nok  (%)  dl_bs | pusch  rsrp  mcs  brate   ok  nok  (%)    bsr     ta  phr
   1 4602 |  15 1.0   27   167k   47    0   0%      0 |   2.6   ovl    3    96k   34    0   0%      0   113n    0
   1 4602 |  15 1.0   27    42k   33    0   0%      0 |   2.6   ovl    3    60k   21    0   0%      0      0   -1
   1 4602 |  15 1.0   27    16k   20    0   0%      0 |   2.7   ovl    3    66k   23    0   0%      0      0   -2
   1 4602 |  15 1.0   27   701k   54    1   1%      0 |   2.9   ovl    3   112k   39    0   0%  3.91k    73n    0
   1 4602 |  15 1.0   27   1.1M  101    0   0%      0 |   3.3   ovl    3   147k   55    0   0%      0   130n   13
   1 4602 |  15 1.0   27   670k   90    0   0%      0 |   2.8   ovl    3   188k   67    0   0%      0    73n    0
   1 4602 |  15 1.0   27   636k   82    1   1%      0 |   2.9   ovl    3   172k   61    0   0%      0      0    2
   1 4602 |  15 1.0   27   248k   34    0   0%      0 |   2.5   ovl    3    59k   19    0   0%      0    65n    0
   1 4602 |  15 1.0   27    29k   18    0   0%      0 |   2.7   ovl    3    31k   11    0   0%      0    40n    2
   1 4602 |  15 1.0   27    21k   12    0   0%      0 |   2.7   ovl    3    34k   12    0   0%      0      0   -1
   1 4602 |  15 1.0   27   4.7k    7    0   0%      0 |   2.5   ovl    3    15k    5    0   0%      0   105n    0

          |--------------------DL---------------------|-------------------------UL------------------------------
 pci rnti | cqi  ri  mcs  brate   ok  nok  (%)  dl_bs | pusch  rsrp  mcs  brate   ok  nok  (%)    bsr     ta  phr
   1 4602 |  15 1.0   27   6.0k    3    0   0%      0 |   2.5   ovl    3   6.0k    2    0   0%      0    65n    0
   1 4602 |  15 1.0   27   2.7k    4    0   0%      0 |   2.4   ovl    3   8.9k    3    0   0%      0    65n    0
   1 4602 |  15 1.0   27   4.0k    6    0   0%      0 |   3.3   ovl    4    17k    6    0   0%      0   122n    1
   1 4602 |  15 1.0   27   1.3k    2    0   0%      0 |   2.5   ovl    3    18k    6    0   0%      0    56n    0
```

### 3. Iperf
- captured image from mobile phone, using `iperf client`
<img src="https://github.com/pchat-imm/bladeRF_SDR/assets/40858099/6a4357a5-90c2-4b8c-81e0-f5a5e7132891" width="60%" height="auto">
- gnb trace

```
         |--------------------DL---------------------|-------------------------UL------------------------------
 pci rnti | cqi  ri  mcs  brate   ok  nok  (%)  dl_bs | pusch  rsrp  mcs  brate   ok  nok  (%)    bsr     ta  phr
   1 4602 |  15 1.0    0      0    0    0   0%      0 |   n/a   n/a    0      0    0    0   0%      0    89n    1
   1 4602 |  15 1.0   27    12k   14    0   0%      0 |   2.5   ovl    3    39k   13    0   0%      0   138n    0
   1 4602 |  15 1.0   27   4.8M  194    0   0%      0 |   3.2   ovl    3   140k   50    0   0%      0    81n    0
   1 4602 |  15 1.0   28   8.3M  318    0   0%      0 |   3.6   ovl    5   299k  102    5   4%      0    81n    0
   1 4602 |  15 1.0   28   9.8M  363    0   0%      0 |   3.5   ovl    4   327k  116    0   0%      0      0    1
   1 4602 |  15 1.0   28   9.5M  358    0   0%      0 |   4.0   ovl    4   365k  123    6   4%      0    40n    0
   1 4602 |  15 1.0   28   5.2M  204    0   0%      0 |   3.3   ovl    3   286k  102    0   0%      0      0    1
   1 4602 |  15 1.0   27   8.7M  334    8   2%      0 |   3.7   ovl    4   349k  120    5   4%  2.01k    81n    0
   1 4602 |  15 1.0   26   9.4M  376    3   0%      0 |   3.7   ovl    4   263k   94    5   5%  1.04k    65n   -1
   1 4602 |  15 1.0   26   8.4M  338    2   0%  6.47k |   3.7   ovl    3   253k   98    1   1%      0    97n    0
   1 4602 |  15 1.0   27   9.9M  367    0   0%      7 |   3.3   ovl    3   246k   89    0   0%      0   113n    0

          |--------------------DL---------------------|-------------------------UL------------------------------
 pci rnti | cqi  ri  mcs  brate   ok  nok  (%)  dl_bs | pusch  rsrp  mcs  brate   ok  nok  (%)    bsr     ta  phr
   1 4602 |  15 1.0   27   9.0M  346    6   1%      0 |   4.7   ovl    6   271k  107   13  10%      0    89n    0
   1 4602 |  15 1.0   27   9.8M  371    2   0%      0 |   4.5   ovl    6   208k   81   13  13%      0    56n    0
   1 4602 |  15 1.0   27   9.6M  381    3   0%      0 |   4.0   ovl    4   305k  121    5   3%    535      0    5
   1 4602 |  15 1.0   26    11M  410    3   0%      0 |   3.3   ovl    3   290k  110    0   0%      0      0    1
   1 4602 |  15 1.0   27   9.1M  348    4   1%      0 |   4.0   ovl    5   266k   94    5   5%  1.04k   105n    1
   1 4602 |  15 1.0   26    11M  418    4   0%      0 |   4.0   ovl    5   271k   97    5   4%    102   113n    1
   1 4602 |  15 1.0   27   8.4M  322    1   0%      0 |   4.3  -0.0    4   268k  106    3   2%      0    97n    1
   1 4602 |  15 1.0   27   6.5M  268    3   1%      0 |   3.3   ovl    3   176k   74    3   3%      0   146n    2
   1 4602 |  15 1.0   27   6.8M  273    1   0%      0 |   3.7   ovl    4   191k   75    5   6%    745    73n    0
   1 4602 |  15 1.0   27    10M  383    1   0%      0 |   3.3   ovl    3   215k   82    0   0%      0    81n    1
   1 4602 |  15 1.0   27   8.8M  345    2   0%      0 |   3.7   ovl    4   228k   95    5   5%      0      0    0

          |--------------------DL---------------------|-------------------------UL------------------------------
 pci rnti | cqi  ri  mcs  brate   ok  nok  (%)  dl_bs | pusch  rsrp  mcs  brate   ok  nok  (%)    bsr     ta  phr
   1 4602 |  15 1.0   27    10M  392    8   2%      0 |   3.1   ovl    3   284k  100    0   0%      0    48n    1
   1 4602 |  15 1.0   27    11M  398    1   0%      0 |   3.7   ovl    4   255k   98    0   0%      0      0    3
   1 4602 |  15 1.0   27    10M  397    3   0%      0 |   3.3   ovl    3   284k  103    0   0%    535   105n    0
   1 4602 |  15 1.0   27    11M  424    1   0%      0 |   3.3   ovl    3   278k  103    0   0%      0      0   -1
   1 4602 |  15 1.0   27    12M  437    0   0%      0 |   3.2   ovl    3   266k   95    0   0%      0   105n   -1
   1 4602 |  15 1.0   27   9.9M  378    0   0%      0 |   3.2   ovl    3   298k  107    0   0%  2.01k      0   -1
   1 4602 |  15 1.0   27    11M  401    0   0%      0 |   3.2   ovl    3   313k  106    0   0%    745    73n    0
   1 4602 |  15 1.0   28    12M  449    0   0%      0 |   3.3   ovl    4   282k   95    0   0%      0      0   -2
   1 4602 |  15 1.0   28    13M  464    0   0%      0 |   3.6   ovl    4   306k  108    0   0%      0      0   -1
   1 4602 |  15 1.0   28    12M  442    0   0%      0 |   3.6   ovl    4   314k  104    5   4%    384      0    0
   1 4602 |  15 1.0   28   9.1M  342    0   0%      0 |   3.8   ovl    4   232k   89    5   5%      0   113n    0

          |--------------------DL---------------------|-------------------------UL------------------------------
 pci rnti | cqi  ri  mcs  brate   ok  nok  (%)  dl_bs | pusch  rsrp  mcs  brate   ok  nok  (%)    bsr     ta  phr
   1 4602 |  15 1.0   27   912k   41    0   0%      0 |   3.1   ovl    3    52k   19    0   0%      0   130n    0
   1 4602 |  15 1.0   27    14k    5    1  16%      0 |   2.4   ovl    3   8.9k    3    0   0%      0   113n    0
   1 4602 |  15 1.0   27   6.7k   10    0   0%      0 |   2.5   ovl    3    23k    8    0   0%      0   130n    0
   1 4602 |  15 1.0    0      0    0    0   0%      0 |   n/a   n/a    0      0    0    0   0%      0   138n    0
   1 4602 |  15 1.0    0      0    0    0   0%      0 |   n/a   n/a    0      0    0    0   0%      0   122n    0
   1 4602 |  15 1.0    0      0    0    0   0%      0 |   2.6   ovl    3   3.0k    1    0   0%      0   105n    0
   1 4602 |  15 1.0   27   9.4k    8    0   0%      0 |   2.4   ovl    3    15k    5    0   0%      0      0    0
   1 4602 |  15 1.0   27   101k   43    4   8%      0 |   2.5   ovl    3    92k   32    0   0%      0   105n    0
   1 4602 |  15 1.0   27   160k   31    0   0%      0 |   2.8   ovl    3   115k   41    0   0%      0   122n    0
   1 4602 |  15 1.0   27    58k   25    0   0%      0 |   2.9   ovl    3   106k   36    0   0%    276      0    0
   1 4602 |  15 1.0   27   648k   50    0   0%      0 |   3.6   ovl    4    78k   27    0   0%      0      0   15

          |--------------------DL---------------------|-------------------------UL------------------------------
 pci rnti | cqi  ri  mcs  brate   ok  nok  (%)  dl_bs | pusch  rsrp  mcs  brate   ok  nok  (%)    bsr     ta  phr
   1 4602 |  15 1.0   27    63k   22    0   0%      0 |   2.9   ovl    3    89k   30    0   0%      0    81n    0
   1 4602 |  15 1.0   27    14k    8    0   0%      0 |   2.6   ovl    3    15k    5    0   0%      0   105n    0
Late: 0; Underflow: 0; Overflow: 16;
   1 4602 |  15 1.0   27    19k   20    0   0%      0 |   2.8   ovl    3    72k   24    0   0%      0    65n    0
   1 4602 |  15 1.0   27    23k   17    0   0%      0 |   3.1   ovl    3    44k   16    0   0%      0      0    0
   1 4602 |  15 1.0   27   411k   49    0   0%      0 |   2.9   ovl    3    64k   22    0   0%      0    65n    0
   1 4602 |  15 1.0   27   118k   14    0   0%      0 |   2.8   ovl    3    26k    9    0   0%      0   105n    0
   1 4602 |  15 1.0   27   5.4k    6    0   0%      0 |   2.5   ovl    3    15k    5    0   0%      0    40n    0
   1 4602 |  15 1.0   27   8.1k   11    0   0%      0 |   2.6   ovl    3    24k    8    0   0%      0    73n    0
   1 4602 |  15 1.0    0      0    0    0   0%      0 |   n/a   n/a    0      0    0    0   0%      0    73n    0
   1 4602 |  15 1.0    0      0    0    0   0%      0 |   2.7   ovl    3   3.0k    1    0   0%      0    89n    0
   1 4602 |  15 1.0    0      0    0    0   0%      0 |   2.6   ovl    3   8.9k    3    0   0%      0    81n    0

          |--------------------DL---------------------|-------------------------UL------------------------------
 pci rnti | cqi  ri  mcs  brate   ok  nok  (%)  dl_bs | pusch  rsrp  mcs  brate   ok  nok  (%)    bsr     ta  phr
   1 4602 |  15 1.0    0      0    0    0   0%      0 |   2.6   ovl    3   3.0k    1    0   0%      0    65n    0
   1 4602 |  15 1.0   27   9.9k    9    0   0%      0 |   2.8   ovl    3    45k   15    0   0%      0    48n    0
   1 4602 |  15 1.0   27   3.4k    5    0   0%      0 |   2.4   ovl    3    12k    4    0   0%      0    81n   -1
   1 4602 |  15 1.0   27  10.0k    9    1  10%      0 |   2.6   ovl    3    52k   18    0   0%      0    73n    0
   1 4602 |  15 1.0   27   5.4k    7    0   0%      0 |   2.3   ovl    3    12k    4    0   0%      0      0    1
   1 4602 |  15 1.0   27    14k   14    0   0%      0 |   4.0   ovl    4    82k   25    0   0%      0    81n    0
   1 4602 |  15 1.0   27    15k   17    0   0%      0 |   2.7   ovl    3    61k   21    0   0%      0    89n    0
   1 4602 |  15 1.0   27    15k   19    0   0%      0 |   2.6   ovl    3    36k   12    0   0%      0      0    1
   1 4602 |  15 1.0   27   7.7k    8    0   0%      0 |   2.6   ovl    3    24k    8    0   0%      0    48n    2
   1 4602 |  15 1.0   27   6.7k    8    0   0%      0 |   2.8   ovl    3    29k   10    0   0%      0   105n    1
   1 4602 |  15 1.0   27    22k   18    1   5%      0 |   3.1   ovl    3    65k   22    0   0%      0    56n    6

          |--------------------DL---------------------|-------------------------UL------------------------------
 pci rnti | cqi  ri  mcs  brate   ok  nok  (%)  dl_bs | pusch  rsrp  mcs  brate   ok  nok  (%)    bsr     ta  phr
   1 4602 |  15 1.0   27   106k   32    2   5%      0 |   2.9   ovl    3   104k   36    0   0%      0    97n    1
   1 4602 |  15 1.0   27    47k   15    0   0%      0 |   3.0   ovl    3    32k   11    0   0%      0    89n    1
   1 4602 |  15 1.0   27    86k   29    1   3%      0 |   3.3   ovl    3   140k   45    0   0%      0    97n    0
   1 4602 |  15 1.0   27   4.6k    6    0   0%      0 |   2.7   ovl    3    12k    4    0   0%      0   105n    1
   1 4602 |  15 1.0   27    15k   12    0   0%      0 |   3.3   ovl    4    57k   18    0   0%      0      0    1
   1 4602 |  15 1.0   27   1.3k    2    0   0%      0 |   2.7   ovl    3   6.0k    2    0   0%      0    89n    0
   1 4602 |  15 1.0   27    13k   13    0   0%      0 |   3.0   ovl    3    72k   24    0   0%      0   113n    0
   1 4602 |  15 1.0   27   7.4k    6    0   0%      0 |   3.1   ovl    3    38k   13    0   0%      0   162n    1
   1 4602 |  15 1.0   27   5.4k    5    0   0%      0 |   2.5   ovl    3    21k    7    0   0%      0    48n   -2
```