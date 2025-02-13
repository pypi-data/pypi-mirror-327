import os
import json
import torchaudio


class Build:
    def __init__(self, audio_path: str):
        self.audio_path = audio_path

        if not os.path.isfile(self.audio_path):
            raise FileNotFoundError(f"Audio file not found: {self.audio_path}")

        waveform, sr = torchaudio.load(self.audio_path)
        num_samples = waveform.shape[1]
        self.duration = num_samples / sr

    def manifest(self) -> str:
        manifest_data = {
            "audio_filepath": self.audio_path,
            "offset": 0.0,
            "duration": self.duration,
            "text": ""
        }

        audio_dir = os.path.dirname(self.audio_path)
        manifest_path = os.path.join(audio_dir, "manifest.json")

        with open(manifest_path, "w", encoding="utf-8") as f:
            f.write(json.dumps(manifest_data, ensure_ascii=False))

        return manifest_path
