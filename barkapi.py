from bark import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav
from fastapi import FastAPI
from fastapi.responses import FileResponse
import random

preload_models()

barkapi = FastAPI()

@barkapi.get("/txt2wav")
def txt2wav(inputstring: str):
    text_prompt = inputstring
    audio_array = generate_audio(text_prompt, history_prompt="voices/matlighty.npz")
    filename = f"{inputstring}-{random.randint(1000, 9999)}.wav"  
    write_wav(filename, SAMPLE_RATE, audio_array)
    return FileResponse(filename, media_type="audio/wav")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(barkapi, host="0.0.0.0", port=8086)