from time import sleep_ms
from system_icons import empty
from system_functions import roll_led_tubes
from system_functions import flip_led_tubes
from system_functions import flip_screen
from system_functions import blink_screen
from system_functions import get_game_data
from system_functions import config_game_data


def notice(perl, mode, game_flow=None):
    if mode == "start":
        flip_screen(perl.screen, empty(), 0)
        flip_screen(perl.screen, empty(), 1)
        perl.screen.pixels("1", game_flow.init_disp_info)
        perl.screen.refresh()
        blink_screen(perl, 3, 50, 100, False)
        flip_led_tubes(perl.timer, "3333")
        flip_led_tubes(perl.scorer, "3333")
        for i in range(3, 0, -1):
            perl.timer.chars(str(i) * 4)
            perl.scorer.chars(str(i) * 4)
            perl.buzzer.on()
            sleep_ms(100)
            perl.buzzer.off()
            sleep_ms(900)
        perl.buzzer.on()
        for _ in range(3):
            perl.timer.chars("GOGO")
            perl.scorer.chars("GOGO")
            perl.buzzer.on()
            sleep_ms(100)
            perl.timer.chars("    ")
            perl.scorer.chars("    ")
            sleep_ms(50)
        perl.buzzer.off()
    elif mode == "over":
        blink_screen(perl, 3, 200, 150)
        flip_led_tubes(perl.timer, "GAME")
        perl.timer.segmode("8")
        flip_led_tubes(perl.scorer, "OvEr")
    elif mode == "pause":
        perl.buzzer.buzz(50)
        flip_led_tubes(perl.timer, "GAME")
        perl.timer.segmode("8")
        flip_led_tubes(perl.scorer, "StOP")
    elif mode == "resume":
        perl.buzzer.buzz(50)
        flip_led_tubes(perl.timer, game_flow.game_timer.encoded_seconds)
        perl.timer.segmode("7")
        flip_led_tubes(perl.scorer, game_flow.game_scorer.encoded_score)
        
        
def bind_button_events(perl, game_flow, pages, mode):
    perl.buttons.handlers = {}
    if mode == "start":
        for event in game_flow.button_events:
            perl.buttons.assign(event[0], event[1], event[2])
        perl.buttons.assign("back", stop_game, (perl, game_flow, pages, "pause"))
    elif mode == "pause":
        perl.buttons.assign("ok", start_game, (perl, game_flow, pages, "resume"))
        perl.buttons.assign("back", quit_game, (game_flow, pages))
    elif mode == "over":
        perl.buttons.assign("ok", notice, (perl, "resume", game_flow))
        perl.buttons.assign("back", quit_game, (game_flow, pages))


def start_game(perl, game_flow, pages, mode="start"):
    if mode == "start":
        roll_led_tubes(start=False)
        perl.screen.clearbuffer()
    notice(perl, mode, game_flow)
    game_flow.game_timer.start()
    game_flow.game_scorer.show()
    bind_button_events(perl, game_flow, pages, "start")
    game_flow.clock.init(
        mode=game_flow.clock.PERIODIC,
        period=game_flow.clock_period,
        callback=game_flow.refresh)


def stop_game(perl, game_flow, pages, mode):
    game_flow.clock.deinit()
    game_flow.game_timer.stop()
    notice(perl, mode)
    bind_button_events(perl, game_flow, pages, mode)


def quit_game(game_flow, pages):
    save_game_record(pages.game_list[pages.game_index][0],
                     game_flow.game_timer,
                     game_flow.game_scorer)
    pages.game_select(0)


def set_game_timer(GameTimer, perl, game_name):
    countdown, time_limit = get_game_data(game_name, ("countdown", "time limit"))
    return GameTimer(perl.timer, time_limit if countdown else None)


def save_game_record(game_name, game_timer, game_scorer):
    records = get_game_data(game_name, "score records")
    records.append([game_timer.get_seconds_used(), game_scorer.encoded_score])
    records.sort(key=lambda item: item[1], reverse=True)
    if len(records) > 99:
        records.pop()
    config_game_data(game_name, "score records", records)
