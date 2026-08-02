from __future__ import annotations

import random
import re
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import requests


DEFAULT_SERVER = "http://127.0.0.1:8188"
DEFAULT_CHECKPOINT = "animagine-xl-4.0-opt.safetensors"


@dataclass(frozen=True)
class GenerationResult:
    prompt_id: str
    output_files: tuple[Path, ...]
    elapsed_seconds: float


def _prompt_sections(prompt: str) -> dict[str, str]:
    matches = list(re.finditer(r"(?m)^\[([A-Z][A-Z AND]+)\]\s*$", prompt))
    sections: dict[str, str] = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(prompt)
        sections[match.group(1)] = prompt[match.end():end].strip()
    return sections


def adapt_project_prompt(prompt: str) -> tuple[str, str]:
    sections = _prompt_sections(prompt)
    positive_parts = [
        "masterpiece, high score, great score, absurdres, 1girl, solo, exactly one character, single centered subject",
        sections.get("SHOT", ""),
        sections.get("CHARACTER", ""),
        sections.get("STYLE", ""),
        sections.get("FACE AND ANATOMY", ""),
    ]
    positive = "\n".join(part for part in positive_parts if part)
    negative = sections.get("NEGATIVE", "")
    negative = ", ".join(
        part for part in (
            "low score, worst quality, low quality, bad anatomy, bad hands, extra fingers, extra arms, missing fingers, deformed, blurry",
            "text, letters, logo, watermark, signature, copied character-reference outfit, copied character-reference background, multiple girls, multiple people, duplicate person, collage, inset portrait, split screen",
            negative,
        ) if part
    )
    return positive, negative


def choose_sdxl_size(image_path: Path) -> tuple[int, int]:
    from PIL import Image

    with Image.open(image_path) as image:
        ratio = image.width / image.height
    buckets = ((1024, 1024), (832, 1216), (1216, 832), (896, 1152), (1152, 896), (768, 1344), (1344, 768))
    return min(buckets, key=lambda size: abs(size[0] / size[1] - ratio))


class ComfyUIClient:
    def __init__(
        self,
        server: str = DEFAULT_SERVER,
        comfy_root: Path = Path(r"D:\AI\ComfyUI"),
        checkpoint: str = DEFAULT_CHECKPOINT,
        timeout_seconds: int = 900,
    ) -> None:
        self.server = server.rstrip("/")
        self.comfy_root = Path(comfy_root)
        self.checkpoint = checkpoint
        self.timeout_seconds = timeout_seconds
        self.session = requests.Session()

    def ensure_ready(self) -> None:
        response = self.session.get(f"{self.server}/system_stats", timeout=10)
        response.raise_for_status()

    def upload_image(self, path: str | Path) -> str:
        image_path = Path(path)
        with image_path.open("rb") as stream:
            response = self.session.post(
                f"{self.server}/upload/image",
                files={"image": (image_path.name, stream)},
                data={"type": "input", "overwrite": "true"},
                timeout=120,
            )
        response.raise_for_status()
        return response.json()["name"]

    def _workflow(
        self,
        positive: str,
        negative: str,
        identity_name: str,
        template_name: str,
        width: int,
        height: int,
        filename_prefix: str,
        steps: int,
        denoise: float,
        identity_weight: float,
        seed: int,
    ) -> dict[str, Any]:
        return {
            "1": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": self.checkpoint}},
            "2": {"class_type": "LoadImage", "inputs": {"image": identity_name}},
            "3": {"class_type": "PrepImageForClipVision", "inputs": {"image": ["2", 0], "interpolation": "LANCZOS", "crop_position": "center", "sharpening": 0.15}},
            "4": {"class_type": "IPAdapterUnifiedLoader", "inputs": {"model": ["1", 0], "preset": "PLUS (high strength)"}},
            "5": {"class_type": "IPAdapterAdvanced", "inputs": {"model": ["4", 0], "ipadapter": ["4", 1], "image": ["3", 0], "weight": identity_weight, "weight_type": "linear", "combine_embeds": "average", "start_at": 0.0, "end_at": 0.72, "embeds_scaling": "K+V w/ C penalty"}},
            "6": {"class_type": "LoadImage", "inputs": {"image": template_name}},
            "7": {"class_type": "ImageScale", "inputs": {"image": ["6", 0], "upscale_method": "lanczos", "width": width, "height": height, "crop": "center"}},
            "8": {"class_type": "VAEEncode", "inputs": {"pixels": ["7", 0], "vae": ["1", 2]}},
            "9": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["1", 1], "text": positive}},
            "10": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["1", 1], "text": negative}},
            "11": {"class_type": "KSampler", "inputs": {"model": ["5", 0], "seed": seed, "steps": steps, "cfg": 5.0, "sampler_name": "dpmpp_2m_sde", "scheduler": "karras", "positive": ["9", 0], "negative": ["10", 0], "latent_image": ["8", 0], "denoise": denoise}},
            "12": {"class_type": "VAEDecode", "inputs": {"samples": ["11", 0], "vae": ["1", 2]}},
            "13": {"class_type": "SaveImage", "inputs": {"images": ["12", 0], "filename_prefix": filename_prefix}},
        }

    def generate(
        self,
        prompt: str,
        character_references: list[str],
        template_reference: str,
        filename_prefix: str,
        *,
        steps: int = 28,
        denoise: float = 0.65,
        identity_weight: float = 0.55,
        identity_reference_index: int = 2,
        seed: int | None = None,
    ) -> GenerationResult:
        if not character_references:
            raise ValueError("At least one character reference is required")
        self.ensure_ready()
        template_path = Path(template_reference)
        selected_index = min(max(identity_reference_index, 1), len(character_references)) - 1
        identity_name = self.upload_image(character_references[selected_index])
        template_name = self.upload_image(template_path)
        width, height = choose_sdxl_size(template_path)
        positive, negative = adapt_project_prompt(prompt)
        workflow = self._workflow(
            positive,
            negative,
            identity_name,
            template_name,
            width,
            height,
            filename_prefix,
            steps,
            denoise,
            identity_weight,
            random.randrange(2**32) if seed is None else seed,
        )
        started = time.monotonic()
        response = self.session.post(f"{self.server}/prompt", json={"prompt": workflow}, timeout=30)
        response.raise_for_status()
        payload = response.json()
        if payload.get("node_errors"):
            raise RuntimeError(f"ComfyUI rejected workflow: {payload['node_errors']}")
        prompt_id = payload["prompt_id"]
        deadline = started + self.timeout_seconds
        while time.monotonic() < deadline:
            history_response = self.session.get(f"{self.server}/history/{prompt_id}", timeout=30)
            history_response.raise_for_status()
            history = history_response.json().get(prompt_id)
            if history:
                status = history.get("status", {})
                if status.get("status_str") == "error":
                    raise RuntimeError(f"ComfyUI generation failed: {status}")
                images: list[Path] = []
                for node in history.get("outputs", {}).values():
                    for image in node.get("images", []):
                        if image.get("type") == "output":
                            images.append(self.comfy_root / "output" / image.get("subfolder", "") / image["filename"])
                if images:
                    return GenerationResult(prompt_id, tuple(images), time.monotonic() - started)
            time.sleep(2)
        raise TimeoutError(f"ComfyUI did not finish prompt {prompt_id} within {self.timeout_seconds}s")
