/* Source: https://github.com/Zest4ek/CustomPB/src/example.c */

#include "custom_pb.h"
#include <time.h>

const int MAX_RANDOM = 100; // max value of delay


void rgb_bar(void) 
{   
    BAR pb = init_bar();

    int r=255,g=0,b=0;
    int step = 15;
    
    for (int i = 0; i <= 100; i++) {
        pb.PERCENT = i; // update percent
        fgtruecol(&pb, r,g,b); // update color
        
        char* bar = getsmoothbar(&pb); // get a dynamic string
        printf("\r%s %d%% ",bar,i);
        free(bar); // clear this string

        // check the current values of color and update them
        if (r == 255 && b == 0 && g < 255) {
            g += step;
            if (g > 255) g = 255;
        } else if (g == 255 && b == 0 && r > 0) {
            r -= step;
            if (r < 0) r = 0;
        } else if (g == 255 && r == 0 && b < 255) {
            b += step;
            if (b > 255) b = 255;
        } else if (b == 255 && r == 0 && g > 0) {
            g -= step;
            if (g < 0) g = 0;
        } else if (b == 255 && g == 0 && r < 255) {
            r += step;
            if (r > 255) r = 255;
        } else if (r == 255 && g == 0 && b > 0) {
            b -= step;
            if (b < 0) b = 0;
        }

        fflush(stdout);

        int rand_ms = rand() % (MAX_RANDOM+1); // get a random number from 0 to MAX_RANDOM
        Sleep(rand_ms); // simulate a delay
    }
    putchar('\n');
}


void default_bar(int col) 
{ 
    BAR pb = init_bar();
    fgextdcol(&pb,col);

    for (int i = 0; i <= 100; i++) {
        pb.PERCENT = i; // update percent
        
        putchar('\r');
        printsmbar(&pb); // call automatic bar output
        printf(" %d%% ",i);

        fflush(stdout);

        int rand_ms = rand() % (MAX_RANDOM+1); // get a random number from 0 to MAX_RANDOM
        Sleep(rand_ms); // simulate a delay
    }
    putchar('\n');
}


int main(void) {
    init_console();
    srand((unsigned int)time(NULL)); // random reset
    rgb_bar();

    return 0;
}