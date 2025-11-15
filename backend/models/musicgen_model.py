import uuid
import os
import soundfile as sf
import torch
from transformers import AutoProcessor, MusicgenForConditionalGeneration


class MusicGenerator:
    def __init__(self):
        print("🎵 Loading MusicGen model (facebook/musicgen-small)...")
        self.processor = AutoProcessor.from_pretrained("facebook/musicgen-small")
        self.model = MusicgenForConditionalGeneration.from_pretrained(
            "facebook/musicgen-small"
        ).to("cpu")
        print("✅ MusicGen model loaded successfully.")

    def generate_variants(self, prompt, num_variants=3, max_new_tokens=256):
        """
        Generates multiple music samples in a single forward pass.
        These samples will be different, not identical clones.
        """

        print(f"🎶 Generating {num_variants} music variations for: {prompt}")

        # Create a batch of identical prompts → model generates different samples
        prompts = [prompt] * num_variants

        inputs = self.processor(
            text=prompts,
            padding=True,
            return_tensors="pt"
        ).to("cpu")

        # MULTI-SAMPLE forward pass
        outputs = self.model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=True,        # ensures randomness
            top_k=50,
            top_p=0.95,
            temperature=1.0
        )

        os.makedirs("generated", exist_ok=True)

        file_paths = []

        # Save each generated sample separately
        for i in range(num_variants):
            audio = outputs[i].cpu().numpy().squeeze()
            filename = f"{uuid.uuid4().hex}.wav"
            path = os.path.join("generated", filename)
            sf.write(path, audio, 32000)
            file_paths.append(path)
            print(f"🎵 Variant {i+1} saved → {path}")

        return file_paths
