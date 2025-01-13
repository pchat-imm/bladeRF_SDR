bladerf_send_pss_seq.md

## task
1. in `workarea/npn_5g/bladeRF_SDR/imm_test/test_bladerf_api.py`
in pysdr - understand each lines of `Recieving samples in python` section

follow pysdr tutorial along with bladerf tutorial
- https://pysdr.org/content/bladerf.html
- https://github.com/Nuand/bladeRF/blob/master/host/examples/python/txrx/txrx.py


-----------------------------------------------------------------------------------------------------------------------------------------
## Current process

from: https://pysdr.org/content/bladerf.html
```
cd bladeRF/host
cd ../libraries/libbladeRF_bindings/python
sudo python3 setup.py install
```
can run `bladerf-tool`


1. test its functionality by receiving 1M samples in the FM radio band, at 10 MHz sample rate, to a file /tmp/samples.sc16:
```
$ bladerf-tool rx --num-samples 1000000 /tmp/samples.sc16 100e6 10e6
[WARNING @ host/libraries/libbladeRF/src/bladerf.c:563] Setting gain mode to manual
```
it works and it return a 4MB /tmp/samples.sc16 file.

2. test python API
```
$ python3
>>> import bladerf
>>> bladerf.BladeRF()
<BladeRF(<DevInfo(libusb:device=4:2 instance=0 serial=04b118a874844193991adcd5af35ea4a)>)>
>>> exit()
```
3. (PYTHON) print info of bladerf sdr
```
from bladerf import _bladerf
import numpy as np
import matplotlib.pyplot as plt

sdr = _bladerf.BladeRF()

print("Device info:", _bladerf.get_device_list()[0])
print("Version: ", _bladerf.version())
print("Firmware version: ", sdr.get_fw_version())
print("FPGA version: ", sdr.get_fpga_version())

rx_ch = sdr.Channel(_bladerf.CHANNEL_RX(0))
print("sample_rate_range: ", rx_ch.sample_rate_range)
print("bandwidth_range: ", rx_ch.bandwidth_range)
print("frequency_range:", rx_ch.frequency_range)
print("gain_modes: ", rx_ch.gain_modes)
print("manual gain range:", sdr.get_gain_range(_bladerf.CHANNEL_RX(0)))
```
4. (PYTHON) example of setup
```
sample_rate = 15.36e6
center_freq = 3.5e9
gain = 50   # -15 to 60 dB
num_samples = int(1e6)

rx_ch.frequency = center_freq
rx_ch.sample_rate = sample_rate
rx_ch.bandwidth = sample_rate/2
rx_ch.gain_mode = _bladerf.GainMode.Manual
rx_ch.gain = gain
```

### Receiving samples in python
