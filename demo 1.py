# =========================================================
# VOICE / TEXT TO ISL GLOSS USING RULE-BASED NLP (PYTHON)
# =========================================================

import speech_recognition as sr
import re

# =========================================================
# 1) VOICE → TEXT
# =========================================================

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
        print("Speech recognition error:", e)
        return ""

# =========================================================
# 2) RULE-BASED NLP (TEXT → ISL GLOSS)
# =========================================================

STOP_WORDS = {
    "AM", "IS", "ARE", "WAS", "WERE",
    "A", "AN", "THE", "TO", "OF", "IN", "ON", "AT",
    "WILL", "SHALL", "WOULD", "DO", "DID"
}

TIME_WORDS = {
    "TODAY", "TOMORROW", "YESTERDAY",
    "MORNING", "NIGHT", "EVENING"
}

NEGATION_WORDS = {"NOT", "NO", "NEVER"}

WH_WORDS = {"WHAT", "WHERE", "WHY", "HOW", "WHEN"}

SUBJECT_WORDS = {"I", "YOU", "HE", "SHE", "WE", "THEY"}

VERB_MAP = {
    "GOING": "GO",
    "WENT": "GO",
    "COME": "COME",
    "COMING": "COME",
    "LIKING": "LIKE",
    "LOVING": "LOVE",
    "EATING": "EAT",
    "ATE": "EAT"
}

GLOSS_DICT = {
    "I": "I",
    "YOU": "YOU",
    "HE": "HE",
    "SHE": "SHE",
    "WE": "WE",
    "THEY": "THEY",
    "GO": "GO",
    "COME": "COME",
    "LIKE": "LIKE",
    "LOVE": "LOVE",
    "EAT": "EAT",
    "SCHOOL": "SCHOOL",
    "COLLEGE": "COLLEGE",
    "FOOD": "FOOD",
    "TODAY": "TODAY",
    "TOMORROW": "TOMORROW",
    "YESTERDAY": "YESTERDAY",
    "NO": "NO"
}

def text_to_gloss(text):
    tokens = re.findall(r"\w+", text.upper())

    time = []
    subject = []
    verb = []
    obj = []
    negation = []
    wh = []

    for word in tokens:

        if word in STOP_WORDS:
            continue

        if word in TIME_WORDS:
            time.append(word)
            continue

        if word in NEGATION_WORDS:
            negation.append("NO")
            continue

        if word in WH_WORDS:
            wh.append(word)
            continue

        if word in VERB_MAP:
            word = VERB_MAP[word]

        if word in SUBJECT_WORDS:
            subject.append(word)
        elif word in GLOSS_DICT:
            if word in VERB_MAP.values():
                verb.append(word)
            else:
                obj.append(word)
        else:
            obj.append(word)

    # ISL ORDER: TIME – OBJECT – SUBJECT – VERB – NEG – WH
    gloss_sentence = time + obj + subject + verb + negation + wh
    return gloss_sentence

# =========================================================
# 3) GLOSS → BVH FILES (BLENDER)
# =========================================================

BVH_MAP = {
    "I": "i.bvh",
    "YOU": "you.bvh",
    "GO": "go.bvh",
    "COME": "come.bvh",
    "LOVE": "love.bvh",
    "LIKE": "like.bvh",
    "EAT": "eat.bvh",
    "SCHOOL": "school.bvh",
    "COLLEGE": "college.bvh",
    "FOOD": "food.bvh",
    "TODAY": "today.bvh",
    "TOMORROW": "tomorrow.bvh",
    "YESTERDAY": "yesterday.bvh",
    "NO": "no.bvh",
    "WHERE": "where.bvh"
}

def gloss_to_bvh(gloss_list):
    bvh_files = []

    for g in gloss_list:
        if g in BVH_MAP:
            bvh_files.append(BVH_MAP[g])
        else:
            print(f"⚠ No BVH file for: {g}")

    return bvh_files

# =========================================================
# 4) MAIN PIPELINE
# =========================================================

print("🎯 Voice/Text → ISL Grammar → Gloss → Blender BVH")

text = voice_to_text()
print("📝 Recognized Text:", text)

gloss_output = text_to_gloss(text)
print("🔤 ISL Gloss:", gloss_output)

bvh_sequence = gloss_to_bvh(gloss_output)
print("🎬 BVH Sequence:", bvh_sequence)

print("\n✅ Import BVH files sequentially in Blender.")
