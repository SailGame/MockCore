import os, sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir + "/protos")

from concurrent import futures

import grpc
import core.error_pb2 as error
import core.provider_pb2 as provider
import uno.uno_pb2 as uno
import core.core_pb2_grpc
import msg_builder as builder

class GameCoreServicer(core.core_pb2_grpc.GameCoreServicer):

    def __init__(self):
        pass

    def Provider(self, request_iterator, context):
        for new_provider_msg in request_iterator:
            seqId = new_provider_msg.sequenceId
            msg_type = new_provider_msg.WhichOneof("Msg")

            if msg_type == "registerArgs":
                args = new_provider_msg.registerArgs
                print("RegisterArgs Received, id: {}, name: {}, maxUsers: {}, minUsers: {}".format(
                    args.id, args.gameName, args.gameSetting.maxUsers, args.gameSetting.minUsers
                ))

                msg = builder.create_register_ret(seqId + 1, error.OK)
                print("msg sent, type = {}".format(msg.WhichOneof("Msg")))
                yield msg

                msg = builder.create_start_game_args(seqId + 2, 1205, [1, 2, 3],
                    builder.create_start_game_settings(True, True, False, False, 15))
                print("msg sent, type = {}".format(msg.WhichOneof("Msg")))
                yield msg
                
            elif msg_type == "notifyMsgArgs":
                
                pass
            else:
                assert False

    
if __name__ == "__main__":
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    core.core_pb2_grpc.add_GameCoreServicer_to_server(
        GameCoreServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()