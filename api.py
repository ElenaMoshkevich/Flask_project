# сервер предназначен для генерации примеров по запросу
from flask import Flask, request, jsonify
from generation import Task

app = Flask(__name__)


@app.route('/api', methods=['GET'])
def api_gen():  # по данным запроса генерирует примеры
    count = int(request.args.get('count', 2))  # число примеров
    complexity = request.args.get("complexity", 'Средний уровень')  # сложность
    notation_inp = int(request.args.get("notation_inp", 3))
    notation_out = int(request.args.get("notation_out", 10))
    rnd_inp = bool(request.args.get("rnd_inp", False))
    rnd_out = bool(request.args.get("rnd_out", False))
    # создаем экземпляр класса примеров и передаем в него полученные параметры
    tr = Task(count=int(count),
              complexity=complexity,
              notation_inp=notation_inp,
              notation_out=notation_out,
              rnd_inp=rnd_inp, rnd_out=rnd_out)
    # возможна ситуация, когда получить нужное число различных примеров не возможно
    # например 10 различных 2-х значных чисел (10,11 и все...)
    if not tr.success:
        jsonify({"message": "it is not possible to generate examples with the given parameters", "Error": 406})
    return jsonify(tr.primeri)


@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"message": "request parameters are not correct", "Error": 404})


if __name__ == '__main__':
    app.run(port=8081, host='127.0.0.1')
# пример запроса к серверу
# /api?count=3&complexity=Средний уровень&notation_inp=13&notation_out=10&rnd_out=True
