from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
from typing import Any, Iterable


PROJECT_DIR = Path(__file__).resolve().parents[3]
SESSION_FILE = PROJECT_DIR / "config" / "photoset_resume_session.json"
SESSION_VERSION = 1
RESUME_ARGUMENTS = {"l", "--resume-session", "--load-session", "--resume"}


class PhotosetSessionError(RuntimeError):
    pass


def resume_requested(args: Iterable[str]) -> bool:
    return any(str(argument).strip().lower() in RESUME_ARGUMENTS for argument in args)


def _now_text() -> str:
    return dt.datetime.now().astimezone().isoformat(timespec="seconds")


def _session_path(path: Path | None = None) -> Path:
    return Path(path) if path is not None else SESSION_FILE


def _validate_schedule_item(item: Any, index: int) -> dict[str, Any]:
    if not isinstance(item, dict):
        raise PhotosetSessionError(f"存档中的第 {index + 1} 个任务格式错误。")
    character = str(item.get("character", "")).strip()
    template_id = str(item.get("template_id", "")).strip()
    try:
        shot_index = int(item.get("shot_index"))
    except (TypeError, ValueError) as exc:
        raise PhotosetSessionError(f"存档中的第 {index + 1} 个任务缺少有效图片编号。") from exc
    if not character or not template_id or shot_index < 1:
        raise PhotosetSessionError(f"存档中的第 {index + 1} 个任务不完整。")
    return {
        "character": character,
        "template_id": template_id,
        "shot_index": shot_index,
    }


def load_session(path: Path | None = None) -> dict[str, Any]:
    session_path = _session_path(path)
    if not session_path.exists():
        raise PhotosetSessionError("没有找到可继续的 E/E2 模式进度。请先正常启动一次 E 或 E2。")
    try:
        data = json.loads(session_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise PhotosetSessionError(f"无法读取 E/E2 进度存档：{session_path}") from exc
    if not isinstance(data, dict) or data.get("version") != SESSION_VERSION:
        raise PhotosetSessionError("E/E2 进度存档版本无效，请正常启动新的 E/E2 任务覆盖它。")
    mode = str(data.get("mode", "")).upper()
    if mode not in {"E", "E2"}:
        raise PhotosetSessionError("E/E2 进度存档中的模式无效。")
    raw_schedule = data.get("schedule")
    if not isinstance(raw_schedule, list) or not raw_schedule:
        raise PhotosetSessionError("E/E2 进度存档中没有任务队列。")
    schedule = [_validate_schedule_item(item, index) for index, item in enumerate(raw_schedule)]
    try:
        next_index = int(data.get("next_index", 0))
    except (TypeError, ValueError) as exc:
        raise PhotosetSessionError("E/E2 进度存档中的当前位置无效。") from exc
    if not 0 <= next_index <= len(schedule):
        raise PhotosetSessionError("E/E2 进度存档中的当前位置超出任务范围。")
    data["mode"] = mode
    data["schedule"] = schedule
    data["next_index"] = next_index
    return data


def _write_session(data: dict[str, Any], path: Path | None = None) -> Path:
    session_path = _session_path(path)
    session_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = session_path.with_suffix(session_path.suffix + ".tmp")
    temporary_path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    temporary_path.replace(session_path)
    return session_path


def save_new_session(
    mode: str,
    schedule: Iterable[dict[str, Any]],
    scheduled_start: dt.datetime | None,
    path: Path | None = None,
) -> Path:
    normalized_mode = str(mode).upper()
    if normalized_mode not in {"E", "E2"}:
        raise PhotosetSessionError(f"不能为模式 {mode!r} 创建 E/E2 存档。")
    normalized_schedule = [
        _validate_schedule_item(item, index)
        for index, item in enumerate(schedule)
    ]
    if not normalized_schedule:
        raise PhotosetSessionError("不能保存空的 E/E2 任务队列。")
    now = _now_text()
    return _write_session(
        {
            "version": SESSION_VERSION,
            "mode": normalized_mode,
            "status": "active",
            "created_at": now,
            "updated_at": now,
            "scheduled_start": scheduled_start.isoformat(timespec="minutes") if scheduled_start else None,
            "next_index": 0,
            "schedule": normalized_schedule,
        },
        path,
    )


def mark_resume_started(
    scheduled_start: dt.datetime | None,
    path: Path | None = None,
) -> Path:
    data = load_session(path)
    data["status"] = "active"
    data["updated_at"] = _now_text()
    data["scheduled_start"] = scheduled_start.isoformat(timespec="minutes") if scheduled_start else None
    return _write_session(data, path)


def advance_session(next_index: int, path: Path | None = None) -> Path:
    data = load_session(path)
    bounded_index = max(data["next_index"], min(int(next_index), len(data["schedule"])))
    data["next_index"] = bounded_index
    data["updated_at"] = _now_text()
    data["status"] = "completed" if bounded_index >= len(data["schedule"]) else "active"
    return _write_session(data, path)


def resumable_mode(path: Path | None = None) -> str:
    data = load_session(path)
    if data["next_index"] >= len(data["schedule"]):
        raise PhotosetSessionError("上一次 E/E2 任务已经全部完成，没有尚未生成的图片。")
    return data["mode"]
