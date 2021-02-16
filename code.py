import time
import board
import usb_hid
from digitalio import DigitalInOut, Direction, Pull
import analogio
from adafruit_hid.gamepad import Gamepad

# max 16 buttons with gamepad library
SWITCH_CONFIG = [
    {
        'pin': board.D4,
    },
    {
        'pin': board.D5,
    },
    {
        'pin': board.D6,
    },
    {
        'pin': board.D9,
    },
    {
        'pin': board.D10,
    },
    {
        'pin': board.D11,
    },
    {
        'pin': board.D12,
    },
]

# max 4 axes with Gamepad library
POT_CONFIG = [
    {
        'pin': board.A2,
    },
    {
        'pin': board.A3,
    },
    {
        'pin': board.A4,
    },
]


def main(switch_config, pot_config):
    gamepad = Gamepad(usb_hid.devices)

    switches = configure_switches(switch_config)
    pots = configure_pots(pot_config)

    switch_state = [None for _ in switches]
    pot_axes = ['x', 'y', 'z', 'r_z']

    while True:
        buttons_to_press = []
        buttons_to_release = []
        for i, switch in enumerate(switches):
            val = switch.value
            if val != switch_state[i]:
                if val:
                    buttons_to_press.append(i+1)
                else:
                    buttons_to_release.append(i+1)
                switch_state[i] = val

        if buttons_to_press:
            gamepad.press_buttons(*buttons_to_press)
        if buttons_to_release:
            gamepad.release_buttons(*buttons_to_release)

        pot_args = {}
        for i, pot in enumerate(pots):
            pot_args[pot_axes[i]] = map_pot_value(pot)

        gamepad.move_joysticks(**pot_args)

        time.sleep(0.01)


def map_pot_value(pot):
    # convert 0-65536 to -127-127
    value = pot.value / 256
    value -= 128
    return  int(min(127, max(-127, value)))


def configure_switches(switch_config):
    switches = []
    for indiv_switch_config in switch_config:
        switch_obj = DigitalInOut(indiv_switch_config['pin'])
        switch_obj.direction = indiv_switch_config.get('direction', Direction.INPUT)
        switch_obj.pull = indiv_switch_config.get('pull', Pull.UP)
        switches.append(switch_obj)

    return switches


def configure_pots(pot_config):
    pots = []
    for indiv_pot_config in pot_config:
        pot_obj = analogio.AnalogIn(indiv_pot_config['pin'])
        pots.append(pot_obj)

    return pots


main(SWITCH_CONFIG, POT_CONFIG)
