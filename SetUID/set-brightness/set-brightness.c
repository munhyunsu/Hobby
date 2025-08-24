// set_brightness.c
#define _GNU_SOURCE
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main(int argc, char *argv[]) {
    const char *path = "/sys/class/backlight/intel_backlight/brightness";
    const char *val  = (argc > 1) ? argv[1] : "19393";

    int fd = open(path, O_WRONLY);
    if (fd < 0) { perror("open"); return 1; }

    dprintf(fd, "%s\n", val);
    if (close(fd) < 0) { perror("close"); return 1; }
    return 0;
}

