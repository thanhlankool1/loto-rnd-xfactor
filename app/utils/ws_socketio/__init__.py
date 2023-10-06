# -*- coding: utf-8 -*-
from .events_client import *
from .events_server import *



ws_event_mapping = {
    #
    #   Websocket Server
    # '*': {'handler': all_event, 'namespace': None},
    "connect": {"handler": client_connected, "namespace": None},
    "disconnect": {"handler": client_disconnected, "namespace": None},
    "client-set-name" :  {"handler": client_set_name, "namespace": None},
    "client-create-room" : {"handler": client_create_room, "namespace": None},
    "client-join-room" : {"handler": client_join_room, "namespace": None},
    "client-out-room" : {"handler": out_room, "namespace": None},
    "owner-out-room" : {"handler": owner_out_room, "namespace": None},
    "get-list-room" : {"handler": get_list_room, "namespace": None},
    "change-owner-room" : {"handler": None, "namespace": None},
    "random-lucky-number-to-user" : {"handler": random_lucky_number_to_user, "namespace": None},
    "send-lucky-number-to-user" : {"handler": send_lucky_number_to_user, "namespace": None},
    "reset-lucky-number" : {"handler": reset_lucky_number, "namespace": None},
    "bingo" : {"handler": bingo, "namespace": None},
    "start-game" : {"handler": start_game, "namespace": None}
}
