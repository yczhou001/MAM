def modality_selection(question, file_name):
    if file_name.endswith(('.jpg', '.jpeg', '.png')):
        return 'image'
    elif file_name.endswith(('.wav', '.mp3')):
        return 'audio'
    elif file_name.endswith(('.mp4')):
        return 'video'
    else:
        return 'text'
    return None
