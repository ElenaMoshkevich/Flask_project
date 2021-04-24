# сервер предназначен для работы с пользователем
from flask import Flask, request, jsonify, render_template, url_for, redirect, session
from generation import ALFAVIT, COMPLEXITY
import requests
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = "Moshkevich"

app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(
    days=365
)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/help')
def help():
    return render_template('help.html')


@app.route('/description')
def description():
    return render_template('description.html')


@app.route('/form_data', methods=['POST', 'GET'])
def form_data():  # запрашивает данные для генерации примеров
    if request.method == 'GET':
        return render_template('form.html', compl=COMPLEXITY, title="Ввод данных")
    elif request.method == 'POST':
        rnd_inp, rnd_out = "", ""
        if request.form['notation_inp'] == "сгенерировать автоматически":
            rnd_inp = True
            notation_inp = 5
        else:
            notation_inp = int(request.form['notation_inp'])
        if request.form['notation_out'] == "сгенерировать автоматически":
            rnd_out = True
            notation_out = 10
        else:
            notation_out = int(request.form['notation_out'])
        params = {}
        params["count"] = int(request.form["numtask"])
        params["complexity"] = request.form["complexity"]
        params["notation_inp"] = notation_inp
        params["notation_out"] = notation_out
        params["rnd_inp"] = rnd_inp
        params["rnd_out"] = rnd_out
        #  нужно указать адрес сервера, который генерирует примеры
        url = "http://127.0.0.1:8081/api"
        response = requests.get(url, params)
        json = response.json()
        session['data'] = json
        return redirect(url_for('trening'))


@app.route('/trening', methods=['POST', 'GET'])
def trening():  # показывает примеры и ждет ввода ответов, после этого перенапрвляет
    # на просмотр результата решения
    if request.method == 'GET':
        pr_dict = session['data']
        return render_template('trening.html', pr_dict=pr_dict, title="Решение примеров")
    elif request.method == 'POST':
        session['answer'] = dict(request.form)
        return redirect(url_for('answers'))


@app.route('/answers_true')
def answers_true():  # показывает верные ответы
    pr_dict = session['data']
    html_pr = "<font size=20> Верные ответы: </font> <hr><br>"
    for key in pr_dict:
        html_pr += answer_html(pr_dict[key]) + "<hr><br>"
    return html_pr + f"<p><hr><a href='/index'> На главную </a>"


@app.route('/answers', methods=['POST', 'GET'])
def answers():  # для каждого решения выдает вердикт -верно и пр...
    if request.method == 'GET':
        pr_dict = session['data']
        ans = session['answer']
        results = []
        key_sort = sorted(ans.keys())
        for key in key_sort:
            keys = key.split(":")
            results.append(result_pr(ans[key], pr_dict[keys[1]]))
        session['result'] = results
        return render_template('answer.html', result=results, title="Ваши результаты")
    else:
        return redirect(url_for('answers_true'))


def task_html(num_dict):  # представляет задание примера в формате html
    html_task = f'<h1> &nbsp;&nbsp;{num_dict["number"]}<sub>{num_dict["notation_inp"]}</sub> =</h1>'
    return html_task


def result_pr(ans, task):
    if ans == task['trans_num']:
        verdict = 'Верно!!!'
    else:  # проверяем корректность ввода ответа
        if ans == '':
            verdict = 'Ничего не введено!!!'
            ans = "?"
        # все введенные символы есть в алфавите итоговой системы счисления
        elif set(ans) <= set(ALFAVIT[:task["notation_out"]]):
            verdict = 'Ошибка в вычислениях!'
        # введеные символы могли бы встретиться в числах
        elif set(ans) <= set(ALFAVIT):
            verdict = 'В системе счисления нет введеных цифр!!!'
        else:
            verdict = 'Введены недопустимые символы!!!'
    return {"pr": [task["number"], task["notation_inp"], task["notation_out"]],
            "ans_user": ans,
            "verdict": verdict}


def answer_html(num_dict):  # прредставляет пример в формате html  с правильным ответом
    html_answer = f'<font size = 5> &nbsp; &nbsp;{num_dict["number"]}<sub>{num_dict["notation_inp"]}</sub> =' \
                  f' {num_dict["trans_num"]}<sub>{num_dict["notation_out"]}</sub>&nbsp;</font>'
    return html_answer


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
