import math
import PySimpleGUI as sg

info_text = """
        Лялин А.И ИУ5-15M
"""
def show_popup_with_image():
    image_filename = r'Sasha-L.png'  # Change this to the actual path of your image
    layout = [
        [sg.Image(filename=image_filename)],
        [sg.Text('Выполнил: Лялин А.И. Группа ИУ5-15М')],
        [sg.OK('Продолжить')]
    ]

    window = sg.Window('Приветствие', layout, finalize=True)
    event, values = window.read()
    window.close()

ROUND = 3
def initApp():
    col1 = [
            [sg.Text('Время наработки на отказ, ч', size=(25, 1)), sg.Input('', key='tno', do_not_clear=True, size=(6, 1))],
            [sg.Text('Время ремонта, ч', size=(25, 1)),            sg.Input('', key='t0', do_not_clear=True, size=(6, 1))],
              [sg.Text('Количество компьютеров', size=(25, 1)),   sg.Input('', key='N', do_not_clear=True, size=(6, 1))],
              [sg.Text('Количество специалистов', size=(25, 1)),  sg.Input('', key='c', do_not_clear=True, size=(6, 1))],
        ]
    
    col2 = [
            [sg.Text('З/п специалиста, руб/час', size=(25, 1)),    sg.Input('', key='S1', do_not_clear=True, size=(6, 1))],
              [sg.Text('Финансовые потери, руб/час', size=(25, 1)), sg.Input('', key='S', do_not_clear=True, size=(6, 1))],
              [sg.Text('Точность', size=(25, 1)), sg.Input('', key='r', do_not_clear=True, size=(6, 1))],
    ]
    # menu_def = [['О программе', 'Справка']]

    COL_SIZE = 15
    layout = [
        # [sg.Menu(menu_def)],
            [
                sg.Column(col1),
                sg.Column(col2)
            ],
            [sg.Button('Вычислить', key='calc', button_color=('white', 'green')),
            sg.Button('О разработчике', key='about_dev', button_color=('white', 'blue')),
            sg.Exit(button_color=('white', 'red'))],
    ]

    window = sg.Window('Модель "Ремонтник"').Layout(layout)
    return window

def HandleEvents(window):
    while True:
        event, values = window.Read()
        if event == 'calc':
            try:
                calc_values(window, values)
            except ValueError:
                sg.PopupError('Введите корректные значения!')
        elif event == 'about_dev':
            sg.Popup(info_text)
        elif event is None or event == 'Exit':
            break
        elif event == 'О разработчике':
            sg.PopupOK(info_text)


def calc_values(w, values):
    tno = int(values['tno'])
    # tno = 800
    t0 = int(values['t0'])
    N = int(values['N'])
    S1 = int(values['S1'])
    S = int(values['S'])
    c = int(values['c'])
    r = int(values['r'])
    Uno = 1/tno
    U0 = 1/t0
    F = Uno/U0
    P0 = 0
    P01 = 0

    P001 = 0
    for k in range(0, c+1):
        P01 = (math.factorial(N) * pow(F, k)) / (math.factorial(k) * math.factorial(N-k))
        P001 += P01

    P002 = 0
    for k in range(c+1, N+1):
        P02 = (math.factorial(N) * pow(F, k)) / (pow(c, k - c) * math.factorial(c) * math.factorial(N - k))
        P002 += P02
    P = P001 + P002
    P0 = pow(P, -1)
    print("P0_", c, " = ", P0)

    Pk = []
    # k = 1
    for k in range(1, c+1):
        Pk1 = (math.factorial(N) * pow(F, k)) / (math.factorial(k) * math.factorial(N - k)) * P0
        Pk.append(Pk1)

    for k in range(c+1, N+1):
        Pk2 = (math.factorial(N) * pow(F, k)) / (pow(c, k - c) * math.factorial(c) * math.factorial(N - k)) * P0
        Pk.append(Pk2)

    Q = 0
    for k in range(c, N+1):
        Q += (k-c)*Pk[k-1]
    print('Q =', Q)

    L = 0
    for k in range(1, N+1):
        L += k * Pk[k-1]
    print('L =', L)

    U = L - Q
    print('U =', U)

    p0 = U/c
    print('p0 =', p0)

    Tp = (L*tno)/(N-L)
    print('Tp =', Tp)

    W = Tp - t0
    print('W =', W)

    Tc = Tp + tno
    print('Tc =', Tc)

    pe = tno/Tc
    print('pe =', pe)

    n = N - L
    print('n =', n)

    pp = pe/p0
    print('pp =', pp)

    Y = c * S1 + L * S
    print('Y =', Y)

    sg.Popup(
             'Результаты',
             'Вероятность работы всех компьютетеров: P0 = ' + str(round(P0, r)),
             'Среднее количество компьютеров в очереди на ремонт: Q = ' + str(round(Q, r)),
             'Среднее количество неисправных компьютеров: L = ' + str(round(L, r)),
             'Среднее количество компьютеров на ремонте: U = ' + str(round(U, r)),
             'Коэффициент загрузки одного специалиста: p0 = ' + str(round(p0, r)),
             'Среднее количество исправных компьютеров: n = ' + str(round(n, r)),
             'Коэффициент загрузки компьютера: pe = ' + str(round(pe, r)),
             'Среднее время пребывания в очереди на ремонт: W = ' + str(round(W, r)),
             'Среднее время пребывания в неисправном состоянии: Tp = ' + str(round(Tp, r)),
             'Среднее время цикла для компьютера: Tц = ' + str(round(Tc, r)),
             'Режим работы: pe/p0 = ' + str(round(pp, r)),
             'Убытки предприятия: Y = ' + str(round(Y, r)),
             line_width=70
    )


if __name__ == '__main__':
    show_popup_with_image()
    window = initApp()
    HandleEvents(window)
