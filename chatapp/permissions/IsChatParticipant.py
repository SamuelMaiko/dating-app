from rest_framework import permissions

class IsChatParticipant(permissions.BasePermission):
    """
    Custom permission to only allow participants of a chat to perform certain actions.
    """

    def has_object_permission(self, request, view, obj):
        """
        Check if the requesting user is a participant of the chat.
        """
        # Assuming the user is authenticated and the chat object has a participants field
        return request.user in obj.participants.all()
