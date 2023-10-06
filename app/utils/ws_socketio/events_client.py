from .events_handler import SocketIOHandler

socket_handler = SocketIOHandler()

# -*- coding: utf-8 -*-
async def client_connected(sid, *args, **kwargs):
    await SocketIOHandler().save_user_id_socket_id(sid=sid)
    
async def client_disconnected(sid, *args, **kwargs):
    await SocketIOHandler().check_user_out_room(sid=sid)
    await SocketIOHandler().remove_user_id_socket_id(sid=sid)
    

async def client_set_name(sid, data, *args, **kwargs):
    if data and data.get("name"):
        await SocketIOHandler().set_name_by_sid(sid, data.get('name'))
    
async def client_create_room(sid, data, *args, **kwargs):
    if data and data.get("name"):
        await SocketIOHandler().client_create_room(sid, data.get('name'))
        
async def client_join_room(sid, data, *args, **kwargs):
    # print(f'--> ws get event=client_join_room {sid=} ')
    if data and data.get("name"):
        await SocketIOHandler().client_join_room(sid, data.get('name'))
        
async def out_room(sid, *args, **kwargs):
    # print(f'--> ws get event=client_join_room {sid=} ')
    await SocketIOHandler().check_user_out_room(sid)

async def owner_out_room(sid, data, *args, **kwargs):
    if data:
        await SocketIOHandler().owner_out_room_new(sid, data.get("room_id"))

async def get_list_room(sid, *args, **kwargs):
    await SocketIOHandler().get_list_room(sid)
    
async def send_lucky_number_to_user(sid, data, *args, **kwargs):
    if data:
        await SocketIOHandler().send_lucky_number_to_user(sid, data.get("lucky_number"), data.get("room_id"))

async def random_lucky_number_to_user(sid, data, *args, **kwargs):
    if data:
        await SocketIOHandler().random_lucky_number_to_user(sid, data.get("room_id"))
        
async def reset_lucky_number(sid, data, *args, **kwargs):
    if data:
        await SocketIOHandler().reset_lucky_number(sid, data.get("room_id"))

async def bingo(sid, data, *args, **kwargs):
    if data:
        await SocketIOHandler().bingo(sid, data.get("lucky_range"), data.get("room_id"))

async def start_game(sid, data, *args, **kwargs):
    if data:
        await SocketIOHandler().start_game(sid, data.get("countdown_time"), data.get("room_id"))

# async def client_join_room(sid, data, *args, **kwargs):
#     print(f'--> ws get event=client_join_room {sid=} ')
#     print("data", data)
#     if data and data.get("name"):
#         # await SocketIOHandler().set_name_by_sid(sid, data.get('name'))
#         pass