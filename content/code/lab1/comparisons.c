#include <stdio.h>
#include <stdbool.h>

int main(int argc, char* argv[])
{
    int x;

    x = (5 > -1) + (3 <= 4) +
        (2*2 == 2+2) + (2*3 != 2+3);

    printf("x = %d\n", x);

    return 0;
}
