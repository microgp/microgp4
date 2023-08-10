// (!) by Giovanni Squillero <giovanni.squillero@polito.it>
// +---------------------------------------------------------+
// |   -=*=-  THIS FILE IS NOT INTENDED FOR SHARING  -=*=-   |
// +---------------------------------------------------------+
// The intellectual and technical concepts are proprietary.
// Reproduction or distribution is prohibited and may result
// in civil charges and criminal penalties.

#include <stdio.h>

long int onemax(void);

int main(void)
{
    unsigned long int result = onemax();

    int fitness = 0;
    for(unsigned long int b=1; b; b <<= 1)
        fitness += !!(result & b);
    printf("%d\n", fitness);

    return 0;
}
