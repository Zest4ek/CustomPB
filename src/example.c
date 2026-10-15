#include "custom_pb.h"
#include <time.h>

const int max_cd = 100; // max value of cooldown


void rgb_bar(void) 
{   
    BAR pb = init_bar();

    int r=255,g=0,b=0;
    int step = 15;
    
    for (int i = 0; i <= 100; i++) {
        pb.PERCENT = i;
        fgtruecol(&pb, r,g,b);

        int rand_ms = rand() % (max_cd+1);
        
        char* bar = getsmoothbar(&pb);
        printf("\r%s %d%% ",bar,i);
        free(bar);

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
        Sleep(rand_ms);
    }
    putchar('\n');
}

void default_bar(int col) 
{   
    BAR pb = init_bar();
    fgextdcol(&pb,col);

    for (int i = 0; i <= 100; i++) {
        pb.PERCENT = i;
        int rand_ms = rand() % (max_cd+1);
        
        putchar('\r');
        printsmbar(pb);
        printf(" %d%% ",i);

        fflush(stdout);
        Sleep(rand_ms);
    }
    putchar('\n');
}

int main(void) 
{
    srand((unsigned int)time(NULL));

    init_console();
    default_bar(2);
    putchar('\n');
    rgb_bar();

    return 0;
}