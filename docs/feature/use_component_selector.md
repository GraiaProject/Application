# 使用 Component Selector(消息元素选择器)

有时候, 对 MessageChain 的处理实在是太过枯燥, 因为不能直接正则, 导致处理起来相当麻烦...  
这就是为什么我们提供了 `Component Selector` 的原因.

## 安装

!> **注意** 由于本特性使用了较高 Python 版本中的特性, 所以如果想使用本特性,
请确保你的 Python 版本在 `3.7` 及以上!

该机制并不内置于 Graia Application for Mirai 中,
所以你需要通过你的包管理器获取:

``` bash
pip install graia-component-selector
# 使用 poetry
poetry add graia-component-selector
```

## 使用
当你顺利安装了库后, 你就可以导入并使用了:

``` python
from graia.component import Components
```

在这里, `Components` 是一个 `Decorater`(参数修饰器),
`Decorater` 可以放置于参数定义中的 `default`, 同样用于为函数体内部提供特定的值,
唯一不同的是, `Decorater` 可以先获取到 `Dispatcher` 解析得出的值,
然后对其进行更改和调整.

你需要使用以下格式使用 `Components`:

``` python
def xxx(a: MessageChain = Components[____:____:____])
                                     ^^^^ ^^^^ ^^^^
                                     $Type Num $Skip
```

`Components` 使最后可被获取到的参数成为 `MessageChain[List, $Type]`,
且使该参数所指向的消息链仅包含特定类型的消息元素(即 `$Type`).

 - `$Type` 可以为一个单独的 `Type[InternalElement | ExternalElement]`,
也可以是 `Sequence[Type[InternalElement | ExternalElement]]`.
 - `$Num` 表示函数体中最大能访问到特定元素的次数.
 - `$Skip` 表示跳过特定元素的次数.