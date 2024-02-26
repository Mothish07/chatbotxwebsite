import json
from django.http import JsonResponse
from openAIModule import OpenAIModule
from audioRegonizationModule import voice_to_text
import speech_recognition as sr
from django.views.decorators.http import require_POST
from .models import ChatMessage

def generate_reply(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.decoder.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data in the request body'}, status=400)
        user_input = data.get('user_input')
        if user_input is None:
            return JsonResponse({'error': 'Missing user_input field'}, status=400)
        openai_module = OpenAIModule()
        reply = openai_module.generate_reply(user_input)
        return JsonResponse({'reply': reply})
    else:
        return JsonResponse({'error': 'Invalid request method'})


def convert_voice_to_text(request):
    if request.method == 'POST':
        try:
            text = voice_to_text()
            return JsonResponse({'text': text})
        except sr.UnknownValueError:
            return JsonResponse({'error': "Could not understand the audio"}, status=500)
        except sr.RequestError as e:
            return JsonResponse({'error': f"Could not request results from Google Web Speech API: {e}"}, status=500)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
def save_chat(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode('utf-8'))
            user_uid = data.get("uid")
            input_text = data.get("input")
            reply_text = data.get("reply")
            
            # Check if all required fields are present
            if user_uid is None or input_text is None or reply_text is None:
                return JsonResponse({"status": "error", "error": "Missing required fields"}, status=400)
            
            # Save the chat message
            ChatMessage.objects.create(user_uid=user_uid, input=input_text, reply=reply_text)
            
            return JsonResponse({"status": "success"})
        
        except json.decoder.JSONDecodeError:
            return JsonResponse({"status": "error", "error": "Invalid JSON data in the request body"}, status=400)
        except Exception as e:
            return JsonResponse({"status": "error", "error": str(e)}, status=500)
    
    return JsonResponse({"status": "error", "error": "Method not allowed"}, status=405)

def get_chat_history(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        user_uid = data.get("uid")
        if not user_uid:
            return JsonResponse({"status": "error", "message": "Missing user UID"})
        chat_history = ChatMessage.objects.filter(user_uid=user_uid)
        chat_history_data = []
        for message in chat_history:
            chat_history_data.append({
                "input": message.input,
                "reply":message.reply,
                "timestamp": message.timestamp.strftime("%Y-%m-%d %H:%M:%S")
            })
        return JsonResponse({"chatHistory": chat_history_data})
    return JsonResponse({"status": "error", "message": "Method not allowed"})

@require_POST
def delete_chat_history(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        user_uid = data.get("uid")
        if not user_uid:
            return JsonResponse({"status": "error", "message": "Missing user UID"})
    
        try:
            # Delete all chat messages associated with the user
            deleted_count, _ = ChatMessage.objects.filter(user_uid=user_uid).delete()
            if deleted_count > 0:
                return JsonResponse({"status": "success", "message": "Chat history deleted successfully"})
            else:
                return JsonResponse({"status": "error", "message": "No chat history found for the user"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": "Failed to delete chat history", "error": str(e)})
    
