#include <stdio.h>

int main(int argc, char* argv[])
{
    int start, stop, step;
    printf("Generator of progression.\n"
           "Enter start, stop, step:");
    scanf("%d%d%d", &start, &stop, &step);

    int sign = (step > 0)? +1: -1;
    int x = start;
    while (sign*x < sign*stop)
    {
        printf("x = %d\n", x);
        x += step;
    }

    printf("After: x = %d\n", x);

    return 0;
}
