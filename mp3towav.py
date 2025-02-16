import ffmpeg

def convert_mp3_to_wav(mp3_file, wav_file="converted.wav"):
    """使用 ffmpeg-python 将 MP3 转换为 WAV"""
    try:
        ffmpeg.input(mp3_file).output(wav_file, format="wav", ar="16000").run(overwrite_output=True)
        print(f"转换成功: {wav_file}")
        return wav_file
    except ffmpeg.Error as e:
        print("转换失败:", e)
        return None

# 测试
mp3_path = "test.mp3"
convert_mp3_to_wav(mp3_path)
