from django.contrib.auth.middleware import get_user
from django.db.models import Max, Q
from django.db.models.query import Prefetch
from django.http import HttpResponse, JsonResponse
from messenger_backend.models import Conversation, Message
from online_users import online_users
from rest_framework.views import APIView
from rest_framework.request import Request


class Conversations(APIView):
    """get all conversations for a user, include latest message text for preview, the number of unread messages and all messages
    include other user model so we have info on username/profile pic (don't include current user info)
    TODO: for scalability, implement lazy loading"""

    def get(self, request: Request):
        try:
            user = get_user(request)           

            if user.is_anonymous:
                return HttpResponse(status=401)
            user_id = user.id

            conversations = (
                Conversation.objects.filter(
                    Q(user1=user_id) | Q(user2=user_id))
                .prefetch_related(
                    Prefetch(
                        "messages", queryset=Message.objects.order_by("createdAt")
                    )
                )
                .all()
            )

            conversations_response = []

            for convo in conversations:            

                num_unread_messages = convo.messages.filter(wasRead=False).exclude(senderId=user_id).count()            

                last_read_message = convo.messages.filter(senderId=user_id).exclude(wasRead=False).last()

                if last_read_message:
                    last_read_message_id = last_read_message.id             
                else:
                    last_read_message_id = None    

                convo_dict = {
                    "id": convo.id,
                    "numUnreadMessages": num_unread_messages,
                    "lastReadMessageId": last_read_message_id,
                    "messages": [
                        message.to_dict(
                            ["id", "text", "senderId", "createdAt"])
                        for message in convo.messages.all()
                    ],
                }

                # set properties for notification count and latest message preview
                convo_dict["latestMessageText"] = convo_dict["messages"][-1]["text"]



                # set a property "otherUser" so that frontend will have easier access
                user_fields = ["id", "username", "photoUrl"]
                if convo.user1 and convo.user1.id != user_id:
                    convo_dict["otherUser"] = convo.user1.to_dict(user_fields)
                elif convo.user2 and convo.user2.id != user_id:
                    convo_dict["otherUser"] = convo.user2.to_dict(user_fields)

                # set property for online status of the other user
                if convo_dict["otherUser"]["id"] in online_users:
                    convo_dict["otherUser"]["online"] = True
                else:
                    convo_dict["otherUser"]["online"] = False

                conversations_response.append(convo_dict)
            conversations_response.sort(
                key=lambda convo: convo["messages"][0]["createdAt"],
                reverse=True,
            )
            return JsonResponse(
                conversations_response,
                safe=False,
            )
        except Exception as e:
            print("e")
            print(e)
            return HttpResponse(status=500)

    class Read(APIView):
        """set the wasRead field to True on all unread messages that are part of the conversation"""

        def patch(self, request):

            try:
                user = get_user(request)

                if user.is_anonymous:
                    return HttpResponse(status=401)            

                senderId = request.data.get("senderId")
                recipientId = request.data.get("recipientId")             

                if user.id != senderId and user.id != recipientId:
                    return HttpResponse(status=403)   

                conversation = Conversation.find_conversation(senderId, recipientId)   

                recipient_unread_messages = Message.objects.filter(conversation=conversation, wasRead=False).exclude(senderId=senderId)      
                
                for unread_message in recipient_unread_messages:          
                    unread_message.wasRead = True

                Message.objects.bulk_update(recipient_unread_messages, ['wasRead'])

                return HttpResponse(status=204)
            except Exception as e:
                return HttpResponse(status=500)    
