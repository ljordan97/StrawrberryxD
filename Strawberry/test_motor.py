import spidev
spi = spidev.SpiDev()
spi.open(bus, device)
#spi.open(spidev1.0, device)
to_send = [0x01, 0x02, 0x03]
spi.xfer(to_send)
