#include <stdlib.h>
#include <stdio.h>

int main(void)
{
    int acc = 2;
    
    if (acc == 1)
    {
        acc += 1;
    }
    else
    {
        acc += 8;
    }
    
    printf("Acc : %d\n", acc);
    
    return 0;
}
