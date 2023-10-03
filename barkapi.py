from bark import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import random
import io
import os

preload_models()
barkapi = FastAPI()

@barkapi.get("/txt2wav")
def txt2wav(inputstring: str, voicefile: str = None):
    if voicefile:
        voicechoice = f'voices/{voicefile}'
        audio_array = generate_audio(inputstring, history_prompt=voicechoice)
    else:
        audio_array = generate_audio(inputstring)
    wav_io = io.BytesIO()
    write_wav(wav_io, SAMPLE_RATE, audio_array)
    wav_io.seek(0)
    return StreamingResponse(wav_io, media_type="audio/wav")
    
@barkapi.get("/voices")
def voices():
    voices_dir = "voices"
    voiceslist = [f for f in os.listdir(voices_dir) if f.endswith(".npz")]
    return {"voices": voiceslist}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(barkapi, host="0.0.0.0", port=8086)