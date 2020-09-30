from machine import ADC
adc = ADC()
batt = adc.channel(attn=1, pin='P16')
print(batt.value())