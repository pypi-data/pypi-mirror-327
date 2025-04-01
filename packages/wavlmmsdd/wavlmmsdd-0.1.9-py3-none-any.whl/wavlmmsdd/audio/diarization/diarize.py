from omegaconf import OmegaConf
from nemo.collections.asr.models import ClusteringDiarizer
from wavlmmsdd.audio.feature.embedding import XVector
from importlib.resources import files

class Diarizer:
    def __init__(
        self,
        embedding: XVector = None
    ):
        if embedding is None:
            raise ValueError("embedding parametresi None olamaz. XVector nesnesi bekleniyor.")

        default_config = files("wavlmmsdd.config") / "diar_infer_telephonic.yaml"
        diar_config_path = str(default_config)

        manifest_path = "temp/manifest.json"

        self.cfg = OmegaConf.load(diar_config_path)
        self.cfg.diarizer.manifest_filepath = manifest_path

        self.clustering_diarizer = ClusteringDiarizer(cfg=self.cfg)
        self.clustering_diarizer.speaker_embeddings = embedding

    def run(self):
        diarization_results = self.clustering_diarizer.diarize()
        return diarization_results
