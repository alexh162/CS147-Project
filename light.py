import serial
import time
from kasa import SmartBulb
import asyncio
import sqlite3

BULB_IP = "192.168.1.252"

bulb = SmartBulb(BULB_IP)

def get_latest_settings():
    conn = sqlite3.connect('bulb_state.db')
    c = conn.cursor()
    c.execute('SELECT brightness, color_temp FROM settings ORDER BY id DESC LIMIT 1')
    settings = c.fetchone()
    conn.close()
    return settings if settings else (100, 2700) # default

async def store_bulb_state(state):
    await bulb.update()
    brightness = bulb.brightness
    color_temp = bulb.color_temp
    
    conn = sqlite3.connect('bulb_state.db')
    c = conn.cursor()
    c.execute('INSERT INTO bulb_state (state, brightness, color_temp) VALUES (?, ?, ?)', 
              (state, brightness, color_temp))
    conn.commit()
    conn.close()

async def turn_on_bulb():
    brightness, color_temp = get_latest_settings()
    await bulb.update()
    await bulb.set_brightness(brightness)
    await bulb.set_color_temp(color_temp)
    await bulb.turn_on()
    await store_bulb_state("ON")

async def turn_off_bulb():
    await bulb.update()
    await bulb.turn_off()
    await store_bulb_state("OFF")

async def handle_clap_detection():
    ser = serial.Serial('/dev/tty.usbserial-57460248441', 9600, timeout=1)
    time.sleep(2)
    print("Waiting for sound cue...")

    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            if line == "Clap detected":
                print("Clap detected")
            if line == "LED turned ON":
                print("Turning bulb ON")
                await turn_on_bulb()
            elif line == "LED turned OFF":
                print("Turning bulb OFF")
                await turn_off_bulb()

def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(handle_clap_detection())

if __name__ == "__main__":
    main()