# Tests

## **direction-tests**
Tests sounds coming from multiple directions while fixing other variables. Aims to validate the direction detection algorithm
- Equilateral mic setup
  - 10cm triangle side
- Pure frequency sound source
  - 1000Hz
  - 0.1 amplitude
  - 5m distance
  - Directions within [-170, 180] degree range, with 10° steps
- No noise
- Decay rate 0.5
- 1s detection window

## **frequency-tests**
Tests sounds coming from a few directions while varying source frequency and fixing other variables. Validates behaviour for different frequencies
- Equilateral mic setup
  - 10cm triangle side
- Pure frequency sound source
  - Varying between 100Hz, 500Hz, 1000Hz, 2000Hz, 5000Hz and 10000Hz
  - 0.1 amplitude
  - 5m distance
  - Directions within [45, 53] degree range, with 1° steps
- No noise
- Decay rate 0.5
- 1s detection window

## **sample-tests**
Tests sounds coming from a few directions while varying source frequency and fixing other variables. Validates behaviour for real sounds
- Equilateral mic setup
  - 10cm triangle side
- Sample sound source
  - Varying between glass breaking, stepping on a tree branch and a ball kicking
  - Varying amplitude
  - 5m distance
  - Directions within [45, 53] degree range, with 1° steps
- No noise
- Decay rate 0.5
- 1.5s detection window
  - Increased from usual 1s window to accommodate for the ball kicking sample

## **sound-noise-freq-tests**
Tests sounds coming from a few directions while varying source frequency and noise parameters, keeping other variables fixed. The noise source was positioned on top of the sound source
- Equilateral mic setup
  - 10cm triangle side
- Pure frequency sound source
  - Varying between 1000Hz and 2000Hz
  - 0.1 amplitude
  - 5m distance
  - Directions within [45, 53] degree range, with 1° steps
- White and pink noise with SNR varying between -20dB, 0dB and 20dB
- Decay rate 0.5
- 1s detection window

## **mic-noise-freq-tests**
Tests sounds coming from a few directions while varying source frequency and noise parameters, keeping other variables fixed
Each microphone had it's own internal noise source
- Equilateral mic setup
  - 10cm triangle side
- Pure frequency sound source
  - Varying between 1000Hz and 2000Hz
  - 0.1 amplitude
  - 5m distance
  - Directions within [45, 53] degree range, with 1° steps
- White and pink noise with SNR varying between -20dB, 0dB and 20dB
- Decay rate 0.5
- 1s detection window

## **mic-noise-sample-tests**
Tests sounds coming from a set direction while varying source samples and noise parameters, keeping other variables fixed
Each microphone had it's own internal noise source
- Equilateral mic setup
  - 10cm triangle side
- Sample sound source
  - Varying between glass breaking, stepping on a tree branch and a ball kicking
  - Varying amplitude
  - 5m distance
  - Direction fixed on 47°
    - Reduced test time
- White and pink noise with SNR varying between -20dB, 0dB, 20dB, 40dB and 60dB
  - Repeated 4 times per noise source due to the random nature of noise
- Decay rate 0.5
- 1.5s detection window

## **amplitude-tests**
Tests sounds coming from a set direction while varying source amplitude and source type, keeping other variables fixed
Each microphone had it's own internal noise source
- Equilateral mic setup
  - 10cm triangle side
- Pure frequency and sample sound sources
  - Varying between 1000Hz sine wave and glass breaking
  - Varying amplitude between 0.01, 0.05, 0.1, 0.25 and 0.5
  - 5m distance
  - Direction fixed on 30°
- White noise with 20dB SNR
  - Repeated 4 times per noise source due to the random nature of noise
- Decay rate 0.5
- 1.5s detection window

## **distance-tests**
Tests sounds coming from a set direction while varying source distance and source type, keeping other variables fixed
Each microphone had it's own internal noise source
- Equilateral mic setup
  - 10cm triangle side
- Pure frequency and sample sound sources
  - Varying between 1000Hz sine wave and glass breaking
  - 0.1 amplitude
  - Varying distance between 1m, 5m, 10m, 25m and 50m 
  - Direction fixed on 30°
- White noise with 20dB SNR
  - Repeated 4 times per noise source due to the random nature of noise
- Decay rate 0.5
- 1.5s detection window

## **detection-window-tests**
Tests sounds coming from a set direction while varying source types and detection window time, keeping other variables fixed
Each microphone had it's own internal noise source
- Equilateral mic setup
  - 10cm triangle side
- Pure frequency and sample sound sources
  - Varying between 1000Hz sine wave, glass breaking, stepping on a tree branch and a ball kicking
  - Varying amplitude
  - 5m distance
  - Direction fixed on 30°
- No noise
- Decay rate 0.5
- Detection window varying between 0.1s, 0.25s, 0.5s, 1.0s and 1.5s

## **detection-window-noise-tests**
Tests sounds coming from a set direction while varying source types (with noise) and detection window time, keeping other variables fixed
Each microphone had it's own internal noise source
- Equilateral mic setup
  - 10cm triangle side
- Pure frequency and sample sound sources
  - Varying between 1000Hz sine wave, glass breaking, stepping on a tree branch and a ball kicking
  - Varying amplitude
  - 5m distance
  - Direction fixed on 30°
- White noise with 20dB SNR
  - Repeated 4 times per noise source due to the random nature of noise
- Decay rate 0.5
- Detection window varying between 0.1s, 0.25s, 0.5s, 1.0s and 1.5s

## **equi-setup-tests**
Tests sounds coming from a few directions while varying source types and the size of the microphone triangle, keeping other variables fixed
Each microphone had it's own internal noise source
- Equilateral mic setup
  - Triangle sides varying between 1cm, 5cm, 10cm, 15cm and 20cm
- Pure frequency and sample sound sources
  - Varying between 1000Hz sine wave, and glass breaking
  - Varying amplitude
  - 5m distance
  - Directions within [45, 53] degree range, with 1° steps
- White noise with 20dB SNR
  - Repeated 4 times per noise source due to the random nature of noise
- Decay rate 0.5
- 1.5s detection window

## **isos-setup-tests**
Tests sounds coming from a few directions while varying source types and the size of the microphone triangle, keeping other variables fixed
Each microphone had it's own internal noise source
- Isosceles mic setup
  - Triangle sides varying between 1cm, 5cm, 10cm, 15cm and 20cm
  - 120° obtuse angle
- Pure frequency and sample sound sources
  - Varying between 1000Hz sine wave, and glass breaking
  - Varying amplitude
  - 5m distance
  - Directions within [45, 53] degree range, with 1° steps
- White noise with 20dB SNR
  - Repeated 4 times per noise source due to the random nature of noise
- Decay rate 0.5
- 1.5s detection window

## **TODO**
Variables to be studied:
- Simulation sound decay rate