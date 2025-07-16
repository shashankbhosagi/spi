import spidev
import sys
from collections import defaultdict

def parse_byte(value: str) -> int:
    """Parse a byte from hex (FF) or binary (0b10101010)."""
    if value.startswith("0b"):  # binary input
        return int(value, 2)
    else:  # default hex
        return int(value, 16)

def main():
    if len(sys.argv) != 4:
        print(f"Usage: python {sys.argv[0]} <baudrate> <byte_to_send> <count>")
        print(f"  <byte_to_send> can be hex (FF) or binary (0b10101010)")
        print(f"Example: python {sys.argv[0]} 12000000 FF 10")
        print(f"         python {sys.argv[0]} 500000 0b10101010 5")
        sys.exit(1)

    baudrate = int(sys.argv[1])            # e.g. 12000000
    byte_to_send = parse_byte(sys.argv[2]) # supports hex or binary
    count = int(sys.argv[3])               # how many bytes to send

    # === SPI Setup ===
    spi = spidev.SpiDev()
    spi.open(1, 0)  # /dev/spidev1.0
    spi.mode = 0
    spi.max_speed_hz = baudrate
    spi.bits_per_word = 8

    sent_bits = f"{byte_to_send:08b}"
    match_count = 0
    mismatch_patterns = defaultdict(int)

    print(f"Sending: {sent_bits} ({byte_to_send:02X})")
    print("Received bits:")

    for _ in range(count):
        rx = spi.xfer2([byte_to_send])[0]
        rx_bits = f"{rx:08b}"
        print(rx_bits, end=" ")

        if rx == byte_to_send:
            match_count += 1
        else:
            mismatch_patterns[rx_bits] += 1

    print("\n\n=== REPORT ===")
    print(f"Total sent:     {count}")
    print(f"Matched:        {match_count}")
    print(f"Mismatched:     {count - match_count}")

    if mismatch_patterns:
        print("\nMismatched patterns:")
        for pattern, occurrences in mismatch_patterns.items():
            print(f"  {pattern} -> {occurrences} times")

if __name__ == "__main__":
    main()


