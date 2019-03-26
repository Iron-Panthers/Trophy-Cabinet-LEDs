#pragma once

#include <Arduino.h>
#include <FastLED.h>
#include "constants.h"

class LEDPattern {
  public:
    /**
     * Called once at the beginning of a LED cycle
     */
    virtual void begin(CRGB* leds) = 0;
    /**
     * Called after begin, and called repeatedly until the LED cycle ends
     */
    virtual void loop(CRGB* leds) = 0;
    /**
     * Called when the LED cycle ends. Does not need to turn off the LEDs, the loop will do it for you
     */
    virtual void end(CRGB* leds) = 0;
};

/**
 * A hue cycle, with the lower one going right and the upper one going left.
 */
class LinearHue : public LEDPattern {
  uint8_t inc;
  uint8_t hue;
  uint16_t del;
  public:
    LinearHue(uint16_t delay, uint8_t inc);
    void begin(CRGB* leds);
    void loop(CRGB* leds);
    void end(CRGB* leds);
};

/**
 * A single wave bouncing left and right.
 */
class BouncingWave : public LEDPattern {
  unsigned int k;
  uint8_t step;
  unsigned int del;
  int wavePos;
  bool increasing;

  uint8_t getBrightness(int error);
  public:
    BouncingWave(unsigned int delay, uint8_t step, int k);
    void begin(CRGB* leds);
    void loop(CRGB* leds);
    void end(CRGB* leds);
};
