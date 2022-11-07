# Данная программа предназначена для расчета площади покрытия металлоконструкций стандартного профиля


import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb
import re
from PIL import Image, ImageTk
import data as dt


# Основные параметры GUI
w = tk.Tk()
w.geometry("1435x720+20+10")
w.title('    ПЛОЩАДЬ & МАССА МЕТАЛЛОПРОКАТА')
w.resizable(True, True)


# Menu
my_menu = tk.Menu(w)


# Styles
font_arial = "Arial 10 bold"
font_about_program = "Times 14"
w.option_add("*TCombobox*Listbox*Font", font_arial)
color_1 = '#dedbd8'
color_2 = '#16436c'
color_3 = '#eceb9e'
w['bg'] = color_1
s = ttk.Style()
s.theme_use('xpnative')


# background image
i = "background.jpg"
img = Image.open(i)
resize_img = img.resize((1920, 1080))
img = ImageTk.PhotoImage(resize_img)


# Иконка программы
photo = tk.PhotoImage(file='calculator.png')
w.iconphoto(False, photo)


def closing():
    """Функция закрытия основного окна"""
    if count > 1:
        if mb.askokcancel("Внимание", "Вы уверены, что хотите выйти из программы?\nДанный расчет не будет сохранен"):
            w.destroy()
    else:
        w.destroy()


def create_frame():
    """Создаем фрейм (рамку), в которую помещаем все виджеты"""
    global frame, bg_label
    frame = tk.Frame(w, bg=color_1, width=1435, height=700)
    frame.place(x=0, y=0, relheight=1, relwidth=1)
    bg_label = tk.Label(frame, image=img)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)


def delete():
    """Удаляем фрейм, обнуляем все данные, создаем заново все блоки"""
    global count, massive, massive_copy
    count = 0
    massive.clear()
    massive_copy.clear()
    massive_copy = [[0]] * 20
    frame.destroy()
    create_frame()
    create_label()
    create_combobox()
    create_button_add()
    create_button_stop()
    create_frame_out()
    create_label_result()
    ms.delete(0, tk.END)
    sq.delete(0, tk.END)


def create_menu():
    """Функция создания меню"""
    file_menu = tk.Menu(my_menu, tearoff=0)
    file_menu.add_command(label="Новый расчет",
                          background='white',
                          foreground='black',
                          activeforeground='black',
                          activebackground='#bab8b7',
                          command=delete)
    file_menu.add_command(label="Выход",
                          background='white',
                          foreground='black',
                          activeforeground='black',
                          activebackground='#bab8b7',
                          command=closing)
    my_menu.add_cascade(label="Файл", menu=file_menu)
    w.config(menu=my_menu)


# Иконка для кнопки <Удалить/Вернуть>
image_delete = Image.open("icon_delete.png")
image_remove = Image.open("icon_remove.png")

resize_image_delete = image_delete.resize((95, 23))
resize_image_remove = image_remove.resize((95, 23))

img_delete = ImageTk.PhotoImage(resize_image_delete)
img_remove = ImageTk.PhotoImage(resize_image_remove)


# Основные переменные
count = 0  # определяет количество позиций на экране (наша нумерация)
massive = []  # список, содержащий данные, считывающиеся из виджетов
massive_copy = [[0]]*20  # список, содержащий копию элементов данных (используется для восстановления данных)
delimiters = " / ", "  +  ", " +  ", "  + ", " + ", " +", "+ ", \
             " , ", ",  ", ", ", "  ", " ", "/ ", "/", "+", \
             " x ", " X ", "x ", "X ", " x", " X", "x", "X", \
             " х ", " Х ", "х ", "Х ", " х", " Х", "х", "Х"
regexPattern = '|'.join(map(re.escape, delimiters))  # сортировка delimiters по формату для split


# global Values
number_position = tk.Label()
section = ttk.Combobox()
gost = ttk.Combobox()
profile = ttk.Combobox()
size = ttk.Combobox()
thickness = ttk.Combobox()
enter_length = tk.Entry()
enter_elements = tk.Spinbox()
mass_el = tk.Entry()
mass = tk.Entry()
square_el = tk.Entry()
square = tk.Entry()
but_del_rem = tk.Button()
button_add = tk.Button()
button_stop = tk.Button()
ms = tk.Entry()
sq = tk.Entry()


# Заголовок
positions = [
    "№ п/п",
    "Металлопрокат,\nсечение",
    "ГОСТ",
    "Профиль",
    "Размер",
    "Толщина,\nмм",
    "Длина элемента, м\nРазмер листа/полосы, мм",
    "Кол-во,\nшт.",
    "Масса\nна ед., кг",
    "Общая\nмасса, кг",
    "Площадь\nна ед., м²",
    "Общая\nплощадь, м²",
    "Удалить /\nВернуть"
]


# Сортамент
sort = [
    "Лист", ["19903-2015"],
    "Полоса", ["103-2006"],
    "Труба круглая", ["10704-91", "2590-2006"],
    "Квадрат", ["30245-2003", "8639-82", "2591-2006"],
    "Прямоугольник", ["30245-2003", "8645-68"],
    "Уголок", ["Равнополочный", "8509-93",
               "Неравнополочный", "8510-86"],
    "Швеллер", ["8240-97"],
    "Двутавр", ["Р 57837-2017"]
]


def create_label():
    """Создаем неизменяемую шапку программы"""
    """№ п/п"""
    tk.Label(frame,
             text=positions[0],
             font=font_arial,
             bg='#eceb9e',
             fg='black',
             bd=2,
             relief=tk.RIDGE).grid(row=0,
                                   column=0,
                                   sticky="nswe",
                                   padx=(10, 3),
                                   pady=(10, 3))
    """Металлопрокат, сечение"""
    tk.Label(frame,
             text=positions[1],
             font=font_arial,
             bg=color_3,
             fg='black',
             bd=2,
             relief=tk.RIDGE).grid(row=0,
                                   column=1,
                                   sticky="nswe",
                                   padx=(3, 3),
                                   pady=(10, 3))
    """ГОСТ"""
    tk.Label(frame,
             text=positions[2],
             font=font_arial,
             bg=color_3,
             fg='black',
             bd=2,
             relief=tk.RIDGE).grid(row=0,
                                   column=2,
                                   sticky="nswe",
                                   padx=(3, 3),
                                   pady=(10, 3))
    """Профиль"""
    tk.Label(frame,
             text=positions[3],
             font=font_arial,
             bg=color_3,
             fg='black',
             bd=2,
             relief=tk.RIDGE).grid(row=0,
                                   column=3,
                                   sticky="nswe",
                                   padx=(3, 3),
                                   pady=(10, 3))
    """Размер"""
    tk.Label(frame,
             text=positions[4],
             font=font_arial,
             bg=color_3,
             fg='black',
             bd=2,
             relief=tk.RIDGE).grid(row=0,
                                   column=4,
                                   sticky="nswe",
                                   padx=(3, 3),
                                   pady=(10, 3))
    """Толщина, мм"""
    tk.Label(frame,
             text=positions[5],
             font=font_arial,
             bg=color_3,
             fg='black',
             bd=2,
             relief=tk.RIDGE).grid(row=0,
                                   column=5,
                                   sticky="nswe",
                                   padx=(3, 3),
                                   pady=(10, 3))
    """
    Длина элемента, м
    Размер листа/полосы, мм
    """
    tk.Label(frame,
             text=positions[6],
             font=font_arial,
             bg=color_3,
             fg='black',
             bd=2,
             relief=tk.RIDGE).grid(row=0,
                                   column=6,
                                   sticky="nswe",
                                   padx=(3, 3),
                                   pady=(10, 3))
    """Кол-во, шт."""
    tk.Label(frame,
             text=positions[7],
             font=font_arial,
             bg=color_3,
             fg='black',
             bd=2,
             relief=tk.RIDGE).grid(row=0,
                                   column=7,
                                   sticky="nswe",
                                   padx=(3, 3),
                                   pady=(10, 3))
    """Масса на ед., кг"""
    tk.Label(frame,
             text=positions[8],
             font=font_arial,
             bg=color_3,
             fg='black',
             bd=2,
             relief=tk.RIDGE).grid(row=0,
                                   column=8,
                                   sticky="nswe",
                                   padx=(3, 3),
                                   pady=(10, 3))
    """Общая масса, кг"""
    tk.Label(frame,
             text=positions[9],
             font=font_arial,
             bg=color_3,
             fg='black',
             bd=2,
             relief=tk.RIDGE).grid(row=0,
                                   column=9,
                                   sticky="nswe",
                                   padx=(3, 3),
                                   pady=(10, 3))
    """Площадь на ед., м²"""
    tk.Label(frame,
             text=positions[10],
             font=font_arial,
             bg=color_3,
             fg='black',
             bd=2,
             relief=tk.RIDGE).grid(row=0,
                                   column=10,
                                   sticky="nswe",
                                   padx=(3, 3),
                                   pady=(10, 3))
    """Общая площадь, м²"""
    tk.Label(frame,
             text=positions[11],
             font=font_arial,
             bg=color_3,
             fg='black',
             bd=2,
             relief=tk.RIDGE).grid(row=0,
                                   column=11,
                                   sticky="nswe",
                                   padx=(3, 3),
                                   pady=(10, 3))
    """Удалить /Вернуть"""
    tk.Label(frame,
             text=positions[12],
             font=font_arial,
             bg=color_3,
             fg='black',
             bd=2,
             relief=tk.RIDGE).grid(row=0,
                                   column=12,
                                   sticky="nswe",
                                   padx=(3, 3),
                                   pady=(10, 3))

    w.grid_rowconfigure(0, minsize=20)


def create_combobox():
    """Создаем таблицу - основной интерфейс"""
    global count, number_position, section, gost, profile, size, thickness, enter_length, enter_elements, \
        mass_el, mass, square_el, square, but_del_rem
    count += 1
    number_position = tk.Label(frame,
                               text=count,
                               width=6,
                               font=font_arial,
                               bg="#adaaff",
                               anchor="e")
    section = ttk.Combobox(frame,
                           values=sort[::2],
                           width=10,
                           state="readonly",
                           font=font_arial)
    gost = ttk.Combobox(frame,
                        values=sort[1],
                        state="readonly",
                        width=12,
                        font=font_arial)
    profile = ttk.Combobox(frame,
                           values=["---"],
                           state="disabled",
                           width=18,
                           font=font_arial)
    size = ttk.Combobox(frame,
                        values=["---"],
                        state="disabled",
                        width=8,
                        font=font_arial)
    thickness = ttk.Combobox(frame,
                             values=dt.sheet,
                             state="readonly",
                             width=8,
                             font=font_arial)
    enter_length = tk.Entry(frame,
                            font=font_arial,
                            width=27,
                            bd=1)
    enter_elements = tk.Spinbox(frame,
                                from_=1,
                                to=9999,
                                command=change_positions_mass_square,
                                font=font_arial,
                                width=8)
    mass_el = tk.Entry(frame,
                       font=font_arial,
                       width=10,
                       bg='#ffda4f',
                       fg='black',
                       disabledbackground='#fff3ac',
                       disabledforeground='black',
                       bd=2)
    mass = tk.Entry(frame,
                    font=font_arial,
                    width=10,
                    bg='#ff0c00',
                    fg='white',
                    disabledbackground='#e9957f',
                    disabledforeground='white',
                    bd=2)
    square_el = tk.Entry(frame,
                         font=font_arial,
                         width=15,
                         bg='#ffda4f',
                         fg='black',
                         disabledbackground='#fff3ac',
                         disabledforeground='black',
                         bd=2)
    square = tk.Entry(frame,
                      font=font_arial,
                      width=15,
                      bg='#ff0c00',
                      fg='white',
                      disabledbackground='#e9957f',
                      disabledforeground='white',
                      bd=2)
    but_del_rem = tk.Button(frame,
                            text=f'Удалить {count}',
                            image=img_delete,
                            bd=0,
                            bg=color_2,
                            activebackground=color_2,
                            state="disabled")

    section.current(0)
    gost.current(0)
    profile.current(0)
    size.current(0)
    thickness.current(0)
    enter_length.insert(0, "1000x1000")
    mass_el.insert(0, "3.140")
    mass.insert(0, "3.140")
    square_el.insert(0, "2.00")
    square.insert(0, "2.00")

    number_position.grid(row=count, column=0, sticky="nswe", padx=(10, 3), pady=(3, 3))
    section.grid(row=count, column=1, sticky="nswe", padx=(3, 3), pady=(3, 3))
    gost.grid(row=count, column=2, sticky="nswe", padx=(3, 3), pady=(3, 3))
    profile.grid(row=count, column=3, sticky="nswe", padx=(3, 3), pady=(3, 3))
    size.grid(row=count, column=4, sticky="nswe", padx=(3, 3), pady=(3, 3))
    thickness.grid(row=count, column=5, sticky="nswe", padx=(3, 3), pady=(3, 3))
    enter_length.grid(row=count, column=6, sticky="nswe", padx=(3, 3), pady=(3, 3))
    enter_elements.grid(row=count, column=7, sticky="nswe", padx=(3, 3), pady=(3, 3))
    mass_el.grid(row=count, column=8, sticky="nswe", padx=(3, 3), pady=(3, 3))
    mass.grid(row=count, column=9, sticky="nswe", padx=(3, 3), pady=(3, 3))
    square_el.grid(row=count, column=10, sticky="nswe", padx=(3, 3), pady=(3, 3))
    square.grid(row=count, column=11, sticky="nswe", padx=(3, 3), pady=(3, 3))
    but_del_rem.grid(row=count, column=12, sticky="nswe", padx=(3, 3))

    section.bind("<<ComboboxSelected>>", callback_section)
    gost.bind("<<ComboboxSelected>>", callback_gost)
    profile.bind("<<ComboboxSelected>>", callback_profile)
    size.bind("<<ComboboxSelected>>", callback_size)
    thickness.bind("<<ComboboxSelected>>", callback_thickness)
    enter_length.bind("<KeyRelease>", callback_thickness)
    enter_elements.bind("<KeyRelease>", callback_thickness)
    but_del_rem.bind("<Button-1>", lambda event, but_del_rem=but_del_rem: delete_remove(event, but_del_rem))


def callback_section(event):
    """Отслеживает любое событие для <section> - меняет <gost>"""
    if event:
        change_positions_gost()
        change_positions_mass_square()


def callback_gost(event):
    """Отслеживает любое событие для <gost> - меняет <profile>"""
    if event:
        change_positions_profile()
        change_positions_mass_square()


def callback_profile(event):
    """Отслеживает любое событие для <profile> - меняет <size>"""
    if event:
        change_positions_size()
        change_positions_mass_square()


def callback_size(event):
    """Отслеживает любое событие для <size> - меняет <thickness>"""
    if event:
        change_positions_thickness()
        change_positions_mass_square()


def callback_thickness(event):
    """Отслеживает любое событие для <size> - меняет <thickness>"""
    if event:
        change_positions_mass_square()


def change_positions_gost():
    """Меняем позиции <gost>, а также <profile> и <size> в зависимости от выбора <section>"""
    if section.get() == sort[0]:  # Лист
        enter_length.delete(0, tk.END)
        enter_length.insert(0, "1000x1000")
        gost["values"] = sort[1]
        gost.current(0)
        profile["values"] = ["---"]
        profile.current(0)
        profile["state"] = "disabled"
        size["values"] = ["---"]
        size.current(0)
        size["state"] = "disabled"
        thickness["values"] = dt.sheet
        thickness.current(0)
        thickness["state"] = "readonly"

    elif section.get() == sort[2]:  # Полоса
        enter_length.delete(0, tk.END)
        enter_length.insert(0, "1000x1000")
        gost["values"] = sort[3]
        gost.current(0)
        profile["values"] = ["---"]
        profile.current(0)
        profile["state"] = "disabled"
        size["values"] = ["---"]
        size.current(0)
        size["state"] = "disabled"
        thickness["values"] = dt.strip
        thickness.current(0)
        thickness["state"] = "readonly"

    elif section.get() == sort[4]:  # Труба круглая
        enter_length.delete(0, tk.END)
        enter_length.insert(0, "1")
        size["state"] = "readonly"
        gost["values"] = sort[5]
        gost.current(0)
        profile["values"] = ["---"]
        profile.current(0)
        profile["state"] = "disabled"
        size["values"] = dt.kr1[::3]
        size.current(0)
        thickness["values"] = dt.kr1[2][::2]
        thickness.current(0)
        thickness["state"] = "readonly"

    elif section.get() == sort[6]:  # Квадрат
        enter_length.delete(0, tk.END)
        enter_length.insert(0, "1")
        size["state"] = "readonly"
        gost["values"] = sort[7]
        gost.current(0)
        profile["values"] = ["---"]
        profile.current(0)
        profile["state"] = "disabled"
        size["values"] = dt.kv1[::3]
        size.current(0)
        thickness["values"] = dt.kv1[2][::2]
        thickness.current(0)
        thickness["state"] = "readonly"

    elif section.get() == sort[8]:  # Прямоугольник
        enter_length.delete(0, tk.END)
        enter_length.insert(0, "1")
        size["state"] = "readonly"
        gost["values"] = sort[9]
        gost.current(0)
        profile["values"] = ["---"]
        profile.current(0)
        profile["state"] = "disabled"
        size["values"] = dt.pr1[::3]
        size.current(0)
        thickness["values"] = dt.pr1[2][::2]
        thickness.current(0)
        thickness["state"] = "readonly"

    elif section.get() == sort[10]:  # Уголок
        enter_length.delete(0, tk.END)
        enter_length.insert(0, "1")
        profile["state"] = "readonly"
        size["state"] = "readonly"
        gost["values"] = sort[11][1::2]
        gost.current(0)
        profile["values"] = sort[11][::2]
        profile.current(0)
        size["values"] = dt.ug_r[::3]
        size.current(0)
        thickness["values"] = dt.ug_r[2][::2]
        thickness.current(0)
        thickness["state"] = "readonly"

    elif section.get() == sort[12]:  # Швеллер
        enter_length.delete(0, tk.END)
        enter_length.insert(0, "1")
        profile["state"] = "readonly"
        size["state"] = "readonly"
        gost["values"] = sort[13]
        gost.current(0)
        profile["values"] = dt.sh[::2]
        profile.current(0)
        size["values"] = dt.sh[1][::2]
        size.current(0)
        thickness["values"] = ["---"]
        thickness.current(0)
        thickness["state"] = "disabled"

    elif section.get() == sort[14]:  # Двутавр
        enter_length.delete(0, tk.END)
        enter_length.insert(0, "1")
        profile["state"] = "readonly"
        size["state"] = "readonly"
        gost["values"] = sort[15]
        gost.current(0)
        profile["values"] = dt.dv[::2]
        profile.current(0)
        size["values"] = dt.dv[1][::2]
        size.current(0)
        thickness["values"] = ["---"]
        thickness.current(0)
        thickness["state"] = "disabled"


def change_positions_profile():
    """Меняем позиции <profile> и <size> в зависимости от выбора <gost>"""
    if gost.get() == sort[5][0]:  # Труба круглая ГОСТ 10704-91
        size["values"] = dt.kr1[::3]
        size.current(0)
        thickness["values"] = dt.kr1[2][::2]
        thickness.current(0)
        thickness["state"] = "readonly"

    elif gost.get() == sort[5][1]:  # Труба круглая ГОСТ 2590-2006
        size["values"] = dt.kr2[::3]
        size.current(0)
        thickness["values"] = ["---"]
        thickness.current(0)
        thickness["state"] = "disabled"

    elif section.get() == sort[6] and gost.get() == sort[7][0]:  # Квадрат ГОСТ 30245-2003
        size["values"] = dt.kv1[::3]
        size.current(0)
        thickness["values"] = dt.kv1[2][::2]
        thickness.current(0)
        thickness["state"] = "readonly"

    elif gost.get() == sort[7][1]:  # Квадрат ГОСТ 8639-82
        size["values"] = dt.kv2[::3]
        size.current(0)
        thickness["values"] = dt.kv2[2][::2]
        thickness.current(0)
        thickness["state"] = "readonly"

    elif gost.get() == sort[7][2]:  # Квадрат ГОСТ 2591-2006
        size["values"] = dt.kv3[::3]
        size.current(0)
        thickness["values"] = ["---"]
        thickness.current(0)
        thickness["state"] = "disabled"

    elif section.get() == sort[8] and gost.get() == sort[9][0]:  # Прямоугольник ГОСТ 30245-2003
        size["values"] = dt.pr1[::3]
        size.current(0)
        thickness["values"] = dt.pr1[2][::2]
        thickness.current(0)
        thickness["state"] = "readonly"

    elif gost.get() == sort[9][1]:  # Прямоугольник ГОСТ 8645-68
        size["values"] = dt.pr2[::3]
        size.current(0)
        thickness["values"] = dt.pr2[2][::2]
        thickness.current(0)
        thickness["state"] = "readonly"

    elif gost.get() == sort[11][1]:  # Уголок равнополочный ГОСТ 8509-93
        profile["values"] = sort[11][::2]
        profile.current(0)
        size["values"] = dt.ug_r[::3]
        size.current(0)
        thickness["values"] = dt.ug_r[2][::2]
        thickness.current(0)
        thickness["state"] = "readonly"

    elif gost.get() == sort[11][3]:  # Уголок неравнополочный ГОСТ 8510-86
        profile["values"] = sort[11][::2]
        profile.current(1)
        size["values"] = dt.ug_n[::3]
        size.current(0)
        thickness["values"] = dt.ug_n[2][::2]
        thickness.current(0)
        thickness["state"] = "readonly"


def change_positions_size():
    """Меняем позиции <size>, а также для уголка <gost> в зависимости от выбора <profile>"""
    if profile.get() == sort[11][0]:  # если уголок равнополочный - gost = ГОСТ 8509-93
        gost.current(0)
        size["values"] = dt.ug_r[::3]
        size.current(0)
        thickness["values"] = dt.ug_r[2][::2]
        thickness.current(0)
        thickness["state"] = "readonly"

    elif profile.get() == sort[11][2]:  # если уголок неравнополочный - gost = ГОСТ 8510-86
        gost.current(1)
        size["values"] = dt.ug_n[::3]
        size.current(0)
        thickness["values"] = dt.ug_n[2][::2]
        thickness.current(0)
        thickness["state"] = "readonly"

    elif section.get() == sort[12]:  # Швеллер
        for i in range(len(dt.sh[::2])):
            if profile.get() == dt.sh[i * 2]:
                size["values"] = dt.sh[(i * 2) + 1][::2]
                size.current(0)

    elif section.get() == sort[14]:  # Двутавр
        for i in range(len(dt.dv[::2])):
            if profile.get() == dt.dv[i * 2]:
                size["values"] = dt.dv[(i * 2) + 1][::2]
                size.current(0)


def change_positions_thickness():
    """Меняем позицию <thickness> в зависимости от выбора <size>"""
    if gost.get() == sort[5][0]:  # ---> если ГОСТ 10704-91, то...
        for i in range(len(dt.kr1[::3])):
            if size.get() == dt.kr1[i * 3]:
                thickness["values"] = dt.kr1[(i * 3) + 2][::2]
                thickness.current(0)

    elif section.get() == sort[6] and gost.get() == sort[7][0]:  # ---> если квадрат и ГОСТ 30245-2003, то...
        for i in range(len(dt.kv1[::3])):
            if size.get() == dt.kv1[i * 3]:
                thickness["values"] = dt.kv1[(i * 3) + 2][::2]
                thickness.current(0)

    elif gost.get() == sort[7][1]:  # ---> если ГОСТ 8639-82, то...
        for i in range(len(dt.kv2[::3])):
            if size.get() == dt.kv2[i * 3]:
                thickness["values"] = dt.kv2[(i * 3) + 2][::2]
                thickness.current(0)

    elif section.get() == sort[8] and gost.get() == sort[9][0]:  # ---> если прямоугольник и ГОСТ 30245-2003, то...
        for i in range(len(dt.pr1[::3])):
            if size.get() == dt.pr1[i * 3]:
                thickness["values"] = dt.pr1[(i * 3) + 2][::2]
                thickness.current(0)

    elif gost.get() == sort[9][1]:  # ---> если ГОСТ 8645-68, то...
        for i in range(len(dt.pr2[::3])):
            if size.get() == dt.pr2[i * 3]:
                thickness["values"] = dt.pr2[(i * 3) + 2][::2]
                thickness.current(0)

    elif gost.get() == sort[11][1]:  # ---> если ГОСТ 8509-93, то...
        for i in range(len(dt.ug_r[::3])):
            if size.get() == dt.ug_r[i * 3]:
                thickness["values"] = dt.ug_r[(i * 3) + 2][::2]
                thickness.current(0)

    elif gost.get() == sort[11][3]:  # ---> если ГОСТ 8510-86, то...
        for i in range(len(dt.ug_n[::3])):
            if size.get() == dt.ug_n[i * 3]:
                thickness["values"] = dt.ug_n[(i * 3) + 2][::2]
                thickness.current(0)


def change_positions_mass_square():
    """Основная функция, в которой просчитывается масса и площадь, в зависимости от выбранных позиций"""
    def enter(ml, mm, sl, ss):
        """Функция вывода данных в виджет"""
        mass_el.delete(0, tk.END)
        mass_el.insert(0, str(format(ml, '.3f')))
        mass.delete(0, tk.END)
        mass.insert(0, str(format(mm, '.3f')))
        square_el.delete(0, tk.END)
        square_el.insert(0, str(format(sl, '.3f')))
        square.delete(0, tk.END)
        square.insert(0, str(format(ss, '.3f')))

    def error():
        """Вывод ошибки ERROR"""
        mass.delete(0, tk.END)
        mass.insert(0, "ERROR")
        square.delete(0, tk.END)
        square.insert(0, "ERROR")

    if section.get() == sort[0] or section.get() == sort[2]:  # ЕСЛИ ЛИСТ ИЛИ ПОЛОСА
        try:
            ent = re.split(regexPattern, enter_length.get())
            if len(ent) % 2 > 0:
                raise ValueError()
            else:
                ent_sum_m = 0
                ent_sum_s_x = 0
                ent_sum_s_y = 0
                for z in range(len(ent)//2):
                    ent_sum_m += float(ent[z * 2]) * float(ent[(z * 2) + 1])
                    ent_sum_s_x += 2 * ent_sum_m
                    ent_sum_s_y += 2 * (float(ent[z * 2]) + float(ent[(z * 2) + 1]))
            els = int(enter_elements.get())
            thick = float(thickness.get().replace(',', '.'))
            m_el = 7850 * thick * 10 ** -3
            m = m_el * els * ent_sum_m * 10 ** -6
            sq_el = 2 + 4 * thick * 10 ** -3
            sq = els * (ent_sum_s_x + thick * ent_sum_s_y) * 10 ** -6
            if m_el <= 0 or sq_el <= 0 or m <= 0 or sq <= 0:
                raise ValueError()
            enter(m_el, m, sq_el, sq)
        except:
            error()

    elif section.get() == sort[4]:  # ЕСЛИ ТРУБА КРУГЛАЯ
        if gost.get() == sort[5][0]:  # ЕСЛИ ТРУБА КРУГЛАЯ/10704-91
            for i in range(len(dt.kr1[::3])):
                if size.get() == dt.kr1[i * 3]:
                    for j in range(len(dt.kr1[(i * 3) + 2][::2])):
                        if thickness.get() == dt.kr1[(i * 3) + 2][(j * 2)]:
                            try:
                                ent = re.split(regexPattern, enter_length.get())
                                ent_sum = 0
                                for z in range(len(ent)):
                                    ent_sum += float(ent[z])
                                els = int(enter_elements.get())
                                m_el = dt.kr1[(i * 3) + 2][(j * 2) + 1]
                                m = m_el * els * ent_sum
                                sq_el = dt.kr1[(i * 3) + 1]
                                sq = sq_el * els * ent_sum
                                if m_el <= 0 or sq_el <= 0 or m <= 0 or sq <= 0:
                                    raise ValueError()
                                enter(m_el, m, sq_el, sq)
                            except:
                                error()

        elif gost.get() == sort[5][1]:  # ЕСЛИ ТРУБА КРУГЛАЯ/2590-2006
            for i in range(len(dt.kr2[::3])):
                if size.get() == dt.kr2[(i * 3)]:
                    try:
                        ent = re.split(regexPattern, enter_length.get())
                        ent_sum = 0
                        for z in range(len(ent)):
                            ent_sum += float(ent[z])
                        els = int(enter_elements.get())
                        m_el = dt.kr2[(i * 3) + 2]
                        m = m_el * els * ent_sum
                        sq_el = dt.kr2[(i * 3) + 1]
                        sq = sq_el * els * ent_sum
                        if m_el <= 0 or sq_el <= 0 or m <= 0 or sq <= 0:
                            raise ValueError()
                        enter(m_el, m, sq_el, sq)
                    except:
                        error()

    elif section.get() == sort[6]:  # ЕСЛИ КВАДРАТ
        if gost.get() == sort[7][0]:  # ЕСЛИ КВАДРАТ/30245-2003
            for i in range(len(dt.kv1[::3])):
                if size.get() == dt.kv1[i * 3]:
                    for j in range(len(dt.kv1[(i * 3) + 2][::2])):
                        if thickness.get() == dt.kv1[(i * 3) + 2][(j * 2)]:
                            try:
                                ent = re.split(regexPattern, enter_length.get())
                                ent_sum = 0
                                for z in range(len(ent)):
                                    ent_sum += float(ent[z])
                                els = int(enter_elements.get())
                                m_el = dt.kv1[(i * 3) + 2][(j * 2) + 1]
                                m = m_el * els * ent_sum
                                sq_el = dt.kv1[(i * 3) + 1]
                                sq = sq_el * els * ent_sum
                                if m_el <= 0 or sq_el <= 0 or m <= 0 or sq <= 0:
                                    raise ValueError()
                                enter(m_el, m, sq_el, sq)
                            except:
                                error()

        elif gost.get() == sort[7][1]:  # ЕСЛИ КВАДРАТ/8639-82
            for i in range(len(dt.kv2[::3])):
                if size.get() == dt.kv2[i * 3]:
                    for j in range(len(dt.kv2[(i * 3) + 2][::2])):
                        if thickness.get() == dt.kv2[(i * 3) + 2][(j * 2)]:
                            try:
                                ent = re.split(regexPattern, enter_length.get())
                                ent_sum = 0
                                for z in range(len(ent)):
                                    ent_sum += float(ent[z])
                                els = int(enter_elements.get())
                                m_el = dt.kv2[(i * 3) + 2][(j * 2) + 1]
                                m = m_el * els * ent_sum
                                sq_el = dt.kv2[(i * 3) + 1]
                                sq = sq_el * els * ent_sum
                                if m_el <= 0 or sq_el <= 0 or m <= 0 or sq <= 0:
                                    raise ValueError()
                                enter(m_el, m, sq_el, sq)
                            except:
                                error()

        elif gost.get() == sort[7][2]:  # ЕСЛИ КВАДРАТ/2591-2006
            for i in range(len(dt.kv3[::3])):
                if size.get() == dt.kv3[(i * 3)]:
                    try:
                        ent = re.split(regexPattern, enter_length.get())
                        ent_sum = 0
                        for z in range(len(ent)):
                            ent_sum += float(ent[z])
                        els = int(enter_elements.get())
                        m_el = dt.kv3[(i * 3) + 2]
                        m = m_el * els * ent_sum
                        sq_el = dt.kv3[(i * 3) + 1]
                        sq = sq_el * els * ent_sum
                        if m_el <= 0 or sq_el <= 0 or m <= 0 or sq <= 0:
                            raise ValueError()
                        enter(m_el, m, sq_el, sq)
                    except:
                        error()

    elif section.get() == sort[8]:  # ЕСЛИ ПРЯМОУГОЛЬНИК
        if gost.get() == sort[9][0]:  # ЕСЛИ ПРЯМОУГОЛЬНИК/30245-2003
            for i in range(len(dt.pr1[::3])):
                if size.get() == dt.pr1[i * 3]:
                    for j in range(len(dt.pr1[(i * 3) + 2][::2])):
                        if thickness.get() == dt.pr1[(i * 3) + 2][(j * 2)]:
                            try:
                                ent = re.split(regexPattern, enter_length.get())
                                ent_sum = 0
                                for z in range(len(ent)):
                                    ent_sum += float(ent[z])
                                els = int(enter_elements.get())
                                m_el = dt.pr1[(i * 3) + 2][(j * 2) + 1]
                                m = m_el * els * ent_sum
                                sq_el = dt.pr1[(i * 3) + 1]
                                sq = sq_el * els * ent_sum
                                if m_el <= 0 or sq_el <= 0 or m <= 0 or sq <= 0:
                                    raise ValueError()
                                enter(m_el, m, sq_el, sq)
                            except:
                                error()

        elif gost.get() == sort[9][1]:  # ЕСЛИ ПРЯМОУГОЛЬНИК/8645-68
            for i in range(len(dt.pr2[::3])):
                if size.get() == dt.pr2[i * 3]:
                    for j in range(len(dt.pr2[(i * 3) + 2][::2])):
                        if thickness.get() == dt.pr2[(i * 3) + 2][(j * 2)]:
                            try:
                                ent = re.split(regexPattern, enter_length.get())
                                ent_sum = 0
                                for z in range(len(ent)):
                                    ent_sum += float(ent[z])
                                els = int(enter_elements.get())
                                m_el = dt.pr2[(i * 3) + 2][(j * 2) + 1]
                                m = m_el * els * ent_sum
                                sq_el = dt.pr2[(i * 3) + 1]
                                sq = sq_el * els * ent_sum
                                if m_el <= 0 or sq_el <= 0 or m <= 0 or sq <= 0:
                                    raise ValueError()
                                enter(m_el, m, sq_el, sq)
                            except:
                                error()

    elif section.get() == sort[10]:  # ЕСЛИ УГОЛОК
        if gost.get() == sort[11][1]:  # ЕСЛИ УГОЛОК РАВНОПОЛОЧНЫЙ/8509-93
            for i in range(len(dt.ug_r[::3])):
                if size.get() == dt.ug_r[i * 3]:
                    for j in range(len(dt.ug_r[(i * 3) + 2][::2])):
                        if thickness.get() == dt.ug_r[(i * 3) + 2][(j * 2)]:
                            try:
                                ent = re.split(regexPattern, enter_length.get())
                                ent_sum = 0
                                for z in range(len(ent)):
                                    ent_sum += float(ent[z])
                                els = int(enter_elements.get())
                                m_el = dt.ug_r[(i * 3) + 2][(j * 2) + 1]
                                m = m_el * els * ent_sum
                                sq_el = dt.ug_r[(i * 3) + 1]
                                sq = sq_el * els * ent_sum
                                if m_el <= 0 or sq_el <= 0 or m <= 0 or sq <= 0:
                                    raise ValueError()
                                enter(m_el, m, sq_el, sq)
                            except:
                                error()

        elif gost.get() == sort[11][3]:  # ЕСЛИ УГОЛОК НЕРАВНОПОЛОЧНЫЙ/8510-86
            for i in range(len(dt.ug_n[::3])):
                if size.get() == dt.ug_n[i * 3]:
                    for j in range(len(dt.ug_n[(i * 3) + 2][::2])):
                        if thickness.get() == dt.ug_n[(i * 3) + 2][(j * 2)]:
                            try:
                                ent = re.split(regexPattern, enter_length.get())
                                ent_sum = 0
                                for z in range(len(ent)):
                                    ent_sum += float(ent[z])
                                els = int(enter_elements.get())
                                m_el = dt.ug_n[(i * 3) + 2][(j * 2) + 1]
                                m = m_el * els * ent_sum
                                sq_el = dt.ug_n[(i * 3) + 1]
                                sq = sq_el * els * ent_sum
                                if m_el <= 0 or sq_el <= 0 or m <= 0 or sq <= 0:
                                    raise ValueError()
                                enter(m_el, m, sq_el, sq)
                            except:
                                error()

    elif section.get() == sort[12]:  # ЕСЛИ ШВЕЛЛЕР
        for i in range(len(dt.sh[::2])):
            if profile.get() == dt.sh[i * 2]:
                for j in range(len(dt.sh[(i * 2) + 1][::2])):
                    if size.get() == dt.sh[(i * 2) + 1][(j * 2)]:
                        try:
                            ent = re.split(regexPattern, enter_length.get())
                            ent_sum = 0
                            for z in range(len(ent)):
                                ent_sum += float(ent[z])
                            els = int(enter_elements.get())
                            m_el = dt.sh[(i * 2) + 1][(j * 2) + 1][1]
                            m = m_el * els * ent_sum
                            sq_el = dt.sh[(i * 2) + 1][(j * 2) + 1][0]
                            sq = sq_el * els * ent_sum
                            if m_el <= 0 or sq_el <= 0 or m <= 0 or sq <= 0:
                                raise ValueError()
                            enter(m_el, m, sq_el, sq)
                        except:
                            error()

    elif section.get() == sort[14]:  # ЕСЛИ ДВУТАВР
        for i in range(len(dt.dv[::2])):
            if profile.get() == dt.dv[i * 2]:
                for j in range(len(dt.dv[(i * 2) + 1][::2])):
                    if size.get() == dt.dv[(i * 2) + 1][(j * 2)]:
                        try:
                            ent = re.split(regexPattern, enter_length.get())
                            ent_sum = 0
                            for z in range(len(ent)):
                                ent_sum += float(ent[z])
                            els = int(enter_elements.get())
                            m_el = dt.dv[(i * 2) + 1][(j * 2) + 1][1]
                            m = m_el * els * ent_sum
                            sq_el = dt.dv[(i * 2) + 1][(j * 2) + 1][0]
                            sq = sq_el * els * ent_sum
                            if m_el <= 0 or sq_el <= 0 or m <= 0 or sq <= 0:
                                raise ValueError()
                            enter(m_el, m, sq_el, sq)
                        except:
                            error()


def create_button_add():
    """Создаем кнопку <Добавить позицию>"""
    global button_add
    button_add = tk.Button(frame,
                           text="Добавить позицию",
                           font=font_arial,
                           activebackground="#167822",
                           activeforeground="white",
                           fg="black",
                           bg="#15bc54",
                           bd=3,
                           command=add_new_branch)
    button_add.grid(row=count + 1, column=1)
    button_add.bind("<Enter>", cursor_on_button_add)
    button_add.bind("<Leave>", cursor_out_button_add)


def cursor_on_button_add(event):
    """Меняем цвет кнопки <Добавить позицию>, если курсор мыши наведен на виджет"""
    if event:
        button_add["bg"] = "#01fe17"
    else:
        button_add["bg"] = "#15bc54"


def cursor_out_button_add(event):
    """Меняем цвет кнопки <Добавить позицию>, если курсор мыши вне виджета"""
    if event:
        button_add["bg"] = "#15bc54"
    else:
        button_add["bg"] = "#01fe17"


def add_new_branch():
    """Нажатием на <Добавить позицию> создаем новый блок.
    Прежде, чем создать, удаляем все кнопки ниже, и вновь создаем их на 1 позицию ниже"""
    if check_input_data() and count_max():
        if button_stop["state"] == "normal":
            append_massive()
            change_output()
        section["state"] = "disabled"
        gost["state"] = "disabled"
        profile["state"] = "disabled"
        size["state"] = "disabled"
        thickness["state"] = "disabled"
        enter_length["state"] = "disabled"
        enter_elements["state"] = "disabled"
        mass_el["state"] = "disabled"
        mass["state"] = "disabled"
        square_el["state"] = "disabled"
        square["state"] = "disabled"
        but_del_rem["state"] = "normal"
        button_add.destroy()
        button_stop.destroy()
        create_combobox()
        create_button_add()
        create_button_stop()


def count_max():
    """Задаем максимальное количество строк в окне = не более 20 шт."""
    try:
        if count >= 20:
            raise ValueError()
        else:
            return 1
    except:
        mb.showerror(title='Внимание!', message='Превышено максимальное количество позиций в программе. '
                                                'Пожалуйста, создайте новый расчет или зайдите заново.')


def create_button_stop():
    """Создаем кнопку <<Посчитать>>"""
    global button_stop
    button_stop = tk.Button(frame,
                            text="Посчитать",
                            font=font_arial,
                            activebackground="#a51d17",
                            activeforeground="white",
                            fg="black",
                            bg="#ff0600",
                            width=11,
                            bd=3,
                            command=last_elem_massive)
    button_stop.grid(row=count + 1, column=2, sticky="nswe", padx=(5, 5), pady=(3, 3))
    button_stop.bind("<Enter>", cursor_on_button_stop)
    button_stop.bind("<Leave>", cursor_out_button_stop)


def cursor_on_button_stop(event):
    """Меняем цвет кнопки <Посчитать>, если курсор мыши наведен на виджет"""
    if event:
        button_stop["bg"] = "#fcf301"
    else:
        button_stop["bg"] = "#ff0600"


def cursor_out_button_stop(event):
    """Меняем цвет кнопки <Посчитать>, если курсор мыши вне виджета"""
    if event:
        button_stop["bg"] = "#ff0600"
    else:
        button_stop["bg"] = "#fcf301"


def last_elem_massive():
    """Блокируем всю строку для записи, добавляем в массив последние элементы,
    блокируем кнопку <Закончить>, разблокировываем кнопку <Посчитать>"""
    if check_input_data():
        section["state"] = "disabled"
        gost["state"] = "disabled"
        profile["state"] = "disabled"
        size["state"] = "disabled"
        thickness["state"] = "disabled"
        enter_length["state"] = "disabled"
        enter_elements["state"] = "disabled"
        mass_el["state"] = "disabled"
        mass["state"] = "disabled"
        square_el["state"] = "disabled"
        square["state"] = "disabled"
        but_del_rem["state"] = "normal"
        append_massive()
        change_output()
        button_stop["state"] = "disabled"


def check_input_data():
    """Проверяем <mass> и <square> на то, что введено число или набор чисел"""
    try:
        value1 = mass.get().replace(".", "")
        value2 = square.get().replace(".", "")
        if not (value1.isdigit() and value2.isdigit()):
            raise ValueError()
    except ValueError:
        mb.showerror(title='Ошибка', message='Проверьте правильность введенных данных')
    else:
        return 1


def delete_remove(event, button):
    """Заменяем кнопку <Удалить> на <Восстановить> и наоборот, считываем позицию кнопки через 'text'"""
    if event:
        if button["state"] == "normal":
            for i in range(1, 21):
                if button["text"] == f'Удалить {i}':
                    button["text"] = f'Вернуть {i}'
                    button["image"] = img_remove
                    massive_copy[i-1] = massive[i-1]
                    massive[i-1] = [0]
                    change_output()
                elif button["text"] == f'Вернуть {i}':
                    button["text"] = f'Удалить {i}'
                    button["image"] = img_delete
                    massive[i-1] = massive_copy[i-1]
                    change_output()


def append_massive():
    """Сохранение всех значений в список"""
    massive.append([
        section.get(),  # 0
        gost.get(),  # 1
        profile.get(),  # 2
        section.get(),  # 3
        size.get(),  # 4
        thickness.get(),  # 5
        enter_length.get(),  # 6
        enter_elements.get(),  # 7
        mass_el.get(),  # 8
        mass.get(),  # 9
        square_el.get(),  # 10
        square.get()  # 11
    ])


def change_output():
    """Вывод результатов в итоговое окно при любом изменении параметров"""
    var_ms = 0
    var_sq = 0
    for i in range(len(massive)):
        if massive[i] == [0]:
            continue
        else:
            var_ms += float(massive[i][9])
            var_sq += float(massive[i][11])

    ms.delete(0, tk.END)
    ms.insert(0, str(format(var_ms, '.3f')))
    sq.delete(0, tk.END)
    sq.insert(0, str(format(var_sq, '.3f')))


def create_label_result():
    """Создаем итоговое окно со значениями массы и площади"""
    global ms, sq
    tk.Label(frame_out,
             text="Итоговая масса:",
             bg='#3985ff',
             fg='black',
             font=font_arial).grid(row=0,
                                   column=0,
                                   padx=(10, 0),
                                   pady=4)
    tk.Label(frame_out,
             text="Итоговая площадь:",
             bg='#3985ff',
             fg='black',
             font=font_arial).grid(row=0,
                                   column=3,
                                   padx=(10, 0),
                                   pady=4)
    tk.Label(frame_out,
             text="кг",
             bg='#3985ff',
             fg='black',
             font=font_arial).grid(row=0,
                                   column=2,
                                   padx=(0, 10),
                                   pady=4)
    tk.Label(frame_out,
             text="м²",
             bg='#3985ff',
             fg='black',
             font=font_arial).grid(row=0,
                                   column=5,
                                   padx=(0, 10),
                                   pady=4)
    ms = tk.Entry(frame_out, font=font_arial, width=15, bg='red', fg='white')
    ms.grid(row=0, column=1, padx=5, pady=4)
    sq = tk.Entry(frame_out, font=font_arial, width=15, bg='red', fg='white')
    sq.grid(row=0, column=4, padx=5, pady=4)


def create_frame_out():
    """Создаем отдельный фрейм для итоговых значений"""
    global frame_out
    frame_out = tk.Frame(w, width=700, height=160, bg='#3985ff', bd=4, relief=tk.RIDGE)
    frame_out.place(x=857, y=655)


# <<<<<<<<<<<------------HEAD SCRIPT------------->>>>>>>>>>>>
frame = tk.Frame(w, bg=color_1, width=1435, height=720)
frame.place(x=0, y=0, relheight=1, relwidth=1)
bg_label = tk.Label(frame, image=img)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)
create_menu()
create_label()
create_combobox()
create_button_add()
create_button_stop()

frame_out = tk.Frame(w, width=700, height=160, bg='#3985ff', bd=4, relief=tk.RIDGE)
frame_out.place(x=857, y=655)

create_label_result()

w.protocol("WM_DELETE_WINDOW", closing)

w.mainloop()
