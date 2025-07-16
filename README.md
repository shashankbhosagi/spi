# SPI LOOPBACK TEST

test_spi.py - calls spidev xfer2 10 times and prints the result.
spi.hex - a minimal spi that just listens the master the cpu and sends whatever
that is present in the spi buff {the buff contains the previous sent byte}
