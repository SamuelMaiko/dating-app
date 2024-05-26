from chatapp.models import Block

def can_view_profile(viewer, profile_owner):
    return not Block.objects.filter(blocker=profile_owner, blocked=viewer).exists()
