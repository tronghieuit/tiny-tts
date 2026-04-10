from setuptools import setup, find_packages

setup(
    name="tiny-tts",
    version="0.1.0",
    description="Ultra-lightweight English text-to-speech model (~9M params, ~20MB)",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    license="Apache-2.0",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "tiny_tts.text": ["cmudict.rep", "cmudict_cache.pickle"],
        "tiny_tts.checkpoints": ["*.safetensors", "*.pth"],
    },
    python_requires=">=3.8",
    install_requires=[
        "torch>=2.0",
        "torchaudio>=2.0",
        "soundfile",
        "g2p-en",
        "transformers",
        "numba",
        "huggingface_hub",
        "safetensors",
    ],
    entry_points={
        "console_scripts":[
            "tiny-tts=tiny_tts.infer:main",
        ],
    },
)