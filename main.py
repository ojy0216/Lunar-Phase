from tkinter import *
import gui
import api_key
import urllib.request
from urllib.parse import urlencode, quote_plus
from xml.etree import ElementTree
import matplotlib.pyplot as plt
import numpy as np
import math

SYNODIC_MONTH = 29.53


def draw_moon(lunar_date, date):
    plt.style.use('dark_background')

    plt.figure(figsize=(5, 5))
    plt.xlim(-1, 1)
    plt.ylim(-1, 1)

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

    plt.xlabel('\n{} / {} / {}\nLunar Age: {}'.format(
        date['year'],
        date['month'],
        date['day'],
        lunar_date
    ))
    plt.tight_layout()
    plt.show()


def main(verbose=False):
    root = Tk()
    g = gui.Gui(root)
    date = g.check_date()
    if verbose:
        print(date)

    if not date:
        return

    my_key = api_key.my_key
    url = 'http://apis.data.go.kr/B090041/openapi/service/LunPhInfoService/getLunPhInfo'
    query_params = '?' + urlencode({
        quote_plus('ServiceKey'): my_key,
        quote_plus('solYear'): date['year'],
        quote_plus('solMonth'): date['month'],
        quote_plus('solDay'): date['day']
    })

    request = urllib.request.Request(url + query_params)
    request.get_method = lambda: 'GET'
    response_body = urllib.request.urlopen(request).read()

    root_element = ElementTree.fromstring(response_body)

    iter_element = root_element.iter(tag='item')
    lunage = None

    try:
        for element in iter_element:
            lunage = element.find('lunAge').text
        if verbose:
            print(lunage)
        if not lunage:
            root.withdraw()
            gui.error()
            return
        root.destroy()
        draw_moon(float(lunage), date)
    except NameError:
        gui.error()


if __name__ == '__main__':
    main()
