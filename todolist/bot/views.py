import os

from django.http import JsonResponse
from dotenv import load_dotenv
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from bot.models import TgUser
from bot.tg.client import TgClient
from core.models import User

load_dotenv()


class BotVerifyView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):

        token = os.getenv("BOT_TOKEN")
        tg_client = TgClient(token)
        verification_code = request.data.get('verification_code')

        try:
            tg_user = TgUser.objects.get(verification_code=verification_code)
        except TgUser.DoesNotExist:
            return JsonResponse({'error': 'Invalid verification code'}, status=404)

        user_id = self.request.user.id
        tg_user.user_id = User.objects.get(id=user_id)
        tg_user.save()

        chat_id = tg_user.tg_chat_id
        tg_client.send_message(chat_id, 'Связка успешно подтверждена!')

        response_data = {
            'message': 'Verification successful',
            'user_id': user_id,
        }

        return JsonResponse(response_data)
