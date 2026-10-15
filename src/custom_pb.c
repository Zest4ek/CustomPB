#include "custom_pb.h"


void init_console(void)
{
    SetConsoleOutputCP(65001); // enable UTF-8

    HANDLE hOut = GetStdHandle(STD_OUTPUT_HANDLE);
    if (hOut != INVALID_HANDLE_VALUE) {
        DWORD dwMode = 0;
        GetConsoleMode(hOut, &dwMode);

        dwMode |= 0x0004; // enable support of ANSI-colors
        SetConsoleMode(hOut, dwMode);
    }
}

BAR init_bar(void) {
    BAR pb = {0,30,"\033[0m","\033[100m"};
    return pb; 
}


void setfgnul(BAR* pb) {
    if (pb == NULL) return;
    memset(pb->FOREGROUND, 0, sizeof(pb->FOREGROUND));
}
void setbgnul(BAR* pb) {
    if (pb == NULL) return;
    memset(pb->BACKGROUND, 0, sizeof(pb->BACKGROUND));
}

void fgstdcol(BAR* pb, int col) {
    if (pb == NULL) return;
    else if ((col >= 30 && col <= 37) || (col >= 90 && col <= 97)) snprintf(pb->FOREGROUND, sizeof(pb->FOREGROUND), "\033[%dm", col); // allowed values: 30-37, 90-97
    else setfgnul(pb);
}
void fgextdcol(BAR* pb, int col) {
    if (pb == NULL) return;
    else if (col >= 0 && col <= 231) snprintf(pb->FOREGROUND, sizeof(pb->FOREGROUND), "\033[38;5;%dm", col); // allowed values: 0-231
    else setfgnul(pb);
}
void fgtruecol(BAR* pb, int r, int g, int b) {
    if (pb == NULL) return;
    else if (r >= 0 && r <= 255 && g >= 0 && g <= 255 && b >= 0 && b <= 255) snprintf(pb->FOREGROUND, sizeof(pb->FOREGROUND), "\033[38;2;%d;%d;%dm", r,g,b); // allowed values for any variable: 0-255
    else setfgnul(pb);
}
void bgstdcol(BAR* pb, int col) {
    if (pb == NULL) return;
    else if ((col >= 40 && col <= 47) || (col >= 100 && col <= 107)) snprintf(pb->BACKGROUND, sizeof(pb->BACKGROUND), "\033[%dm", col); // allowed values: 30-37, 90-97
    else setbgnul(pb);
}
void bgextdcol(BAR* pb, int col) {
    if (pb == NULL) return;
    else if (col >= 0 && col <= 231) snprintf(pb->BACKGROUND, sizeof(pb->BACKGROUND), "\033[48;5;%dm", col); // allowed values: 0-231
    else setbgnul(pb);
}
void bgtruecol(BAR* pb, int r, int g, int b) {
    if (pb == NULL) return;
    else if (r >= 0 && r <= 255 && g >= 0 && g <= 255 && b >= 0 && b <= 255) snprintf(pb->BACKGROUND, sizeof(pb->BACKGROUND), "\033[48;2;%d;%d;%dm", r,g,b); // allowed values for any variable: 0-255
    else setbgnul(pb);
}


static bool __chkpercent(BAR* pb) { 
    if (pb->PERCENT >= 0 && pb->PERCENT <= 100) return 1;
    return 0;
}
static bool __chkwidth(BAR* pb) { 
    if (pb->WIDTH > 0 && pb->WIDTH <= 1000) return 1;
    return 0;
}


char* getstrbar(BAR* pb)
{
    if (!(__chkpercent(pb) && __chkwidth(pb))) return NULL;

    int total_ticks = (pb->PERCENT*pb->WIDTH*8)/100; // total number of ticks
    int full_ticks = total_ticks/8;                  // total number of full blocks

    size_t result_size = pb->WIDTH*sizeof(FULL_BLOCK) + strlen(pb->BACKGROUND)+strlen(pb->FOREGROUND)+5;

    char* result = (char*)malloc(result_size);
    result[0] = '\0';

    if (pb->BACKGROUND[0] != '\0') strcat(result, pb->BACKGROUND);
    if (pb->FOREGROUND[0] != '\0') strcat(result, pb->FOREGROUND);

    for (int j = 0; j < pb->WIDTH; j++) {
        if (j < full_ticks) strcat(result, FULL_BLOCK);
        else strcat(result, " ");
    }
    strcat(result, "\033[0m"); // reset colors
    return result;
};

char* getsmoothbar(BAR* pb) 
{
    if (!(__chkpercent(pb) && __chkwidth(pb))) return NULL;

    int total_ticks = (pb->PERCENT*pb->WIDTH*8)/100; // total number of ticks
    int full_ticks = total_ticks/8;                  // total number of full blocks
    int part_ticks = total_ticks%8;                  // total number of block parts
    char block_char[4] = FULL_BLOCK;

    size_t result_size = pb->WIDTH*sizeof(FULL_BLOCK) + strlen(pb->BACKGROUND)+strlen(pb->FOREGROUND)+5;
    char* result = (char*)malloc(result_size);
    result[0] = '\0';

    if (pb->BACKGROUND[0] != '\0') strcat(result, pb->BACKGROUND);
    if (pb->FOREGROUND[0] != '\0') strcat(result, pb->FOREGROUND);

    for (int j = 0; j < pb->WIDTH; j++) {
        if (j == full_ticks && part_ticks > 0)
            block_char[2] = (char)(0x8F-(part_ticks-1)); // set the char for the partially filled block
        
        if (j < full_ticks) 
            strcat(result, FULL_BLOCK);
        else if (j == full_ticks && part_ticks > 0) 
            strcat(result, block_char);
        else 
            strcat(result, " ");
    }
    strcat(result, "\033[0m"); // reset colors
    return result;
}


void printbar(BAR pb)
{
    char* bar = getstrbar(&pb);
    printf("%s",bar);
    free(bar);
}
void printsmbar(BAR pb)
{
    char* bar = getsmoothbar(&pb);
    printf("%s",bar);
    free(bar);
}