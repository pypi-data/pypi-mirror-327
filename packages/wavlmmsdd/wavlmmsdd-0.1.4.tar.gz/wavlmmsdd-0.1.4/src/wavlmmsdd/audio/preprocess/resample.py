import torch
import torchaudio


class Resample:
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

    def to_16k(self):
        if self.sample_rate == 16000:
            return self.waveform, self.sample_rate

        resampler = torchaudio.transforms.Resample(orig_freq=self.sample_rate)
        self.waveform = resampler(self.waveform)
        self.sample_rate = 16000
        return self.waveform, self.sample_rate

