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

  FastLED.addLeds<WS2812B, DATA_PIN, GRB>(leds, NUM_LEDS);
  FastLED.clear();
  FastLED.show();

  if (!rtc.begin()) {
    Serial.println("RTC not detected! Entering failure mode.");
    while (true) {
      digitalWrite(13, HIGH);
      delay(1);
      digitalWrite(13, LOW);
      delay(999);
    }
  } else {
    Serial.println("RTC successfully detected.");
  }

  Serial.println("Waiting 3 seconds before entering into normal mode...");
  Serial.setTimeout(3000);
  char buf[1];
  if (Serial.readBytes(buf, 1)) {
    Serial.println("Received input. Entering test mode.");
    testPatterns();
  }
  Serial.setTimeout(1000);
 
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
}

void loop() {
  LEDDuration* scheduleEntry = &schedule[scheduleIndex];
  unsigned long currentTime = rtc.now().unixtime();
  unsigned long waitDuration = 1000 * (scheduleEntry->start - currentTime);
  
  Serial.print("Current time: ");
  Serial.println(currentTime);
  
  Serial.print("Next time:    ");
  Serial.println(scheduleEntry->start);

  Serial.print("Delay for: ");
  Serial.print(waitDuration);
  Serial.println("ms");

  // Heartbeat blink every 10 seconds.
  unsigned long beginTime = millis();  // A measure taken to prevent overflow. 
  while (waitDuration - (millis() - beginTime) >= 10000) {  // The subtraction underflow will cancel it out.
    delay(9999);
    digitalWrite(13, HIGH);
    delay(1);
    digitalWrite(13, LOW);
  }
  delay(waitDuration - (millis() - beginTime));

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

void testPatterns() {
  int i = 0;
  while (true) {
    Serial.print("Displaying #");
    Serial.println(i);
    LEDPattern* pat = PATTERNS[i];
    
    pat->begin(leds);
    
    while (!Serial.available()) {  // Wait for any serial input
      pat->loop(leds);
    }
    pat->end(leds);
    FastLED.clear();
    FastLED.show();
    
    while (Serial.available()) {  // Clear buffer
      Serial.read();
    }
    
    Serial.println("Ended");
    i = (i + 1) % PATTERN_COUNT;
    delay(2000);
  }
}
