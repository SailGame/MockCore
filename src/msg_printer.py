import core.error_pb2 as error
import core.provider_pb2 as provider
import uno.uno_pb2 as uno
import util

def print_provider_msg(msg):
    print("ProviderMsg Received, seqId: {}, type: {}".format(
        msg.sequenceId, msg.WhichOneof("Msg")
    ))

def print_register_args(args):
    print("  RegisterArgs Received, id: {}, name: {}, maxUsers: {}, minUsers: {}".format(
        args.id, args.gameName, args.gameSetting.maxUsers, args.gameSetting.minUsers
    ))

def print_notify_msg_args(_args):
    args = provider.NotifyMsgArgs()
    args.CopyFrom(_args)
    print("  NotifyMsgArgs Received, err: {}, roomId: {}, userId: {}, type: {}".format(
        args.err, args.roomId, args.userId,
        util.unpack_to_notify_msg(args.custom).WhichOneof("Msg")
    ))

def print_game_start(game_start):
    print("    GameStart Received, initHandcards: {}, flippedCard: {}, firstPlayerId: {}"
        .format(util.convert_cardlist_to_str(game_start.initHandcards),
            util.convert_card_to_str(game_start.flippedCard),
            game_start.firstPlayerId
    ))

def print_draw(draw):
    print("    Draw Received, number: {}".format(draw.number))

def print_skip(skip):
    print("    Skip Received")

def print_play(play):
    print("    Play Received, card: {}, nextColor: {}".format(
        util.convert_card_to_str(play.card), play.nextColor
    ))

def print_draw_rsp(draw_rsp):
    print("    DrawRsp Received, cards: {}".format(
        util.convert_cardlist_to_str(draw_rsp.cards)
    ))