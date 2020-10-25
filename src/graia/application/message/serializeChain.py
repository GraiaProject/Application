"把消息链转化成mirai码，为了保证可逆，纯文本中'['用'[['代替"

from graia.application.entry import MessageChain, Source, Plain, AtAll, At, Face, Image, FlashImage
import re


def serializeChain(chain: MessageChain) -> str:
    result = []
    for m in chain.__root__:
        if isinstance(m, Plain):
            result.append(m.asSerializationString().replace('[', '[['))
        else:
            result.append(m.asSerializationString())
    return ''.join(result)


PARSE_FUNCTIONS = {
    'atall': lambda args: AtAll(),
    'source': lambda args: Source(id=args[0], time=args[1]),
    'at': lambda args: At(target=args[0], display=args[1]),
    'face': lambda args: Face(faceId=args[0]),
    'image': lambda args: Image(imageId=args[0]),
    'flash': lambda args: FlashImage(imageId=args[0]),
}


def deserializeChain(raw: str) -> MessageChain:
    result = []
    matches = re.split(r'(\[mirai:.+?\])', raw)
    i = 0
    length = len(matches)
    while i < length:
        m = re.fullmatch(r'\[mirai:(.+?)(:(.+?))\]', matches[i])
        if m:
            # 容错：参数数量太少不行，太多可以
            args = m.group(3).split(',')
            result.append(PARSE_FUNCTIONS[m.group(1)](args))
        elif matches[i]:
            trailing = re.search(r'\[*$', matches[i]).group(0)
            if len(trailing) % 2 != 0:
                # 下一串匹配原文就是"[mirai:...]"
                result.append(
                    Plain((matches[i]+matches[i+1]).replace('[[', '[')))
                i += 1
            else:
                result.append(Plain(matches[i].replace('[[', '[')))
        i += 1
    return MessageChain.create(result)
