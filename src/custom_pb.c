/* Source: https://github.com/Zest4ek/CustomPB/src/custom_pb.c */

#include "custom_pb.h"


void init_console(void)
{   
    SetConsoleCP(CP_UTF8);
    SetConsoleOutputCP(CP_UTF8);

    HANDLE hOut = GetStdHandle(STD_OUTPUT_HANDLE);
    if (hOut != INVALID_HANDLE_VALUE) {
        DWORD dwMode = 0;
        GetConsoleMode(hOut, &dwMode);

        dwMode |= 0x0004; // enable ANSI-colors support
        SetConsoleMode(hOut, dwMode);
    }
}

BAR init_bar(void) {
    BAR pb = {0,30,"\033[37m","\033[100m"};
    return pb; 
}


bool chkfgstdcol(int col) {
    return (col >= 30 && col <= 37) || (col >= 90 && col <= 97);
}
bool chkbgstdcol(int col) {
    return (col >= 40 && col <= 47) || (col >= 100 && col <= 107);
}
bool chkextdcol(int col) {
    return col >= 0 && col <= 255;
}
bool chktruecol(int r, int g, int b) {
    return chkextdcol(r) && chkextdcol(g) && chkextdcol(b);
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
    else if (chkfgstdcol(col)) snprintf(pb->FOREGROUND, sizeof(pb->FOREGROUND), "\033[%dm", col);
    else setfgnul(pb);
}
void bgstdcol(BAR* pb, int col) {
    if (pb == NULL) return;
    else if (chkbgstdcol(col)) snprintf(pb->BACKGROUND, sizeof(pb->BACKGROUND), "\033[%dm", col);
    else setbgnul(pb);
}

void fgextdcol(BAR* pb, int col) {
    if (pb == NULL) return;
    else if (chkextdcol(col)) snprintf(pb->FOREGROUND, sizeof(pb->FOREGROUND), "\033[38;5;%dm", col);
    else setfgnul(pb);
}
void bgextdcol(BAR* pb, int col) {
    if (pb == NULL) return;
    else if (chkextdcol(col)) snprintf(pb->BACKGROUND, sizeof(pb->BACKGROUND), "\033[48;5;%dm", col);
    else setbgnul(pb);
}

void fgtruecol(BAR* pb, int r, int g, int b) {
    if (pb == NULL) return;
    else if (chktruecol(r,g,b)) snprintf(pb->FOREGROUND, sizeof(pb->FOREGROUND), "\033[38;2;%d;%d;%dm", r,g,b);
    else setfgnul(pb);
}
void bgtruecol(BAR* pb, int r, int g, int b) {
    if (pb == NULL) return;
    else if (chktruecol(r,g,b)) snprintf(pb->BACKGROUND, sizeof(pb->BACKGROUND), "\033[48;2;%d;%d;%dm", r,g,b);
    else setbgnul(pb);
}


char* getstrbar(const BAR* pb)
{
    if (!(pb->PERCENT >= 0 && pb->PERCENT <= 100) && (pb->WIDTH > 0 && pb->WIDTH <= 1000)) return NULL;

    int total_ticks = (pb->PERCENT*pb->WIDTH*8)/100; // total number of ticks
    int full_ticks = total_ticks/8;                  // total number of ticks for full blocks

    size_t result_size = pb->WIDTH*strlen(FULL_BLOCK) + strlen(pb->BACKGROUND)+strlen(pb->FOREGROUND) + sizeof("\033[0m");
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


char* getsmoothbar(const BAR* pb) 
{
    if (!(pb->PERCENT >= 0 && pb->PERCENT <= 100) && (pb->WIDTH > 0 && pb->WIDTH <= 1000)) return NULL;

    char block_char[4] = FULL_BLOCK;
    int total_ticks = (pb->PERCENT*pb->WIDTH*8)/100; // total number of ticks
    int full_ticks = total_ticks/8;                  // total number of ticks for full blocks
    int part_ticks = total_ticks%8;                  // total number of ticks for block parts

    size_t result_size = pb->WIDTH*strlen(FULL_BLOCK) + strlen(pb->BACKGROUND)+strlen(pb->FOREGROUND) + sizeof("\033[0m");
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


void printbar(const BAR* pb)
{
    char* bar = getstrbar(pb);
    printf("%s",bar);
    free(bar);
}
void printsmbar(const BAR* pb)
{
    char* bar = getsmoothbar(pb);
    printf("%s",bar);
    free(bar);
}