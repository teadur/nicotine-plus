from pynicotine.pluginsystem import BasePlugin


def enable(plugins):
    global PLUGIN
    PLUGIN = Plugin(plugins)


def disable(plugins):
    global PLUGIN
    PLUGIN = None


class Plugin(BasePlugin):
    __name__ = "Anti-SHOUT"
    __version__ = "2008-11-18r00"
    __author__ = "quinox"
    __desc__ = """Tries to spot people shouting and converts their messages to a more polite form."""
    settings = {
        'maxscore': 0.6,
        'minlength': 10,
    }
    metasettings = {
        'maxratio': {
            'description': 'The maximum ratio capitals/noncapitals before fixing capitalization',
            'type': 'float', 'minimum': 0, 'maximum': 1, 'stepsize': 0.1},
        'minlength': {
            'description': 'Lines shorter than this never not be altered', 'type': 'integer',
            'minimum': 0},
    }

    def capitalize(self, text):
        # Dont alter words that look like protocol links (fe http://, ftp://)
        if text.find('://') > -1:
            return text
        return text.capitalize()

    def IncomingPrivateChatEvent(self, nick, line):
        return (nick, self.antishout(line))

    def IncomingPublicChatEvent(self, room, nick, line):
        return (room, nick, self.antishout(line))

    def antishout(self, line):
        lowers = len([x for x in line if x.islower()])
        uppers = len([x for x in line if x.isupper()])
        score = -2  # unknown state (could be: no letters at all)
        if uppers > 0:
            score = -1  # We have at least some upper letters
        if lowers > 0:
            score = uppers / float(lowers)
        newline = line
        if len(line) > self.settings['minlength'] and (score == -1 or score > self.settings['maxscore']):
            newline = '. '.join([self.capitalize(x) for x in line.split('. ')])
        if newline == line:
            return newline
        else:
            return newline + " [as]"
