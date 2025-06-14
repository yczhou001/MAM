import json
import os

def memory(id, question, file_name, modality_type, answer):
    history_text_file='./history/text_history.json'
    history_image_file='./history/image_history.json'
    history_video_file='./history/video_history.json'
    history_audio_file = './history/audio_history.json'
    if modality_type=='text':
        if os.path.exists(history_text_file):
            with open(history_text_file, 'r') as file:
                data = json.load(file)

        else:
            data = []
        item={
            "id":id,
            "question": question,
            "answer": answer
        }
        data.append(item)
        with open(history_text_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return "done"
    elif modality_type=='image':
        if os.path.exists(history_image_file):
            with open(history_image_file, 'r') as file:
                data = json.load(file)

        else:
            data = []
        item={
            "id":id,
            "file_name": file_name,
            "question": question,
            "answer": answer
        }
        data.append(item)
        with open(history_image_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return "done"
    elif modality_type=='video':
        if os.path.exists(history_video_file):
            with open(history_video_file, 'r') as file:
                data = json.load(file)

        else:
            data = []
        item={
            "id":id,
            "file_name": file_name,
            "question": question,
            "answer": answer
        }
        data.append(item)
        with open(history_video_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return "done"
    elif modality_type=='audio':
        if os.path.exists(history_audio_file):
            with open(history_audio_file, 'r') as file:
                data = json.load(file)
        else:
            data = []
        item={
            "id":id,
            "file_name": file_name,
            "question": question,
            "answer": answer
        }
        data.append(item)
        with open(history_audio_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return "done"
