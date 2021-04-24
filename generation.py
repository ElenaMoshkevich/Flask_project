from random import sample, randint

ALFAVIT = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
# для задания уровня сложности используем словарь, по ключу сложности храним максимальное число,
# которое будет предложено для перевода (число может быть незначительно больше или меньше заданного)
COMPLEXITY = {"Начальный уровень": "100",
              "Средний уровень": "257",
              "Сложный уровень": "512",
              "Очень сложный уровень": "2048"}


class Task():  # создающий задание

    def __init__(self, count=2, complexity='Средний уровень', notation_inp=3, notation_out=10, rnd_inp=False,
                 rnd_out=False):
        self.rnd_inp = rnd_inp  # флаг определяет задавать ли начальную систему счисления случайно
        self.rnd_out = rnd_out  # флаг определяет задавать ли конечную систему счисления случайно
        self.count = count  # количество примеров
        self.notation_inp = notation_inp  # начальная система счисления
        self.notation_out = notation_out  # конечная система счисления
        # вычисляем какой длины должно быть исходное число. в зависимости от сложности
        self.length = self.complexity_to_length(complexity, self.notation_inp)
        self.primeri = {}  # храним примеры и ответы,  каждый пример словарь
        self.success = self.initialization()

    def initialization(self):
        # генерирует нужное число примеров и записывает в словарь словарей, по уникальному ключу
        #  возвращает False - если не возможно сгенерировать нужное число уникальных примеров для заданных параметров
        number_of_attempts = 0
        while len(self.primeri) < self.count:
            if self.rnd_inp:
                self.notation_inp = randint(2, 16)
            if self.rnd_out:
                self.notation_out = randint(2, 16)
            # если начальная система совпадает с конечной (переводить по сути нечего),
            # генерируем другую конечную систему
            while self.notation_out == self.notation_inp:
                self.notation_out = randint(2, 16)
            key_number, number = self.gen_number()  # генерируем число, которое нужно перевести
            number_of_attempts += 1
            while key_number in self.primeri:  # если такое число уже было, то генерируем новое, пока не будет повторения
                key_number, number = self.gen_number()
                number_of_attempts += 1
                # если сгенерировать нужное число различных чисел не возможно, выходим
                if number_of_attempts > self.count * 100:
                    return False
            self.primeri[key_number] = number
        return True

    def gen_number(self):  # генерирует ключ и словарь, для одного задания
        # получаем первую цифру числа из существующих в системе счисления,кроме 0, остальные берем все возможные
        if self.length == 1:
            chislo = sample(ALFAVIT[1:self.notation_inp], 1)
        else:
            chislo = sample(ALFAVIT[1:self.notation_inp], 1) + sample(ALFAVIT[:self.notation_inp] * 10, self.length - 1)
        num = ''.join(chislo)
        # получаем уникальный ключ
        key_number = f"{num}_{self.notation_inp}_{self.notation_out}"
        number = {'number': num,
                  "notation_inp": self.notation_inp,
                  "notation_out": self.notation_out,
                  "trans_num": self.trans_dec_x(str(int(num, self.notation_inp)), self.notation_out)}
        return key_number, number

    def trans_dec_x(self, shislo, osn_x):  # переводит число из десятичной системы в произвольную
        znach = int(shislo)
        rez = ''
        while znach >= osn_x:
            rez = ALFAVIT[znach % osn_x] + rez
            znach //= osn_x
        return ALFAVIT[znach] + rez

    def answer_html(self, num_dict):  # прредставляет пример в формате html  с правильным ответом
        html_answer = f'<font size = 5> &nbsp; &nbsp;{num_dict["number"]}<sub>{num_dict["notation_inp"]}</sub> =' \
                      f' {num_dict["trans_num"]}<sub>{num_dict["notation_out"]}</sub>&nbsp;</font>'
        return html_answer

    def task_html(self, num_dict):  # представляет задание примера в формате html
        html_task = f'<h1> Переведи число&nbsp;&nbsp;{num_dict["number"]}<sub>{num_dict["notation_inp"]}</sub>' \
                    f' в систему счисления с основанием - {num_dict["notation_out"]}!</h1>'
        return html_task

    def complexity_to_length(self, compl,
                             notation_inp):  # переводит из словесного уровня сложности в длину генерируемого числа
        return len((str(self.trans_dec_x(COMPLEXITY[compl], notation_inp))))
