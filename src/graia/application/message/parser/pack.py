import copy
from typing import List, Sequence, Union
from .signature import FullMatch, PatternReceiver


class Arguments:
    content: List[PatternReceiver]

    @property
    def isGreed(self) -> bool:
        return any([i.isGreed for i in self.content])

    def __init__(self, content: List[PatternReceiver]) -> None:
        self.content = content

    def __repr__(self) -> str:
        return "<Argument content={0}>".format(str(self.content))


def merge_signature_chain_fullmatch(
    chain: Sequence[Union[FullMatch, PatternReceiver]]
) -> Sequence[Union[Arguments, FullMatch]]:
    result = []

    temp_l1 = []

    for i in chain:
        if isinstance(i, FullMatch):
            temp_l1.append(i.pattern)
        else:
            if temp_l1:
                result.append(FullMatch("".join(temp_l1)))
                temp_l1.clear()
            result.append(i)
    else:
        if temp_l1:
            result.append(FullMatch("".join(temp_l1)))
            temp_l1.clear()

    return type(chain)(result)


def merge_signature_chain(
    chain: Sequence[Union[FullMatch, PatternReceiver]]
) -> Sequence[Union[Arguments, FullMatch]]:
    chain = merge_signature_chain_fullmatch(chain)
    result = []
    temp_l1 = []

    for i in chain:
        if isinstance(i, PatternReceiver):
            temp_l1.append(i)
        else:
            if temp_l1:
                result.append(Arguments(temp_l1))
                temp_l1 = []
            result.append(i)
    else:
        if temp_l1:
            result.append(Arguments(temp_l1))
            temp_l1 = []

    return type(chain)(result)
