# 关于图片(Image)

图片在以富文本为消息载体的 QQ 上漫天飞舞的传递着丰富的信息,
而 Graia Framework 基于 mirai-api-http 提供了灵活且易于使用的各式关于图片的接口和封装,
并根据其特点对原有 API 的局限性加以改进, 使得图片的发送和接受基本上都达到了无障碍的级别.

## 认识 Image

`Image` 为一继承了 `InternalElement`, 可作为消息组件的类实现;
你可以从模块 `graia.application.message.elements.internal` 处导入该类.

一般的, 你需要获得 `Image` 实例才能将该实例中的图片发送到目标区域,
而实例化 `Image` 则需要 `imageId`, `url`, `path` 中的任意一个,
但如果使用这种方式, Graia Framework 将无法保证你的消息发出后是否能为 `mirai-api-http` 正确处理并正常工作,
所以我们提供了几个工厂函数(Factory), 以此保证你的发送行为可以被正确处理,
并保护无头客户端处不会发生意料之外的错误.

## 通过本地文件路径发送图片

你只需要使用 `Image.fromLocalFile` 类方法即可:

``` python
from pathlib import Path

MessageChain.create([
    Image.fromLocalFile("./images/num1.jpg"), # 你可以使用字符串表示文件路径.
    Image.fromLocalFile(Path("./images/num2.jpg")) # 你也可以手动传入 pathlib.Path 实例.
])
```

?> **提示**: 我们也实现了一个**不保证发送安全性**的方法 `Image.fromUnsafePath`,
这个方法不保证发送安全性和可靠性.

## 通过不安全的 bytes 发送图片

!> **注意**: Graia Framework 不保证你传入的 bytes 作为图片的有效性.

你需要使用 `Image.fromUnsafeBytes` 方法:

``` python
from pathlib import Path

...
image_bytes = response.read()
...

MessageChain.create([
    Image.fromUnsafeBytes(image_bytes)
])
```

## 获取作为 bytes 的已有图片

调用 `Image.http_to_bytes` 方法即可:

?> **注意**: 该方法需保证 `Image.url` 非空才能获取.

``` python
image_bytes: bytes = await image.http_to_bytes()
```