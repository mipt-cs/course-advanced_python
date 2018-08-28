#include <stdio.h>

int main()
{
    printf("I'm a Bot. What's your name?\n");
    char name;
    scanf("%s", name);
    printf("Hello, %s! How old are you?\n");
    int age;
    scanf("%d", age);
    printf("You are looking younger! "
           "I thought you are %d!\n", age-3);
    return 0;
}
