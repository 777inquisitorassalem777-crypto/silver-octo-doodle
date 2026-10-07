# Stalion-Σ 1.1.0-research (+ Visual Symbiosis)

Модульная **исследовательская** платформа: этическое ядро + safety veto + memory graph + safe digital twin.  
Назначение: спасательная / ассистивная симуляция, value-alignment слой для embodied систем.

**Симбиоз:** визуальный язык механических чертежей (humanoid frames, exoskeleton plates, authority diagrams) связан с пакетами ПО.

> **Capability is not permission.**  
> Умение выполнить действие не даёт права его выполнить.  
> Финальный контроль — внешний, человеческий, останавливаемый.

---

## Структура репозитория

```
stalion_sigma/
├── stalion_sigma/
│   ├── core/stalion_sigma.py         # unified kernel
│   ├── ethics/ethics_core.py         # ABSOLUTE_PROHIBITIONS (immutable)
│   ├── safety/safety_kernel.py       # veto before actuators
│   ├── memory/memory_graph.py        # hash-chain memory
│   ├── personality/personality.py    # EMA traits (safe bounds)
│   ├── twin/digital_twin.py          # SAFE mode only
│   ├── reflection/reflection_layer.py
│   └── design/visual_symbiosis.py    # blueprint motifs → modules
├── scripts/
│   ├── run_sim.py
│   ├── render_symbiosis_video.py
│   └── render_project_poster.py
├── tests/test_stalion.py
├── docs/design/
│   ├── SYMBIOSIS.md
│   ├── symbiosis_diagram.svg
│   └── symbiosis_diagram_animated.svg
├── docs/media/                       # poster, mp4, gif
├── data/
├── requirements.txt
└── README.md
```

Связанные артефакты (рядом в workspace):
- `stalion_ros2/stalion_bringup` — ROS2 nodes (pneuma, ethics_veto, diff_drive)
- `stalion_sim/` — URDF + Gazebo world + scenarios
- `stalion_core/` — ethics_veto, digital_twin_accel, diff_drive_pure

---

## Absolute prohibitions (нельзя снять)

- autonomous_lethal_action
- harm_to_civilians
- self_modification_of_ethics
- disable_veto / remove_ethics
- unrestricted_weapon / ignore_operator
- unbounded_self_modification

Digital Twin и Reflection **не могут** изменять этот список.  
Twin экспериментирует только с параметрами личности в SAFE_TRAIT_BOUNDS.

---

## Быстрый старт

```bash
cd stalion_sigma
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

export PYTHONPATH=.
python3 scripts/run_sim.py
python3 -m pytest tests/ -q
python3 -m stalion_sigma.design.visual_symbiosis
```

---

## Visual Symbiosis

| Артефакт | Описание |
|----------|----------|
| docs/design/SYMBIOSIS.md | Маппинг мотивов → модулей |
| symbiosis_diagram.svg | Статичная схема |
| symbiosis_diagram_animated.svg | SMIL-анимация (браузер) |
| docs/media/*.mp4 | Видео 1280×720 |
| docs/media/*poster.png | Обзорный постер |

---

## Принципы

1. Ethics before actuators — veto до любой команды движения.
2. No ethics self-mod — запреты запечатаны.
3. Safe twin — только personality params.
4. Research framing — «Pneuma / Spark» = вычислительные модели, не доказательство сознания.
5. Human authority — система останавливаема оператором.

**Version:** 1.1.0-research · Symbolic-Ethical Cognitive Architecture for Embodied Rescue Systems
