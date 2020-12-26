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
                draw = msg.draw
                printer.print_draw(draw)
            elif msg_type == "skip":
                skip = msg.skip
                printer.print_skip(skip)
            elif msg_type == "play":
                play = msg.play
                printer.print_play(play)
            elif msg_type == "drawRsp":
                draw_rsp = msg.drawRsp
                printer.print_draw_rsp(draw_rsp)
            else:
                assert False

        else:
            assert False