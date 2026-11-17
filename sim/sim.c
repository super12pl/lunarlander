#include <stdio.h>
#include <time.h>
#include <stdbool.h>
#include <pthread.h>
#include <stdlib.h>
#include <string.h>

void delay(float sec)
{
    clock_t start = clock();
    while (clock() - start < sec * CLOCKS_PER_SEC)
        ;
}

const float g = 1.6;
float m,H_0,v_0,F_c,H,V,timeflow;
char nazwapliku[256];
bool silnik = false;
float H,v;
void *silniklistener()
{
    while (H > 0)
    {
        getchar();
        silnik = !silnik;
    }
    return NULL;
}
int main(int argc,char *argv[])
{
    m = argc>=2 ? strtof(argv[1],NULL):2000;
    H_0 = argc>=3 ? strtof(argv[2],NULL):500;
    v_0 = argc>=4 ? strtof(argv[3],NULL):10;
    F_c = argc>=5 ? strtof(argv[4],NULL):4500;
    strcpy(nazwapliku,(argc>=6 ? argv[5]:"ksiezycOutput.csv"));
    timeflow = argc>=7 ? strtof(argv[6],NULL):0.2;
    H = H_0;
    v = v_0;
    FILE *f;
    f = fopen(nazwapliku, "w");
    fprintf(f, "\"Wysokosc nad powierzchnia\";\"Predkosc pionowa w dol\";\"Stan silnika\"");
    printf("H=%.2fm, V=%.2fm/s, %s\n", H, v, silnik ? "ON" : "OFF");
    pthread_t listener;
    pthread_create(&listener, NULL, silniklistener, NULL);
    while (1)
    {
        delay(timeflow);
        H -= v * timeflow;
        v += timeflow * (g - (silnik ? F_c / m : 0));
        printf("H=%.2fm, V=%.2fm/s, %s\n", H, v, silnik ? "ON" : "OFF");
        fprintf(f, "\n%f;%f;%d", H, v, silnik);
        if (H <= 0)
        {
            printf("Ladownik %s. Nacisnij Enter aby zakonczyc program.", v < 1 ? "wyladowal bezpiecznie" : "rozbil sie");
            break;
        }
    }
    pthread_join(listener, NULL);
    fclose(f);
    return 0;
}
