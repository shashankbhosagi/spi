#include <gpiod.h>
#include <stdio.h>
#include <unistd.h>

#define CONSUMER "vaaman-toggle"
#define CHIPNAME "/dev/gpiochip2"
#define LINE_OFFSET 9  // PIN_31

#define ITERATIONS 10000000

int main(void) {
    struct gpiod_chip *chip;
    struct gpiod_line *line;
    int val = 0;

    chip = gpiod_chip_open(CHIPNAME);
    if (!chip) { perror("chip_open"); return 1; }
    line = gpiod_chip_get_line(chip, LINE_OFFSET);
    if (!line) { perror("chip_get_line"); return 1; }
    if (gpiod_line_request_output(line, CONSUMER, 0) < 0) {
        perror("line_request_output");
        return 1;
    }

    for (int i = 0; i < ITERATIONS; i++) {
        gpiod_line_set_value(line, val);
        val = !val;
    }

    gpiod_line_release(line);
    gpiod_chip_close(chip);
    return 0;
}
