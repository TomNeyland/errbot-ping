from errbot import BotPlugin, botcmd
from errbot.builtins.webserver import webhook
from collections import defaultdict


class Ping(BotPlugin):

    """A Ping Group function for Err"""
    min_err_version = '1.6.0'  # Optional, but recommended
    # max_err_version = '3.0.0'  # Optional, but recommended

    presences = defaultdict(dict)

    def callback_presence(self, presence):

        presences = self.presences

        if presence.chatroom:
            room = presence.chatroom.node
            user = presence.nick
            status = presence.status

            if status == 'online':
                presences[room][user] = presence
            elif user in presences[room]:
                del presences[room][user]

    @botcmd
    def ping_all(self, mess, args):

        room = mess.getFrom().getNode()
        usernames = sorted(self.presences[room].keys())

        return " ".join(usernames)

    @botcmd(split_args_with="||")
    def ping_set(self, mess, args):
        """Create/Update a group."""

        group_str = str(args[0])
        group_tuple = group_str.split(" ", 1)

        if len(group_tuple) > 1:
            group, text = group_tuple
            group = group.lower()

            old_value = self[group]
            self[group] = text
            if old_value:
                return "Updated group '%s', previous value was: %s" % (group, old_value,)
            else:
                return "Created group '%s'." % (group,)
        else:
            group = group_tuple[0]
            group = group.lower()
            if group in self.keys():
                del self[group]
                return "Deleted group %s" % group

    @botcmd(split_args_with=' ')
    def ping_add(self, mess, args):
        """Append something to a ping group"""

        if len(args) > 1:
            group = str(args[0]).lower()
            message = self[group] or ""
            message = message + " " + " ".join(args[1:])
            self[group] = message
            return "Done."

    @botcmd(split_args_with=' ')
    def ping_remove(self, mess, args):
        """Remove something from a ping group"""

        if len(args) > 1:
            group = str(args[0]).lower()
            message = self[group] or ""
            term = " ".join(args[1:])
            self[group] = message.replace(term, "")
            return "Done."

    @botcmd(split_args_with=None)
    def ping(self, mess, args):
        """Ping a specified group"""

        group = str(args[0])
        group = group.lower()

        group_text = self[group]

        if group_text != None:
            return group_text
        else:
            return "No such group, valid groups are: %s" % (", ".join(sorted(self.keys())),)

    @botcmd(split_args_with=None)
    def ping_groups(self, mess, args):
        """Show the groups that can be pinged"""

        groups = self.keys()

        return ", ".join(sorted(groups))

    def __getitem__(self, key):
        try:
            return super(Ping, self).__getitem__(key)
        except KeyError:
            return None
