import re
import random
from model.language_model import MedicalAssistant
from model.image_model import HuatuoChatbot
from model.video_model import VideoLLaMAChatbot
from model.audio_model import AudioChatbot

#data_file='2406_data_example'


def get_discuss_prompt(role_name, role_responsibilities, question, disease_type):
    prompt = f'''You are a {role_name}, responsible for the following tasks: {role_responsibilities}. Please thoughtfully express your views for the following question.
    Input: 
    **Question type**: {disease_type}.
    **Question**: {question}.
    
    Example output: 
    **Assessment Steps**:
    - Initial Assessment: [Provide a detailed overview of the initial assessment process]
    - Diagnostic Studies (e.g., imaging, lab tests): [Include relevant details about any studies conducted]
    - Additional Considerations: [Mention any other pertinent factors or evaluations]
    **Possible Answers**:
    - Answer 1: [Briefly explain answer 1]
      Reasoning: [Briefly describe the corresponding reason for answer 1]
    - Answer 2: [Briefly explain answer 2]
      Reasoning: [Briefly describe the corresponding reason for answer 2]
    - Answer 3: [Briefly explain answer 3]
      Reasoning: [Briefly describe the corresponding reason for answer 3]
    **Conclusion**: [Summarize the findings and provide a final recommendation or insight]
    '''
    return prompt



def get_summarize_prompt(question,discussion):
    prompt = f'''You are a specialized doctor serving as the moderator of this meeting. Please provide a detailed summary of the discussions that have taken place.
    
    Example output:
    **Possible Answers**:
    - Answer 1: [Briefly explain answer 1]
    - Answer 2: [Briefly explain answer 2]
    - Answer 3: [Briefly explain answer 3]
    **Agreements**:
    - [Description of any agreements reached]
    **Disagreements**:
    - [Description of any disagreements that were noted]
    **Conclusions**:
    - [Final thoughts or conclusions drawn from the discussion]
    
    Input: The question is {question}. The previous discussion of the meeting includes: {discussion}.
    '''
    return prompt




def get_vote_prompt(role_name, role_responsibilities, question, summary):
    prompt = f'''You are a {role_name}, responsible for the following tasks: {role_responsibilities}. 
    Please answer just using "yes" or "no" according to the following questions and the corresponding summery and the contents of the given file(if any).
    Input: The question is {question}, and the summery of the discussion is:
    {summary}
    Do you agree with the summery above? Please answer just using "yes" or "no".    
    '''
    return prompt

def get_determine_prompt(dis):
    prompt = f'''
    Question: Is there any medical reasoning errors, redundant statements, or invalid outputs in the following paragraph? Please answer just using "yes" or "no".
    Please read the rollowing paragraph:
    {dis}
    '''
    return prompt

class Role:
    def __init__(self, name, responsibilities):
        self.name = name
        self.responsibilities = responsibilities
        self.vote = None

    def discuss(self, question, file_name, modality_type, type_name):
        query = get_discuss_prompt(self.name, self.responsibilities, question, type_name)
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
            output = assistant.generate_response(query, max_new_tokens=512)
        return output

class Moderator:
    def determine(self, dis):
        query = get_determine_prompt(dis)
        assistant = MedicalAssistant()
        output = assistant.generate_response(query, max_new_tokens=512)
        if 'yes' in output.lower():
            return True
        else:
            return False
    def summarize(self, question, record_discussions):
        query = get_summarize_prompt(question,record_discussions)
        summary = "Summary of discussions:\n"
        assistant = MedicalAssistant()
        output = assistant.generate_response(query, max_new_tokens=2560)
        summary += output
        return summary

    def vote(self, roles, question, file_name, modality_type, type_name, summary):
        agree_number=0
        disagree_number=0
        for role in roles:
            query = get_vote_prompt(role.name, role.responsibilities, question, summary)
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
                output = assistant.generate_response(query, max_new_tokens=512)

            if 'yes' in output.lower():
                agree_number=agree_number+1
            elif 'no' in output.lower():
                disagree_number=disagree_number+1
            else:
                agree_number=agree_number+1

        return agree_number, disagree_number


def extract_roles_from_text(text):
    role_pattern = r"\*\*(.*?)\*\*(.*?):\n(.*?)(?=\n\*\*|$)"
    matches = re.findall(role_pattern, text, re.DOTALL)
    roles = []
    role_count = 0
    for n, name, responsibilities in matches:
        #responsibilities = responsibilities.replace('\n- ', '\n').strip()
        if role_count<3:
            name = n + name
            roles.append(Role(name, responsibilities))
        role_count=role_count+1    
    return roles


def discussion_and_voting(roles, question, file_name, modality_type, type_name, history_item):
    history_information = f"\n The following is the relevant information that can be used as a reference：{history_item}"
    record_all=""
    record_discussions="Record of discussion:\n"
    moderator = Moderator()
    max_rounds = 3
    for round_number in range(1, max_rounds + 1):
        print(f"\n--- Round {round_number} ---")
        for role in roles:
            dis = f"{role.name} discussed:\n {role.discuss(question, file_name, modality_type, type_name)}\n"
            if moderator.determine(dis):
                dis = f"{role.name} discussed:\n {role.discuss(question, file_name, modality_type, type_name)}\n"
            record_discussions += dis
            #print(role.discuss(question, file_name, modality_type, type_name))
        record_discussions += history_information
        print(record_discussions)
        #record_all+=record_discussions
        summary = moderator.summarize(question, record_discussions)
        #summary+=history_information
        print(summary)
        record_all+="Summary of discussions:\n"
        record_all+=f"{summary}\n"
        #record_all = f"{summary}\n"
        
        agree_votes, disagree_votes = moderator.vote(roles, question, file_name, modality_type, type_name, summary)
        print(f"Votes: agree number: {agree_votes}, disagree number: {disagree_votes}")
        record_all+=f"Votes: agree number: {agree_votes}, disagree number: {disagree_votes}\n"
        
        if disagree_votes==0:
            print("All roles agree on the diagnosis.")
            record_all+="All roles agree on the diagnosis."
            #print(history_information)
            #record_all+=history_information
            break
        elif round_number == max_rounds:
            print("Reached maximum discussion rounds.")
            record_all+="Reached maximum discussion rounds.\n"
            if agree_votes>disagree_votes:
                print("The minority is subordinate to the majority, and the opinion of the meeting is carried")
                record_all+="The minority is subordinate to the majority, and the opinion of the meeting is carried"
            #print(history_information)
            #record_all+=history_information
            break
        else:
            print("Not all roles agree, continuing discussion.")
            record_all+="Not all roles agree, continuing discussion."
    return record_all



def roles_meeting(question, file_name, modality_type, type_name, roles_generated, history_item):
    roles = extract_roles_from_text(roles_generated)
    meeting_record = discussion_and_voting(roles, question, file_name, modality_type, type_name, history_item)
    return meeting_record


#roles_meeting("What does the picture show?", 'tmp/image.png', "image", "Lung, CT",generated_result)
