from django.contrib.messages import get_messages

def get_serializable_messages(request):
    storage = get_messages(request)
    messages = []
    for message in storage:
        messages.append({
            'message': message.message,
            'level': message.level,
            'tags': message.tags,
            'extra_tags': message.extra_tags,
        })
    return messages
