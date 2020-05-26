#include "elecanisms.h"
#include "ws2812b.h"
#define NUM 30  //total number of neopixels used
#define PNUM 21 //number of neopixels in the cyclone circle
#define neo_data D0
#define coin D3
#define LED D1
#define Button D2

int pos = 0;
uint8_t red[NUM], green[NUM], blue[NUM];
int counter = 0;
int state = 0;
int tpos = 10;
int point;
int health = 3;
int hb = 24;

/*state 0:waiting for insert of coin
        1:waiting for press of button
        2:game in play*/

void update_led(void) //this function allows us to display and turn off the neopixels that we want
{
  int i;
  disable_interrupts();
  for (i = 0; i < NUM; i++)
  {
    ws2812b_write(red[i], green[i], blue[i]);
  }
  enable_interrupts();
}

void lose_health(void) //this function reduces the health and also changes the display on the healthbar
{
  health--;
  red[hb + health] = 0;
  update_led();
}

int main(void)
{
  //initialisation code
  init_elecanisms();
  init_ws2812b();
  T1CON = 0x0030; //our timer is set to raise it's interrupt flag for every 0.1 seconds
  PR1 = 0x1869;   //

  D1_DIR = OUT; //depending on which pin you use to set control the LED on your button, you have to set that pin as output type

  TMR1 = 0;
  IFS0bits.T1IF = 0;
  int i;

  //main loop
  while (1)
  {
    //we always need to reset these factors whenever the game is reset, hence it is inside the game's while loop
    health = 3;
    point = 0;
    pos = 0;

    //while we're waiting for the player to insert a coin, the neopixels in the cyclone circle will shine white and the healthbar is empty.
    for (i = 0; i < PNUM; i++)
    {
      red[i] = 100;
      blue[i] = 100;
      green[i] = 100;
    }
    for (i = PNUM; i < NUM; i++)
    {
      red[i] = 0;
      blue[i] = 0;
      green[i] = 0;
    }
    update_led();
    state = 0;

    //waiting for coin to be inserted loop
    while (state == 0)
    {
      if (coin == 1)
      {
        state = 1;
        //once the penny is inserted, we turn off the lights
        for (i = 0; i < PNUM; i++)
        {
          red[i] = 0;
          blue[i] = 0;
          green[i] = 0;
        }
        update_led();
      }
    }

    T1CONbits.TON = 1; //starting the timer
    IFS0bits.T1IF = 0; //lowering the timer's interrupt flag
    counter = 0;       //initialising our counter so that we can keep track of the number of times 0.1 seconds has passed

    //waiting for button to be pressed
    while (state == 1)
    {
      if (IFS0bits.T1IF == 1) //once the interrupt flag is raised
      {
        IFS0bits.T1IF = 0; //we lower the flag
        counter++;         //and we increase the counter
      }

      if (counter % 2 == 0) //if the counter is even
      {
        LED = 1; //we turn on the LED on the button
      }
      if (counter % 2 == 0) //if the counter is odd
      {
        LED = 0; //we turn off the LED on the button
      }
      //this makes the LED on the button blink once every 0.2 seconds for a duration of 0.1 second

      //when the button is pressed
      if (Button == 0)
      {
        //create healthbar
        for (i = hb; i < hb + 3; i++)
        {
          red[i] = 255;
        }
        //create countdown bar
        for (i = 0; i < 5; i++)
        {
          green[i] = 255;
        }
        update_led();

        counter = 0;       //we reset the counter
        IFS0bits.T1IF = 0; //and the interrupt flag

        //5 second countdown begins
        while (counter < 50)
        {
          if (IFS0bits.T1IF == 1)
          {
            IFS0bits.T1IF = 0;
            counter++;
            if (counter % 2 == 0) //when the counter is even, we make the target led blink so that the player will know which led to hit
            {
              blue[tpos] = 255;
              if (counter % 10 == 0) //every one second we dim the furthest countdown neopixel
              {
                i--;
                green[i] = 0;
              }
            }
            else
            {
              blue[tpos] = 0; //together with the if statement on top, this causes the target led to blink with a frequency of 10Hz
            }
            update_led();
          }
        }
        //exit waiting for button stage
        state = 2;
      }
    }

    //initiate pos 0 with yellow light
    red[pos] = 255;
    green[pos] = 255;

    //reset Timer
    T1CONbits.TON = 0;
    TMR1 = 0;
    IFS0bits.T1IF = 0;
    T1CONbits.TON = 1;

    //gameplay while loop
    while (state == 2)
    {
      if (IFS0bits.T1IF == 1) //when 0.1 second is past, we dim the current neopixel
      {
        IFS0bits.T1IF = 0;
        red[pos] = 0;
        green[pos] = 0;

        if (pos == PNUM) //then according to the neopixel, we either increment the position by one or reset it to 0 if it's at the end
        {
          pos = 0;
        }
        else
        {
          pos++;
        }
        if (pos == tpos) //if the new position is the target position, we make it shine white
        {
          red[pos] = 255;
          blue[pos] = 255;
          green[pos] = 255;
        }
        else //if not the new position shines yellow. This makes it look as though the light is moving in a circle
        {
          red[pos] = 255;
          green[pos] = 255;
        }
        update_led();
        if (pos == tpos)
        {
          if (Button == 0)
          {
            point++; //you would just display the point on a 7-segment
          }
          else
          {
            lose_health();
            if (health == 0) //when you're out of health
            {
              //timer reset
              T1CONbits.TON = 0;
              TMR1 = 0;
              IFS0bits.T1IF = 0;
              T1CONbits.TON = 1;

              //turn off all the neopixels that are on at that point
              blue[pos] = 0;
              blue[tpos] = 0;
              green[tpos] = 0;
              green[pos] = 0;

              counter = 0;
              while (counter <= 28) //flash red for a total duration less than 3 seconds
              {
                if (IFS0bits.T1IF == 1)
                {
                  IFS0bits.T1IF = 0;
                  if (counter % 3 == 0)
                  {
                    for (i = 0; i <= PNUM; i++)
                    {
                      red[i] = 200;
                    }
                    update_led();
                  }
                  if (counter % 3 == 2)
                  {
                    for (i = 0; i <= PNUM; i++)
                    {
                      red[i] = 0;
                    }
                    update_led();
                  }
                  counter++;
                }
              }
              state = 3; //the state is set to three is just to go to a new state, if none, like this case, it just resets and awaits a new penny.
            }
          }
        }
      }
    }
  }
}
