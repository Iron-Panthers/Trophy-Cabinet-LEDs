#include <RTClib.h>
#include <FastLED.h>

#include "constants.h"
#include "schedule.h"
#include "LEDDuration.h"
#include "LEDPattern.h"


#define DATA_PIN 8


//HSV Constants
int MAX_HUE = 255;
int SATURATION = 255;
int VALUE = 255;

int scheduleIndex = 0;

RTC_DS3231 rtc;
CRGB leds[NUM_LEDS];

void setup() {
  Serial.begin(115200);

  pinMode(13, OUTPUT);

  if (!rtc.begin()) {
    Serial.println("RTC not detected! Entering failure mode.");
    while (true) {
      digitalWrite(13, HIGH);
      delay(100);
      digitalWrite(13, LOW);
      delay(900);
    }
  }
 
  unsigned long currentTime = rtc.now().unixtime();
  Serial.print("Current time: ");
  Serial.println(currentTime);

  LEDDuration* next = &schedule[0];
  for (int i = 0; i < SCHEDULE_COUNT; i++) {
    LEDDuration* s = &schedule[i];
    if (currentTime < s->start) {
      continue;
    }
    unsigned long periodsBefore = (currentTime - s->start) / PERIOD;
    s->start += (periodsBefore + 1) * PERIOD;

    if (s->start < next->start) {
      next = s;
      scheduleIndex = i;
    }
  }

  Serial.println("Adjusted LED Schedule");
  for (int i = 0; i < SCHEDULE_COUNT; i++) {
    Serial.print(i);
    Serial.print(". ");
    Serial.print(schedule[i].start);
    Serial.print(" to ");
    Serial.println(schedule[i].start + schedule[i].duration);
  }
  Serial.println();

  Serial.print("Starting at index ");
  Serial.print(scheduleIndex);
  Serial.print(" (which begins at ");
  Serial.print(schedule[scheduleIndex].start);
  Serial.println(")");
  
  FastLED.addLeds<WS2812B, DATA_PIN, GRB>(leds, NUM_LEDS);

  FastLED.clear();
  FastLED.show();
}

void loop() {
  LEDDuration* scheduleEntry = &schedule[scheduleIndex];
  unsigned long currentTime = rtc.now().unixtime();
  unsigned long waitDuration = 1000 * (scheduleEntry->start - currentTime);
  
  Serial.print("Current time: ");
  Serial.println(currentTime);
  
  Serial.print("Next time: ");
  Serial.println(scheduleEntry->start);

  Serial.print("Delay for: ");
  Serial.print(waitDuration);
  Serial.println("ms");

  // Heartbeat blink every 5 seconds.
  unsigned long beginTime = millis();  // A measure taken to prevent overflow. 
  while (millis() - beginTime <= waitDuration) {  // The subtraction underflow will cancel it out.
    delay(4990);
    digitalWrite(13, HIGH);
    delay(10);
    digitalWrite(13, LOW);
  }

  unsigned long endTime = scheduleEntry->start + scheduleEntry->duration;
  Serial.print("The wait is over. LEDs on until: ");
  Serial.println(endTime);

  digitalWrite(13, HIGH);

  scheduleEntry->pattern->begin(leds);
  while (rtc.now().unixtime() < endTime) {
    scheduleEntry->pattern->loop(leds);
  }
  scheduleEntry->pattern->end(leds);

  FastLED.clear();
  FastLED.show();

  digitalWrite(13, LOW);

  scheduleEntry->start += PERIOD;
  Serial.print("LED cycle finished. Next time for this entry is ");
  Serial.println(scheduleEntry->start);
  scheduleIndex = (scheduleIndex + 1) % SCHEDULE_COUNT;
}
