#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>

int main()
{
    char buf[2];
    char nums[10] = {
            0b01111110, 0b00110000, 0b01101101, 0b01111001, 0b00110011,
            0b01011011, 0b00011111, 0b01110000, 0b01111111, 0b01110011};
    char temp;
    int fd = open("/dev/virtual_buffer", O_WRONLY);
    lseek(fd, 0L, SEEK_SET);

    int i;
    int j;
    while(1)
    {
        j = 0;
        for(i = 1; i < 10; i++)
        {
            buf[1] = i;
            buf[0] = nums[j];
            write(fd, buf, 2);
            j = j + 1;
        }
        temp = nums[0];
        for(i = 0; i < 9; i++)
        {
            nums[i] = nums[i+1];
        }
        nums[9] = temp;
        sleep(1);
    }

    close(fd);
    return 0;
}
