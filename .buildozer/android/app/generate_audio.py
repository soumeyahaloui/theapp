from gtts import gTTS
import os

# Animal names mapping
animal_names = {
    "1": {"ar": "أسد", "fr": "Lion"},
    "2": {"ar": "نمر", "fr": "Tigre"},
    "3": {"ar": "فهد", "fr": "Guépard"},
    "4": {"ar": "وحيد القرن", "fr": "Rhinocéros"},
    "5": {"ar": "دب", "fr": "Ours"},
    "6": {"ar": "ذئب", "fr": "Loup"},
    "7": {"ar": "ضبع", "fr": "Hyène"},
    "8": {"ar": "غوريلا", "fr": "Gorille"},
    "9": {"ar": "غزال", "fr": "Gazelle"},
    "10": {"ar": "ثعلب", "fr": "Renard"},
    "11": {"ar": "باندا", "fr": "Panda"},
    "12": {"ar": "كنغر", "fr": "Kangourou"},
    "13": {"ar": "زرافة", "fr": "Girafe"},
    "14": {"ar": "قرد", "fr": "Singe"},
    "15": {"ar": "فيل", "fr": "Éléphant"}
}

# Output directories
output_dir_ar = "assets/audio/ar/"
output_dir_fr = "assets/audio/fr/"

# Ensure output directories exist
os.makedirs(output_dir_ar, exist_ok=True)
os.makedirs(output_dir_fr, exist_ok=True)

# Generate audio files
for image_num, names in animal_names.items():
    # Arabic audio
    tts_ar = gTTS(text=f"{names['ar']}", lang="ar")
    tts_ar.save(os.path.join(output_dir_ar, f"{image_num}_ar.mp3"))

    # French audio
    tts_fr = gTTS(text=f"{names['fr']}", lang="fr")
    tts_fr.save(os.path.join(output_dir_fr, f"{image_num}_fr.mp3"))

print("Audio files generated successfully!")
