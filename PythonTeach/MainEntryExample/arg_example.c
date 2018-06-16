#include <stdio.h>
#include <stdlib.h>

int sum(int, int);

int main(int argc, char *argv[]) {
    int x = atoi(argv[1]);
    int y = atoi(argv[2]);

    printf("%d + %d = %d\n", x, y, sum(x, y));

    return 0;
}

int sum(int a, int b) {
    return a+b;
}
