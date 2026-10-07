# Stalion-Σ Visual Symbiosis

Интеграция визуального языка механических / steampunk-чертежей в архитектуру проекта.

## Принцип симбиоза

| Чертёжный мотив | Модуль ПО | Смысл |
|-----------------|-----------|--------|
| Humanoid full-body blueprint | `core.stalion_sigma` | Единый цикл embodiment |
| Exoskeleton / piston joints | `safety.safety_kernel` | Контроль актуаторов, scale/veto |
| Exploded assembly plates | package layout | Каждый пакет = «пластина» |
| **Authority is not computed** | `ethics.ethics_core` | Capability ≠ Permission |
| Coil / resonance apparatus | `reflection` + pneuma heuristic | Метафора когерентности |
| Multi-lens head cluster | edge / detectors | Сенсорный стек |

## Жёсткое правило (из диаграммы Authority)

> **Capability is not permission.**  
> Умение выполнить действие не даёт права его выполнить.  
> Финальный контроль — внешний, человеческий, останавливаемый.

Это уже реализовано как:

- `ABSOLUTE_PROHIBITIONS` (immutable)
- `SafetyKernel.veto_command` до любого motion
- Digital Twin **не может** трогать ethics keys

## Что НЕ интегрируется в код

Следующие визуальные мотивы **исключены из реализации**:

- формы взрывных устройств
- режущие диски / оружейные end-effector’ы
- автономные lethal-механизмы

Они остаются только как «анти-паттерны» в `EXCLUDED_FROM_IMPLEMENTATION`.

## Структура design-слоя

```
stalion_sigma/design/visual_symbiosis.py  — ModuleRegistry + SymbiosisManifest
docs/design/SYMBIOSIS.md                  — этот документ
```

## Запуск манифеста

```bash
export PYTHONPATH=.
python3 -m stalion_sigma.design.visual_symbiosis
```

## Симбиоз с ядром

```
[ Blueprint aesthetics ]
        ↓ maps to
[ Module plates / packages ]
        ↓ gated by
[ Ethics absolute + Safety veto ]
        ↓ optional
[ Digital Twin: personality only ]
```

Research-only. Не production autonomy.
