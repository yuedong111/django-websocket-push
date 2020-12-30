from websocket import create_connection
ws = create_connection("ws://127.0.0.1:8000/ws/tuisong/haha")
ws.send("Hello, World")
print(f"recevice {ws.recv()}")
ws.send("2 world")
while True:
    print(f"{ws.recv()}")
# print(f"recevice {ws.recv()}")