from typing import Dict,List
from app.ws import sio
from ..abc.singleton import SingletonClass
from copy import deepcopy, copy
from uuid import uuid4
import logging


#-------------------------- Function data mapping socket id ------------------------------------
class SocketIOHandler(SingletonClass):
    def _singleton_init(self):
        # ---- update ---
        # example : 
        """
        list_room : {
            room_id : {
                "name" : ""
                "total_user" : ""
            }
        }
        
        list_user : {
            user_id : {
                "name" : ""
                "room_id" : ""
            }
        }
        """
        self.list_room = {}
        self.list_user = {}
        self.list_user_vs_room = {}
        self.room_id = {}
        
    async def save_user_id_socket_id(self, sid):
        self.list_user.update({
            sid : {
                "name" : None,
                "info_room" : {
                    "role" : None,
                    "room_id" : None
                }
            }
        })
        await self.get_list_room(sid)
    
    async def remove_user_id_socket_id(self, sid):
        try:
            self.list_user.pop(sid)
        except Exception as e:
            print("remove_user_id_socker_id", e)

    async def set_name_by_sid(self, sid, name):
        try:
            if self.list_user.get(sid):
                self.list_user[sid]['name'] = name
            await self.send_msg_to_sid('update-username', name, sid)
        except Exception as e:
            print("set_name_by_sid", e)

    async def get_username_by_sid(self, sid):
        if self.list_user:
            return self.list_user.get(sid).get("name")
##     
#### ROOM
##
    async def set_info_room_by_sid(self, sid, room_name, role):
        info_user = self.list_user.get(sid)
        if info_user:
            info_user['info_room'] = {
                    "role" : role,
                    "room_id" : room_name
                }
        else:
            print('không tồn tại')
            
     
##        
## info room
##
    async def get_list_room(self, sid):
        list_info =[]
        for key, value in self.list_room.items():
            list_info.append({
                "room name":key,
                "owner" : value.get("author").get("user"),
                "total" : value.get("total")
            })
        print("list_info", list_info)
        await self.send_msg_to_sid('list-room', list_info, sid)
     
##        
## in room
##
    async def client_create_room(self, sid, room_name):
        if self.list_room.get(room_name):
            print("room name exits")
            await self.send_msg_to_sid("notification-error", "Tên phòng đã tồn tại", sid)
            return
        else:
            self.list_room.update({
                room_name : {
                    "total" : 1,
                    "author" : {
                        "sid" : sid,
                        "user" : await self.get_username_by_sid(sid)
                    },
                    "list_sid" : {sid},
                    "lucky_number" :[],
                    "status" : "new"
                }
            })
            await self.set_info_room_by_sid(sid, room_name, 'owner')
            await self.send_msg_to_sid("client-join-room", {"role" : 'owner', 'room_id' : room_name}, sid)
            
        print("self.list_user", self.list_user)

            
    async def client_join_room(self, sid, room_name):
        is_exits_room = self.list_room.get(room_name)
        
        if not is_exits_room:
            print("Room name is not exits")
            return
        else:
            if is_exits_room.get("status") == "running":
                await self.send_msg_to_sid("notification", "Trò chơi đã bắt đầu !!!!", sid)
                return 
            print(100*"#")
            print("owner", is_exits_room.get('author').get("user"))
            print("room_name", room_name)
            new_list_sid = is_exits_room.get("list_sid", [])
            if is_exits_room.get('author').get('sid') == sid:
                print("You are owner room")
                return
            if sid in new_list_sid:
                print("You are already in this room")
                return
            new_list_sid.add(sid)
            is_exits_room.update({
                "total" : is_exits_room.get("total") + 1,
                "list_sid" : new_list_sid
            })
            await self.set_info_room_by_sid(sid, room_name, 'client')
            await self.send_msg_to_sid("client-join-room", {"role" : 'client', 'room_id' : room_name}, sid)
            await self.send_msg_to_sid("change-info-room", {"total": is_exits_room.get("total"), "list_user" : []}, is_exits_room.get("author", {}).get("sid"))

            
##        
## out room
##
    async def owner_out_room_new(self, sid, room_id):
        info_user = self.list_user.get(sid)
        if not info_user:
            print("user is not exits")
            return
        
        info_room  = self.list_room.get(room_id)
        if not info_room:
            print("room is not exits")
            return
        
        list_sid_player = deepcopy(info_room.get("list_sid"))
        self.list_room.pop(room_id)
        
        info_user['info_room'] = {
                "role" : None,
                "room_id" : None
            }
        for sid_in_list in list_sid_player:
            sid_info = self.list_user.get(sid_in_list)
            if sid_info:
                sid_info['info_room'] = {
                "role" : None,
                "room_id" : None
            }
        await self.send_msg_to_sid("out-room", {"status" : True, "message" : "out room thành công"}, sid)
        await self.send_msg_to_list_sid("out-room", {"status" : True, "message" : "chủ phòng đã out room"}, list_sid_player, sid)

        # print(self.list_user.get(new_owner_id))
        #assign room to random user

    async def check_user_out_room(self, sid):
        info = self.list_user.get(sid)
        if info:
            role = info.get("info_room").get('role')
            room_id = info.get("info_room").get('room_id')
            if role == 'owner':
                print('bạn là chủ phòng', sid)
                await self.owner_out_room(sid)
            elif role == 'client':
                print("bạn là khách", sid)
                await self.client_out_room(sid)
            else:
                print("eo co gi")
                
    async def owner_out_room(self, sid):
        info_user = self.list_user.get(sid)
        if not info_user:
            print("user is not exits")
            return
        
        room_id = info_user.get("info_room").get('room_id')
        info_room = self.list_room.get(room_id)
        if not info_room:
            print("room is not exits")
            return
            
        if len(info_room.get('list_sid')) == 1:
            #remove info room in user
            info_user['info_room'] = {
                    "role" : None,
                    "room_id" : None
                }
            #remove info user in room
            self.list_room.pop(room_id)
            await self.send_msg_to_sid("out-room",{"status" : True, "message" : "out room thành công"} , sid)
            print(f"xoá room {room_id} done")
        else:
            print('gán room')
            #remove info room in user
            info_user['info_room'] = {
                    "role" : None,
                    "room_id" : None
                }
            print("info_room.get('list_sid')", info_room.get('list_sid'))
            info_room["list_sid"].remove(sid)
            new_owner_id = next(iter(info_room.get('list_sid')))
            print("new_owner_id", new_owner_id)
            if new_owner_id:
                new_owner_name =  await self.get_username_by_sid(new_owner_id)
            
            info_room["total"] = info_room.get("total") - 1
            info_room["author"] = {"sid" : new_owner_id, "user" : new_owner_name}
            
            ## update info user
            await self.set_info_room_by_sid(new_owner_id, room_id, 'owner')
            await sio.emit("change-onwer", {"role" : 'owner', 'room_id' : room_id},to=new_owner_id)
            await self.send_msg_to_sid("out-room", {"status" : True, "message" : "out room thành công"}, sid)
            await self.send_msg_to_sid("change-info-room", {"total": info_room.get("total"), "list_user" : []}, info_room.get("author", {}).get("sid"))
            # print(self.list_user.get(new_owner_id))
            #assign room to random user
        
        print('owner out room done')

    async def client_out_room(self, sid):
        info_user = self.list_user.get(sid)
        if not info_user:
            print("user is not exits")
            return
        room_id = info_user.get("info_room").get('room_id')
        info_room = self.list_room.get(room_id)
        
        #remove info room in user
        info_user['info_room'] = {
                    "role" : None,
                    "room_id" : None
                }
        #remove info user in room
        info_room["list_sid"].remove(sid)
        info_room["total"] = info_room.get("total") - 1
        await self.send_msg_to_sid("change-info-room", {"total": info_room.get("total"), "list_user" : []}, info_room.get("author", {}).get("sid"))
        print('client out room done')
        
    async def bingo(self, sid ,lucky_range, room_id):
        print("lucky_range", lucky_range)
        print("room_id", room_id)
        print("inffo_room", self.list_room)
        info_room = self.list_room.get(str(room_id))
        print("inffo_room", info_room)
        winner = self.list_user.get(sid)
        print("winner", winner)
        await self.send_msg_to_list_sid('bingo', {"username" : winner.get("name"), "lucky_range" : lucky_range}, info_room.get("list_sid"))

    async def start_game(self, sid, countdown_time, room_id):
        info_room = self.list_room.get(room_id)
        info_room['status'] = 'running'
        await self.send_msg_to_list_sid('count-down', {"countdown_time" : countdown_time}, info_room.get("list_sid"))
        
    # async def start_game(self, sid, countdown_time, room_id):
    #     info_room = self.list_room.get(room_id)
    #     await self.send_msg_to_list_sid('count-down', {"countdown_time" : countdown_time}, info_room.get("list_sid"))
###
    async def send_lucky_number_to_user(self, sid, lucky_number, room_id):
        info_room = self.list_room.get(room_id)
        if info_room:
            if sid != info_room.get("author").get("sid"):
                print("bạn không phải chủ phòng")
                return
                
            info_room['lucky_number'].append(lucky_number)
        await self.send_msg_to_list_sid("lucky-range", [info_room.get("lucky_number")], list(info_room.get('list_sid')))
        print(info_room)
        # self.list_room.get(user_info.get("author").get("room_id")).get("lucky_number").append(lucky_number)
    
    async def reset_lucky_number(self, sid, room_id):
        info_room = self.list_room.get(room_id)
        if info_room:
            info_room['lucky_number'] = []
        await self.send_msg_to_list_sid("lucky-range", [], list(info_room.get('list_sid')))
        
    async def random_lucky_number_to_user(self, sid, room_id):
        info_room = self.list_room.get(room_id)
        if info_room:
            await self.send_msg_to_list_sid("random-lucky-number", True, list(info_room.get('list_sid')))
                
### send message
    async def send_msg_to_sid(self, msg_event , msg, sid):
        try:
            print('[send_msg_to_sid]: ', msg_event, sid)
            await sio.emit(msg_event, msg, sid)
        except Exception as e:
            print("send_msg_to_sid", e)


    async def send_msg_to_list_sid(self, msg_event, msg, list_sid = [], sid_onwer = None):
        try:
            if list_sid:
                for sid in list_sid:
                    if sid == sid_onwer:
                        continue
                    print('[send_msg_to_list_sid]: ', sid)
                    await sio.emit(msg_event, msg, sid)
        except Exception as e:
            print("Error send_msg_to_list_sid :", e)
        finally:
            pass
