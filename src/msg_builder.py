import core.error_pb2 as error
import core.provider_pb2 as provider
import uno.uno_pb2 as uno

def create_register_ret(seqId, err):
    ret = provider.RegisterRet()
    ret.err = err

    msg = provider.ProviderMsg()
    msg.sequenceId = seqId
    msg.registerRet.CopyFrom(ret)
    return msg

def create_start_game_args(seqId, roomId, userIds, custom):
    args = provider.StartGameArgs()
    args.roomId = roomId
    args.userId.extend(userIds)
    args.custom.Pack(custom)

    msg = provider.ProviderMsg()
    msg.sequenceId = seqId
    msg.startGameArgs.CopyFrom(args)
    return msg

def create_start_game_settings(isDraw2Consumed, canSkipRespond,
    hasWildSwapHandsCard, canDoubtDraw4, roundTime):
    settings = uno.StartGameSettings()
    settings.isDraw2Consumed = isDraw2Consumed
    settings.canSkipRespond = canSkipRespond
    settings.hasWildSwapHandsCard = hasWildSwapHandsCard
    settings.canDoubtDraw4 = canDoubtDraw4
    settings.roundTime = roundTime
    return settings

def create_user_operation_args(seqId, roomId, userId, custom):
    args = provider.UserOperationArgs()
    args.roomId = roomId
    args.userId = userId
    args.custom.Pack(custom)

    msg = provider.ProviderMsg()
    msg.sequenceId = seqId
    msg.userOperationArgs.CopyFrom(args)
    return msg

def create_draw(number):
    draw = uno.Draw()
    draw.number = number

    ret = uno.UserOperation()
    ret.draw.CopyFrom(draw)
    return ret

def create_skip():
    skip = uno.Skip()
    ret = uno.UserOperation()
    ret.skip.CopyFrom(skip)
    return ret

def create_play(card, nextColor):
    play = uno.Play()
    play.card.CopyFrom(card)
    play.nextColor = nextColor
    
    ret = uno.UserOperation()
    ret.play.CopyFrom(play)
    return ret

def create_card(color, text):
    card = uno.Card()
    uno.color = color
    uno.text = text
    return card