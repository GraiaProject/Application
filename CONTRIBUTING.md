# Contributing for Graia Application

**在此为所有向 `Graia Project` 作出贡献, 为社区添砖加瓦的每位开发者/使用者表示衷心的感谢, 你们的支持就是我们开发的动力.**

`Graia Project` 下所有项目都欢迎任何环抱开源精神的贡献者.
而本文档则提到了我们能想到的在贡献本项目时你应该/不应该做的事.

你可以通过以下方式向本项目 `Graia Application` 作出贡献:

 - 协助寻找 BUG 
 - 协助修复已发现的/潜在的 BUG
 - 为本项目开发新特性/功能(请先通过 Github Issue 向我们提出建议 ~~然后我们可能会推出官方的方案~~ )
 - 添加非必要的功能支持
 - 修改异常的代码行为
 - 在 Github Issue 里写关于某个文档尚未提到的特性的使用方法探索
 - 帮助撰写 [GraiaDocument](https://github.com/GreyElaina/GraiaDocument)

以下是我能想到的注意事项:

 - 能用 `is` 就用 `is`, 但注意引用地址, Python 的小整数池, `str` 的 immutable 等问题(通常情况下我们会协助和指导你进行修改)
 - 尽量的使用已有的库(例如使用 `regex` 代替标准库中的 `re`, 以获取更好的性能)
 - 尽量别引入新的库
 - 不严格要求代码风格, 但请别写的太烂.
 - 如果需要测试文件, 可以通过创建 `src/test.py`, 这个文件已经被标记为无需被 git 跟踪
 - 最好是所有声明的变量都加上类型注解, 不加也行, 但最好.
 - 使用 `poetry` 管理环境
 - 别修改 `setup.py`, 使用 `poetry`
 - 修改一项东西的名称时, 务必三思(包括但不限于类名, 方法名, 函数名, 参数名等)
 - 如果涉及到修改有关 `mirai-api-http` 交互的部分, 请先测试下, 并在 PR 里标出你所使用的版本
 - 看不懂的东西请别改...
 - `docstring` 都是用的 Google Style, 当然, 如果能帮忙改成 jsdoc 样式的也行, 那样就可以直接生成了~~坐等PR~~
 - 类名使用 `PascalCase`, 单词首字母全大写; 方法名用 `camelCase`, 除第一个单词外的所有单词首字母大写; 文档里提到某种东西
    请别使用缩写, 用 `` ` `` 框起来, 然后如果有 `kebab-case` 的名称优先用; 可以用 markdown.
 - 需要添加一个实用函数请在 `graia.application.utilles` 这个模块下面加