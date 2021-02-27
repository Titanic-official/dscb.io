"""Creativity on point :O"""
class MissingArgument(Exception):

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

class BadArgument(Exception):

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

class HttpExcpetion(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

class NotFound(Exception):

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message






