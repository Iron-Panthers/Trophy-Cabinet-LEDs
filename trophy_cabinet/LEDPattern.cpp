#include "LEDPattern.h"

#include <Arduino.h>
#include <FastLED.h>
#include "constants.h"

#define BOUNCING_WAVE_RESOLUTION 100

LinearHue::LinearHue(uint16_t delay, uint8_t inc): inc(inc), del(delay) { }

void LinearHue::begin(CRGB* leds) {
  hue = 0;
}

void LinearHue::loop(CRGB* leds) {
  for (int i = NUM_LEDS - 1; i > 0; i--) {
    leds[i] = leds[i - 1];
  }
  leds[0] = CHSV(hue, 255, 255);
  hue += inc;
  FastLED.show();
  delay(this->del);
}

void LinearHue::end(CRGB* leds) {
  
}

BouncingWave::BouncingWave(unsigned int delay, uint8_t step, int k) : del(delay), step(step), k(k) { }

uint8_t BouncingWave::getBrightness(int error) {
  long brightness = ((long)error) * k;
  brightness *= -brightness;
  brightness /= BOUNCING_WAVE_RESOLUTION;
  brightness /= BOUNCING_WAVE_RESOLUTION;
  brightness += 255;
  return max(brightness, 0);
}

void BouncingWave::begin(CRGB* leds) {
  wavePos = 0;
}

void BouncingWave::loop(CRGB* leds) {
  wavePos += step;
  if (wavePos > BOUNCING_WAVE_RESOLUTION) {
    wavePos = -wavePos;
  }

  int truePos = abs(wavePos);
  
  for (int i = LOWER_COUNT; i < NUM_LEDS; i++) {
    int virtPos = map(i, NUM_LEDS, LOWER_COUNT, 0, BOUNCING_WAVE_RESOLUTION);
    int hue = map(i, NUM_LEDS, LOWER_COUNT, 0, 255);
    leds[i] = CHSV(hue, 255, getBrightness(truePos - virtPos));
  }
  
  for (int i = 0; i < LOWER_COUNT; i++) {
    int virtPos = map(i, 0, LOWER_COUNT, 0, BOUNCING_WAVE_RESOLUTION);
    int hue = map(i, LOWER_COUNT, NUM_LEDS, 0, 255);
    leds[i] = CHSV(hue, 255, getBrightness(truePos - virtPos));
  }
  
  FastLED.show();
  delay(this->del);
}

void BouncingWave::end(CRGB* leds) {
  
}
