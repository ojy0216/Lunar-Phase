from tkinter import *
import gui
from os import environ
import urllib.request
from urllib.parse import urlencode, quote_plus
from xml.etree import ElementTree
import matplotlib.pyplot as plt
import numpy as np
import math

SYNODIC_MONTH = 29.53


def draw_moon(lunar_date, date, time):
    plt.style.use('dark_background')

    fig, ax = plt.subplots(figsize=(6, 6))
    fig.canvas.manager.set_window_title('Lunar Phase')
    plt.xlim(-1, 1)
    plt.ylim(-1, 1)
    ax.set_aspect('equal')

    phase = lunar_date * math.pi / (SYNODIC_MONTH / 2)
    double_phase = 2 * phase
    phase_cos = math.cos(phase)
    if math.sin(double_phase) > 0:
        sign = 1
    else:
        sign = -1

    if phase_cos > 0:
        case = 1
    else:
        case = 0

    mag = abs(phase_cos)

    y = np.arange(-1, 1, 0.001)

    def left_half():
        lf_mag = 0
        while lf_mag <= 1:
            xlf = []
            for i in y:
                xlf.append(-np.sqrt(lf_mag ** 2 * (1 - i ** 2)))
            plt.plot(xlf, y, color='w', linewidth=3)
            lf_mag += 0.01

    def right_half():
        rf_mag = 0
        while rf_mag <= 1:
            xrf = []
            for j in y:
                xrf.append(np.sqrt(rf_mag ** 2 * (1 - j ** 2)))
            plt.plot(xrf, y, color='w', linewidth=3)
            rf_mag += 0.01

    if lunar_date != 0:
        if case == 1:
            while mag <= 1:
                x = []
                for i in y:
                    x.append(sign * np.sqrt(mag ** 2 * (1 - i ** 2)))
                plt.plot(x, y, color='w', linewidth=3)
                mag += 0.01
        elif case == 0:
            if sign == -1:
                right_half()
            else:
                left_half()
            while mag >= 0:
                x = []
                for i in y:
                    x.append(sign * np.sqrt(mag ** 2 * (1 - i ** 2)))
                plt.plot(x, y, color='w', linewidth=3)
                mag -= 0.01

    plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
    plt.tick_params(axis='y', which='both', left=False, top=False, labelleft=False)

    plt.xlabel('\n{} / {} / {}\nLunar Age : {}\nRise: {} | Transit: {} | Set: {} (@ Seoul, S. Korea)'.format(
        date['year'],
        date['month'],
        date['day'],
        lunar_date,
        time['rise'],
        time['transit'],
        time['set']
    ))
    plt.tight_layout()
    plt.show()


def main(verbose=False, visual=True):
    root = Tk()
    g = gui.Gui(root)
    date = g.check_date()
    if verbose:
        print(date)

    if not date:
        return

    concat_date = date['year'] + date['month'] + date['day']

    """Get Lunar Phase w/ API"""
    # lunar_phase_key = api_key.lunar_phase_key
    lunar_phase_key = environ['lunar_key']
    phase_url = 'http://apis.data.go.kr/B090041/openapi/service/LunPhInfoService/getLunPhInfo'
    phase_query_params = '?' + urlencode({
        quote_plus('ServiceKey'): lunar_phase_key,
        quote_plus('solYear'): date['year'],
        quote_plus('solMonth'): date['month'],
        quote_plus('solDay'): date['day']
    })

    if verbose:
        print("Requesting Lunar Phase API...")
    request = urllib.request.Request(phase_url + phase_query_params)
    request.get_method = lambda: 'GET'
    phase_response_body = urllib.request.urlopen(request).read()
    if verbose:
        print("Lunar Phase API received")
        print(phase_response_body)
    root_element = ElementTree.fromstring(phase_response_body)

    iter_element = root_element.iter(tag='item')
    lunage = None

    try:
        for element in iter_element:
            lunage = element.find('lunAge').text
        if verbose:
            print(lunage)
        if not lunage:
            root.withdraw()
            gui.phase_error()
            return
        root.quit()
    except NameError:
        gui.phase_error()
        root.destroy()
        return
    except AttributeError:
        gui.phase_error()
        root.destroy()
        return

    """Get Lunar Times w/ API"""
    # lunar_time_key = api_key.lunar_time_key
    lunar_time_key = environ['lunar_key']
    time_url = 'http://apis.data.go.kr/B090041/openapi/service/RiseSetInfoService/getAreaRiseSetInfo'
    time_query_params = '?' + urlencode({
        quote_plus('ServiceKey'): lunar_time_key,
        quote_plus('locdate'): concat_date,
        quote_plus('location'): '서울'
    })

    if verbose:
        print('Requesting Lunar Times API ..')
    request = urllib.request.Request(time_url + time_query_params)
    request.get_method = lambda: 'GET'
    time_response_body = urllib.request.urlopen(request).read()
    if verbose:
        print('Lunar Times API received')
        print(time_response_body)
    root_element = ElementTree.fromstring(time_response_body)

    iter_element = root_element.iter(tag='item')
    moon_time = {}

    try:
        for element in iter_element:
            moon_time['rise'] = element.find('moonrise').text[:4]
            moon_time['transit'] = element.find('moontransit').text[:4]
            moon_time['set'] = element.find('moonset').text[:4]
        if not moon_time:
            root.withdraw()
            gui.time_error()
            return
        root.destroy()
    except NameError:
        gui.time_error()
        root.destroy()
        return
    except AttributeError:
        gui.time_error()
        root.destroy()
        return

    for key, value in moon_time.items():
        tmp = value
        moon_time[key] = tmp[:2] + ':' + tmp[:-2]
    if verbose:
        print(moon_time)

    if visual:
        draw_moon(float(lunage), date, moon_time)


if __name__ == '__main__':
    main(verbose=False)
