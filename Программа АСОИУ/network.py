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

def initApp():
    sg.theme('DarkGrey5')  # Выберите интересующую вас тему оформления
    font_style = ('Helvetica', 12)  # Задаем стиль шрифта и его размер

    # image_filename = r'photo_2023-12-18_01-43-00.jpg'  # Change this to the actual path of your image
    # image_element = sg.Image(filename=image_filename, size=(20, 20), background_color='#008080')

    col1 = [
        [sg.Text('Количество рабочих станций', size=(52, 1), font=font_style),
         sg.Input('', key='N', do_not_clear=True, size=(10, 1), font=font_style)],
        [sg.Text('Среднее время доробатки запроса на PC, ч', size=(52, 1), font=font_style),
         sg.Input('', key='T0', do_not_clear=True, size=(10, 1), font=font_style)],
        [sg.Text('Среднее время формирования запроса на PC, ч', size=(52, 1), font=font_style),
         sg.Input('', key='Tp', do_not_clear=True, size=(10, 1), font=font_style)],
        [sg.Text('Среднее время передачи через канал в прямом направлении', size=(52, 1), font=font_style),
         sg.Input('', key='tk1', do_not_clear=True, size=(10, 1), font=font_style)],
        [sg.Text('Среднее время передачи через канал в обратном направлении', size=(52, 1), font=font_style),
         sg.Input('', key='tk2', do_not_clear=True, size=(10, 1), font=font_style)],
        [sg.Text('Количество процессоров', size=(52, 1), font=font_style),
         sg.Input('', key='C', do_not_clear=True, size=(10, 1), font=font_style)],
        [sg.Text('Среднее время обработки запроса на процессоре', size=(52, 1), font=font_style),
         sg.Input('', key='tnp', do_not_clear=True, size=(10, 1), font=font_style)],
    ]

    col2 = [
        [sg.Text('Количество дисков', size=(52, 1), font=font_style),
         sg.Input('', key='D', do_not_clear=True, size=(10, 1), font=font_style)],
        [sg.Text('Среднее время обработки запроса на диске', size=(52, 1), font=font_style),
         sg.Input('', key='td', do_not_clear=True, size=(10, 1), font=font_style)],
        [sg.Text('Вероятность обращения запроса к ЦП', size=(52, 1), font=font_style),
         sg.Input('', key='j', do_not_clear=True, size=(10, 1), font=font_style)],
        [sg.Text('K1 = ', size=(4, 1), font=font_style),
         sg.Input('0.995', key='K1', do_not_clear=True, size=(10, 1), font=font_style)],
        [sg.Text('K2 = ', size=(4, 1), font=font_style),
         sg.Input('100', key='K2', do_not_clear=True, size=(10, 1), font=font_style)],
        [sg.Text('delta = ', size=(5, 1), font=font_style),
         sg.Input('0.05', key='delta', do_not_clear=True, size=(10, 1), font=font_style)],
        [sg.Text('Точность =', size=(9, 1), font=font_style),
         sg.Input('4', key='r', do_not_clear=True, size=(10, 1), font=font_style)],
    ]

    # menu_def = [['О программе', 'О разработчике']]

    layout = [
        # [sg.Menu(menu_def)],
        # [sg.Image(filename=image_filename)],
        [
            sg.Column(col1),
            sg.Column(col2),
            # image_element
        ],
        [sg.Button('Вычислить', key='calc', button_color=('white', 'green')),
         sg.Button('О разработчике', key='about_dev', button_color=('white', 'blue')),
         sg.Exit(button_color=('white', 'red'))],
    ]
    window = sg.Window('Модель "Сеть"').Layout(layout)
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
    tk1 = float(values['tk1'])
    tk2 = float(values['tk2'])
    C = int(values['C'])
    tnp = float(values['tnp'])
    td = int(values['td'])
    j = float(values['j'])
    N = int(values['N'])
    D = int(values['D'])
    T0 = int(values['T0'])
    Tp = int(values['Tp'])
    delta = float(values['delta'])
    K1 = float(values['K1'])
    K2 = float(values['K2'])
    r = int(values['r'])

    b = 1/(1-j)
    Pi = 1/D
    # K1 = 0.995
    tk = 0.5 * (tk1 + tk2)
    A = 1/(2*tk)
    B = C/(b*tnp)
    H = 1/(b*Pi*td)
    M = min(A, B, H)
    lf1 = K1 * M *((N-1) / N)
    Tk = (2*tk)/(1 - (2*lf1*tk))
    x = (b * lf1 * tnp) / C
    y = pow(x, C)
    Tnp = (b * tnp) / (1 - y)
    Td = (b*td)/(1 - (b*Pi*lf1*td))
    lf = (N-1)/(T0 + Tp + Tk + Tnp + Td)

    lfOld = lf1
    n = 0
    while abs(lfOld - lf) / lf > delta:
        lf = lfOld - abs(lfOld - lf) / K2

        Tk = 2 * tk / (1 - lf * tk)
        x = (b * lf1 * tnp) / C
        y = pow(x, C)
        Tnp = (b * tnp) / (1 - y)
        Td = (b * td) / (1 - (b * Pi * lf * td))
        Tc = T0 + Tp + Tk + Tnp + Td

        lfOld = lf
        lf = (N - 1) / Tc

        n += 1

    Tc = T0 + Tp + Tk + Tnp + Td
    l = N / Tc
    Ppc = (T0 + Tp)/Tc
    ppol = Tp / Tc
    pk = 2 * l * tk
    pnp = b * l * (tnp/C)
    pd = b * l * Pi * td
    Tr = Tc - Tp

    sg.Popup(
        'Результаты',
        'Загрузка рабочей станции: Pрс = ' + str(round(Ppc, r)),
        'Загрузка  пользователя рабочей станции: Pпол = ' + str(round(ppol, r)),
        # 'Среднее количество работающих РС: Pрс = ' + str(round(Ppc, r)),
        'Загрузка канала: Pк = ' + str(round(pk, r)),
        'Загрузка процессора: Pпр = ' + str(round(pnp, r)),
        'Загрузка дисков: Pд = ' + str(round(pd, r)),
        'Время цикла: Tцикла = ' + str(round(Tc, r)),
        'Время реакции: Треакц = ' + str(round(Tr, r)),
        'Начальная интенсивность ФП: Lf1 = ' + str(round(lf1, r)),
        'Конечная интенсивность ФП: LF = ' + str(round(lf, r)),
        'Колиечство итераций: n = ' + str(round(n, r)),
        line_width=70

    )


if __name__ == '__main__':
    show_popup_with_image() 
    window = initApp()
    HandleEvents(window)
