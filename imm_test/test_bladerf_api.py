from bladerf import _bladerf
import numpy as np
import matplotlib.pyplot as plt

sdr = _bladerf.BladeRF()

# print("Device info:", _bladerf.get_device_list()[0])
# print("Version: ", _bladerf.version())
# print("Firmware version: ", sdr.get_fw_version())
# print("FPGA version: ", sdr.get_fpga_version())

rx_ch = sdr.Channel(_bladerf.CHANNEL_RX(0))
# print("sample_rate_range: ", rx_ch.sample_rate_range)
# print("bandwidth_range: ", rx_ch.bandwidth_range)
# print("frequency_range:", rx_ch.frequency_range)
# print("gain_modes: ", rx_ch.gain_modes)
# print("manual gain range:", sdr.get_gain_range(_bladerf.CHANNEL_RX(0)))

sample_rate = 15.36e6
center_freq = 3.5e9
gain = 50   # -15 to 60 dB
num_samples = int(1e6)

rx_ch.frequency = center_freq
rx_ch.sample_rate = sample_rate
rx_ch.bandwidth = sample_rate/2
rx_ch.gain_mode = _bladerf.GainMode.Manual
rx_ch.gain = gain

##################################################
# Receiving samples in python 
# - from pysdr

# Setup synchronous stream
sdr.sync_config(layout=_bladerf.ChannelLayout.RX_X1, 
                fmt = _bladerf.Format.SC16_Q11, #init16s
                num_buffers    = 16,
                buffer_size    = 8192,
                num_transfers  = 8,
                stream_timeout = 3500)

# create recieve buffer
bytes_per_sample = 4    # don't change this, it will always use init16s
buf = bytearray(1024 * bytes_per_sample)

# enable module
print("Starting recieve")
rx_ch.enable = True

# Receive loop
x = np.zeros(num_samples, dtype=np.complex64)
num_samples_read = 0
while True:
    if num_samples > 0 and num_samples_read == num_samples:
        break
    elif num_samples > 0:
        num = min(len(buf) // bytes_per_sample, num_samples - num_samples_read)
    else:
        num = len(buf) // bytes_per_sample
    sdr.sync_rx(buf, num)   # Read into buffer
    samples = np.frombuffer(buf, dtype=np.int16)
    samples = samples[0::2] + 1j * samples[1::2]    # convert to complex type
    samples /= 2048.0   # scale to -1 to 1 (its using 12 bit ADC)
    x[num_samples_read:num_samples_read+num] = samples[0:num]   # store buf in samples array
    num_samples_read += num

print("Stopping")
rx_ch.enable = False
print(x[0:10])
print(np.max(x))