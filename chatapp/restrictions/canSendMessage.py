from chatapp.models import Block

def can_send_message(sender, receiver):
    return not Block.objects.filter(blocker=receiver, blocked=sender).exists()
