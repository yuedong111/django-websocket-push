import asyncio
import websockets

# 向服务器端认证，用户名密码通过才能退出循环
async def auth_system(websocket):
    while True:
        cred_text = input("please enter your username and password: ")
        await websocket.send(cred_text)
        response_str = await websocket.recv()
        if "congratulation" in response_str:
            return True

# 向服务器端发送认证后的消息
import time
async def send_msg(websocket):

    _text = "hello world"
    if _text == "exit":
        print(f'you have enter "exit", goodbye')
        await websocket.close(reason="user exit")
        return False
    await websocket.send(_text)
    count=0
    while count<4:
        time.sleep(1)
        recv_text = await websocket.recv()
        print(f"{recv_text}")
        count = count+1

# 客户端主逻辑
async def main_logic():
    async with websockets.connect('ws://127.0.0.1:8000/ws/tuisong/haha') as websocket:
        await send_msg(websocket)

asyncio.get_event_loop().run_until_complete(main_logic())

# print(f"recevice {ws.recv()}")