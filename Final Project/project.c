#include "elecanisms.h"
#include "ws2812b.h"
#define NUM 30 //total number of neopixels used
#define PNUM 21 //number of neopixels in the circle

int pos=0;
uint8_t red[NUM],green[NUM],blue[NUM];
int counter=0;
int state=0;
int tpos=10;
int point;
int health=3;
int hb=24;

/*state 0:waiting for insert of conditions
        1:waiting for press of switch
        2:game in play*/

void update_led(void)
{
  int i;
  disable_interrupts();
  for(i=0;i<NUM;i++)
  {
    ws2812b_write(red[i],green[i],blue[i]);
  }
  enable_interrupts();
}

void lose_health(void)
{
  health--;
  red[hb+health]=0;
  update_led();
}

int main(void)
{
  init_elecanisms();
  init_ws2812b();
  T1CON=0x0030;
  PR1=0x1869;

  D1_DIR=OUT;

  TMR1=0;
  IFS0bits.T1IF=0;
  int i;

  //main loop
  while(1)
  {
    health=3;
    point=0;
    pos=0;



    for(i=0;i<PNUM;i++)
    {
      red[i]=100;
      blue[i]=100;
      green[i]=100;
    }
    for(i=PNUM;i<NUM;i++)
    {
      red[i]=0;
      blue[i]=0;
      green[i]=0;
    }
    update_led();
    state=0;

    //waiting for coin to be inserted
    while(state==0)
    {
      if(SW3==0)
      {
        state=1;
      }
    }


    //turn off light
    for(i=0;i<PNUM;i++)
    {
      red[i]=0;
      blue[i]=0;
      green[i]=0;
    }
    update_led();

    //waiting for button to be pressed
    T1CONbits.TON=1;
    IFS0bits.T1IF=0;
    counter=0;
    while(state==1)
    {
      if(IFS0bits.T1IF==1)
      {
        IFS0bits.T1IF=0;
        counter++;
      }
      //cause the LED on the button to blink
      if(counter%2==0)
      {
        D1=1;
      }
      if(counter%2==0)
      {
        D1=0;
      }

      //when button is pressed
      if(D2==0)
      {
        //create healthbar
        for(i=hb;i<hb+3;i++)
        {
          red[i]=255;
        }
        //create countdown bar
        for(i=0;i<5;i++)
        {
          green[i]=255;
        }
        update_led();

        counter=0;
        IFS0bits.T1IF=0;

        //5 second countdown begins
        while(counter<50)
        {
          if(IFS0bits.T1IF==1)
          {
            IFS0bits.T1IF=0;
            counter++;
            if(counter%2==0)
            {
              blue[tpos]=255;
              if(counter%10==0)
              {
                i--;
                green[i]=0;
              }
            }
            else
            {
              blue[tpos]=0;
            }
            update_led();
          }
        }
        //exit waiting for button stage
        state=2;
      }
    }

    //initiate pos 0 with yellow light
    red[pos]=255;
    green[pos]=255;


    //reset Timer
    T1CONbits.TON=0;
    TMR1=0;
    IFS0bits.T1IF=0;
    T1CONbits.TON=1;

    //gameplay while loop
    while(state==2)
    {
      if(IFS0bits.T1IF==1)
      {
        IFS0bits.T1IF=0;
        red[pos]=0;
        green[pos]=0;
        
        if(pos==PNUM)
        {
          pos=0;
        }
        else
        {
          pos++;
        }
        if(pos==tpos)
        {
          red[pos]=255;
          blue[pos]=255;
          green[pos]=255;
        }
        else
        {
          red[pos]=255;
          green[pos]=255;
        }
        update_led();
        if(pos==tpos)
        {
          if(D2==0)
          {
            LED2=ON;
            point++;
          }
          else
          {
            lose_health();
            if(health==0)
            {
              T1CONbits.TON=0;
              TMR1=0;
              IFS0bits.T1IF=0;
              T1CONbits.TON=1;

              blue[pos]=0;
              blue[tpos]=0;
              green[tpos]=0;
              green[pos]=0;

              counter=0;
              while(counter<=28)
              {
                if(IFS0bits.T1IF==1)
                {
                  IFS0bits.T1IF=0;
                  if(counter%3==0)
                  {
                    for(i=0;i<=PNUM;i++)
                    {
                      red[i]=200;
                    }
                    update_led();
                  }
                  if(counter%3==2)
                  {
                    for(i=0;i<=PNUM;i++)
                    {
                      red[i]=0;
                    }
                    update_led();
                  }
                  counter++;
                }
              }
              state=3;
            }
          }
        }
      }
    }
  }
}
