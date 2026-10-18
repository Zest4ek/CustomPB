#include <stdio.h>
#include <stdlib.h>
#include <windows.h>
#include <stdbool.h>
#include <string.h>

#ifndef CUSTOM_PB
#define CUSTOM_PB

#define FULL_BLOCK "\xE2\x96\x88"


typedef struct {
    int PERCENT;            // fill percent
    int WIDTH;              // bar width
    char FOREGROUND[20];    // foreground ANSI-color
    char BACKGROUND[20];    // background ANSI-color
} BAR;


void init_console(void);    // enable UTF-8 and support of ANSI-colors
BAR init_bar(void);         // set default value for the bar

bool chkpercent(const BAR* pb);               // percent value check
bool chkwidth(const BAR* pb);                 // width value check
bool chkfgstdcol(int col);              // standard color value check (foreground)
bool chkbgstdcol(int col);              // standard color value check (background)
bool chkextdcol(int col);               // extended color value check
bool chktruecol(int r, int g, int b);   // true color value check

void setfgnul(BAR* pb);                         // clear foreground
void setbgnul(BAR* pb);                         // clear background
void fgstdcol(BAR* pb, int col);                // set foreground standard color
void bgstdcol(BAR* pb, int col);                // set background standard color
void fgextdcol(BAR* pb, int col);               // set foreground extended color
void bgextdcol(BAR* pb, int col);               // set background extended color
void fgtruecol(BAR* pb, int r, int g, int b);   // set foreground true color
void bgtruecol(BAR* pb, int r, int g, int b);   // set background true color

char* getstrbar(const BAR* pb);       // get a bar as a dynamic string 
char* getsmoothbar(const BAR* pb);    // get a smooth bar as a dynamic string
void printbar(const BAR* pb);          // output a bar to the console
void printsmbar(const BAR* pb);        // output a smooth bar to the console


#endif 