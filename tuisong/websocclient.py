from websocket import create_connection
import json
import gzip
import websocket
import threading

ws = create_connection("wss://api.huobi.pro/ws")


def data_compress(data):
    return gzip.compress(str(data).encode())


def on_message(ws, message):
    res = gzip.decompress(message)
    res = json.loads(res)
    print(res)
    if "ping" in res:
        num = res["ping"]
        data = {"pong": int(num)}
        data = json.dumps(data).encode()
        ws.send(data)
    # res = ws.recv()
    # res = gzip.decompress(res)
    # print(res)


def on_ping(ws):
    data = {
        "sub": "market.btccny.kline.1min",
        "id": "id1"
    }
    # data = gzip.compress(str(data).encode())
    data = json.dumps(data).encode()
    ws.send(data)


def on_open(ws):
    def run(*args):
        data = {
            "sub": "market.btcusdt.kline.1min",
            "id": "id1"
        }
        # data = gzip.compress(str(data).encode())
        data = json.dumps(data).encode()
        ws.send(data)
    t = threading.Thread(target=run, args=())
    t.start()


def on_close(ws):
    print("closed")


websocket.enableTrace(True)
ws = websocket.WebSocketApp("wss://api.huobi.pro/ws", on_message=on_message, on_close=on_close)
ws.on_open = on_open
ws.run_forever()
