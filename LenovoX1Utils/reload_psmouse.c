#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <unistd.h>

int main() {
    printf("Escalate permission from %d to root\n", getuid());
    setuid(0);
    printf("Reload psmouse with uid: %d\n", getuid());
    system("modprobe -r psmouse");
    system("modprobe psmouse");
    printf("Done\n");
    return 0;
}
