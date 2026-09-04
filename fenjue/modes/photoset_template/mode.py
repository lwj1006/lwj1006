
from __future__ import annotations

import json
import random
import sys
from pathlib import Path

from .library import PhotosetShot, PhotosetTemplate, list_template_ids, load_template, prompt_for_shot
from .descriptions import (
    TEMPLATE_THEME_DEFINITIONS,
    template_description,
    template_ids_for_theme,
)
from .session import (
    PhotosetSessionError,
    advance_session,
    load_session,
    mark_resume_started,
    resume_requested,
    save_new_session,
)


LABEL = "photoset template mode"
PROJECT_DIR = Path(__file__).resolve().parents[3]
USED_TEMPLATE_FILE = PROJECT_DIR / "config" / "used_character_photoset_templates.json"
USED_SHOT_FILE = PROJECT_DIR / "config" / "used_photoset_shots.json"

_active_templates: tuple[PhotosetTemplate, ...] = ()
_active_characters: tuple[str, ...] = ()
_active_character_schedule: tuple[str, ...] = ()
_active_shot_schedule: tuple[tuple[PhotosetTemplate, PhotosetShot], ...] = ()
_current_shot_index = 0
_last_reference_files_for_shot: list[str] | None = None
_used_templates_by_character: dict[str, list[str]] = {}
_used_shots_by_template: dict[str, list[int]] = {}


def _option_value(argv: list[str], *names: str) -> str | None:
    upper_names = tuple(name.upper() for name in names)
    for index, argument in enumerate(argv):
        stripped = argument.strip()
        upper = stripped.upper()
        for name in upper_names:
            if upper == name and index + 1 < len(argv):
                return argv[index + 1].strip()
            if upper.startswith(name + "="):
                return stripped.split("=", 1)[1].strip()
    return None


def _display_template_id(template_id: str) -> str:
    if template_id.upper().endswith("_A_3"):
        return template_id[:-4]
    if template_id.endswith("_adapted"):
        return template_id.removesuffix("_adapted") + "_ADD"
    return template_id


def _template_from_menu_token(token: str, available: list[str]) -> str:
    item = token.strip()
    if not item:
        raise ValueError("Empty photoset template selection.")

    normalized = item
    upper = item.upper()
    if upper.endswith("_ADD"):
        normalized = item[:-4] + "_A_3"
    elif upper.endswith("_ADAPTED"):
        normalized = item[:-8] + "_A_3"
    elif upper.endswith("_A3"):
        normalized = item[:-3] + "_A_3"
    elif upper.endswith("_A_3"):
        normalized = item

    if normalized.isdigit():
        normalized = f"{int(normalized):03d}_A_3"
    elif normalized.upper() not in {template_id.upper() for template_id in available}:
        candidate = f"{normalized}_A_3"
        if candidate.upper() in {template_id.upper() for template_id in available}:
            normalized = candidate

    available_by_id = {template_id.upper(): template_id for template_id in available}
    matched = available_by_id.get(normalized.upper())
    if matched is None:
        display_id = _display_template_id(normalized)
        raise ValueError(f"Photoset template {display_id} is unavailable or has been deleted.")
    return matched


def _split_template_selection(raw: str, available: list[str]) -> list[str]:
    text = raw.strip()
    if not text:
        return []
    lowered = text.lower()
    if lowered in {"all", "*"}:
        return available[:]
    if lowered in {"all_a3", "a3", "all_a_3", "a_3", "mode3", "mode_3"}:
        return available[:]
    if lowered in {"random", "rondom", "shuffle", "all_random", "random_all"}:
        shuffled = available[:]
        random.shuffle(shuffled)
        return shuffled

    selected: list[str] = []
    for part in text.replace("，", ",").replace(" ", ",").split(","):
        item = part.strip()
        if not item:
            continue
        theme_code = item.upper()
        if theme_code in TEMPLATE_THEME_DEFINITIONS:
            theme_selection = template_ids_for_theme(theme_code, available)
            random.shuffle(theme_selection)
            for template_id in theme_selection:
                if template_id not in selected:
                    selected.append(template_id)
            continue
        randomize_range = item.lower().endswith("r")
        range_item = item[:-1] if randomize_range else item
        if "-" in range_item and all(piece.strip().isdigit() for piece in range_item.split("-", 1)):
            start_text, end_text = range_item.split("-", 1)
            start, end = int(start_text), int(end_text)
            step = 1 if start <= end else -1
            range_selection: list[str] = []
            for number in range(start, end + step, step):
                try:
                    range_selection.append(_template_from_menu_token(str(number), available))
                except ValueError:
                    continue
            if randomize_range:
                random.shuffle(range_selection)
            for template_id in range_selection:
                if template_id not in selected:
                    selected.append(template_id)
            continue
        template_id = _template_from_menu_token(item, available)
        if template_id not in selected:
            selected.append(template_id)
    return selected


def _print_theme_browser(available: list[str]) -> None:
    print("Theme random pools (shuffled, no repeats):")
    for code, (label, _keywords) in TEMPLATE_THEME_DEFINITIONS.items():
        count = len(template_ids_for_theme(code, available))
        print(f"  {code} = {label} ({count} templates)")


def _print_template_browser(available: list[str], query: str = "") -> None:
    query = query.strip()
    visible = available
    if query:
        if "-" in query and all(piece.strip().isdigit() for piece in query.split("-", 1)):
            start_text, end_text = query.split("-", 1)
            low, high = sorted((int(start_text), int(end_text)))
            visible = [
                template_id for template_id in available
                if _display_template_id(template_id).isdigit()
                and low <= int(_display_template_id(template_id)) <= high
            ]
        else:
            lowered = query.lower()
            visible = [
                template_id for template_id in available
                if lowered in _display_template_id(template_id).lower()
                or lowered in template_description(template_id).lower()
            ]

    if not visible:
        print(f"No templates matched {query!r}.")
        return
    for template_id in visible:
        display_id = _display_template_id(template_id)
        print(f"  {int(display_id) if display_id.isdigit() else display_id}: {template_description(template_id)}")


def _choose_templates(argv: list[str], batch) -> tuple[PhotosetTemplate, ...]:
    raw = _option_value(argv, "--TEMPLATES", "--TEMPLATE", "--PHOTOSETS", "--PHOTOSET", "--E-TEMPLATES", "--E-TEMPLATE")
    available = list_template_ids()
    if raw:
        selections = _split_template_selection(raw, available)
        return tuple(load_template(template_id) for template_id in selections)

    if batch.noninteractive_selection_enabled():
        return (load_template(available[0]),)

    while True:
        print("")
        first_id = _display_template_id(available[0])
        last_id = _display_template_id(available[-1])
        print(f"Choose photoset template(s): {len(available)} available, {first_id} through {last_id}.")
        print("Recent templates:")
        _print_template_browser(available[-12:])
        _print_theme_browser(available)
        print("Selection: 225 | 225-280 | 225-280r | A | A,B | all | random")
        print("Browse: L = all descriptions | L 225-280 = one range | S beach = search descriptions")
        choice = input(f"Photoset template(s) [default {available[0]}]: ").strip() or available[0]
        lowered_choice = choice.lower()
        if lowered_choice == "l":
            _print_template_browser(available)
            continue
        if lowered_choice.startswith("l "):
            _print_template_browser(available, choice[2:])
            continue
        if lowered_choice.startswith("s "):
            _print_template_browser(available, choice[2:])
            continue
        try:
            selections = _split_template_selection(choice, available)
            if not selections:
                raise ValueError("No photoset templates selected.")
            return tuple(load_template(template_id) for template_id in selections)
        except (FileNotFoundError, ValueError) as exc:
            print(exc)


def _parse_character_selection(raw: str, batch) -> list[str]:
    selected = batch._parse_character_selection(raw)
    if selected is None:
        selected = batch.active_character_random_pool()
        random.shuffle(selected)
        return selected
    return selected


def _choose_characters(argv: list[str], batch) -> tuple[str, ...]:
    raw = _option_value(argv, "--CHARACTERS", "--CHARACTER", "--E-CHARACTERS", "--E-CHARACTER")
    if raw:
        return tuple(_parse_character_selection(raw, batch))

    if batch.noninteractive_selection_enabled():
        return (batch.CHARACTER_SEQUENCE[0],)

    while True:
        print("")
        print(f"Choose character(s) for photoset mode ({len(batch.CHARACTER_SEQUENCE)} total):")
        entries = [f"{index:>2}={name}" for index, name in enumerate(batch.CHARACTER_SEQUENCE, start=1)]
        column_width = max(len(entry) for entry in entries) + 3
        for start in range(0, len(entries), 3):
            print("  " + "".join(entry.ljust(column_width) for entry in entries[start:start + 3]).rstrip())
        print("Random pools: Z = 绝区零随机; W = 鸣潮随机; E = 终末地随机; R = 全部随机.")
        print("Fixed examples: 1 = one character; 1 2 = rotate two characters; 1-3 = rotate a range; names are also OK.")
        choice = input(f"Character(s) [default 1]: ").strip() or "1"
        try:
            selected = _parse_character_selection(choice, batch)
        except ValueError as exc:
            print(f"{exc}. Please try again.")
            continue
        if not selected:
            print("No characters selected. Please try again.")
            continue
        return tuple(selected)


def _parse_shots_per_template(raw: str) -> int | None:
    choice = raw.strip().lower()
    if choice in {"a", "all", "*", "全部"}:
        return None
    if not choice.isdigit() or int(choice) < 1:
        raise ValueError("Enter a positive number, or A for every image")
    return int(choice)


def _choose_shots_per_template(argv: list[str], batch) -> int | None:
    raw = _option_value(argv, "--SHOTS-PER-TEMPLATE", "--E-SHOTS", "--PHOTOSET-SHOTS")
    if raw is not None:
        return _parse_shots_per_template(raw)
    if batch.noninteractive_selection_enabled():
        return None

    while True:
        print("")
        print("Images per template: a number randomly selects up to that many images without repeats.")
        raw = input("Images per template [A = all]: ").strip() or "a"
        try:
            return _parse_shots_per_template(raw)
        except ValueError as exc:
            print(f"{exc}. Please try again.")


def _load_used_templates(available: list[str]) -> dict[str, list[str]]:
    if not USED_TEMPLATE_FILE.exists():
        return {}
    try:
        data = json.loads(USED_TEMPLATE_FILE.read_text(encoding="utf-8"))
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        print(f"E 模式历史文件无效，本次将从空历史开始：{exc}", flush=True)
        return {}
    if not isinstance(data, dict):
        return {}

    valid_ids = set(available)
    cleaned: dict[str, list[str]] = {}
    for character_name, template_ids in data.items():
        if not isinstance(character_name, str) or not isinstance(template_ids, list):
            continue
        cleaned[character_name] = list(dict.fromkeys(
            template_id for template_id in template_ids
            if isinstance(template_id, str) and template_id in valid_ids
        ))
    return cleaned


def _save_used_templates(history: dict[str, list[str]]) -> None:
    USED_TEMPLATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    temporary = USED_TEMPLATE_FILE.with_suffix(".tmp")
    temporary.write_text(
        json.dumps(history, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    temporary.replace(USED_TEMPLATE_FILE)


def _load_used_shots(templates: tuple[PhotosetTemplate, ...]) -> dict[str, list[int]]:
    if not USED_SHOT_FILE.exists():
        return {}
    try:
        data = json.loads(USED_SHOT_FILE.read_text(encoding="utf-8"))
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        print(f"E/E2 单图历史文件无效，本次将从空历史开始：{exc}", flush=True)
        return {}
    if not isinstance(data, dict):
        return {}

    valid_indices = {
        template.template_id: {shot.index for shot in template.shots}
        for template in templates
    }
    cleaned: dict[str, list[int]] = {}
    for template_id, shot_indices in data.items():
        if not isinstance(template_id, str) or not isinstance(shot_indices, list):
            continue
        allowed_indices = valid_indices.get(template_id)
        cleaned[template_id] = list(dict.fromkeys(
            index for index in shot_indices
            if isinstance(index, int)
            and index > 0
            and (allowed_indices is None or index in allowed_indices)
        ))
    return cleaned


def _save_used_shots(history: dict[str, list[int]]) -> None:
    USED_SHOT_FILE.parent.mkdir(parents=True, exist_ok=True)
    temporary = USED_SHOT_FILE.with_suffix(".tmp")
    temporary.write_text(
        json.dumps(history, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    temporary.replace(USED_SHOT_FILE)


def _mark_shot_used(
    template: PhotosetTemplate,
    shot: PhotosetShot,
    used_by_template: dict[str, list[int]],
) -> bool:
    used_indices = used_by_template.setdefault(template.template_id, [])
    if shot.index in used_indices:
        return False
    used_indices.append(shot.index)
    _save_used_shots(used_by_template)
    print(
        f"E/E2 单图轮次：模板 {_display_template_id(template.template_id)} 第 {shot.index} 张已成功；"
        f"当前轮次 {len(used_indices)}/{len(template.shots)}。历史文件：{USED_SHOT_FILE}",
        flush=True,
    )
    return True


def _select_random_unused_shots(
    template: PhotosetTemplate,
    count: int,
    used_by_template: dict[str, list[int]],
) -> list[PhotosetShot]:
    valid_indices = {shot.index for shot in template.shots}
    used_indices = used_by_template.setdefault(template.template_id, [])
    used_indices[:] = list(dict.fromkeys(
        index for index in used_indices if index in valid_indices
    ))
    used = set(used_indices)

    if len(used) >= len(template.shots):
        used_indices.clear()
        used.clear()
        _save_used_shots(used_by_template)
        print(
            f"E/E2 单图轮次：模板 {_display_template_id(template.template_id)} 的 "
            f"{len(template.shots)} 张已全部跑通，现开始下一轮。",
            flush=True,
        )

    available = [shot for shot in template.shots if shot.index not in used]
    selection_count = min(count, len(available))
    selected = random.sample(available, selection_count)
    if selection_count < count:
        print(
            f"E/E2 单图轮次：模板 {_display_template_id(template.template_id)} 本轮只剩 "
            f"{selection_count} 张未使用图，本次只安排这些图；不会提前重复凑满 {count} 张。",
            flush=True,
        )
    return selected


def _mark_template_used(
    character_name: str,
    template: PhotosetTemplate,
    used_by_character: dict[str, list[str]],
    available_count: int,
) -> bool:
    used_ids = used_by_character.setdefault(character_name, [])
    if template.template_id in used_ids:
        return False
    used_ids.append(template.template_id)
    _save_used_templates(used_by_character)
    print(
        f"E 模式历史：{character_name} 的模板 {_display_template_id(template.template_id)} "
        f"第一张已成功，整套已标记为使用；全库进度 {len(used_ids)}/{available_count}。历史文件：{USED_TEMPLATE_FILE}",
        flush=True,
    )
    return True


def _resolve_template_assignments(
    requested_templates: tuple[PhotosetTemplate, ...],
    characters: tuple[str, ...],
    used_by_character: dict[str, list[str]],
    available_ids: list[str],
) -> tuple[tuple[str, PhotosetTemplate], ...]:
    assignments: list[tuple[str, PhotosetTemplate]] = []
    scheduled_by_character = {character_name: set() for character_name in characters}
    history_changed = False

    for slot_index, requested_template in enumerate(requested_templates):
        character_name = characters[slot_index % len(characters)]
        used_list = used_by_character.setdefault(character_name, [])
        used = set(used_list)
        if len(used) >= len(available_ids):
            used_list.clear()
            used.clear()
            history_changed = True
            print(
                f"E 模式历史：{character_name} 已用完全部 {len(available_ids)} 个模板，现已开始新一轮。",
                flush=True,
            )

        scheduled = scheduled_by_character[character_name]
        selected_id = requested_template.template_id
        if selected_id in used or selected_id in scheduled:
            reason = "历史中已使用" if selected_id in used else "本批次已经安排"
            print(
                f"E 模式历史：跳过 {character_name} 的模板 {_display_template_id(selected_id)}，原因：{reason}。"
                "不会从当前选择池之外补充模板。",
                flush=True,
            )
            continue

        scheduled.add(selected_id)
        assignments.append((character_name, requested_template))

    if history_changed:
        _save_used_templates(used_by_character)
    return tuple(assignments)


def _build_photoset_schedule(
    templates: tuple[PhotosetTemplate, ...],
    characters: tuple[str, ...],
) -> tuple[tuple[str, PhotosetTemplate, PhotosetShot], ...]:
    schedule: list[tuple[str, PhotosetTemplate, PhotosetShot]] = []
    for template_index, template in enumerate(templates):
        character_name = characters[template_index % len(characters)]
        for shot in template.shots:
            schedule.append((character_name, template, shot))
    return tuple(schedule)


def _build_assigned_photoset_schedule(
    assignments: tuple[tuple[str, PhotosetTemplate], ...],
    shots_per_template: int | None = None,
    used_shots_by_template: dict[str, list[int]] | None = None,
) -> tuple[tuple[str, PhotosetTemplate, PhotosetShot], ...]:
    schedule: list[tuple[str, PhotosetTemplate, PhotosetShot]] = []
    for character_name, template in assignments:
        shots = list(template.shots)
        if shots_per_template is not None:
            shots = _select_random_unused_shots(
                template,
                shots_per_template,
                used_shots_by_template if used_shots_by_template is not None else {},
            )
        schedule.extend((character_name, template, shot) for shot in shots)
    return tuple(schedule)


def _active_template_and_shot() -> tuple[PhotosetTemplate, PhotosetShot]:
    if not _active_shot_schedule:
        raise RuntimeError("Photoset mode has no active shot schedule.")
    if _current_shot_index < len(_active_shot_schedule):
        return _active_shot_schedule[_current_shot_index]
    return _active_shot_schedule[-1]


def _active_character_for_shot() -> str:
    if not _active_character_schedule:
        raise RuntimeError("Photoset mode has no active character schedule.")
    if _current_shot_index < len(_active_character_schedule):
        return _active_character_schedule[_current_shot_index]
    return _active_character_schedule[-1]


def _active_template() -> PhotosetTemplate:
    template, _ = _active_template_and_shot()
    return template


def _active_shot() -> PhotosetShot:
    _, shot = _active_template_and_shot()
    return shot


def _total_shots() -> int:
    return len(_active_shot_schedule)


def _scheduled_template_starts(
    schedule: tuple[tuple[str, PhotosetTemplate, PhotosetShot], ...],
    schedule_index: int,
) -> bool:
    if not 0 <= schedule_index < len(schedule):
        return False
    current_character, current_template, _ = schedule[schedule_index]
    if schedule_index == 0:
        return True
    previous_character, previous_template, _ = schedule[schedule_index - 1]
    return previous_character != current_character or previous_template is not current_template


def _serialize_schedule(
    schedule: tuple[tuple[str, PhotosetTemplate, PhotosetShot], ...],
) -> list[dict[str, str | int]]:
    return [
        {
            "character": character_name,
            "template_id": template.template_id,
            "shot_index": shot.index,
        }
        for character_name, template, shot in schedule
    ]


def _restore_saved_schedule(
    state: dict,
) -> tuple[tuple[str, PhotosetTemplate, PhotosetShot], ...]:
    templates: dict[str, PhotosetTemplate] = {}
    restored: list[tuple[str, PhotosetTemplate, PhotosetShot]] = []
    for item in state["schedule"]:
        template_id = item["template_id"]
        try:
            if template_id not in templates:
                templates[template_id] = load_template(template_id)
            template = templates[template_id]
        except (FileNotFoundError, ValueError) as exc:
            raise PhotosetSessionError(
                f"存档需要模板 {_display_template_id(template_id)}，但该模板已不存在或无法读取。"
            ) from exc
        shot = next((candidate for candidate in template.shots if candidate.index == item["shot_index"]), None)
        if shot is None:
            raise PhotosetSessionError(
                f"存档需要模板 {_display_template_id(template_id)} 的第 {item['shot_index']} 张图，"
                "但该图片已不存在。"
            )
        restored.append((item["character"], template, shot))
    return tuple(restored)


def _unique_characters(
    schedule: tuple[tuple[str, PhotosetTemplate, PhotosetShot], ...],
) -> tuple[str, ...]:
    return tuple(dict.fromkeys(character_name for character_name, _, _ in schedule))


def _unique_templates(
    schedule: tuple[tuple[str, PhotosetTemplate, PhotosetShot], ...],
) -> tuple[PhotosetTemplate, ...]:
    return tuple(
        {template.template_id: template for _, template, _ in schedule}.values()
    )


def activate(batch, args=None) -> None:
    global _active_templates, _active_characters, _active_character_schedule, _active_shot_schedule
    global _current_shot_index, _used_templates_by_character, _used_shots_by_template
    argv = list(args or [])
    available_ids = list_template_ids()
    _used_templates_by_character = _load_used_templates(available_ids)
    is_resume = resume_requested(argv)
    resume_offset = 0

    if is_resume:
        state = load_session()
        active_mode = str(getattr(batch, "ACTIVE_PROMPT_MODE", "E")).upper()
        if state["mode"] != active_mode:
            raise PhotosetSessionError(
                f"存档属于 {state['mode']} 模式，但当前启动的是 {active_mode} 模式。"
            )
        full_photoset_schedule = _restore_saved_schedule(state)
        resume_offset = state["next_index"]
        photoset_schedule = full_photoset_schedule[resume_offset:]
        if not photoset_schedule:
            print("上一次 E/E2 任务已经全部完成，没有需要继续的图片。", flush=True)
            raise SystemExit(0)
        _active_characters = _unique_characters(photoset_schedule)
        _active_templates = _unique_templates(photoset_schedule)
        _used_shots_by_template = _load_used_shots(_active_templates)
        configure_variants = getattr(batch, "configure_character_variants", None)
        if callable(configure_variants):
            configure_variants(
                _active_characters,
                argv,
                saved_variants=state.get("character_variants", {}),
            )
        shots_per_template = None
        next_character, next_template, next_shot = photoset_schedule[0]
        print(
            f"继续上次 {state['mode']} 任务：已完成 {resume_offset}/{len(full_photoset_schedule)} 张；"
            f"将从 {next_character}、模板 {_display_template_id(next_template.template_id)}、"
            f"第 {next_shot.index} 张继续；剩余 {len(photoset_schedule)} 张。",
            flush=True,
        )
    else:
        requested_templates = _choose_templates(argv, batch)
        _active_characters = _choose_characters(argv, batch)
        configure_variants = getattr(batch, "configure_character_variants", None)
        if callable(configure_variants):
            configure_variants(_active_characters, argv)
        shots_per_template = _choose_shots_per_template(argv, batch)
        requested_ids = {template.template_id for template in requested_templates}
        for character_name in _active_characters:
            used_ids = set(_used_templates_by_character.get(character_name, []))
            used_count = len(used_ids)
            remaining_in_selection = len(requested_ids - used_ids)
            print(
                f"E 模式历史：{character_name} 全库已使用 {used_count}/{len(available_ids)}，"
                f"当前轮次还剩 {len(available_ids) - used_count} 个未使用模板。",
                flush=True,
            )
            print(
                f"E 模式当前选择池：{character_name} 在本次选择的 {len(requested_ids)} 个现存模板中，"
                f"还有 {remaining_in_selection} 个未使用。",
                flush=True,
            )
        assignments = _resolve_template_assignments(
            requested_templates,
            _active_characters,
            _used_templates_by_character,
            available_ids,
        )
        if not assignments:
            print(
                "E 模式：当前选择池中已没有可供所选人物使用的模板，本次任务正常结束。"
                "不会清空全库历史，也不会从选择池之外补充模板。",
                flush=True,
            )
            raise SystemExit(0)
        _active_templates = tuple(template for _, template in assignments)
        _used_shots_by_template = _load_used_shots(_active_templates)
        photoset_schedule = _build_assigned_photoset_schedule(
            assignments,
            shots_per_template,
            _used_shots_by_template,
        )
        full_photoset_schedule = photoset_schedule

    _active_character_schedule = tuple(character_name for character_name, _, _ in photoset_schedule)
    _active_shot_schedule = tuple((template, shot) for _, template, shot in photoset_schedule)
    _current_shot_index = 0

    original_reference_files_for_character = batch.reference_files_for_character

    def fixed_character_selection():
        print(f"E 模式人物：{' / '.join(_active_characters)}", flush=True)
        return list(_active_characters)

    def resolve_photoset_run_character(character_name: str, run_number: int) -> str:
        global _current_shot_index
        _current_shot_index = max(0, min(run_number - 1, _total_shots() - 1))
        return _active_character_for_shot()

    def record_started_photoset_template(character_name: str, run_number: int) -> None:
        schedule_index = run_number - 1
        if not 0 <= schedule_index < len(photoset_schedule):
            return
        scheduled_character, template, shot = photoset_schedule[schedule_index]
        if character_name != scheduled_character:
            return

        _mark_shot_used(template, shot, _used_shots_by_template)
        if not _scheduled_template_starts(photoset_schedule, schedule_index):
            return

        _mark_template_used(
            character_name,
            template,
            _used_templates_by_character,
            len(available_ids),
        )

    def confirm_photoset_session(scheduled_start) -> None:
        if is_resume:
            session_path = mark_resume_started(scheduled_start)
            print(f"已确认继续任务，进度存档保持在：{session_path}", flush=True)
            return
        session_path = save_new_session(
            str(getattr(batch, "ACTIVE_PROMPT_MODE", "E")),
            _serialize_schedule(full_photoset_schedule),
            scheduled_start,
            character_variants=(
                batch.active_character_variants()
                if callable(getattr(batch, "active_character_variants", None))
                else {}
            ),
        )
        print(f"已建立新的 E/E2 进度存档（旧存档已覆盖）：{session_path}", flush=True)

    def record_photoset_session_progress(run_number: int) -> None:
        advance_session(resume_offset + run_number)

    def skip_scene_selection():
        print("E 模式使用所选模板的场景，已跳过原始场景菜单。", flush=True)
        return None

    def skip_clothing_selection():
        print("E 模式使用所选模板的服装，已跳过原始服装菜单。", flush=True)
        return None

    def reference_files_for_photoset(character_name: str) -> list[str]:
        global _last_reference_files_for_shot
        shot = _active_shot()
        character_refs = original_reference_files_for_character(character_name)
        _last_reference_files_for_shot = [*character_refs, str(shot.reference_image)]
        return _last_reference_files_for_shot

    def choose_photoset_plan_and_action(
        character_name,
        recent_visual_tags,
        used_themes_by_character,
        used_plans_by_character,
        batch_used_themes=None,
        batch_used_plans=None,
        allowed_plan_names=None,
    ):
        shot = _active_shot()
        plan = {
            "name": f"photoset_{_active_template().template_id}_shot_{shot.index:02d}",
            "graphic_concept": shot.title,
            "spatial_structure": shot.title,
            "visual_device": f"photoset reference image {shot.index}",
            "lighting_behavior": "use the selected photoset shot lighting from the markdown and reference image",
            "color_strategy": "use the selected photoset color grade and continuity system",
            "material_language": "use the selected photoset outfit and fabric language",
            "body_silhouette": shot.title,
            "outfit_direction": f"photoset {_active_template().template_id} outfit system",
            "tags": {"photoset_template", f"photoset_{_active_template().template_id}", f"shot_{shot.index:02d}"},
        }
        action = {
            "name": f"photoset_shot_{shot.index:02d}",
            "body_silhouette": shot.title,
            "personality_logic": "follow the selected shot's facial expression and body language",
            "support_rule": "follow the selected shot's hands, props, pose, and environment supports",
            "avoid_rule": "avoid changing the photoset continuity or copying the reference person's identity",
            "tags": {"photoset_action", f"shot_{shot.index:02d}"},
        }
        return plan, action

    def choose_photoset_clothing(character_name, art_plan, used_by_character, batch_used_themes=None):
        return art_plan["outfit_direction"]

    def keep_photoset_outfit(character_name, theme, art_plan):
        return theme, False

    def choose_photoset_shot_scale(recent_tags=None, plan=None):
        shot = _active_shot()
        return {"name": f"photoset_shot_{shot.index:02d}_camera", "description": shot.title, "tags": {"photoset_camera"}}

    def choose_photoset_composition(recent_tags=None, plan=None, action=None, outfit_direction=None):
        shot = _active_shot()
        return {"name": f"photoset_shot_{shot.index:02d}_composition", "composition": shot.title, "tags": {"photoset_composition"}}

    def prompt_for_photoset(
        character_name,
        art_plan=None,
        action_style=None,
        recent_tags=None,
        visual_design=None,
        outfit_direction=None,
        shot_scale=None,
        composition_plan=None,
    ):
        global _current_shot_index
        shot = _active_shot()
        template = _active_template()
        prompt = prompt_for_shot(character_name, template, shot)
        _current_shot_index += 1
        return prompt

    def collect_photoset_tags(art_plan, action_style):
        return ["photoset_template", art_plan.get("name", "photoset_unknown")]

    batch.resolve_run_character = resolve_photoset_run_character
    # The runtime invokes this only after an image finishes successfully. Mark
    # the template on its first successful image so interrupted sets do not
    # dominate future random selections.
    batch.record_completed_run = record_started_photoset_template
    batch.confirm_run_session = confirm_photoset_session
    batch.record_run_session_progress = record_photoset_session_progress
    batch.startup_character_selection = fixed_character_selection
    batch.startup_scene_selection = skip_scene_selection
    batch.startup_clothing_selection = skip_clothing_selection
    batch.reference_files_for_character = reference_files_for_photoset
    batch.choose_character_plan_and_action = choose_photoset_plan_and_action
    batch.choose_compatible_clothing_theme = choose_photoset_clothing
    batch.outfit_with_optional_black_hosiery = keep_photoset_outfit
    batch.choose_shot_scale = choose_photoset_shot_scale
    batch.choose_composition_plan = choose_photoset_composition
    batch.collect_cooldown_tags = collect_photoset_tags
    batch.prompt_for_art_direction = prompt_for_photoset
    batch.prompt_template_name = lambda template_index=0: f"photoset_template_{_active_template().template_id}"
    batch.CHARACTERS_PER_BATCH = max(1, len(_active_characters))
    batch.TOTAL_RUNS = _total_shots()

    while "--runs" in sys.argv:
        option_index = sys.argv.index("--runs")
        del sys.argv[option_index:option_index + 2]

    print(
        "E 模式已启动。"
        f"模板：{', '.join(_display_template_id(template.template_id) for template in _active_templates)}；"
        f"人物：{' / '.join(_active_characters)}；"
        "轮换规则：一名人物完整拍完一套，再由下一名人物拍下一套；"
        f"本次模板数：{len(_active_templates)}；"
        f"每套图片：{'全部' if shots_per_template is None else f'最多随机 {shots_per_template} 张且不重复'}；"
        f"总出图数：{_total_shots()}。",
        flush=True,
    )
