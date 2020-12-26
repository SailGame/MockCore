import uno.uno_pb2 as uno

def unpack_to_notify_msg(any_message):
    msg = uno.NotifyMsg()
    any_message.Unpack(msg)
    return msg

def convert_card_to_str(card):
    ret = ''
    if card.color == uno.RED:
        ret += 'R'
    elif card.color == uno.YELLOW:
        ret += 'Y'
    elif card.color == uno.GREEN:
        ret += 'G'
    elif card.color == uno.BLUE:
        ret += 'B'
    
    if card.text == uno.SKIP:
        ret += 'S'
    elif card.text == uno.REVERSE:
        ret += 'R'
    elif card.text == uno.DRAW_TWO:
        ret += '+2'
    elif card.text == uno.WILD:
        ret += 'W'
    elif card.text == uno.DRAW_FOUR:
        ret += '+4'
    else:
        ret += str(card.text)

    return ret

def convert_cardlist_to_str(cards):
    ret = '['
    for card in cards:
        ret += convert_card_to_str(card)
        ret += ', '
    ret = ret[:-2] + ']'
    return ret
    