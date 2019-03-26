#pragma once

#include "LEDPattern.h"

struct LEDDuration {
  unsigned long start;  // First time, in seconds
  unsigned long duration;  // Duration of the LEDs being on, in seconds
  LEDPattern* pattern;  // The pattern to display
};
