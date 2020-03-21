from pynicotine.pluginsystem import BasePlugin
from pynicotine.pluginsystem import returncode


def enable(frame):
    global PLUGIN
    PLUGIN = Plugin(frame)


def disable(frame):
    global PLUGIN
    PLUGIN = None


class Plugin(BasePlugin):
    __name__ = "Spamfilter"
    settings = {
        'minlength': 200,
        'maxlength': 400,
        'maxdiffcharacters': 10,
        'badprivatephrases': ['buy viagra now', 'mybrute.com', 'mybrute.es', '0daymusic.biz']
    }
    metasettings = {
        'minlength': {"description": 'The minimum length of a line before it\'s considered as ASCII spam', 'type': 'integer'},
        'maxdiffcharacters': {"description": 'The maximum number of different characters that is still considered ASCII spam', 'type': 'integer'},
        'maxlength': {"description": 'The maximum length of a line before it\'s considered as spam.', 'type': 'integer'},
        'badprivatephrases': {"description": 'Things people send you in private that is spam.', 'type': 'list string'},
    }

    def LoadNotification(self):
        self.log('A line should be at least %s long with a maximum of %s different characters before it\'s considered ASCII spam.' % (self.settings['minlength'], self.settings['maxdiffcharacters']))

    def IncomingPublicChatEvent(self, room, user, line):
        if len(line) >= self.settings['minlength'] and len(set(line)) < self.settings['maxdiffcharacters']:
            self.log('Filtered ASCII spam from "%s" in room "%s"' % (user, room))
            return returncode['zap']
        if len(line) > self.settings['maxlength']:
            self.log('Filtered really long line (%s characters) from "%s" in room "%s"' % (len(line), user, room))
            return returncode['zap']

    def IncomingPrivateChatEvent(self, user, line):
        for phrase in self.settings['badprivatephrases']:
            if line.lower().find(phrase) > -1:
                self.log("Blocked spam from %s: %s" % (user, line))
                return returncode['zap']
