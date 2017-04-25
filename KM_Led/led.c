#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>

int main()
{
    char buf[16];
    int fd = open("/proc/my_led1", O_RDONLY);
    while(1)
    {
        lseek(fd, 0L, SEEK_SET);
        read(fd, buf, 16);
        for(int i = 1; i < 9; i++)
        {
            printf("%c", buf[i]);
        }
        fflush(stdout);
        sleep(1);
        printf("\r");
    }

    close(fd);
}
