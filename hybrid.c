#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<math.h>
#include<stdbool.h>
#define SIZE 131072


int change_count(int counter, char fp_char, int n)
{
    if(fp_char == 'T')
    {
        if(counter == (int)(pow(2,(float)n)-1))

            counter = (int)(pow(2,(float)n)-1);
        else
            counter = counter + 1;
    }
    else if(fp_char == 'N')

    {
        if(counter == 0)

            counter = 0;
        else
        counter = counter - 1;
    }
    return(counter);

}

int main()
{
    printf("***********Hybrid predictor**********\n");   
    FILE *fp;
    size_t nread, nb = 0;
    long int fp_addr, fp_int1, qz, qy, qt;
    long int pht1[SIZE], pht2[SIZE], pht3[SIZE];
    long int qx;
    char fp_char, qv;
    long int counter = 0;
    bool tc1 = 0, tc2 = 0;
    long int misshyb = 0, misslocal = 0, missgshare = 0, total = 0;
    float percent = 0, percent1 = 0, percent2 = 0;
    char *line;
    long int GHR;
    long int LHT[SIZE];
    int nbits;

    fp = fopen("branch-trace-gcc.trace", "r");


    if (ferror(fp)) {
            printf("file can not be opened");
        exit(1);
    }
        printf("Enter the counter size in bits: ");
        scanf("%d", &nbits);


    memset(LHT, 0, sizeof LHT);

    memset(pht1, 0, sizeof pht1);

    memset(pht2, 0, sizeof pht2);

    memset(pht3, 0, sizeof pht3);

    nread = getline(&line,&nb,fp);


    while(nread != -1)

    {
        fscanf(fp, "%ld %c", &fp_addr, &fp_char);

       
        fp_int1 = fp_addr & 0x0001FFFF;
        qt = fp_addr & 0x0001FFFF;

        qy = LHT[fp_int1] & 0x0001FFFF;
           
        if(fp_char == 'T')

        {
            if(pht1[qy] < (int)pow(2,(float)nbits)/2)

            {
                misslocal++;
                tc1 = 1;

            }
            pht1[qy] = change_count(pht1[qy], fp_char, nbits);

            LHT[fp_int1] = LHT[fp_int1] << 1;
            LHT[fp_int1] = LHT[fp_int1] + 1;
            qy = LHT[fp_int1] & 0x0001FFFF;
        }
        if(fp_char == 'N')
        {
            if(pht1[qy] >= (int)pow(2,(float)nbits)/2)

            {
                misslocal++;
                tc1 = 1;

            }
            pht1[qy] = change_count(pht1[qy], fp_char, nbits);
            LHT[fp_int1] = LHT[fp_int1] << 1;
            LHT[fp_int1] = LHT[fp_int1] + 0;
            qy = LHT[fp_int1] & 0x0001FFFF;
        }


        if(fp_char == 'T')
        {
            if(pht2[qx] < (int)pow(2,(float)nbits)/2)

            {
                missgshare++;
                tc2 = 1;

            }
            pht2[qx] = change_count(pht2[qx], fp_char, nbits);
            GHR = GHR << 1;
            GHR = GHR + 1;
            qz = GHR ^ fp_addr;
            qz = qz & 0x0001FFFF;
            qx = qz;
        }
        if(fp_char == 'N')
        {
            if(pht2[qx] >= (int)pow(2,(float)nbits)/2)

            {
                missgshare++;
                tc2 = 1;

            }
            pht2[qx] = change_count(pht2[qx], fp_char, nbits);
            GHR = GHR << 1;
            GHR = GHR + 0;
            qz = GHR ^ fp_addr;
            qz = qz & 0x0001FFFF;
            qx = qz;
        }
       
        if(tc1 == 1)
        {
            if(tc2 == 0)

            {
                if(pht3[qt] < (int)pow(2,(float)nbits)/2)
                    misshyb++;
                pht3[qt] = change_count(pht3[qt], fp_char, nbits);
            }
                       
            tc1 = 0;
            tc2 = 0;

        }
        else if(tc1 == 0)
        {
            if(tc2 == 1)

            {
                if(pht3[qt] >= (int)pow(2,(float)nbits)/2)
                    misshyb++;
                pht3[qt] = change_count(pht3[qt], fp_char, nbits);
            }
            tc1 = 0;
            tc2 = 0;

        }

        nread = getline(&line,&nb,fp);
        total++;
       
    }


   
    
    printf("miss predictions number: %ld\n", misshyb);
    percent = (float)((float)misshyb/(float)total)*100;
    printf("Misprediction percentage: %f\n", percent);

}
