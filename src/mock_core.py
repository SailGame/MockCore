import os, sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir + "/protos")

from concurrent import futures

import grpc
import core.error_pb2 as error
import core.provider_pb2 as provider
import uno.uno_pb2 as uno
import core.core_pb2_grpc

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
                ret = provider.RegisterRet()
                ret.err = error.OK

                msg = provider.ProviderMsg()
                msg.sequenceId = seqId + 1
                msg.registerRet.CopyFrom(ret)
                print("msg sent, type = {}".format(msg.WhichOneof("Msg")))
                yield msg

                settings = uno.StartGameSettings()
                settings.isDraw2Consumed = True
                settings.canSkipRespond = True
                settings.hasWildSwapHandsCard = False
                settings.canDoubtDraw4 = False
                settings.roundTime = 15

                args = provider.StartGameArgs()
                args.roomId = 1205
                args.userId.append(1)
                args.userId.append(2)
                args.userId.append(3)
                args.custom.Pack(settings)

                msg.sequenceId = seqId + 2
                msg.startGameArgs.CopyFrom(args)
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