from omegaconf import OmegaConf
from wavlmmsdd.audio.preprocess.convert import Convert
from wavlmmsdd.audio.preprocess.resample import Resample
from wavlmmsdd.audio.utils.utils import Build
from wavlmmsdd.audio.diarization.diarize import Diarizer
from wavlmmsdd.audio.feature.embedding import XVector


def main():
    # Paths
    diar_config_path = "../../config/diar_infer_telephonic.yaml"
    audio_path = "../../.data/example/ae.wav"
    mono_audio_path = ".temp/ae_16k_mono.wav"
    config_path = "../../config/config.yaml"

    # Configuration
    diar_config = OmegaConf.load(diar_config_path)
    config = OmegaConf.load(config_path)

    # Resample to 16000
    resampler = Resample(audio_file=audio_path)
    wave_16k, sr_16k = resampler.to_16k()

    # Convert to Mono
    converter = Convert(waveform=wave_16k, sample_rate=sr_16k)
    converter.to_mono()
    converter.save(mono_audio_path)

    # Build Manifest
    builder = Build(mono_audio_path)
    mono_manifest = builder.manifest()
    diar_config.diarizer.manifest_filepath = mono_manifest

    # Diarization
    diarizer = Diarizer(diar_config_path=diar_config_path,
                        manifest_path=mono_manifest,
                        embedding=XVector)
    diarizer.clustering_diarizer.speaker_embeddings = XVector(config)
    diarizer.run()


if __name__ == "__main__":
    main()
