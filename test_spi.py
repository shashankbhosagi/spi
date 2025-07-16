import spidev
import time

# === SPI Setup ===
spi = spidev.SpiDev()
spi.open(1, 0)  # /dev/spidev1.0
spi.mode = 0
spi.max_speed_hz = 12_000_000
spi.bits_per_word = 8

hist_tx = None;

for i in range(10):
    tx = [i%256]
    tx_t = [i%256]
    rx = spi.xfer2(tx)
    if hist_tx is not None:
        print(f"TX: {tx_t[0]}, RX: {rx[0]}, Match: {hist_tx == rx[0]}") 
    hist_tx = tx_t[0] 
