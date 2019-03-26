#include <RTClib.h>

RTC_DS3231 rtc;

void setup() {
  Serial.begin(115200);
  rtc.begin();
}

void loop() {
  if (Serial.available()) {
    String buf = Serial.readStringUntil('\n');
    unsigned long t = buf.toInt();
    Serial.println(buf);
    Serial.println(t);
    rtc.adjust(DateTime(t));
  }
}
