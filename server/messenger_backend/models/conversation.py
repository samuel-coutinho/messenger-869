from django.db import models
from django.db.models import Q

from . import utils
from .user import User

class Conversation(utils.CustomModel):

    users = models.ManyToManyField(User)

    createdAt = models.DateTimeField(auto_now_add=True, db_index=True)
    updatedAt = models.DateTimeField(auto_now=True)

    # find conversation given all users Ids
    def find_conversation( list_of_participants ):
        # return conversation or None if it doesn't exist
        try:
            participant = list_of_participants[0]
            conversation = Conversation.objects.filter( users__contains = participant )
            for participant in range(1, len(list_of_participants)):
                conversation = conversation.filter( users__contains = participant )

            return conversation          
        except Conversation.DoesNotExist:
            return None
  
