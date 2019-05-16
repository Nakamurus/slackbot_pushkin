# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from events.pushkin_data import sample_work, word_in_pushkin
import slack

SLACK_VERIFICATION_TOKEN = getattr(settings, 'SLACK_VERIFICATION_TOKEN', None)
SLACK_BOT_USER_TOKEN = getattr(settings, 'SLACK_BOT_USER_TOKEN', None)                                     
Client = slack.WebClient(token=SLACK_BOT_USER_TOKEN)                        

class Events(APIView):
    def post(self, request, *args, **kwargs):

        slack_message = request.data

        if slack_message.get('token') != SLACK_VERIFICATION_TOKEN:
            return Response(status=status.HTTP_403_FORBIDDEN)

        # verification challenge
        if slack_message.get('type') == 'url_verification':
            return Response(data=slack_message,
                            status=status.HTTP_200_OK)

        if 'event' in slack_message:                              
            event_message = slack_message.get('event')            
            
            # ignore bot's own message
            if event_message.get('subtype') == 'bot_message':     
                return Response(status=status.HTTP_200_OK)        
            
            # process user's message
            user = event_message.get('user')                      
            text = event_message.get('text')                      
            channel = event_message.get('channel')   
            bot_text = sample_work(word_in_pushkin(text.lower()))
            if bot_text:
                for i in bot_text: # if bot_text is a list, convert it to a string
                    i = ''.join(i) # and return one by one
                    Client.chat_postMessage(
                        channel=channel,
                        text=i)
                bot_text = None    # prevent endless response
                return Response(status=status.HTTP_200_OK)
                
        return Response(status=status.HTTP_200_OK)
                