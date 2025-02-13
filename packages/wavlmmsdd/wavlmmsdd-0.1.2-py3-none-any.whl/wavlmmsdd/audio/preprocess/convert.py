import torch
import torchaudio
import os


class Convert:
    def __init__(
            self,
            audio_file: str = None,
            waveform: torch.Tensor = None,
            sample_rate: int = None
    ):

        if audio_file is not None:
            wave, sr = torchaudio.load(audio_file)
            self.waveform = wave
            self.sample_rate = sr
        elif waveform is not None and sample_rate is not None:
            self.waveform = waveform
            self.sample_rate = sample_rate
        else:
            raise ValueError("Either 'audio_file' or ('waveform' + 'sample_rate') must be provided.")

    def to_mono(self) -> torch.Tensor:
        if self.waveform.ndim == 1:
            self.waveform = self.waveform.unsqueeze(0)

        if self.waveform.shape[0] > 1:
            self.waveform = self.waveform.mean(dim=0, keepdim=True)

        return self.waveform

    def save(self, output_path: str):
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        torchaudio.save(output_path, self.waveform, self.sample_rate)
        print(f"[Convert.save] 16k+mono dosya kaydedildi: {output_path}")
