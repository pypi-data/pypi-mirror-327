from omegaconf import OmegaConf
from nemo.collections.asr.models import ClusteringDiarizer
from wavlmmsdd.audio.feature.embedding import XVector


class Diarizer:
    def __init__(self, diar_config_path: str, manifest_path: str, embedding: XVector):
        if embedding is None:
            raise ValueError("embedding parametresi None olamaz. XVector nesnesi bekleniyor.")

        self.cfg = OmegaConf.load(diar_config_path)
        self.cfg.diarizer.manifest_filepath = manifest_path

        self.clustering_diarizer = ClusteringDiarizer(cfg=self.cfg)

        self.clustering_diarizer.speaker_embeddings = embedding

    def run(self):
        diarization_results = self.clustering_diarizer.diarize()
        return diarization_results
