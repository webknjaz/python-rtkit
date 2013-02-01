from rtkit.resource import RTResource
from entities import *


class Tracker(RTResource):
    """Tracker Object"""
    def __init__(self, url, username, password, auth, language='en'):
        super(Tracker, self).__init__(url, username, password, auth)
        self.user = self.get_user(auth.username)
        self.language = self.user.language or language

    def get_user(self, value):
        """:return: An instance of :py:class:`rtkit.entities.User`"""
        return self._get_entity(User, value)

    def get_queue(self, value):
        """:return: An instance of :py:class:`rtkit.entities.Queue`"""
        return self._get_entity(Queue, value)

    def get_ticket(self, value):
        """:return: An instance of :py:class:`rtkit.entities.Ticket`"""
        return self._get_entity(Ticket, value)

    def search_tickets(self, query, order):
        """Search tickets
        
           .. warning:: Not yet Implemented
        """
        raise NotImplementedError

    def create_ticket(self, content, attachments=None):
        """Create a ticket
        
           .. warning:: Not yet Implemented
        """
        raise NotImplementedError

    def comment_ticket(self, content, attachments=None):
        """Comment on Ticket
        
           .. warning:: Not yet Implemented
        """
        raise NotImplementedError

    def get_attachment(self, ticket_id, value):
        """:return: An instance of :py:class:`rtkit.entities.Attachment`"""
        return self._get_subentity(Ticket, ticket_id, Attachment, value)

    def get_history(self, ticket_id, value=None, format='l'):
        """:return: An instance of :py:class:`rtkit.entities.History`"""
        return self._get_subentity(Ticket, ticket_id, History, value, format)

    def get_links(self, ticket_id):
        """:return: An instance of :py:class:`rtkit.entities.Links`"""
        return self._get_subentity(Ticket, ticket_id, Links)

    def change_links(self, ticket_id, content):
        """Change Links
        
           .. warning:: Not yet Implemented
        """
        raise NotImplementedError

    def _get_entity(self, Entity, value):
        r = self.get(path='{0}/{1}'.format(Entity.api(), value))
        return Entity(**dict(r.parsed[0]))

    def _get_subentity(self, Entity, e_value, SubEntity, s_value, format=None):
        path = '{0}/{1}/{2}/{3}'.format(Entity.api(), e_value, SubEntity.api(), s_value)
        if format:
            path += '?{0}'.format(format)
        r = self.get(path=path)
        return SubEntity(**dict(r.parsed[0]))
