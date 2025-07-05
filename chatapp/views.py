
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from decouple import config

class OpenAIChatView(APIView):
    def post(self, request):
        # OpenRouter API configuration
        api_key = config('OPENROUTER_API_KEY')
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "your_site_url", 
            "X-Title": "Your Site Name"  
        }

        # client data
        user_input = request.data.get('message', 'Hello, how can DeepSeek help you?')

        # DeepSeek R1 API playload
        payload = {
            "model": "deepseek/deepseek-r1:free",
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are a chatbot that only answers questions related to eCommerce websites, "
                        "like product details, pricing, shipping, payment, offers, customer support, etc. "
                        "If the user asks anything outside of this topic (like jokes, history, politics, etc), "
                        "politely say: 'Sorry, I can only help with eCommerce-related questions.' "
                        "Please also understand and respond in Bengali if the user speaks in Bengali."
                    )
                },
                
                {"role": "user", "content": user_input}
            ],
            "stream": False 
        }

        try:
            # API call
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()  
            result = response.json()
            ai_response = result['choices'][0]['message']['content']
            return Response({"response": ai_response}, status=status.HTTP_200_OK)
        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)