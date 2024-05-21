from rest_framework import permissions

class IsMessageParticipant(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user in obj.chat.participants.all()
