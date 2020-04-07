#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <unistd.h>

int main() {
    printf("Escalate permission from %d to root\n", getuid());
    setuid(0);
    printf("modprobe v4l2loopback with uid: %d\n", getuid());
    system("modprobe -r v4l2loopback");
    system("modprobe v4l2loopback");
    printf("Done\n");
    return 0;
}
