from model.language_model import MedicalAssistant
from model.image_model import HuatuoChatbot
from model.video_model import VideoLLaMAChatbot
from model.audio_model import AudioChatbot

def get_review_prompt(ques,record):
    prompt = f'''
    Input: You're a medical assistant. Please check whether the answer to this question is reasonable, if it is, please answer "yes", if not, please answer "no"

    Question: {ques}.

    Answer: {record}
    '''

    return prompt

def review_all(question, file_name, modality_type, type_name, result_diagnosis):
    query = get_review_prompt(question, result_diagnosis)
    if modality_type=='image':
        bot = HuatuoChatbot()
        output = bot.chat(images=file_name, text=query)
    elif modality_type=='audio':
        bot = AudioChatbot()
        output = bot.chat(audio=file_name,text=query)
    elif modality_type=='video':
        bot = VideoLLaMAChatbot()
        output = bot.chat(paths=file_name, text=query, modal_type='video')
    elif modality_type=='text':
        assistant = MedicalAssistant()
        output = assistant.generate_response(query)
    return output
