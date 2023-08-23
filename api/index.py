from sanic import Sanic
from sanic.response import json

app = Sanic(__name__)

def fibonacci_ratio(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci_ratio(n-1) / fibonacci_ratio(n-2)

@app.route('/fibonacci-ratio/<n:int>')
async def fibonacci_ratio_handler(request, n):
    ratio = fibonacci_ratio(n)
    return json({'ratio': ratio})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
