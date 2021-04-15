Module graia.application.message.parser.literature
==================================================

Classes
-------

`Literature(*prefixs, arguments: Dict[str, graia.application.message.parser.pattern.ParamPattern] = None, allow_quote: bool = False, skip_one_at_in_quote: bool = False)`
:   旅途的浪漫

    ### Ancestors (in MRO)

    * graia.broadcast.entities.dispatcher.BaseDispatcher

    ### Class variables

    `allow_quote: bool`
    :

    `always`
    :

    `arguments: Dict[str, graia.application.message.parser.pattern.ParamPattern]`
    :

    `prefixs: Tuple[str]`
    :

    `skip_one_at_in_quote: bool`
    :

    ### Methods

    `gen_long_map(self)`
    :

    `gen_long_map_with_bar(self)`
    :

    `gen_short_map(self)`
    :

    `gen_short_map_with_bar(self)`
    :

    `parse_message(self, message_chain: graia.application.message.chain.MessageChain)`
    :

    `prefix_match(self, target_chain: graia.application.message.chain.MessageChain)`
    :

    `trans_to_map(self, message_chain: graia.application.message.chain.MessageChain)`
    :