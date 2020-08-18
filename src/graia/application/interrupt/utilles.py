from typing import Callable
from . import Interrupt
from graia.broadcast import BaseEvent
from functools import partial

def interrupt_creator(direct: BaseEvent, block_propagation: bool = False, *args, **kwargs) -> Callable[[Callable], Interrupt]:
    """本函数通过装饰器, 将你自己定义的任意 `Callable` 作为 触发器(`trigger`) 并包装为一个中断定义(`Interrupt`),
    并通过 `InterruptControl.wait` 协程方法使用.

    Args:
        direct (BaseEvent): 你的中断要监听的事件.
        block_propagation (bool, optional): 在触发器执行成功, 中断被释放后是否阻止这之后的事件传递. 默认为 False.

    Returns:
        Callable[[Callable], Interrupt]: 返回的闭包, 用于装饰器.
    """
    def wrapper(any_callable: Callable):
        class InlineInterrupt(Interrupt):
            direct = direct
            _block_propagation = block_propagation
            trigger = partial(any_callable, *args, **kwargs)
        return InlineInterrupt()
    return wrapper