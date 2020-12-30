from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from websocket import create_connection
import json
import gzip
import websocket
import time
import threading


class TuisongConsumer(WebsocketConsumer):

    def connect(self):
        # self.websocket_cli()
        self.cate_name = self.scope["url_route"]['kwargs'].get('category')
        self.cate_group_name = "goup_{}".format(self.cate_name)
        async_to_sync(self.channel_layer.group_add)(
            self.cate_group_name,
            self.channel_name
        )
        # async_to_sync(self.channel_layer.group_send)(
        #     self.cate_group_name,
        #     {
        #         "type": 'tuisong.message',
        #         "message": "res"
        #     }
        # )
        self.accept()

    def websocket_cli(self):

        def on_message(ws, message):
            res = gzip.decompress(message)
            res = json.loads(res)
            if "ping" in res:
                num = res["ping"]
                data = {"pong": int(num)}
                data = json.dumps(data).encode()
                ws.send(data)
            else:
                # print(res)
                pass

        def on_open(ws):
            def run(*args):
                data = {
                    "sub": "market.btcusdt.kline.1min",
                    "id": "id1"
                }
                # data = gzip.compress(str(data).encode())
                data = json.dumps(data).encode()
                ws.send(data)
            return run()
            # t = threading.Thread(target=run, args=())
            # t.start()
        websocket.enableTrace(True)
        self.ws = websocket.WebSocketApp("wss://api.huobi.pro/ws", on_message=on_message)
        self.ws.on_open = on_open
        self.ws.run_forever()

    def disconnect(self, code):
        print("codeis ", code)
        # print(dir(self.channel_layer))
        # async_to_sync(self.channel_layer.group_discard)(
        #     self.cate_group_name,
        #     self.channel_name
        # )
        # self.ws.close()

    def deal(self,data):
        count = 0
        while count < 5:
            self.send(f"yi shou dao {data}-{count}")
            time.sleep(1)
            count = count + 1

    def receive(self, text_data=None, bytes_data=None):

        # text_data = json.loads(text_data)
        print(f"jie shou dao {text_data}")
        t = threading.Thread(target=self.deal, args=(self.channel_name,))
        t.setDaemon(True)
        t.start()
        # print(dir(self))

        # self.channel_layer.send(message="yi shou dao",channel=self.channel_name)
        # async_to_sync(self.channel_layer.send)(
        #     self.cate_group_name,
        #     {
        #         "type": 'tuisong.message',
        #         "message": "res"
        #     }
        # )
        # message = text_data["message"]

        # if not message:
        #     print("没有收到数据，关闭websocket")
        #     self.ws.close()
        # async_to_sync(self.channel_layer.group_send)(
        #     self.cate_group_name,
        #     {
        #         "type": 'tuisong.message',
        #         "message": message
        #     }
        # )

    # def recive_message(self, event):
    #     message = event["message"]
    #     self.send(text_data=json.dumps({
    #         "message": message
    #     }))

