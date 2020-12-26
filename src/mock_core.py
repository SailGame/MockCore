import os, sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir + "/protos")

from concurrent import futures
import threading

import grpc
import core.error_pb2 as error
import core.provider_pb2 as provider
import uno.uno_pb2 as uno
import core.core_pb2_grpc
import msg_builder as builder
import msg_printer as printer
import util

def listen_to_provider(request_iterator):
    for new_provider_msg in request_iterator:
        printer.print_provider_msg(new_provider_msg)

        seqId = new_provider_msg.sequenceId
        msg_type = new_provider_msg.WhichOneof("Msg")

        if msg_type == "registerArgs":
            args = new_provider_msg.registerArgs
            printer.print_register_args(args)

        elif msg_type == "notifyMsgArgs":
            args = new_provider_msg.notifyMsgArgs
            printer.print_notify_msg_args(args)

            msg = util.unpack_to_notify_msg(args.custom)
            msg_type = msg.WhichOneof("Msg")

            if msg_type == "gameStart":
                game_start = msg.gameStart
                printer.print_game_start(game_start)
            elif msg_type == "draw":
                pass

        else:
            assert False

class GameCoreServicer(core.core_pb2_grpc.GameCoreServicer):

    def Provider(self, request_iterator, context):
        thread = threading.Thread(target=listen_to_provider, args=(request_iterator,))
        thread.start()

        while True:
            args = list(map(int, input().split()))
            if args[0] == 0:
                msg = builder.create_register_ret(1, error.OK)
                print("msg sent, type = {}".format(msg.WhichOneof("Msg")))
                yield msg

                msg = builder.create_start_game_args(2, 1205, [11, 22, 33],
                    builder.create_start_game_settings(True, True, False, False, 15))
                print("msg sent, type = {}".format(msg.WhichOneof("Msg")))
                yield msg

            elif args[0] == 1:
                room_id, user_id, number = args[1:4]
                msg = builder.create_user_operation_args(0, room_id, user_id,
                    builder.create_draw(number))
                yield msg

    
if __name__ == "__main__":
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    core.core_pb2_grpc.add_GameCoreServicer_to_server(
        GameCoreServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()