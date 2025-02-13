import torch
from torch import Tensor
from omegaconf import DictConfig
from transformers import Wav2Vec2FeatureExtractor, WavLMForXVector
from src.wavlmmsdd.audio.preprocess.resample import Resample
from src.wavlmmsdd.audio.preprocess.convert import Convert


class XVector:
    def __init__(self, config: DictConfig):
        device_list = config.runtime.device
        device_option = device_list[0]
        if device_option == "cuda" and not torch.cuda.is_available():
            print("[WARNING] CUDA is not available. Falling back to CPU.")
            device_option = "cpu"

        self.device = device_option

        model_name = config.model.xvector

        print(f"[INFO] Loading XVector model: {model_name} on device: {self.device}")
        self.feature_extractor = Wav2Vec2FeatureExtractor.from_pretrained(model_name)
        self.model = WavLMForXVector.from_pretrained(model_name).to(self.device)
        self.model.eval()

        self.xvector_dim = self.model.config.xvector_output_dim
        print(f"[INFO] XVector dimension: {self.xvector_dim}")

    def extract(self, waveform: Tensor, sampling_rate: int = 16000) -> Tensor:
        wave_mono = Convert(waveform).to_mono()
        wave_16k, sr_16k = Resample(wave_mono, sampling_rate).to_16k()

        inputs = self.feature_extractor(
            wave_16k.squeeze(0).cpu().numpy(),
            sampling_rate=sr_16k,
            return_tensors="pt",
            padding=True,
        )
        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        with torch.no_grad():
            outputs = self.model(**inputs)
            embedding = outputs.embeddings.squeeze(0)

        return embedding.cpu().detach()
