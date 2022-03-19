# 此仓库已废弃, 请使用替代品 [Ariadne](https://github.com/GraiaProject/Ariadne); 本项目被标记为 `v4`, 相对的有 `v4+`(Ariadne) 与 `v5`(WIP, 尚未完工), 目前我推荐使用 Ariadne.

# Graia Application for mirai-api-http

当前最新版本: ![PyPI](https://img.shields.io/pypi/v/graia-application-mirai)  
所需求的最低 CPython 版本: ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/graia-application-mirai)  
已确认可以在其上运行的 Python 实现: ![PyPI - Implementation](https://img.shields.io/pypi/implementation/graia-application-mirai)

### 开始使用

文档地址: https://graia-document.vercel.app/  
API 文档地址(使用 `pdoc` 生成): https://graiaproject.github.io/Application/graia/application/index.html

Tencent QQ 交流群: [邀请链接](https://jq.qq.com/?_wv=1027&k=VXp6plBD)  
Discussion: https://github.com/GraiaProject/Application/discussions

#### 从 Pypi 安装
``` bash
pip install graia-application-mirai
# 或使用 poetry
poetry add graia-application-mirai
```

#### 从 Github 安装
``` bash
pip install poetry
git clone https://github.com/GraiaProject/Application graia-app
cd graia-app
poetry install
```

### 作出贡献
`Graia Framework` 欢迎一切形式上的贡献(包括但不限于 `Issues`, `Pull Requests`, `Good Idea` 等)  
我们希望能有更多优秀的开发者加入到对项目的贡献上来. 你的 `Star` 是对我们最大的支持和鼓励.  

我们在[这里](https://github.com/GraiaProject/Application/blob/master/CONTRIBUTING.md)写了你在贡献本项目及
`Graia Project` 时所可能需要注意的事项.

因为历史原因, 我们的文档, 即 [Graia Document](https://github.com/GreyElaina/GraiaDocument) 目前急需改进和完善,
如果有意愿, 欢迎提起 Pull Request.

若你在使用的过程中遇到了问题, 欢迎[提出聪明的问题](https://github.com/ryanhanwu/How-To-Ask-Questions-The-Smart-Way/blob/master/README-zh_CN.md), 也请不要[使用糟糕的方式提问](https://github.com/tangx/Stop-Ask-Questions-The-Stupid-Ways), 我们希望有人能让这个项目变得更好.  

若在使用时发现了本项目的问题, 先检查文档中是否有提及这一情况,
若没有, 你可以在我们的[问题追踪器](https://github.com/GraiaProject/Application/issues)处提出问题,
我们会尽快解决你发现的问题.

你也可以通过 Discussion/QQ 群等方式获取帮助，现在我们更推荐使用 [Discussion](https://github.com/GraiaProject/Application/discussions).

**若使用中发现了并非本项目导致的问题, 请先向其他项目汇报问题, 当然, 记得通知我.**

### 鸣谢&相关项目
> 这些项目也很棒, 去他们的项目页看看, 点个 `Star` 以鼓励他们的开发工作, 毕竟没有他们也没有 `Graia Framework`.

特别感谢 [`mamoe`](https://github.com/mamoe) 给我们带来这些精彩的项目:
 - [`mirai`](https://github.com/mamoe/mirai): 即 `mirai-core`, 一个高性能, 高可扩展性的 QQ 协议库
 - [`mirai-console`](https://github.com/mamoe/mirai-console): 一个基于 `mirai` 开发的插件式可扩展开发平台
 - [`mirai-api-http`](https://github.com/project-mirai/mirai-api-http): 为本项目提供与 `mirai` 交互方式的 `mirai-console` 插件

`Graia Application` 基于以下独立 `Graia Project` 项目实现:
 - [`Broadcast Control`](https://github.com/GraiaProject/BroadcastControl): 扩展性强大, 模块间低耦合, 高灵活性的事件系统支持

`Graia Application` 同样还关联了其他 `Graia Project` 项目:
 - [`Components`](https://github.com/GraiaProject/Components): 简单的消息链元素选择器
 - [`Template`](https://github.com/GraiaProject/Template): 消息模板
 - [`Saya`](https://github.com/GraiaProject/Saya) 为该项目提供了间接但简洁的模块管理系统. [文档](https://graia-document.vercel.app/docs/saya/saya-index)
   - 关于 `Saya`: 这是一个全新的系统, 包含的潜力不亚于 `Application`, 并且实现了更方便的面向模块的 API, 但如果你需要应用到 `Application` 上, 则仍需要先学习相关的内容.

若有相关需求, 我们也强烈建议配合以下独立 `Graia Project` 项目使用:
 - [`Scheduler`](https://github.com/GraiaProject/Scheduler): 简洁的基于 `asyncio` 的定时任务实现.
 
作为学习目的, 主要维护者 `GreyElaina` 以个人名义重新以 `AGPL-3.0` 开源了 `python-mirai`, 即 `Graia Application` 的前身, 希望能为社区的发展助力:
 - [`python-mirai`](https://github.com/GreyElaina/python-mirai): 接口简洁, 支持 `mirai-api-http` 约 `v1.6.x` 版本. 一切的开始.

也感谢所有基于本项目开发的各位开发者, 请积极向上游项目反馈问题.

### 许可证
我们使用 [`GNU AGPLv3`](https://choosealicense.com/licenses/agpl-3.0/) 作为本项目的开源许可证.
