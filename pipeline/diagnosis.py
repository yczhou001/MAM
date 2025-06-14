from model.language_model import MedicalAssistant
from model.image_model import HuatuoChatbot
from model.video_model import VideoLLaMAChatbot
from model.audio_model import AudioChatbot

def get_diagnosis_prompt(ques,record):
    prompt = f'''
    Input: Based on the provided image/video/audio (if applicable) and the meeting record, please provide answer to the following question.

    Question: {ques}.

    Meeting record: {record}
    '''

    return prompt


def final_diagnosis(question, file_name, modality_type, type_name, meeting_record):
    query = get_diagnosis_prompt(question, meeting_record)
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
    print(f"\n--- final diagnosis ---")
    print(output)
    return output
