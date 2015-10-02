#include <stdlib.h>
#include <stdio.h>

int main(void)
{
    int acc = 2;
    
    while (acc != 25)
    {
        if (acc == 3)
        {
            acc += 4;
        }
        
        acc++;
    }
    
    printf("Acc : %d\n", acc);
    
    return 0;
}