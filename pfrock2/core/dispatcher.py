#!/usr/bin/env python
# coding=utf8
from pfrock2.core import logger
from pfrock2.plugins.handler.parser import HandlerParser
from pfrock2.plugins.proxy.parser import ProxyHandlerParser
from pfrock2.plugins.static.parser import StaticHandlerParser

HANDLER_MAP = {
    'pfrock-proxy': ProxyHandlerParser.do,
    'pfrock-static': StaticHandlerParser.do,
    'other': HandlerParser.do
}


class HandlerDispatcher(object):
    @classmethod
    def get_handlers(cls, config_server):
        routes = config_server.routes

        handler_list = []
        for route in routes:

            def add_handler(handler):
                logger.debug("add : " + str(handler))
                handler_list.append(handler)

            if route.handler in HANDLER_MAP:
                handlers = HANDLER_MAP[route.handler](route.path, route.options)

                if type(handlers) == list:
                    for handler in handlers:
                        add_handler(handler)
                else:
                    add_handler(handlers)
            else:
                handler = HANDLER_MAP['other'](route.path, route.handler, route.options)
                add_handler(handler)

        return handler_list
