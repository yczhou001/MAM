import json
import os
import re
from pipeline.modality_selection import modality_selection
from model.language_model import MedicalAssistant
from model.image_model import HuatuoChatbot
from model.video_model import VideoLLaMAChatbot
from model.audio_model import AudioChatbot

def type_classification(modality, ques, file_name):
    data_file='2406_data_example'
    if modality=='image':
        image_paths = [os.path.join(data_file,file_name)]
        bot = HuatuoChatbot()
        query = 'Please answer with a single word: What kind of medical image is this? X-Ray, CT, MRI, Pathology, Biomedical'
        output = bot.chat(images=image_paths, text=query)
        if 'x-ray' in output.lower() or 'ct' in output.lower() or 'mri' in output.lower():
            query_more='Please answer with a single word: What part of the human body does this image show? Brain, bone, abdomen, mediastinum, liver, lung, kidney, soft tissue, pelvis'
            output_more = bot.chat(images=image_paths, text=query_more)
            return output, output_more
        return output
    elif modality=='audio':
        bot = AudioChatbot()
        audio_paths = os.path.join(data_file,file_name)
        query = 'Please answer with a single word: What kind of audio is this? Cardiovascular, Respiratory'
        output = bot.chat(audio=audio_paths,text=query)
        return output
    elif modality=='video':
        video_paths = [os.path.join(data_file, file_name)]
        bot = VideoLLaMAChatbot()
        query = 'Please answer with a single word: What kind of video is this? Sports, Rehabilitation, Emergency'
        output = bot.chat(paths=video_paths, text=query, modal_type='video')
        return output
    elif modality=='text':
        question_text = ques
        assistant = MedicalAssistant()
        question = f'''
        System prompt: You are given a question, please select a question type according to the given question.
        
        Input: The question is {question_text}. Which kind of question is this? Anaesthesia, Anatomy, Biochemistry, Dental, ENT, FM, O&G, Medicine, Microbiology, Ophthalmology, Orthopaedics, Pathology, Pediatrics, Pharmacology, Physiology, Psychiatry, Radiology, Skin, PSM, Surgery, Unknown.
        
        Output example: 
        The question type is **Anaesthesia**.
        '''
        response = assistant.generate_response(question)
        match = re.search(r'question type is (\w+)', response)
        if match:
            return match.group(1)
        else:
            return 'general'
            
