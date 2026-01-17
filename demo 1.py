

# ===============================
# 1) VOICE → TEXT
# ===============================
import speech_recognition as sr
import re
import json
import asyncio
import websockets

# ---------- Speech to Text ----------
def voice_to_text():
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as mic:
            print("🎤 Speak now...")
            recognizer.adjust_for_ambient_noise(mic, duration=0.5)
            audio = recognizer.listen(mic)
    except Exception as e:
        print("Microphone error:", e)
        return ""

    try:
        text = recognizer.recognize_google(audio)
        return text.upper()
    except Exception as e:
        print("Speech error:", e)
        return ""


# ===============================
# 2) TEXT → GLOSS
# ===============================

# Instead of JSON file, using Python dictionary inside same file
GLOSS_DICT = {
    "GOOD": "GOOD",
    "MORNING": "MORNING",
    "I": "I",
    "LOVE": "LOVE",
    "YOU": "YOU"
}

def text_to_gloss(text):
    tokens = re.findall(r"\w+", text.upper())
    gloss_output = []

    for t in tokens:
        if t in GLOSS_DICT:
            gloss_output.append(GLOSS_DICT[t])
        else:
            gloss_output.append(t)
    return gloss_output


# ===============================
# 3) GLOSS → ANIMATION CLIPS
# ===============================

CLIP_MAP = {
    "GOOD": "good.bvh",
    "MORNING": "morning.bvh",
    "YOU": "you.bvh",
    "LOVE": "love.bvh"
}

def gloss_to_clips(gloss_list):
    clips = []
    for g in gloss_list:
        if g in CLIP_MAP:
            clips.append(CLIP_MAP[g])
        else:
            print(f"⚠ No clip for: {g}")
    return clips


# ===============================
# 4) SEND TO UNITY (WebSocket)
# ===============================

async def send_to_unity_async(clips):
    uri = "ws://localhost:9000"

    try:
        async with websockets.connect(uri) as ws:
            message = {
                "type": "play_sequence",
                "clips": clips
            }
            await ws.send(json.dumps(message))
            print("Sent to Unity:", message)
    except Exception as e:
        print("Unity connection error:", e)

def send_to_unity(clips):
    asyncio.run(send_to_unity_async(clips))


# ===============================
# 5) MAIN PIPELINE
# ===============================

print("🎯 Voice → Text → Gloss → Sign Animation")

# STEP 1: VOICE → TEXT
text = voice_to_text()
print("You said:", text)

# STEP 2: TEXT → GLOSS
gloss = text_to_gloss(text)
print("Gloss sequence:", gloss)

# STEP 3: GLOSS → CLIPS
clips = gloss_to_clips(gloss)
print("Animation clips:", clips)

# STEP 4: SEND TO UNITY
if clips:
    send_to_unity(clips)
