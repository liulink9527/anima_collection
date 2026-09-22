#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IELTS Dopamine OS — 动漫大乱斗篇 (PyQt6 版)
============================================
融合动漫角色收藏的雅思学习激励系统。
核心：学习→抽卡→收藏角色→专武精炼→羁绊加成

[版本记录]
v7:
  - 三星祈愿改为掉落通用材料「💫 星尘」×1~3（不再绑定具体角色）
  - 星尘兑换：10 → 随机三星 ｜ 30 → 随机四星 ｜ 70 → 随机五星
    （优先未拥有角色；重复 → 星辉 + 专武精炼+1）
  - 祈愿页新增「星尘兑换所」；兑换出五星同样触发金光动画
  - 状态栏常驻星尘余额；商店五星自选礼包改为星尘礼包
  - 旧存档角色碎片按 1:1 自动折算为星尘
v6: 三星掉落角色碎片（已被 v7 取代）
v5: XP 商店改为祈愿资源商店；双倍经验卡真实生效
v4: 羁绊图鉴/IP图鉴 Tab；专武系统
v3: 角色库外置 anime_characters.py；技能还原原作不关联学习
v2: 委托/周Boss 计时制；星辉商店修复
"""

import sys
import os
import json
import random
from datetime import datetime, date, timedelta

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QLabel, QPushButton, QFrame, QScrollArea, QGridLayout,
    QProgressBar, QMessageBox, QDialog, QTextEdit, QSpinBox,
    QGraphicsDropShadowEffect, QSizePolicy, QSpacerItem,
    QTableWidget, QTableWidgetItem, QHeaderView, QListWidget,
    QCheckBox, QMenu, QDialogButtonBox
)
from PyQt6.QtCore import Qt, QTimer, QSize, pyqtSignal, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import (
    QPixmap, QPainter, QColor, QFont, QPen, QBrush, QLinearGradient,
    QPainterPath, QIcon, QPalette
)

from anime_characters import (
    FIVE_STAR_CHARS, FOUR_STAR_CHARS, THREE_STAR_CHARS,
    FIVE_STAR_SKILLS, FOUR_STAR_SKILLS, ALL_SKILLS,
    BOND_SET_BONUSES, WEEKLY_THEMES, THEME_BONDS,
    THEMES, UP_ROTATION, CHAR_VOCABULARY, GENERAL_VOCABULARY,
)
from signature_weapons import SIGNATURE_WEAPONS

# ============================================================
# 常量 & 数据
# ============================================================
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ielts_data.json")

WEEKLY_BOSS_MINUTES = 240

# [v7] 星尘：三星祈愿掉落 ×1~3；兑换随机角色
STARDUST_NEEDED = {3: 10, 4: 30, 5: 70}
STARDUST_DROP = (1, 3)

STARGITTER_SHOP = [
    {"item": "纠缠之缘 ×1", "cost": 5, "type": "fate", "amount": 1},
    {"item": "双倍经验卡 ×1（下次Session XP翻倍）", "cost": 10, "type": "double_card", "amount": 1},
    {"item": "原石 ×160", "cost": 2, "type": "primogem", "amount": 160},
]

# [v5/v7] XP 商店：祈愿资源商店（不兑换现实物品）
SHOP_ITEMS = [
    {"xp": 300, "label": "⚡ 双倍经验卡 ×1", "type": "double_card", "amount": 1},
    {"xp": 500, "label": "💠 原石 ×100", "type": "primogem", "amount": 100},
    {"xp": 800, "label": "✨ 星辉 ×5", "type": "starglitter", "amount": 5},
    {"xp": 1000, "label": "🎴 纠缠之缘 ×1", "type": "fate", "amount": 1},
    {"xp": 2400, "label": "🎴 纠缠之缘 ×3（省 600 XP）", "type": "fate", "amount": 3},
    {"xp": 1200, "label": "💫 星尘 ×20", "type": "stardust", "amount": 20},
    {"xp": 3000, "label": "💫 星尘 ×55（可直接兑换随机五星）", "type": "stardust", "amount": 55},
]

COMMISSION_TEMPLATES = [
    {"id": "c1", "desc": "完成 1 个学习 Session",
     "check": lambda d: d.get("today_sessions", 0) >= 1, "reward": 30},
    {"id": "c2", "desc": "今日累计学习 ≥ 30 分钟",
     "check": lambda d: d.get("today_study_minutes", 0) >= 30, "reward": 30},
    {"id": "c3", "desc": "完成 2 个学习 Session",
     "check": lambda d: d.get("today_sessions", 0) >= 2, "reward": 40},
    {"id": "c4", "desc": "今日累计学习 ≥ 60 分钟",
     "check": lambda d: d.get("today_study_minutes", 0) >= 60, "reward": 40},
]

ANIME_THEME_MAP = {
    "onepiece": "海贼王",
    "naruto": "火影忍者",
    "demonslayer": "鬼灭之刃",
    "eva": "新世纪福音战士",
    "sao": "刀剑神域",
}

ACHIEVEMENTS = [
    {"id": "first_wish", "name": "初次祈愿", "desc": "完成第一次抽卡", "reward": 100,
     "check": lambda d: d["wish"]["total_wishes"] >= 1},
    {"id": "first_5star", "name": "金光乍现", "desc": "获得第一个五星角色", "reward": 300,
     "check": lambda d: d["wish"]["five_star_count"] >= 1},
    {"id": "wish_10", "name": "十连之始", "desc": "累计抽卡 10 次", "reward": 80,
     "check": lambda d: d["wish"]["total_wishes"] >= 10},
    {"id": "wish_50", "name": "祈愿达人", "desc": "累计抽卡 50 次", "reward": 200,
     "check": lambda d: d["wish"]["total_wishes"] >= 50},
    {"id": "wish_100", "name": "抽卡狂魔", "desc": "累计抽卡 100 次", "reward": 500,
     "check": lambda d: d["wish"]["total_wishes"] >= 100},
    {"id": "collect_3", "name": "初结伙伴", "desc": "收集 3 个不同角色", "reward": 150,
     "check": lambda d: len([k for k, v in d["characters"].items() if v.get("count", 0) > 0]) >= 3},
    {"id": "collect_all_4star", "name": "四星收藏家", "desc": "收集 20 个不同四星角色", "reward": 400,
     "check": lambda d: len([c for c in FOUR_STAR_CHARS if c in d["characters"]]) >= 20},
    {"id": "collect_50", "name": "收藏大亨", "desc": "收集 50 个不同角色", "reward": 800,
     "check": lambda d: len([k for k, v in d["characters"].items() if v.get("count", 0) > 0]) >= 50},
    {"id": "weapon_10", "name": "神兵收藏家", "desc": "解锁 10 把专武", "reward": 300,
     "check": lambda d: sum(1 for cid in SIGNATURE_WEAPONS
                            if d["characters"].get(cid, {}).get("count", 0) >= 1) >= 10},
    {"id": "weapon_r5", "name": "满炼大师", "desc": "任意专武达到 R5", "reward": 500,
     "check": lambda d: any(d["characters"].get(cid, {}).get("count", 0) >= 5
                            for cid in SIGNATURE_WEAPONS)},
    # [v7] 星尘成就
    {"id": "first_synth", "name": "星尘炼成师", "desc": "首次用星尘兑换角色", "reward": 200,
     "check": lambda d: d.get("synth_count", 0) >= 1},
    {"id": "synth_5star", "name": "摘星者", "desc": "用星尘兑换一个五星角色", "reward": 500,
     "check": lambda d: d.get("synth_5star_count", 0) >= 1},
    {"id": "session_10", "name": "初出茅庐", "desc": "累计完成 10 个 Session", "reward": 100,
     "check": lambda d: sum(1 for r in d["history"] if r.get("type") in ("完成奖励", "学习")) >= 10},
    {"id": "session_50", "name": "勤学不辍", "desc": "累计完成 50 个 Session", "reward": 300,
     "check": lambda d: sum(1 for r in d["history"] if r.get("type") in ("完成奖励", "学习")) >= 50},
    {"id": "session_100", "name": "雅思老兵", "desc": "累计完成 100 个 Session", "reward": 600,
     "check": lambda d: sum(1 for r in d["history"] if r.get("type") in ("完成奖励", "学习")) >= 100},
    {"id": "pity_90", "name": "非酋认证", "desc": "在第 80 抽以后才出五星", "reward": 200,
     "check": lambda d: d["wish"].get("max_pity", 0) >= 80},
    {"id": "early_5star", "name": "欧皇降临", "desc": "在 10 抽以内获得五星", "reward": 200,
     "check": lambda d: d["wish"].get("min_pity", 999) <= 10},
    {"id": "up_lost", "name": "歪了", "desc": "第一次五星不是 UP 角色", "reward": 100,
     "check": lambda d: d["wish"].get("lost_5050", False)},
    {"id": "daily_7", "name": "一周不辍", "desc": "连续 7 天有学习记录", "reward": 250,
     "check": lambda d: d.get("streak_days", 0) >= 7},
    {"id": "study_600", "name": "一小时战士", "desc": "单日累计学习 ≥ 60 分钟", "reward": 120,
     "check": lambda d: d.get("today_study_minutes", 0) >= 60},
]


def adventure_exp_needed(rank):
    return int(500 * (rank ** 1.5))


# ============================================================
# 数据层
# ============================================================
def default_data():
    today = date.today()
    return {
        "lifetime_xp": 0,
        "spendable_xp": 0,
        "today_xp": 0,
        "today_sessions": 0,
        "today_study_minutes": 0,
        "today_date": today.isoformat(),
        "daily_win_claimed": False,
        "sleep_bed_time": None,
        "sleep_wake_time": None,
        "sleep_target_hours": 7.5,
        "weekly_boss": {"week_start": _monday_of(today).isoformat(), "minutes": 0, "claimed": False},
        "history": [],
        "purchases": [],
        "primogems": 300,
        "intertwined_fate": 5,
        "starglitter": 0,
        "stardust": 0,              # [v7] 星尘
        "double_cards": 0,
        "adventure_rank": 1,
        "adventure_exp": 0,
        "streak_days": 0,
        "last_study_date": None,
        "wish": {
            "pity_5star": 0,
            "pity_4star": 0,
            "guaranteed_up": False,
            "up_character": UP_ROTATION[today.isocalendar()[1] % len(UP_ROTATION)],
            "total_wishes": 0,
            "five_star_count": 0,
            "max_pity": 0,
            "min_pity": 999,
            "lost_5050": False,
        },
        "characters": {},
        "skills": {},
        "equipped_skills": [],
        "synth_count": 0,           # [v7] 星尘兑换次数
        "synth_5star_count": 0,     # [v7] 星尘兑换五星次数
        "daily_commissions": _fresh_commissions(today),
        "commission_bonus_claimed": False,
        "achievements": {},
        "titles": [],
        "current_title": "",
    }


def _fresh_commissions(today):
    return {"date": today.isoformat(),
            "tasks": [{"id": t["id"], "desc": t["desc"], "reward": t["reward"], "done": False, "claimed": False}
                      for t in COMMISSION_TEMPLATES]}


def _monday_of(d):
    return d - timedelta(days=d.weekday())


def load_data():
    if not os.path.exists(DATA_FILE):
        return default_data()
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        _migrate(data)
        _rollover(data)
        return data
    except Exception:
        return default_data()


def _migrate(d):
    """旧版数据迁移。"""
    defaults = default_data()
    for k, v in defaults.items():
        if k not in d:
            d[k] = v
    if "wish" not in d or not isinstance(d["wish"], dict):
        d["wish"] = defaults["wish"]
    else:
        for k, v in defaults["wish"].items():
            if k not in d["wish"]:
                d["wish"][k] = v
    if not isinstance(d.get("characters"), dict):
        d["characters"] = {}
    if not isinstance(d.get("skills"), dict):
        d["skills"] = {}
    if not isinstance(d.get("equipped_skills"), list):
        d["equipped_skills"] = []
    for k in ("synth_count", "synth_5star_count"):
        if not isinstance(d.get(k), int):
            d[k] = 0
    if not isinstance(d.get("stardust"), int):
        d["stardust"] = 0

    # [v7] 旧「角色碎片」按 1:1 折算为星尘
    cf = d.pop("char_fragments", None)
    if isinstance(cf, dict) and cf:
        try:
            d["stardust"] = d.get("stardust", 0) + int(
                sum(v for v in cf.values() if isinstance(v, (int, float))))
        except Exception:
            pass
    # [v7] 旧「五星自选碎片礼包」购买记录 → 星尘类型（保证可退还逻辑一致）
    for p in d.get("purchases", []):
        if isinstance(p, dict) and p.get("type") == "frag5_pick":
            p["type"] = "stardust"
            p.pop("cid", None)

    # 清理历史退役字段（v4 的 skill_fragments / materials）
    frag = d.pop("skill_fragments", None)
    if isinstance(frag, dict) and frag:
        try:
            bonus = sum(v for v in frag.values() if isinstance(v, (int, float)))
            d["primogems"] = d.get("primogems", 0) + int(bonus) * 5
        except Exception:
            pass
    d.pop("materials", None)

    dc = d.get("daily_commissions")
    try:
        if (not isinstance(dc, dict) or not dc.get("tasks")
                or dc["tasks"][0].get("desc") != COMMISSION_TEMPLATES[0]["desc"]):
            d["daily_commissions"] = _fresh_commissions(date.today())
    except Exception:
        d["daily_commissions"] = defaults["daily_commissions"]

    wb = d.get("weekly_boss")
    if not isinstance(wb, dict) or "minutes" not in wb:
        d["weekly_boss"] = {"week_start": _monday_of(date.today()).isoformat(),
                            "minutes": 0, "claimed": False}


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _rollover(data):
    today = date.today()
    if data.get("today_date") != today.isoformat():
        data["today_xp"] = 0
        data["today_sessions"] = 0
        data["today_study_minutes"] = 0
        data["today_date"] = today.isoformat()
        data["daily_win_claimed"] = False
        data["sleep_bed_time"] = None
        data["sleep_wake_time"] = None
        data["daily_commissions"] = _fresh_commissions(today)
        data["commission_bonus_claimed"] = False
    mon = _monday_of(today).isoformat()
    wb = data.get("weekly_boss")
    if not isinstance(wb, dict) or wb.get("week_start") != mon or "minutes" not in wb:
        data["weekly_boss"] = {"week_start": mon, "minutes": 0, "claimed": False}
    expected_up = UP_ROTATION[today.isocalendar()[1] % len(UP_ROTATION)]
    data["wish"]["up_character"] = expected_up


def add_xp(data, amount, label, detail="", loot=None):
    data["lifetime_xp"] += amount
    data["spendable_xp"] += amount
    data["today_xp"] += amount
    data["adventure_exp"] += max(amount, 0)
    _check_adventure_rank_up(data)
    rec = {"time": datetime.now().strftime("%Y-%m-%d %H:%M"), "type": label,
           "detail": detail, "xp": amount, "loot": loot}
    data["history"].insert(0, rec)
    if len(data["history"]) > 500:
        data["history"] = data["history"][:500]
    _update_streak(data)
    save_data(data)
    return rec


def _check_adventure_rank_up(data):
    while data["adventure_exp"] >= adventure_exp_needed(data["adventure_rank"]):
        data["adventure_exp"] -= adventure_exp_needed(data["adventure_rank"])
        data["adventure_rank"] += 1
        data["primogems"] += 50
        data["intertwined_fate"] += 1


def _update_streak(data):
    today = date.today().isoformat()
    last = data.get("last_study_date")
    if last == today:
        return
    if last:
        try:
            last_d = date.fromisoformat(last)
            if (date.today() - last_d).days == 1:
                data["streak_days"] = data.get("streak_days", 0) + 1
            elif (date.today() - last_d).days > 1:
                data["streak_days"] = 1
        except Exception:
            data["streak_days"] = 1
    else:
        data["streak_days"] = 1
    data["last_study_date"] = today


def delete_history_record(data, index):
    if index < 0 or index >= len(data["history"]):
        return False
    rec = data["history"].pop(index)
    xp = rec["xp"]
    data["lifetime_xp"] -= xp
    data["spendable_xp"] -= xp
    rec_date = rec["time"][:10]
    if rec_date == date.today().isoformat():
        data["today_xp"] -= xp
    if rec.get("type") == "学习" and rec_date == date.today().isoformat():
        m = rec.get("minutes", 0)
        data["today_study_minutes"] = max(0, data.get("today_study_minutes", 0) - m)
        data["today_sessions"] = max(0, data.get("today_sessions", 0) - 1)
        wb = data.get("weekly_boss", {})
        if isinstance(wb, dict):
            wb["minutes"] = max(0, wb.get("minutes", 0) - m)
    save_data(data)
    return True


def spend_xp(data, amount, item_label, purchase_type=None, purchase_amount=0):
    if data["spendable_xp"] < amount:
        return False
    data["spendable_xp"] -= amount
    p = {"time": datetime.now().strftime("%Y-%m-%d %H:%M"),
         "item": item_label, "xp": amount}
    if purchase_type:
        p["type"] = purchase_type
        p["amount"] = purchase_amount
    data["purchases"].insert(0, p)
    save_data(data)
    return True


def purchase_refundable(data, p):
    """检查一条购买记录的资源是否足以退还。"""
    t = p.get("type")
    amount = p.get("amount", 0)
    if not t:
        return True
    if t == "primogem":
        return data.get("primogems", 0) >= amount
    if t == "fate":
        return data.get("intertwined_fate", 0) >= amount
    if t == "starglitter":
        return data.get("starglitter", 0) >= amount
    if t == "double_card":
        return data.get("double_cards", 0) >= amount
    if t == "stardust":
        return data.get("stardust", 0) >= amount
    return True


def delete_purchase(data, index):
    if index < 0 or index >= len(data["purchases"]):
        return False
    p = data["purchases"].pop(index)
    t = p.get("type")
    amount = p.get("amount", 0)
    if t:
        if t == "primogem":
            data["primogems"] -= amount
        elif t == "fate":
            data["intertwined_fate"] -= amount
        elif t == "starglitter":
            data["starglitter"] -= amount
        elif t == "double_card":
            data["double_cards"] -= amount
        elif t == "stardust":
            data["stardust"] -= amount
    data["spendable_xp"] += p["xp"]
    save_data(data)
    return True


def roll(rng):
    return random.randint(rng[0], rng[1])


# ============================================================
# 抽卡引擎
# ============================================================
def _five_star_probability(pity):
    if pity >= 89:
        return 1.0
    if pity >= 75:
        return 0.01 + (pity - 74) * 0.06
    return 0.01


def _four_star_probability(pity):
    if pity >= 9:
        return 1.0
    if pity >= 8:
        return 0.08 + 0.5
    return 0.08


def get_current_weekly_theme():
    today = date.today()
    return WEEKLY_THEMES[today.isocalendar()[1] % len(WEEKLY_THEMES)]


def _weighted_char_choice(char_pool):
    theme = get_current_weekly_theme()
    theme_chars = set(theme["chars"])
    weights = [3 if cid in theme_chars else 1 for cid in char_pool]
    total = sum(weights)
    r = random.uniform(0, total)
    cum = 0
    for cid, w in zip(char_pool, weights):
        cum += w
        if r <= cum:
            return cid
    return char_pool[-1]


def _char_pool_of(cid):
    return (FIVE_STAR_CHARS if cid in FIVE_STAR_CHARS
            else FOUR_STAR_CHARS if cid in FOUR_STAR_CHARS
            else THREE_STAR_CHARS)


def get_weapon_state(data, cid):
    cnt = data["characters"].get(cid, {}).get("count", 0)
    if cnt < 1:
        return False, 0
    return True, min(cnt, 5)


def exchange_stardust(data, rarity):
    """[v7] 星尘兑换随机角色：优先未拥有；重复 → 星辉 + 专武精炼。
    返回 (是否成功, 消息, WishDialog用的result)。"""
    if rarity not in STARDUST_NEEDED:
        return False, "未知星级", None
    need = STARDUST_NEEDED[rarity]
    if data.get("stardust", 0) < need:
        return False, f"星尘不足（{data.get('stardust', 0)}/{need}）", None
    pool = {3: THREE_STAR_CHARS, 4: FOUR_STAR_CHARS, 5: FIVE_STAR_CHARS}[rarity]
    all_ids = list(pool.keys())
    unowned = [c for c in all_ids if data["characters"].get(c, {}).get("count", 0) == 0]
    target_pool = unowned if unowned else all_ids
    char_id = _weighted_char_choice(target_pool)
    data["stardust"] -= need

    owned_before = data["characters"].get(char_id, {}).get("count", 0) > 0
    _add_character(data, char_id)
    char = pool[char_id]

    skill_name = ""
    skill_new = False
    skill_id = char_id + ("_ult" if rarity == 5 else "_skill")
    skill_pool = FIVE_STAR_SKILLS if rarity == 5 else FOUR_STAR_SKILLS
    if skill_id in skill_pool:
        skill_new = _add_skill(data, skill_id)
        skill_name = skill_pool[skill_id]["name"]

    data["synth_count"] = data.get("synth_count", 0) + 1
    if rarity == 5:
        data["synth_5star_count"] = data.get("synth_5star_count", 0) + 1

    detail = (f"星尘兑换：{'⭐' * rarity} {char['name']}（消耗💫×{need}）"
              + (f" +技能:{skill_name}" if skill_name else ""))
    rec = {"time": datetime.now().strftime("%Y-%m-%d %H:%M"), "type": "星尘兑换",
           "detail": detail, "xp": 0, "loot": None}
    data["history"].insert(0, rec)
    if len(data["history"]) > 500:
        data["history"] = data["history"][:500]
    save_data(data)
    _check_achievements(data)

    winfo = SIGNATURE_WEAPONS.get(char_id, {})
    _, wref = get_weapon_state(data, char_id)
    result = {"rarity": rarity, "is_up": False, "is_character": True, "char_id": char_id,
              "char_name": char["name"], "anime": char["anime"], "element": char["element"],
              "xp": 0, "skill_id": skill_id, "skill_name": skill_name, "skill_new": skill_new,
              "weapon_name": winfo.get("name", ""), "weapon_new": not owned_before,
              "weapon_refine": wref, "stardust_gain": 0, "stardust_total": data["stardust"]}
    return True, char["name"], result


def perform_wish(data):
    """执行一次抽卡（角色+技能+专武；三星掉落星尘×1~3）。"""
    if data["intertwined_fate"] < 1:
        return None
    data["intertwined_fate"] -= 1
    w = data["wish"]
    w["total_wishes"] += 1
    w["pity_5star"] += 1
    w["pity_4star"] += 1
    r = random.random()
    p5 = _five_star_probability(w["pity_5star"])
    p4 = _four_star_probability(w["pity_4star"])
    result = {"rarity": 3, "is_up": False, "is_character": False, "char_id": None,
              "char_name": "", "anime": "", "element": "", "xp": 0,
              "skill_id": None, "skill_name": "", "skill_new": False, "skill_dup": False,
              "weapon_name": "", "weapon_new": False, "weapon_refine": 0,
              "stardust_gain": 0, "stardust_total": 0}

    if r < p5:
        # ========== 五星：角色 + 技能（重复精炼专武） ==========
        result["rarity"] = 5
        w["pity_5star"] = 0
        w["five_star_count"] += 1
        w["max_pity"] = max(w.get("max_pity", 0), w["pity_5star"] + 1)
        w["min_pity"] = min(w.get("min_pity", 999), w["pity_5star"] + 1)
        if w["guaranteed_up"] or random.random() < 0.5:
            result["is_up"] = True
            w["guaranteed_up"] = False
            char_id = w["up_character"]
        else:
            result["is_up"] = False
            w["guaranteed_up"] = True
            w["lost_5050"] = True
            others = [c for c in FIVE_STAR_CHARS if c != w["up_character"]]
            char_id = _weighted_char_choice(others)
        result["is_character"] = True
        result["char_id"] = char_id
        char = FIVE_STAR_CHARS[char_id]
        result["char_name"] = char["name"]
        result["anime"] = char["anime"]
        result["element"] = char["element"]
        result["xp"] = random.randint(150, 300)
        if result["is_up"]:
            result["xp"] += 100
        owned_before = data["characters"].get(char_id, {}).get("count", 0) > 0
        _add_character(data, char_id)
        skill_id = char_id + "_ult"
        if skill_id in FIVE_STAR_SKILLS:
            is_new = _add_skill(data, skill_id)
            result["skill_id"] = skill_id
            result["skill_name"] = FIVE_STAR_SKILLS[skill_id]["name"]
            result["skill_new"] = is_new
            result["skill_dup"] = not is_new
        winfo = SIGNATURE_WEAPONS.get(char_id)
        if winfo:
            _, wref = get_weapon_state(data, char_id)
            result["weapon_name"] = winfo["name"]
            result["weapon_new"] = not owned_before
            result["weapon_refine"] = wref
    elif r < p5 + p4:
        # ========== 四星：角色 + 技能（重复精炼专武） ==========
        result["rarity"] = 4
        w["pity_4star"] = 0
        char_id = _weighted_char_choice(list(FOUR_STAR_CHARS.keys()))
        result["is_character"] = True
        result["char_id"] = char_id
        char = FOUR_STAR_CHARS[char_id]
        result["char_name"] = char["name"]
        result["anime"] = char["anime"]
        result["element"] = char["element"]
        result["xp"] = random.randint(50, 100)
        owned_before = data["characters"].get(char_id, {}).get("count", 0) > 0
        _add_character(data, char_id)
        skill_id = char_id + "_skill"
        if skill_id in FOUR_STAR_SKILLS:
            is_new = _add_skill(data, skill_id)
            result["skill_id"] = skill_id
            result["skill_name"] = FOUR_STAR_SKILLS[skill_id]["name"]
            result["skill_new"] = is_new
            result["skill_dup"] = not is_new
        winfo = SIGNATURE_WEAPONS.get(char_id)
        if winfo:
            _, wref = get_weapon_state(data, char_id)
            result["weapon_name"] = winfo["name"]
            result["weapon_new"] = not owned_before
            result["weapon_refine"] = wref
    else:
        # ========== 三星：星尘 ×1~3 [v7] ==========
        result["rarity"] = 3
        n = random.randint(STARDUST_DROP[0], STARDUST_DROP[1])
        data["stardust"] = data.get("stardust", 0) + n
        result["stardust_gain"] = n
        result["stardust_total"] = data["stardust"]
        result["char_name"] = "星尘"
        result["anime"] = "—"
        result["element"] = "材料"
        result["xp"] = random.randint(10, 30)

    if result["xp"] > 0:
        data["lifetime_xp"] += result["xp"]
        data["spendable_xp"] += result["xp"]
        data["today_xp"] += result["xp"]
        data["adventure_exp"] += result["xp"]
        _check_adventure_rank_up(data)

    detail_parts = [f"{'⭐' * result['rarity']} {result['char_name']}"]
    if result["is_up"]:
        detail_parts.append("UP")
    if result["anime"] and result["rarity"] >= 4:
        detail_parts.append(f"《{result['anime']}》")
    if result["skill_name"]:
        detail_parts.append(f"+技能:{result['skill_name']}{'（新）' if result['skill_new'] else ''}")
    if result["skill_dup"]:
        detail_parts.append("技能重复→原石+20")
    if result["weapon_name"]:
        if result["weapon_new"]:
            detail_parts.append(f"+专武:{result['weapon_name']}(R1)")
        elif result["weapon_refine"] >= 5:
            detail_parts.append("专武满炼R5")
        else:
            detail_parts.append(f"专武精炼R{result['weapon_refine']}")
    if result["stardust_gain"]:
        detail_parts.append(f"星尘+{result['stardust_gain']}(累计{result['stardust_total']})")

    rec = {"time": datetime.now().strftime("%Y-%m-%d %H:%M"), "type": "祈愿",
           "detail": " ".join(detail_parts), "xp": result["xp"], "loot": None}
    data["history"].insert(0, rec)
    save_data(data)
    _check_achievements(data)
    return result


def _add_character(data, char_id):
    if char_id in data["characters"]:
        data["characters"][char_id]["count"] += 1
        if char_id in FIVE_STAR_CHARS:
            data["starglitter"] += 10
        else:
            data["starglitter"] += 2
    else:
        data["characters"][char_id] = {"count": 1, "obtained_at": datetime.now().strftime("%Y-%m-%d %H:%M")}


def _add_skill(data, skill_id):
    if skill_id in data["skills"]:
        data["skills"][skill_id]["count"] += 1
        data["primogems"] += 20
        return False
    data["skills"][skill_id] = {"count": 1, "obtained_at": datetime.now().strftime("%Y-%m-%d %H:%M")}
    return True


# ============================================================
# 技能 / 兑换 / 委托 / 成就
# ============================================================
MAX_EQUIPPED = 3


def equip_skill(data, skill_id):
    if skill_id not in data["skills"] or data["skills"][skill_id]["count"] <= 0:
        return False, "你还没有获得这个技能"
    if skill_id in data["equipped_skills"]:
        return False, "该技能已装备"
    if len(data["equipped_skills"]) >= MAX_EQUIPPED:
        return False, f"最多装备 {MAX_EQUIPPED} 个技能，请先卸下一个"
    data["equipped_skills"].append(skill_id)
    save_data(data)
    return True, "装备成功"


def unequip_skill(data, skill_id):
    if skill_id not in data["equipped_skills"]:
        return False, "该技能未装备"
    data["equipped_skills"].remove(skill_id)
    save_data(data)
    return True, "已卸下"


def get_equipment_bonus(data):
    return {
        "all": 0.0, "start": 0.0, "finish": 0.0, "listening": 0.0, "reading": 0.0,
        "writing": 0.0, "speaking": 0.0, "vocab": 0.0, "review": 0.0, "hard": 0.0,
        "long_session": 0.0, "penalty_reduce": 0.0, "double_boost": 0.0,
        "commission_boost": 0.0, "daily_win_boost": 0.0, "late_night_reduce": 0.0,
        "combo_extend": 0,
    }


def exchange_primogems_to_fate(data):
    if data["primogems"] < 160:
        return False
    data["primogems"] -= 160
    data["intertwined_fate"] += 1
    save_data(data)
    return True


def exchange_starglitter(data, item):
    if data.get("starglitter", 0) < item["cost"]:
        return False
    data["starglitter"] -= item["cost"]
    if item["type"] == "fate":
        data["intertwined_fate"] += item["amount"]
    elif item["type"] == "double_card":
        data["double_cards"] = data.get("double_cards", 0) + item["amount"]
    elif item["type"] == "primogem":
        data["primogems"] += item["amount"]
    save_data(data)
    return True


def check_commissions(data):
    for i, task in enumerate(data["daily_commissions"]["tasks"]):
        if not task["done"] and i < len(COMMISSION_TEMPLATES):
            template = COMMISSION_TEMPLATES[i]
            if template["check"](data):
                task["done"] = True
                save_data(data)


def claim_commission(data, index):
    task = data["daily_commissions"]["tasks"][index]
    if not task["done"] or task["claimed"]:
        return False
    task["claimed"] = True
    data["primogems"] += task["reward"]
    save_data(data)
    return task["reward"]


def claim_commission_bonus(data):
    if data.get("commission_bonus_claimed"):
        return False
    if not all(t["done"] for t in data["daily_commissions"]["tasks"]):
        return False
    data["commission_bonus_claimed"] = True
    data["primogems"] += 60
    data["intertwined_fate"] += 1
    save_data(data)
    return 60


def _check_achievements(data):
    newly = []
    for ach in ACHIEVEMENTS:
        if ach["id"] not in data["achievements"] and ach["check"](data):
            data["achievements"][ach["id"]] = datetime.now().strftime("%Y-%m-%d %H:%M")
            data["primogems"] += ach["reward"]
            newly.append(ach)
    if newly:
        save_data(data)
    return newly


# ============================================================
# GUI 层
# ============================================================
GOLD = "#fbbf24"
STAR5_BG = "#2a1f0e"
STAR4_BG = "#1f0e2a"


class StyledButton(QPushButton):
    def __init__(self, text="", bg_color="#1e232b", hover_color="#d4a853", text_color="#d4a853", parent=None):
        super().__init__(text, parent)
        self._bg = bg_color
        self._hover = hover_color
        self._text = text_color
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumHeight(36)
        self._update_style()

    def _update_style(self):
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {self._bg};
                color: {self._text};
                border: 1px solid {self._hover};
                border-radius: 4px;
                padding: 8px 20px;
                font-size: 13px;
                font-weight: bold;
                letter-spacing: 1px;
            }}
            QPushButton:hover {{
                background-color: {self._hover};
                color: #14171d;
            }}
            QPushButton:pressed {{ background-color: {self._hover}; color: #14171d; }}
            QPushButton:disabled {{
                background-color: #1a1e24; color: #5a5548; border: 1px solid #3d3528;
            }}
        """)

    def set_colors(self, bg=None, hover=None, text=None):
        if bg:
            self._bg = bg
        if hover:
            self._hover = hover
        if text:
            self._text = text
        self._update_style()


class CardFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("GenshinCard")
        self.setStyleSheet("""
            QFrame#GenshinCard {
                background-color: #1e232b;
                border: 1px solid #3d3528;
                border-radius: 6px;
            }
        """)
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(24)
        shadow.setColor(QColor(0, 0, 0, 120))
        shadow.setOffset(0, 4)
        self.setGraphicsEffect(shadow)


# ============================================================
# 角色头像生成 (QPixmap)
# ============================================================
_avatar_pixmap_cache = {}


def generate_avatar_pixmap(char_id, size=100):
    cache_key = f"{char_id}_{size}"
    if cache_key in _avatar_pixmap_cache:
        return _avatar_pixmap_cache[cache_key]
    char = FIVE_STAR_CHARS.get(char_id) or FOUR_STAR_CHARS.get(char_id) or THREE_STAR_CHARS.get(char_id)
    if not char:
        return None
    rarity = char["rarity"]
    if rarity == 5:
        bg_top = QColor("#3d2e10"); bg_bottom = QColor("#1a1208")
        border_color = QColor("#d4a853"); text_color = QColor("#f0d890")
    elif rarity == 4:
        bg_top = QColor("#2a1a3a"); bg_bottom = QColor("#120a1e")
        border_color = QColor("#9a7fc8"); text_color = QColor("#c8b0e8")
    else:
        bg_top = QColor("#102530"); bg_bottom = QColor("#050e14")
        border_color = QColor("#5a8a9a"); text_color = QColor("#8ab0c0")

    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    radius = size // 6

    gradient = QLinearGradient(0, 0, 0, size)
    gradient.setColorAt(0, bg_top)
    gradient.setColorAt(1, bg_bottom)
    painter.setBrush(QBrush(gradient))
    painter.setPen(Qt.PenStyle.NoPen)
    path = QPainterPath()
    path.addRoundedRect(0, 0, size, size, radius, radius)
    painter.drawPath(path)

    border_width = max(2, size // 40)
    painter.setPen(QPen(border_color, border_width))
    painter.setBrush(Qt.BrushStyle.NoBrush)
    painter.drawRoundedRect(border_width // 2, border_width // 2,
                            size - border_width, size - border_width,
                            radius - border_width // 2, radius - border_width // 2)

    painter.setPen(border_color)
    painter.setFont(QFont("Arial", size // 12, QFont.Weight.Bold))
    painter.drawText(0, size // 6, size, size // 8, Qt.AlignmentFlag.AlignCenter, "★" * rarity)

    name = char["name"]
    first_char = name[0] if name else "?"
    painter.setPen(text_color)
    painter.setFont(QFont("Microsoft YaHei", size // 2, QFont.Weight.Bold))
    painter.drawText(0, size // 4, size, size // 2, Qt.AlignmentFlag.AlignCenter, first_char)

    anime = char["anime"]
    anime_short = anime[:4] if len(anime) > 4 else anime
    painter.setPen(QColor(text_color.red(), text_color.green(), text_color.blue(), 180))
    painter.setFont(QFont("Microsoft YaHei", size // 10))
    painter.drawText(0, size - size // 5, size, size // 6, Qt.AlignmentFlag.AlignCenter, anime_short)
    painter.end()

    _avatar_pixmap_cache[cache_key] = pixmap
    return pixmap


def generate_silhouette_pixmap(size=100):
    cache_key = f"sil_{size}"
    if cache_key in _avatar_pixmap_cache:
        return _avatar_pixmap_cache[cache_key]
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    radius = size // 6
    painter.setBrush(QColor("#1a1a2e"))
    painter.setPen(QPen(QColor("#333355"), 2))
    painter.drawRoundedRect(1, 1, size - 2, size - 2, radius, radius)
    painter.setPen(QColor("#444466"))
    painter.setFont(QFont("Arial", size // 2, QFont.Weight.Bold))
    painter.drawText(0, 0, size, size, Qt.AlignmentFlag.AlignCenter, "?")
    painter.end()
    _avatar_pixmap_cache[cache_key] = pixmap
    return pixmap


# ============================================================
# 主窗口
# ============================================================
class IELTSMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🎌 IELTS Dopamine OS — 动漫大乱斗篇 (PyQt6)")
        self.setMinimumSize(1180, 780)
        self.setStyleSheet("""
            QWidget {
                background-color: #14171d;
                color: #e8e0d0;
                font-family: 'Microsoft YaHei', 'SimSun', sans-serif;
                font-size: 13px;
            }
            QMainWindow { background-color: #14171d; }
            QToolTip {
                background-color: #1e232b;
                color: #d4a853;
                border: 1px solid #d4a853;
                padding: 4px 8px;
            }
        """)
        self.data = load_data()
        self._session_active = False
        self._session_start = None
        self._timer = QTimer()
        self._timer.timeout.connect(self._update_timer)
        self._build_ui()
        self.refresh()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(12)

        self._build_status_bar(main_layout)

        self.tabs = QTabWidget()
        self.tabs.setUsesScrollButtons(True)
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #3d3528;
                border-radius: 4px;
                background-color: #14171d;
                top: -1px;
            }
            QTabBar::tab {
                background-color: #1e232b;
                color: #9a9080;
                padding: 9px 15px;
                border: 1px solid #3d3528;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                margin-right: 2px;
                font-size: 12px;
                font-weight: bold;
                letter-spacing: 1px;
            }
            QTabBar::tab:selected {
                background-color: #14171d;
                color: #d4a853;
                border: 1px solid #d4a853;
                border-bottom: 1px solid #14171d;
            }
            QTabBar::tab:hover:!selected {
                background-color: #252a33;
                color: #d4a853;
            }
        """)
        main_layout.addWidget(self.tabs, 1)

        self._build_session_tab()
        self._build_wish_tab()
        self._build_chars_tab()
        self._build_bonds_tab()
        self._build_ip_tab()
        self._build_skill_tab()
        self._build_quest_tab()
        self._build_boss_tab()
        self._build_shop_tab()
        self._build_history_tab()

        self.tabs.addTab(self.session_tab, "📚 学习")
        self.tabs.addTab(self.wish_tab, "🎴 祈愿")
        self.tabs.addTab(self.chars_tab, "👥 角色")
        self.tabs.addTab(self.bonds_tab, "🤝 羁绊")
        self.tabs.addTab(self.ip_tab, "🌏 IP图鉴")
        self.tabs.addTab(self.skill_tab, "📜 技能")
        self.tabs.addTab(self.quest_tab, "📜 委托")
        self.tabs.addTab(self.boss_tab, "👹 周Boss")
        self.tabs.addTab(self.shop_tab, "🛒 商店")
        self.tabs.addTab(self.history_tab, "📋 记录")

        self._build_theme_button()

    def _build_status_bar(self, layout):
        bar = CardFrame()
        bar.setFixedHeight(72)
        bar_layout = QHBoxLayout(bar)
        bar_layout.setContentsMargins(20, 8, 20, 8)
        bar_layout.setSpacing(16)

        self.ar_label = QLabel("AR 1")
        self.ar_label.setStyleSheet("color: #d4a853; font-size: 18px; font-weight: bold; letter-spacing: 2px;")
        bar_layout.addWidget(self.ar_label)

        exp_layout = QVBoxLayout()
        self.exp_bar = QProgressBar()
        self.exp_bar.setRange(0, 100)
        self.exp_bar.setTextVisible(False)
        self.exp_bar.setFixedHeight(10)
        self.exp_bar.setStyleSheet("""
            QProgressBar {
                background-color: #0a0d12;
                border-radius: 5px;
                border: 1px solid #3d3528;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #b8943f, stop:0.5 #d4a853, stop:1 #e8c47a);
                border-radius: 4px;
            }
        """)
        self.exp_label = QLabel("经验：0 / 100")
        self.exp_label.setStyleSheet("color: #9a9080; font-size: 11px;")
        exp_layout.addWidget(self.exp_bar)
        exp_layout.addWidget(self.exp_label)
        bar_layout.addLayout(exp_layout, 1)

        self.xp_label = QLabel("💎 0 XP")
        self.xp_label.setStyleSheet("color: #d4a853; font-size: 14px; font-weight: bold;")
        bar_layout.addWidget(self.xp_label)

        self.primogem_label = QLabel("💠 0")
        self.primogem_label.setStyleSheet("color: #9a7fc8; font-size: 14px; font-weight: bold;")
        bar_layout.addWidget(self.primogem_label)

        self.starglitter_label = QLabel("✨ 0")
        self.starglitter_label.setStyleSheet("color: #7aa8c0; font-size: 14px; font-weight: bold;")
        bar_layout.addWidget(self.starglitter_label)

        # [v7] 星尘常驻显示
        self.stardust_label = QLabel("💫 0")
        self.stardust_label.setStyleSheet("color: #06b6d4; font-size: 14px; font-weight: bold;")
        bar_layout.addWidget(self.stardust_label)

        self.fate_label = QLabel("🎴 0")
        self.fate_label.setStyleSheet("color: #d4a853; font-size: 14px; font-weight: bold;")
        bar_layout.addWidget(self.fate_label)

        self.theme_btn = None
        layout.addWidget(bar)

    # ==================== 学习计时 Tab ====================
    def _build_session_tab(self):
        self.session_tab = QWidget()
        layout = QVBoxLayout(self.session_tab)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        timer_card = CardFrame()
        timer_layout = QVBoxLayout(timer_card)
        timer_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        timer_layout.setSpacing(16)

        self.timer_label = QLabel("00:00:00")
        self.timer_label.setStyleSheet(
            "color: #d4a853; font-size: 72px; font-weight: bold; "
            "font-family: 'Consolas', 'SimSun', monospace; letter-spacing: 4px;")
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        timer_layout.addWidget(self.timer_label)

        self.timer_hint = QLabel("点击下方按钮开始学习")
        self.timer_hint.setStyleSheet("color: #9a9080; font-size: 16px; letter-spacing: 2px;")
        self.timer_hint.setAlignment(Qt.AlignmentFlag.AlignCenter)
        timer_layout.addWidget(self.timer_hint)

        btn_layout = QHBoxLayout()
        btn_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        btn_layout.setSpacing(20)

        self.start_btn = QPushButton("▶ 开始学习")
        self.start_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.start_btn.setMinimumWidth(200)
        self.start_btn.setMinimumHeight(56)
        self._apply_start_btn_style(active=False)
        self.start_btn.clicked.connect(self._toggle_session)
        btn_layout.addWidget(self.start_btn)

        timer_layout.addLayout(btn_layout)
        layout.addWidget(timer_card)

        summary_card = CardFrame()
        summary_layout = QVBoxLayout(summary_card)
        summary_layout.setContentsMargins(20, 16, 20, 16)
        summary_layout.setSpacing(6)

        summary_title = QLabel("📈 今日学习进度")
        summary_title.setStyleSheet("color: #d4a853; font-size: 16px; font-weight: bold;")
        summary_layout.addWidget(summary_title)

        self.today_summary_label = QLabel()
        self.today_summary_label.setStyleSheet("color: #9494b8; font-size: 13px;")
        self.today_summary_label.setWordWrap(True)
        summary_layout.addWidget(self.today_summary_label)

        layout.addWidget(summary_card)

        reward_card = CardFrame()
        reward_layout = QVBoxLayout(reward_card)
        reward_layout.setContentsMargins(20, 16, 20, 16)
        reward_layout.setSpacing(6)

        reward_title = QLabel("🎁 学习奖励规则")
        reward_title.setStyleSheet("color: #fbbf24; font-size: 16px; font-weight: bold;")
        reward_layout.addWidget(reward_title)

        for line in ("• 每分钟 3~8 XP，30分钟 +20%，60分钟 +40%",
                     "• 每20分钟获得 1 个纠缠之缘（用于抽卡）",
                     "• 每分钟 2~4 原石",
                     "• 每拥有 1 名不同角色 XP +0.5%，激活羁绊额外加成（上限 100%）",
                     "• 结束学习时自动消耗 1 张双倍经验卡（如有），本次 XP ×2",
                     "• 学习时长自动计入每日委托与周Boss进度"):
            lbl = QLabel(line)
            lbl.setStyleSheet("color: #9494b8; font-size: 13px;")
            reward_layout.addWidget(lbl)

        layout.addWidget(reward_card)
        layout.addStretch()

    def _apply_start_btn_style(self, active=False):
        if active:
            self.start_btn.setStyleSheet("""
                QPushButton {
                    background-color: #2a1a1a; color: #e87070;
                    border: 2px solid #e87070; border-radius: 4px;
                    font-size: 20px; font-weight: bold; padding: 12px 32px; letter-spacing: 4px;
                }
                QPushButton:hover { background-color: #e87070; color: #14171d; border: 2px solid #f09090; }
            """)
        else:
            self.start_btn.setStyleSheet("""
                QPushButton {
                    background-color: #1e232b; color: #d4a853;
                    border: 2px solid #d4a853; border-radius: 4px;
                    font-size: 20px; font-weight: bold; padding: 12px 32px; letter-spacing: 4px;
                }
                QPushButton:hover { background-color: #d4a853; color: #14171d; border: 2px solid #e8c47a; }
            """)

    def _toggle_session(self):
        if self._session_active:
            self._finish_session()
        else:
            self._start_session()

    def _start_session(self):
        self._session_active = True
        self._session_start = datetime.now()
        self._timer.start(1000)
        self.start_btn.setText("⏹ 结束学习")
        self._apply_start_btn_style(active=True)
        self.timer_hint.setText("学习中... 专注就是胜利！")

    def _finish_session(self):
        self._session_active = False
        self._timer.stop()
        duration = (datetime.now() - self._session_start).total_seconds()
        minutes = max(1, int(duration // 60))

        # [v5] 双倍经验卡：自动消耗 1 张
        double_used = False
        if self.data.get("double_cards", 0) > 0:
            self.data["double_cards"] -= 1
            double_used = True

        base_xp = minutes * random.randint(3, 8)
        time_bonus = 0
        if minutes >= 60:
            time_bonus = 0.40
        elif minutes >= 30:
            time_bonus = 0.20
        char_bonus = self._char_skill_bonus()

        total_xp = int(base_xp * (1 + time_bonus + char_bonus) * (2 if double_used else 1))
        fate = max(1, (minutes + 19) // 20)
        primogem = minutes * random.randint(2, 4)

        self.data["today_study_minutes"] = self.data.get("today_study_minutes", 0) + minutes
        self.data["today_sessions"] = self.data.get("today_sessions", 0) + 1
        wb = self.data.get("weekly_boss")
        if not isinstance(wb, dict):
            wb = {"week_start": _monday_of(date.today()).isoformat(), "minutes": 0, "claimed": False}
        wb["minutes"] = wb.get("minutes", 0) + minutes
        self.data["weekly_boss"] = wb

        rec = add_xp(self.data, total_xp, "学习", f"专注学习 {minutes} 分钟")
        rec["minutes"] = minutes
        save_data(self.data)

        self.data["intertwined_fate"] += fate
        self.data["primogems"] += primogem
        save_data(self.data)

        self.timer_label.setText("00:00:00")
        self.start_btn.setText("▶ 开始学习")
        self._apply_start_btn_style(active=False)
        self.timer_hint.setText(f"本次学习 {minutes} 分钟！+{total_xp} XP +{fate}🎴 +{primogem}💠")

        self.refresh()

        double_line = "\n⚡ 已消耗 1 张双倍经验卡（XP ×2）" if double_used else ""
        QMessageBox.information(self, "🎉 学习完成！",
                                f"学习时长：{minutes} 分钟\n"
                                f"获得 XP：+{total_xp}\n"
                                f"纠缠之缘：+{fate} 🎴\n"
                                f"原石：+{primogem} 💠\n\n"
                                f"角色收藏加成：+{int(char_bonus * 100)}%\n"
                                f"时长加成：+{int(time_bonus * 100)}%{double_line}")

    def _update_timer(self):
        if self._session_start:
            delta = datetime.now() - self._session_start
            total_sec = int(delta.total_seconds())
            h = total_sec // 3600
            m = (total_sec % 3600) // 60
            s = total_sec % 60
            self.timer_label.setText(f"{h:02d}:{m:02d}:{s:02d}")

    def _char_skill_bonus(self):
        bonus = 0.0
        owned = [cid for cid, c in self.data["characters"].items() if c.get("count", 0) > 0]
        bonus += 0.005 * len(owned)
        for bond in BOND_SET_BONUSES:
            if all(cid in self.data["characters"] and self.data["characters"][cid].get("count", 0) > 0
                   for cid in bond["chars"]):
                bonus += bond["bonus"]
        for tb in THEME_BONDS:
            if all(cid in self.data["characters"] and self.data["characters"][cid].get("count", 0) > 0
                   for cid in tb["chars"]):
                bonus += tb["bonus"]
        return min(bonus, 1.0)

    # ==================== 抽卡 Tab ====================
    def _build_wish_tab(self):
        self.wish_tab = QWidget()
        layout = QVBoxLayout(self.wish_tab)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        up_card = CardFrame()
        up_layout = QVBoxLayout(up_card)
        up_layout.setContentsMargins(20, 12, 20, 12)

        title = QLabel("🎴 角色活动祈愿")
        title.setStyleSheet("color: #d4a853; font-size: 18px; font-weight: bold; letter-spacing: 2px;")
        up_layout.addWidget(title)

        self.up_info = QLabel()
        self.up_info.setStyleSheet("color: #e8e0d0; font-size: 13px; padding: 4px 0;")
        self.up_info.setWordWrap(True)
        up_layout.addWidget(self.up_info)

        self.weekly_theme_label = QLabel()
        self.weekly_theme_label.setStyleSheet("color: #8b5cf6; font-size: 12px; font-weight: bold;")
        self.weekly_theme_label.setWordWrap(True)
        up_layout.addWidget(self.weekly_theme_label)

        pity_layout = QHBoxLayout()
        self.pity_5label = QLabel()
        self.pity_5label.setStyleSheet("color: #fbbf24; font-size: 13px; font-weight: bold;")
        pity_layout.addWidget(self.pity_5label)
        self.pity_4label = QLabel()
        self.pity_4label.setStyleSheet("color: #9a7fc8; font-size: 13px; font-weight: bold;")
        pity_layout.addWidget(self.pity_4label)
        self.guarantee_label = QLabel()
        self.guarantee_label.setStyleSheet("color: #8b5cf6; font-size: 13px; font-weight: bold;")
        pity_layout.addWidget(self.guarantee_label)
        pity_layout.addStretch()
        up_layout.addLayout(pity_layout)
        layout.addWidget(up_card)

        # [v7] 星尘兑换所
        sd_card = CardFrame()
        sd_layout = QVBoxLayout(sd_card)
        sd_layout.setContentsMargins(20, 12, 20, 12)
        sd_layout.setSpacing(8)

        sd_row1 = QHBoxLayout()
        sd_title = QLabel("💫 星尘兑换所")
        sd_title.setStyleSheet("color: #d4a853; font-size: 14px; font-weight: bold;")
        sd_row1.addWidget(sd_title)
        sd_row1.addStretch()
        self.stardust_wish_label = QLabel("💫 ×0")
        self.stardust_wish_label.setStyleSheet("color: #06b6d4; font-size: 14px; font-weight: bold;")
        sd_row1.addWidget(self.stardust_wish_label)
        sd_layout.addLayout(sd_row1)

        sd_btn_row = QHBoxLayout()
        sd_btn_row.setSpacing(10)
        sd_btn_style = """
            QPushButton {
                background-color: #1e232b; color: #d4a853;
                border: 1px solid #3d3528; border-radius: 4px;
                font-size: 12px; font-weight: bold; padding: 8px 10px;
            }
            QPushButton:hover { background-color: #d4a853; color: #14171d; }
            QPushButton:disabled { background-color: #1a1e24; color: #5a5548; }
        """
        self.sd3_btn = QPushButton("⭐ 随机三星 (10💫)")
        self.sd3_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.sd3_btn.setMinimumHeight(38)
        self.sd3_btn.setStyleSheet(sd_btn_style)
        self.sd3_btn.clicked.connect(lambda checked, r=3: self._exchange_stardust(r))
        sd_btn_row.addWidget(self.sd3_btn, 1)

        self.sd4_btn = QPushButton("⭐⭐ 随机四星 (30💫)")
        self.sd4_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.sd4_btn.setMinimumHeight(38)
        self.sd4_btn.setStyleSheet(sd_btn_style)
        self.sd4_btn.clicked.connect(lambda checked, r=4: self._exchange_stardust(r))
        sd_btn_row.addWidget(self.sd4_btn, 1)

        self.sd5_btn = QPushButton("⭐⭐⭐⭐⭐ 随机五星 (70💫)")
        self.sd5_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.sd5_btn.setMinimumHeight(38)
        self.sd5_btn.setStyleSheet(sd_btn_style)
        self.sd5_btn.clicked.connect(lambda checked, r=5: self._exchange_stardust(r))
        sd_btn_row.addWidget(self.sd5_btn, 1)

        sd_layout.addLayout(sd_btn_row)

        sd_desc = QLabel("三星祈愿掉落星尘 ×1~3。兑换必得该星级随机角色（优先未拥有；"
                         "全拥有后重复 → 星辉 + 专武精炼+1，不亏）。")
        sd_desc.setStyleSheet("color: #9494b8; font-size: 11px;")
        sd_desc.setWordWrap(True)
        sd_layout.addWidget(sd_desc)
        layout.addWidget(sd_card)

        btn_card = CardFrame()
        btn_layout = QHBoxLayout(btn_card)
        btn_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        btn_layout.setSpacing(30)
        btn_layout.setContentsMargins(20, 20, 20, 20)

        self.wish1_btn = QPushButton("🎴 单抽 (1🎴)")
        self.wish1_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.wish1_btn.setMinimumWidth(160)
        self.wish1_btn.setMinimumHeight(60)
        self.wish1_btn.setStyleSheet("""
            QPushButton {
                background-color: #1e232b; color: #d4a853;
                border: 1px solid #d4a853; border-radius: 4px;
                font-size: 16px; font-weight: bold; padding: 12px 24px; letter-spacing: 2px;
            }
            QPushButton:hover { background-color: #d4a853; color: #14171d; border: 1px solid #e8c47a; }
            QPushButton:disabled { background-color: #1a1e24; color: #5a5548; border: 1px solid #3d3528; }
        """)
        self.wish1_btn.clicked.connect(lambda: self._do_wish(1))
        btn_layout.addWidget(self.wish1_btn)

        self.wish10_btn = QPushButton("🎴🎴 十连抽 (10🎴)")
        self.wish10_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.wish10_btn.setMinimumWidth(160)
        self.wish10_btn.setMinimumHeight(60)
        self.wish10_btn.setStyleSheet("""
            QPushButton {
                background-color: #d4a853; color: #14171d;
                border: 1px solid #e8c47a; border-radius: 4px;
                font-size: 16px; font-weight: bold; padding: 12px 24px; letter-spacing: 2px;
            }
            QPushButton:hover { background-color: #e8c47a; color: #14171d; }
            QPushButton:disabled { background-color: #3d3528; color: #5a5548; border: 1px solid #3d3528; }
        """)
        self.wish10_btn.clicked.connect(lambda: self._do_wish(10))
        btn_layout.addWidget(self.wish10_btn)

        layout.addWidget(btn_card)
        layout.addStretch()

    def _update_stardust_panel(self):
        """[v7] 更新星尘余额与兑换按钮状态。"""
        total = self.data.get("stardust", 0)
        self.stardust_wish_label.setText(f"💫 ×{total}")
        for btn, rar in ((self.sd3_btn, 3), (self.sd4_btn, 4), (self.sd5_btn, 5)):
            btn.setEnabled(total >= STARDUST_NEEDED[rar])

    def _exchange_stardust(self, rarity):
        """[v7] 星尘兑换随机角色。"""
        need = STARDUST_NEEDED[rarity]
        if self.data.get("stardust", 0) < need:
            QMessageBox.warning(self, "星尘不足",
                                f"需要 💫{need} 星尘，当前 💫{self.data.get('stardust', 0)}。\n"
                                f"（三星祈愿即可获得星尘）")
            return
        rname = {3: "三星", 4: "四星", 5: "五星"}[rarity]
        reply = QMessageBox.question(self, "确认兑换",
                                     f"消耗 💫{need} 星尘，兑换随机{rname}角色？\n"
                                     f"（优先未拥有角色）")
        if reply != QMessageBox.StandardButton.Yes:
            return
        ok, msg, result = exchange_stardust(self.data, rarity)
        if ok and result:
            self.refresh()
            dlg = WishDialog(self, [result])
            dlg.exec()
        else:
            QMessageBox.warning(self, "兑换失败", msg)

    def _do_wish(self, count):
        if self.data["intertwined_fate"] < count:
            QMessageBox.warning(self, "纠缠之缘不足",
                                f"需要 {count} 个纠缠之缘，当前只有 {self.data['intertwined_fate']} 个。\n去学习获取更多！")
            return
        results = []
        for _ in range(count):
            r = perform_wish(self.data)
            if r:
                results.append(r)
        save_data(self.data)
        self.refresh()
        if results:
            dialog = WishDialog(self, results)
            dialog.exec()

    # ==================== 角色图鉴 Tab ====================
    def _build_chars_tab(self):
        self.chars_tab = QWidget()
        layout = QVBoxLayout(self.chars_tab)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        progress_card = CardFrame()
        progress_layout = QVBoxLayout(progress_card)
        progress_layout.setContentsMargins(20, 16, 20, 16)

        self.collection_title = QLabel("👥 角色收藏")
        self.collection_title.setStyleSheet("color: #d4a853; font-size: 18px; font-weight: bold; letter-spacing: 2px;")
        progress_layout.addWidget(self.collection_title)

        self.collection_progress = QProgressBar()
        self.collection_progress.setRange(0, 100)
        self.collection_progress.setTextVisible(True)
        self.collection_progress.setFormat("%v/%m 角色已收集")
        self.collection_progress.setFixedHeight(20)
        self.collection_progress.setStyleSheet("""
            QProgressBar {
                background-color: #0a0d12;
                border-radius: 10px;
                border: 1px solid #3d3528;
                color: #e8e0d0;
                text-align: center;
                font-size: 12px;
                font-weight: bold;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #b8943f, stop:0.5 #d4a853, stop:1 #e8c47a);
                border-radius: 9px;
            }
        """)
        progress_layout.addWidget(self.collection_progress)

        self.bond_label = QLabel()
        self.bond_label.setStyleSheet("color: #7ab88a; font-size: 13px; padding: 8px 0;")
        self.bond_label.setWordWrap(True)
        progress_layout.addWidget(self.bond_label)
        layout.addWidget(progress_card)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")
        scroll_content = QWidget()
        self.chars_grid = QGridLayout(scroll_content)
        self.chars_grid.setSpacing(12)
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll, 1)

    def _render_chars(self):
        while self.chars_grid.count():
            item = self.chars_grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        all_chars = list(FIVE_STAR_CHARS.items()) + list(FOUR_STAR_CHARS.items()) + list(THREE_STAR_CHARS.items())
        owned_count = 0
        for idx, (cid, char) in enumerate(all_chars):
            owned = self.data["characters"].get(cid, {}).get("count", 0)
            if owned > 0:
                owned_count += 1
            card = self._create_char_card(cid, char, owned)
            self.chars_grid.addWidget(card, idx // 5, idx % 5)

        self.collection_progress.setMaximum(len(all_chars))
        self.collection_progress.setValue(owned_count)

        active_bonds = []
        for bond in BOND_SET_BONUSES:
            if all(c in self.data["characters"] and self.data["characters"][c].get("count", 0) > 0
                   for c in bond["chars"]):
                active_bonds.append(bond)
        for tb in THEME_BONDS:
            if all(c in self.data["characters"] and self.data["characters"][c].get("count", 0) > 0
                   for c in tb["chars"]):
                active_bonds.append(tb)

        if active_bonds:
            bond_text = "🏆 已激活羁绊：\n"
            for b in active_bonds:
                source = f"《{b['anime']}》" if "anime" in b else f"主题「{b.get('theme', '')}」"
                bond_text += f" ✨ {b['name']}（{source}）→ 全队 XP +{int(b['bonus'] * 100)}%\n"
            self.bond_label.setText(bond_text.strip())
        else:
            self.bond_label.setText("收集更多角色解锁羁绊礼装和主题羁绊！")

    def _create_char_card(self, cid, char, owned):
        rarity = char["rarity"]
        card = QFrame()
        if owned > 0:
            bg = "#2a2010" if rarity == 5 else ("#1a1525" if rarity == 4 else "#101a20")
            border = "#d4a853" if rarity == 5 else ("#9a7fc8" if rarity == 4 else "#5a8a9a")
        else:
            bg = "#1a1e24"
            border = "#3d3528"
        card.setObjectName("charCard")
        card.setStyleSheet(f"""
            QFrame#charCard {{
                background-color: {bg};
                border: 1px solid {border};
                border-radius: 4px;
            }}
            QFrame#charCard:hover {{
                border: 2px solid #d4a853;
                background-color: {'#352a15' if owned and rarity == 5 else bg};
            }}
        """)
        card.setFixedSize(150, 200)
        card.setCursor(Qt.CursorShape.PointingHandCursor)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(4)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        if owned > 0:
            avatar = generate_avatar_pixmap(cid, 80)
            if avatar:
                avatar_label = QLabel()
                avatar_label.setPixmap(avatar)
                avatar_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                layout.addWidget(avatar_label)

            stars = QLabel("★" * rarity)
            stars.setAlignment(Qt.AlignmentFlag.AlignCenter)
            stars.setStyleSheet(f"color: {border}; font-size: 12px;")
            layout.addWidget(stars)

            name = QLabel(char["name"])
            name.setAlignment(Qt.AlignmentFlag.AlignCenter)
            name.setStyleSheet(f"color: {border}; font-size: 13px; font-weight: bold;")
            layout.addWidget(name)

            anime = QLabel(f"《{char['anime']}》")
            anime.setAlignment(Qt.AlignmentFlag.AlignCenter)
            anime.setStyleSheet("color: #9a9080; font-size: 10px;")
            layout.addWidget(anime)

            wowned, wref = get_weapon_state(self.data, cid)
            if cid in SIGNATURE_WEAPONS:
                wl = QLabel(f"🗡 R{wref}" if wowned else "🗡 未解锁")
                wl.setAlignment(Qt.AlignmentFlag.AlignCenter)
                wl.setStyleSheet(f"color: {'#d4a853' if wowned else '#4a4a5a'}; font-size: 9px;")
                layout.addWidget(wl)

            if owned > 1:
                count = QLabel(f"持有 ×{owned}")
                count.setAlignment(Qt.AlignmentFlag.AlignCenter)
                count.setStyleSheet("color: #fbbf24; font-size: 10px; font-weight: bold;")
                layout.addWidget(count)
        else:
            sil = generate_silhouette_pixmap(80)
            if sil:
                sil_label = QLabel()
                sil_label.setPixmap(sil)
                sil_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                layout.addWidget(sil_label)

            stars = QLabel("★" * rarity)
            stars.setAlignment(Qt.AlignmentFlag.AlignCenter)
            stars.setStyleSheet("color: #333355; font-size: 12px;")
            layout.addWidget(stars)

            name = QLabel("? ? ?")
            name.setAlignment(Qt.AlignmentFlag.AlignCenter)
            name.setStyleSheet("color: #444466; font-size: 13px; font-weight: bold;")
            layout.addWidget(name)

            locked = QLabel("未解锁")
            locked.setAlignment(Qt.AlignmentFlag.AlignCenter)
            locked.setStyleSheet("color: #333355; font-size: 10px;")
            layout.addWidget(locked)

        card.mousePressEvent = lambda e, c=cid, r=rarity: self._show_char_detail(c, r)
        return card

    def _show_char_detail(self, cid, rarity):
        char = (FIVE_STAR_CHARS if rarity == 5 else (FOUR_STAR_CHARS if rarity == 4 else THREE_STAR_CHARS)).get(cid, {})
        owned = self.data["characters"].get(cid, {}).get("count", 0)
        if owned == 0:
            QMessageBox.information(self, "未解锁",
                                    "这个角色尚未解锁。\n祈愿抽卡或星尘兑换（10/30/70💫）都有机会获得TA！")
            return
        skill_id = cid + ("_ult" if rarity == 5 else "_skill")
        skill = ALL_SKILLS.get(skill_id, {})
        skill_owned = skill_id in self.data["skills"]
        if skill:
            skill_text = f"⚔️ 专属技能：{skill.get('name', '???')}\n    {skill.get('effect', '')}"
            if not skill_owned:
                skill_text += "（技能尚未获得）"
        else:
            skill_text = "⚔️ 专属技能：无（三星角色不附带技能）"

        winfo = SIGNATURE_WEAPONS.get(cid)
        wowned, wref = get_weapon_state(self.data, cid)
        if winfo:
            if wowned:
                weapon_text = f"🗡️ 专武：{winfo['name']}（精炼 R{wref}）\n    {winfo['desc']}"
            else:
                weapon_text = "🗡️ 专武：？？？（获得该角色即可解锁）"
        else:
            weapon_text = "🗡️ 专武：该角色无专属武器记载"

        msg = (f"{'⭐' * rarity} {char['name']}\n"
               f"《{char['anime']}》 【{char['element']}】\n"
               f"「{char['title']}」\n\n"
               f"{char['desc']}\n\n"
               f"能力：{char.get('ability', '')}\n"
               f"{skill_text}\n"
               f"{weapon_text}\n\n"
               f"持有：×{owned}"
               f"{f'（专武精炼 R{min(owned, 5)}）' if owned > 1 else ''}\n"
               f"台词：{char.get('wish_text', '')}")
        QMessageBox.information(self, f"{char['name']} 详情", msg)

    # ==================== 羁绊图鉴 Tab ====================
    def _build_bonds_tab(self):
        self.bonds_tab = QWidget()
        layout = QVBoxLayout(self.bonds_tab)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        header = CardFrame()
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(20, 16, 20, 16)

        title = QLabel("🤝 羁绊图鉴")
        title.setStyleSheet("color: #d4a853; font-size: 18px; font-weight: bold; letter-spacing: 2px;")
        header_layout.addWidget(title)

        desc = QLabel("集齐同一组合的全部角色即可激活羁绊，为学习提供额外 XP 加成。")
        desc.setStyleSheet("color: #9a9080; font-size: 13px;")
        header_layout.addWidget(desc)

        self.bonds_progress = QLabel()
        self.bonds_progress.setStyleSheet("color: #fbbf24; font-size: 14px; font-weight: bold;")
        header_layout.addWidget(self.bonds_progress)
        layout.addWidget(header)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        self.bonds_content = QWidget()
        self.bonds_content.setStyleSheet("background: transparent;")
        self.bonds_layout = QVBoxLayout(self.bonds_content)
        self.bonds_layout.setSpacing(10)
        self.bonds_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        scroll.setWidget(self.bonds_content)
        layout.addWidget(scroll, 1)

    def _render_bonds(self):
        while self.bonds_layout.count():
            item = self.bonds_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        theme_name_map = {t["id"]: t["name"] for t in WEEKLY_THEMES}
        all_bonds = []
        for b in BOND_SET_BONUSES:
            all_bonds.append(("羁绊礼装", f"《{b['anime']}》", b))
        for t in THEME_BONDS:
            all_bonds.append(("主题羁绊", theme_name_map.get(t.get("theme", ""), ""), t))

        activated_count = 0
        cards = []
        for kind, source, bond in all_bonds:
            chars = bond["chars"]
            owned_flags = [self.data["characters"].get(c, {}).get("count", 0) > 0 for c in chars]
            owned_n = sum(owned_flags)
            activated = owned_n >= len(chars)
            if activated:
                activated_count += 1

            card = QFrame()
            card.setObjectName("bondOn" if activated else "bondOff")
            if activated:
                card.setStyleSheet("QFrame#bondOn { background-color: #2a2010; border: 2px solid #d4a853; border-radius: 6px; }")
            else:
                card.setStyleSheet("QFrame#bondOff { background-color: #16162a; border: 1px solid #3d3528; border-radius: 6px; }")

            cl = QVBoxLayout(card)
            cl.setContentsMargins(14, 10, 14, 10)
            cl.setSpacing(6)

            row1 = QHBoxLayout()
            name_lbl = QLabel(("🏆 " if activated else "🔒 ") + bond["name"])
            name_lbl.setStyleSheet(f"color: {'#d4a853' if activated else '#9a9080'}; font-size: 15px; font-weight: bold;")
            row1.addWidget(name_lbl)
            row1.addStretch()
            bonus_lbl = QLabel(f"全队 XP +{int(bond['bonus'] * 100)}%")
            bonus_lbl.setStyleSheet(f"color: {'#fbbf24' if activated else '#5a5548'}; font-size: 13px; font-weight: bold;")
            row1.addWidget(bonus_lbl)
            cl.addLayout(row1)

            meta = QLabel(f"{kind} · {source} · 进度 {owned_n}/{len(chars)}"
                          + ("　✅ 已激活" if activated else ""))
            meta.setStyleSheet(f"color: {'#7ab88a' if activated else '#6a6a7a'}; font-size: 11px;")
            cl.addWidget(meta)

            members = []
            for c, ok in zip(chars, owned_flags):
                members.append(("✅ " if ok else "⬜ ") + self._char_display_name(c))
            members_lbl = QLabel("　".join(members))
            members_lbl.setStyleSheet("color: #9494b8; font-size: 12px;")
            members_lbl.setWordWrap(True)
            cl.addWidget(members_lbl)

            cards.append((activated, card))

        cards.sort(key=lambda x: (not x[0]))
        for _, card in cards:
            self.bonds_layout.addWidget(card)

        self.bonds_progress.setText(f"已激活羁绊：{activated_count} / {len(all_bonds)}")

    # ==================== IP图鉴 Tab ====================
    def _build_ip_tab(self):
        self.ip_tab = QWidget()
        layout = QVBoxLayout(self.ip_tab)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        header = CardFrame()
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(20, 16, 20, 16)

        title = QLabel("🌏 IP 图鉴")
        title.setStyleSheet("color: #d4a853; font-size: 18px; font-weight: bold; letter-spacing: 2px;")
        header_layout.addWidget(title)

        desc = QLabel("按作品（IP）分组展示收藏进度。集齐某 IP 全部角色可解锁对应主题皮肤；🗡 表示专武已解锁。")
        desc.setStyleSheet("color: #9a9080; font-size: 13px;")
        header_layout.addWidget(desc)

        self.ip_progress = QLabel()
        self.ip_progress.setStyleSheet("color: #fbbf24; font-size: 14px; font-weight: bold;")
        header_layout.addWidget(self.ip_progress)
        layout.addWidget(header)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        self.ip_content = QWidget()
        self.ip_content.setStyleSheet("background: transparent;")
        self.ip_layout = QVBoxLayout(self.ip_content)
        self.ip_layout.setSpacing(10)
        self.ip_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        scroll.setWidget(self.ip_content)
        layout.addWidget(scroll, 1)

    def _render_ip(self):
        while self.ip_layout.count():
            item = self.ip_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        groups = {}
        for pool in (FIVE_STAR_CHARS, FOUR_STAR_CHARS, THREE_STAR_CHARS):
            for cid, char in pool.items():
                groups.setdefault(char["anime"], []).append((cid, char))

        unlock_anime = set(ANIME_THEME_MAP.values())
        total_chars = sum(len(v) for v in groups.values())
        total_owned = sum(1 for cid in list(FIVE_STAR_CHARS) + list(FOUR_STAR_CHARS) + list(THREE_STAR_CHARS)
                          if self.data["characters"].get(cid, {}).get("count", 0) > 0)
        completed_ips = 0

        for anime, chars in groups.items():
            owned_flags = [self.data["characters"].get(c, {}).get("count", 0) > 0 for c, _ in chars]
            owned_n = sum(owned_flags)
            full = owned_n >= len(chars)
            if full:
                completed_ips += 1

            card = QFrame()
            card.setObjectName("ipFull" if full else "ipCard")
            if full:
                card.setStyleSheet("QFrame#ipFull { background-color: #2a2010; border: 2px solid #d4a853; border-radius: 6px; }")
            else:
                card.setStyleSheet("QFrame#ipCard { background-color: #16162a; border: 1px solid #3d3528; border-radius: 6px; }")

            cl = QVBoxLayout(card)
            cl.setContentsMargins(14, 10, 14, 10)
            cl.setSpacing(8)

            row1 = QHBoxLayout()
            name_lbl = QLabel(("🏆 " if full else "📖 ") + f"《{anime}》")
            name_lbl.setStyleSheet(f"color: {'#d4a853' if full else '#e8e0d0'}; font-size: 15px; font-weight: bold;")
            row1.addWidget(name_lbl)

            if anime in unlock_anime:
                tag = QLabel("🎨 主题已解锁" if owned_n > 0 else "🎨 集齐解锁主题")
                tag.setStyleSheet("color: #8b5cf6; font-size: 11px; font-weight: bold;")
                row1.addWidget(tag)

            row1.addStretch()
            prog_lbl = QLabel(f"{owned_n}/{len(chars)}")
            prog_lbl.setStyleSheet(f"color: {'#fbbf24' if full else '#9a9080'}; font-size: 14px; font-weight: bold;")
            row1.addWidget(prog_lbl)
            cl.addLayout(row1)

            grid = QGridLayout()
            grid.setSpacing(6)
            for idx, ((cid, char), ok) in enumerate(zip(chars, owned_flags)):
                chip = QLabel()
                chip.setObjectName("ipChip")
                rarity = char["rarity"]
                if ok:
                    wowned, _ = get_weapon_state(self.data, cid)
                    icon = "🗡" if wowned else "★"
                    color = "#d4a853" if rarity == 5 else ("#9a7fc8" if rarity == 4 else "#5a8a9a")
                    bg = "#241c0e" if rarity == 5 else ("#1c1428" if rarity == 4 else "#0e1c24")
                    chip.setText(f"{icon} {char['name']}")
                    chip.setStyleSheet(f"""
                        QLabel#ipChip {{
                            background-color: {bg}; color: {color};
                            border: 1px solid {color}; border-radius: 4px;
                            padding: 4px 8px; font-size: 11px; font-weight: bold;
                        }}
                    """)
                    chip.setToolTip(char["name"])
                else:
                    chip.setText("🔒 ? ? ?")
                    chip.setStyleSheet("""
                        QLabel#ipChip {
                            background-color: #14171d; color: #444466;
                            border: 1px solid #2d2d50; border-radius: 4px;
                            padding: 4px 8px; font-size: 11px;
                        }
                    """)
                    chip.setToolTip(char["name"])
                chip.setAlignment(Qt.AlignmentFlag.AlignCenter)
                chip.setFixedHeight(26)
                chip.setCursor(Qt.CursorShape.PointingHandCursor)
                chip.mousePressEvent = lambda e, c=cid, r=rarity: self._show_char_detail(c, r)
                grid.addWidget(chip, idx // 5, idx % 5)
            cl.addLayout(grid)

            self.ip_layout.addWidget(card)

        self.ip_progress.setText(
            f"总收藏：{total_owned} / {total_chars} 角色　|　全收集 IP：{completed_ips} / {len(groups)}")

    def _char_display_name(self, cid):
        char = (FIVE_STAR_CHARS.get(cid) or FOUR_STAR_CHARS.get(cid) or THREE_STAR_CHARS.get(cid))
        return char["name"] if char else cid

    # ==================== 刷新 ====================
    def refresh(self):
        _rollover(self.data)
        check_commissions(self.data)
        _check_achievements(self.data)

        self._check_daily_class()

        ar = self.data["adventure_rank"]
        self.ar_label.setText(f"AR {ar}")
        need = adventure_exp_needed(ar)
        pct = min(100, int(self.data["adventure_exp"] / need * 100))
        self.exp_bar.setValue(pct)
        self.exp_label.setText(
            f"经验：{self.data['adventure_exp']} / {need}（{pct}%） 连续学习：{self.data.get('streak_days', 0)}天")
        self.xp_label.setText(f"💎 {self.data['spendable_xp']:,} XP")
        self.primogem_label.setText(f"💠 {self.data['primogems']:,}")
        self.starglitter_label.setText(f"✨ {self.data.get('starglitter', 0)}")
        self.stardust_label.setText(f"💫 {self.data.get('stardust', 0)}")
        self.fate_label.setText(f"🎴 {self.data['intertwined_fate']}")

        if hasattr(self, 'today_summary_label'):
            tm = self.data.get("today_study_minutes", 0)
            ts = self.data.get("today_sessions", 0)
            self.today_summary_label.setText(
                f"今日已学习：{tm} 分钟 ｜ 完成 Session：{ts} 个\n"
                f"周Boss充能：{self.data['weekly_boss'].get('minutes', 0)} / {WEEKLY_BOSS_MINUTES} 分钟"
                f" ｜ ⚡双倍卡 ×{self.data.get('double_cards', 0)}")

        up_id = self.data["wish"]["up_character"]
        up_char = FIVE_STAR_CHARS[up_id]
        self.up_info.setText(
            f"当期UP：⭐⭐⭐⭐⭐ 来自《{up_char['anime']}》的神秘角色「？？？」\n"
            f"抽到角色同步获得：专属技能 + 专武（重复 → 专武精炼 R1~R5）\n"
            f"三星祈愿：💫 星尘 ×1~3（10/30/70 可兑换随机三/四/五星角色）")
        wt = get_current_weekly_theme()
        self.weekly_theme_label.setText(f"📅 本周主题：{wt['name']}\n{wt['desc']}")

        w = self.data["wish"]
        self.pity_5label.setText(f"五星保底：{w['pity_5star']}/90")
        self.pity_4label.setText(f"四星保底：{w['pity_4star']}/10")
        self.guarantee_label.setText("大保底已激活" if w["guaranteed_up"] else "小保底（50%UP）")
        self.wish1_btn.setEnabled(self.data["intertwined_fate"] >= 1)
        self.wish10_btn.setEnabled(self.data["intertwined_fate"] >= 10)

        self._update_stardust_panel()
        self._render_chars()

        if hasattr(self, 'bonds_layout'):
            self._render_bonds()
        if hasattr(self, 'ip_layout'):
            self._render_ip()
        if hasattr(self, 'skill_count_label'):
            self._render_skills()
        if hasattr(self, 'commission_frame'):
            self._render_commissions()
            self._render_achievements()
        if hasattr(self, 'boss_prog'):
            self._update_boss()
        if hasattr(self, 'shop_balance'):
            self._render_shop()
        if hasattr(self, 'history_tree'):
            self._render_history()

    # ==================== 主题皮肤切换 ====================
    def _build_theme_button(self):
        self.theme_btn = QPushButton("🎨")
        self.theme_btn.setFixedSize(40, 36)
        self.theme_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.theme_btn.setStyleSheet("""
            QPushButton { background-color: #2d2d50; color: #f5f5fa; border: none; border-radius: 8px; font-size: 16px; }
            QPushButton:hover { background-color: #3d3d6a; }
        """)
        self.theme_btn.clicked.connect(self._show_theme_menu)
        bar = self.ar_label.parent()
        if bar and bar.layout():
            bar.layout().addWidget(self.theme_btn)

    def _show_theme_menu(self):
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu { background-color: #16162a; color: #f5f5fa; border: 1px solid #2d2d50;
                    border-radius: 8px; padding: 4px; }
            QMenu::item { padding: 8px 20px; border-radius: 4px; }
            QMenu::item:selected { background-color: #8b5cf6; }
        """)
        for tid, theme in THEMES.items():
            unlocked = self._is_theme_unlocked(tid)
            if unlocked:
                action = menu.addAction(
                    f"{'✅' if tid == self.data.get('current_theme', 'default') else '  '} {theme['name']}")
                action.triggered.connect(lambda checked, t=tid: self._apply_theme(t))
            else:
                action = menu.addAction(f"🔒 {theme['name']}（{theme['unlock']}）")
                action.setEnabled(False)
        menu.exec(self.theme_btn.mapToGlobal(self.theme_btn.rect().bottomLeft()))

    def _is_theme_unlocked(self, theme_id):
        if theme_id == "default":
            return True
        anime = ANIME_THEME_MAP.get(theme_id)
        if not anime:
            return False
        for cid, cdata in self.data["characters"].items():
            if cdata.get("count", 0) > 0:
                char = FIVE_STAR_CHARS.get(cid) or FOUR_STAR_CHARS.get(cid) or THREE_STAR_CHARS.get(cid)
                if char and char["anime"] == anime:
                    return True
        return False

    def _apply_theme(self, theme_id):
        self.data["current_theme"] = theme_id
        save_data(self.data)
        theme = THEMES[theme_id]
        QMessageBox.information(self, "🎨 主题已切换",
                                f"已切换到「{theme['name']}」主题！\n\n重启程序后完全生效。")

    # ==================== 每日角色小课堂 ====================
    def _check_daily_class(self):
        today_str = date.today().strftime("%Y-%m-%d")
        if self.data.get("last_class_date") == today_str:
            return
        owned = [cid for cid, cdata in self.data["characters"].items() if cdata.get("count", 0) > 0]
        if not owned:
            return
        self.data["last_class_date"] = today_str
        save_data(self.data)
        QTimer.singleShot(500, self._show_daily_class)

    def _show_daily_class(self):
        owned = [cid for cid, cdata in self.data["characters"].items() if cdata.get("count", 0) > 0]
        if not owned:
            return
        five_owned = [cid for cid in owned if cid in FIVE_STAR_CHARS]
        cid = random.choice(five_owned) if five_owned and random.random() < 0.6 else random.choice(owned)
        char = FIVE_STAR_CHARS.get(cid) or FOUR_STAR_CHARS.get(cid) or THREE_STAR_CHARS.get(cid)
        if not char:
            return
        vocab_list = CHAR_VOCABULARY.get(cid, GENERAL_VOCABULARY)
        vocab = random.choice(vocab_list)
        dialog = DailyClassDialog(self, char, vocab)
        dialog.exec()

    # ==================== 技能收藏册 Tab ====================
    def _build_skill_tab(self):
        self.skill_tab = QWidget()
        layout = QVBoxLayout(self.skill_tab)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        info_card = CardFrame()
        info_layout = QVBoxLayout(info_card)
        info_layout.setContentsMargins(20, 16, 20, 16)
        info_layout.setSpacing(6)

        info_title = QLabel("📜 技能收藏册")
        info_title.setStyleSheet("color: #d4a853; font-size: 18px; font-weight: bold; letter-spacing: 2px;")
        info_layout.addWidget(info_title)

        info_desc = QLabel("技能与专武均忠实还原原作设定：首次获得角色时解锁（抽卡或星尘兑换均可），\n"
                           "重复获得角色将精炼专武（最高 R5），重复技能自动转化为原石 ×20。\n技能与专武均为纯收藏展示，收集越完整越好！")
        info_desc.setStyleSheet("color: #9a9080; font-size: 13px;")
        info_layout.addWidget(info_desc)

        self.skill_count_label = QLabel()
        self.skill_count_label.setStyleSheet("color: #fbbf24; font-size: 14px; font-weight: bold;")
        info_layout.addWidget(self.skill_count_label)
        layout.addWidget(info_card)

        s5_card = CardFrame()
        s5_layout = QVBoxLayout(s5_card)
        s5_layout.setContentsMargins(16, 12, 16, 12)

        s5_title = QLabel("⭐⭐⭐⭐⭐ 五星大招收藏")
        s5_title.setStyleSheet("color: #d4a853; font-size: 15px; font-weight: bold; letter-spacing: 1px;")
        s5_layout.addWidget(s5_title)

        self.s5_scroll = QScrollArea()
        self.s5_scroll.setWidgetResizable(True)
        self.s5_scroll.setMinimumHeight(140)
        self.s5_scroll.setMaximumHeight(220)
        self.s5_scroll.setStyleSheet("""
            QScrollArea { border: none; background: transparent; }
            QScrollBar:vertical { background: #0a0d12; width: 8px; border-radius: 4px; }
            QScrollBar::handle:vertical { background: #3d3528; border-radius: 4px; min-height: 20px; }
            QScrollBar::handle:vertical:hover { background: #d4a853; }
        """)
        self.s5_content = QWidget()
        self.s5_content.setStyleSheet("background: transparent;")
        self.s5_grid = QGridLayout(self.s5_content)
        self.s5_grid.setContentsMargins(4, 4, 4, 4)
        self.s5_grid.setSpacing(8)
        self.s5_scroll.setWidget(self.s5_content)
        s5_layout.addWidget(self.s5_scroll)
        layout.addWidget(s5_card)

        s4_card = CardFrame()
        s4_layout = QVBoxLayout(s4_card)
        s4_layout.setContentsMargins(16, 12, 16, 12)

        s4_title = QLabel("⭐⭐⭐⭐ 四星技能收藏")
        s4_title.setStyleSheet("color: #9a7fc8; font-size: 15px; font-weight: bold; letter-spacing: 1px;")
        s4_layout.addWidget(s4_title)

        self.s4_scroll = QScrollArea()
        self.s4_scroll.setWidgetResizable(True)
        self.s4_scroll.setMinimumHeight(140)
        self.s4_scroll.setStyleSheet("""
            QScrollArea { border: none; background: transparent; }
            QScrollBar:vertical { background: #0a0d12; width: 8px; border-radius: 4px; }
            QScrollBar::handle:vertical { background: #3d3528; border-radius: 4px; min-height: 20px; }
            QScrollBar::handle:vertical:hover { background: #d4a853; }
        """)
        self.s4_content = QWidget()
        self.s4_content.setStyleSheet("background: transparent;")
        self.s4_grid = QGridLayout(self.s4_content)
        self.s4_grid.setContentsMargins(4, 4, 4, 4)
        self.s4_grid.setSpacing(8)
        self.s4_scroll.setWidget(self.s4_content)
        s4_layout.addWidget(self.s4_scroll)
        layout.addWidget(s4_card, 1)

    def _render_skills(self):
        for grid in [self.s5_grid, self.s4_grid]:
            while grid.count():
                item = grid.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()

        owned5 = 0
        for idx, (sid, skill) in enumerate(FIVE_STAR_SKILLS.items()):
            owned = sid in self.data["skills"]
            if owned:
                owned5 += 1
            card = self._create_skill_card(sid, skill, owned, 5)
            self.s5_grid.addWidget(card, idx // 4, idx % 4)

        owned4 = 0
        for idx, (sid, skill) in enumerate(FOUR_STAR_SKILLS.items()):
            owned = sid in self.data["skills"]
            if owned:
                owned4 += 1
            card = self._create_skill_card(sid, skill, owned, 4)
            self.s4_grid.addWidget(card, idx // 4, idx % 4)

        self.skill_count_label.setText(
            f"📚 技能收藏：{owned5}/{len(FIVE_STAR_SKILLS)} 五星大招，"
            f"{owned4}/{len(FOUR_STAR_SKILLS)} 四星技能，"
            f"总计 {owned5 + owned4}/{len(FIVE_STAR_SKILLS) + len(FOUR_STAR_SKILLS)}")

    def _create_skill_card(self, sid, skill, owned, rarity):
        card = QFrame()
        if owned:
            bg = STAR5_BG if rarity == 5 else STAR4_BG
            border = "#d4a853" if rarity == 5 else "#9a7fc8"
        else:
            bg = "#16162a"
            border = "#2d2d50"
        card.setObjectName("skillCard")
        card.setStyleSheet(f"""
            QFrame#skillCard {{
                background-color: {bg};
                border: 2px solid {border};
                border-radius: 8px;
            }}
        """)
        card.setFixedSize(160, 110)
        card.setCursor(Qt.CursorShape.PointingHandCursor)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(2)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        if owned:
            stars = QLabel("★" * rarity)
            stars.setAlignment(Qt.AlignmentFlag.AlignCenter)
            stars.setStyleSheet(f"color: {border}; font-size: 11px;")
            layout.addWidget(stars)

            name = QLabel(skill["name"])
            name.setAlignment(Qt.AlignmentFlag.AlignCenter)
            name.setWordWrap(True)
            name.setStyleSheet("color: #f5f5fa; font-size: 11px; font-weight: bold;")
            layout.addWidget(name)

            effect = QLabel(skill["effect"])
            effect.setAlignment(Qt.AlignmentFlag.AlignCenter)
            effect.setWordWrap(True)
            effect.setStyleSheet("color: #9494b8; font-size: 9px;")
            layout.addWidget(effect)

            tag = QLabel("📖 已收藏")
            tag.setAlignment(Qt.AlignmentFlag.AlignCenter)
            tag.setStyleSheet("color: #7ab88a; font-size: 9px; font-weight: bold;")
            layout.addWidget(tag)
        else:
            stars = QLabel("★" * rarity)
            stars.setAlignment(Qt.AlignmentFlag.AlignCenter)
            stars.setStyleSheet("color: #333355; font-size: 11px;")
            layout.addWidget(stars)

            q = QLabel("❓")
            q.setAlignment(Qt.AlignmentFlag.AlignCenter)
            q.setStyleSheet("color: #444466; font-size: 20px; font-weight: bold;")
            layout.addWidget(q)

            name = QLabel("? ? ?")
            name.setAlignment(Qt.AlignmentFlag.AlignCenter)
            name.setStyleSheet("color: #444466; font-size: 11px; font-weight: bold;")
            layout.addWidget(name)

            locked = QLabel("未解锁")
            locked.setAlignment(Qt.AlignmentFlag.AlignCenter)
            locked.setStyleSheet("color: #333355; font-size: 9px;")
            layout.addWidget(locked)

        card.mousePressEvent = lambda e, s=sid: self._show_skill_detail(s)
        return card

    def _show_skill_detail(self, sid):
        skill = ALL_SKILLS.get(sid)
        if not skill:
            return
        if sid not in self.data["skills"]:
            QMessageBox.information(self, "未解锁", "这个技能尚未解锁。\n抽到对应角色（或星尘兑换）即可获得！")
            return
        char_pool = FIVE_STAR_CHARS if skill["rarity"] == 5 else FOUR_STAR_CHARS
        char = char_pool.get(skill["char"], {})
        owned = self.data["skills"][sid].get("count", 1)
        msg = (f"{'⭐' * skill['rarity']} {skill['name']}\n"
               f"类型：{skill.get('type', '')} | 所属：{char.get('name', '???')}\n\n"
               f"能力：{skill.get('effect', '')}\n\n"
               f"{skill['desc']}\n\n"
               f"持有：×{owned}")
        QMessageBox.information(self, f"{skill['name']} 详情", msg)

    # ==================== 每日委托 Tab ====================
    def _build_quest_tab(self):
        self.quest_tab = QWidget()
        layout = QVBoxLayout(self.quest_tab)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        dc_card = CardFrame()
        dc_layout = QVBoxLayout(dc_card)
        dc_layout.setContentsMargins(20, 16, 20, 16)
        dc_layout.setSpacing(8)

        dc_title = QLabel("📜 每日委托")
        dc_title.setStyleSheet("color: #d4a853; font-size: 18px; font-weight: bold; letter-spacing: 2px;")
        dc_layout.addWidget(dc_title)

        dc_desc = QLabel("完成学习 Session / 累计学习时长即可自动完成委托，领取原石。全部完成额外获得纠缠之缘。")
        dc_desc.setStyleSheet("color: #9a9080; font-size: 13px;")
        dc_layout.addWidget(dc_desc)

        self.commission_frame = QVBoxLayout()
        dc_layout.addLayout(self.commission_frame)

        self.commission_bonus_btn = QPushButton("🎁 领取全部完成奖励")
        self.commission_bonus_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.commission_bonus_btn.setStyleSheet("""
            QPushButton { background-color: #fbbf24; color: #1a1a2e; border: none;
                          border-radius: 6px; padding: 10px; font-size: 14px; font-weight: bold; }
            QPushButton:hover { background-color: #fcd34d; }
            QPushButton:disabled { background-color: #3d3528; color: #5a5548; }
        """)
        self.commission_bonus_btn.clicked.connect(self.claim_bonus)
        dc_layout.addWidget(self.commission_bonus_btn)
        layout.addWidget(dc_card)

        ac_card = CardFrame()
        ac_layout = QVBoxLayout(ac_card)
        ac_layout.setContentsMargins(20, 16, 20, 16)

        ac_title = QLabel("🏆 成就")
        ac_title.setStyleSheet("color: #d4a853; font-size: 18px; font-weight: bold; letter-spacing: 2px; padding-bottom: 8px;")
        ac_layout.addWidget(ac_title)

        self.ach_table = QTableWidget(0, 4)
        self.ach_table.setHorizontalHeaderLabels(["成就", "描述", "奖励", "状态"])
        self.ach_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.ach_table.setStyleSheet("""
            QTableWidget {
                background-color: #14171d;
                color: #e8e0d0;
                gridline-color: #2a2520;
                border: 1px solid #3d3528;
                border-radius: 4px;
                font-size: 12px;
            }
            QTableWidget::item { padding: 6px; }
            QHeaderView::section {
                background-color: #1e232b;
                color: #d4a853;
                border: none;
                border-bottom: 1px solid #d4a853;
                padding: 8px;
                font-weight: bold;
                letter-spacing: 1px;
            }
        """)
        ac_layout.addWidget(self.ach_table)
        layout.addWidget(ac_card, 1)

    def _render_commissions(self):
        while self.commission_frame.count():
            item = self.commission_frame.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        check_commissions(self.data)

        all_done = True
        for i, task in enumerate(self.data["daily_commissions"]["tasks"]):
            row = QFrame()
            row.setObjectName("commissionRow")
            row.setStyleSheet(f"""
                QFrame#commissionRow {{
                    background-color: {'#0e2a1a' if task['done'] else '#0e0e1c'};
                    border-radius: 6px;
                }}
            """)
            row_layout = QHBoxLayout(row)
            row_layout.setContentsMargins(12, 8, 12, 8)

            status = "✅" if task["done"] else "⬜"
            lbl = QLabel(f"{status} {task['desc']}")
            lbl.setStyleSheet(f"color: {'#f5f5fa' if task['done'] else '#9494b8'}; font-size: 13px;")
            row_layout.addWidget(lbl, 1)

            reward_lbl = QLabel(f"💎{task['reward']}")
            reward_lbl.setStyleSheet("color: #fbbf24; font-size: 12px; font-weight: bold;")
            row_layout.addWidget(reward_lbl)

            if task["done"] and not task["claimed"]:
                btn = QPushButton("领取")
                btn.setFixedSize(60, 28)
                btn.setCursor(Qt.CursorShape.PointingHandCursor)
                btn.setStyleSheet("QPushButton { background-color: #7ab88a; color: white; border: none; "
                                  "border-radius: 6px; font-size: 11px; font-weight: bold; } "
                                  "QPushButton:hover { background-color: #27ae60; }")
                btn.clicked.connect(lambda checked, idx=i: self._claim_com(idx))
                row_layout.addWidget(btn)
            elif task["claimed"]:
                claimed = QLabel("已领取")
                claimed.setStyleSheet("color: #7ab88a; font-size: 11px;")
                row_layout.addWidget(claimed)

            if not task["done"]:
                all_done = False

            self.commission_frame.addWidget(row)

        if all_done and not self.data.get("commission_bonus_claimed"):
            self.commission_bonus_btn.setEnabled(True)
        else:
            self.commission_bonus_btn.setEnabled(False)

        if self.data.get("commission_bonus_claimed"):
            self.commission_bonus_btn.setText("✅ 额外奖励已领取")
            self.commission_bonus_btn.setEnabled(False)

    def _claim_com(self, idx):
        reward = claim_commission(self.data, idx)
        if reward:
            QMessageBox.information(self, "委托完成", f"领取原石 ×{reward}")
            self.refresh()

    def claim_bonus(self):
        bonus = claim_commission_bonus(self.data)
        if bonus:
            QMessageBox.information(self, "🎉 每日委托全部完成！", f"获得：💎 原石 ×{bonus} + 🎴 纠缠之缘 ×1")
            self.refresh()

    def _render_achievements(self):
        self.ach_table.setRowCount(0)
        for ach in ACHIEVEMENTS:
            done = ach["id"] in self.data["achievements"]
            row = self.ach_table.rowCount()
            self.ach_table.insertRow(row)
            items = [ach["name"], ach["desc"], f"💎{ach['reward']}",
                     "✅ 已达成" if done else "🔒 未达成"]
            for col, text in enumerate(items):
                item = QTableWidgetItem(text)
                item.setForeground(QColor("#34d399" if done else "#9494b8"))
                if col >= 2:
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.ach_table.setItem(row, col, item)

    # ==================== 周 Boss Tab ====================
    def _build_boss_tab(self):
        self.boss_tab = QWidget()
        layout = QVBoxLayout(self.boss_tab)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        card = CardFrame()
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 16, 20, 16)
        card_layout.setSpacing(10)

        boss_title = QLabel("👹 IELTS Weekly Boss")
        boss_title.setStyleSheet("color: #d4a853; font-size: 18px; font-weight: bold; letter-spacing: 2px;")
        card_layout.addWidget(boss_title)

        boss_desc = QLabel(
            f"本周累计学习达到 {WEEKLY_BOSS_MINUTES} 分钟（约 {WEEKLY_BOSS_MINUTES // 60} 小时）即可挑战 Boss！\n"
            f"学习时长自动统计充能，无需手动打卡。每天坚持，Boss 自然倒下。")
        boss_desc.setStyleSheet("color: #9a9080; font-size: 13px;")
        card_layout.addWidget(boss_desc)

        self.boss_bar = QProgressBar()
        self.boss_bar.setTextVisible(False)
        self.boss_bar.setFixedHeight(16)
        self.boss_bar.setStyleSheet("""
            QProgressBar {
                background-color: #0a0d12;
                border-radius: 8px;
                border: 1px solid #3d3528;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #b8434f, stop:0.5 #fb7185, stop:1 #fda4af);
                border-radius: 7px;
            }
        """)
        card_layout.addWidget(self.boss_bar)

        self.boss_prog = QLabel()
        self.boss_prog.setStyleSheet("color: #fbbf24; font-size: 15px; font-weight: bold;")
        card_layout.addWidget(self.boss_prog)

        self.btn_boss = StyledButton("⚔️ 挑战 Weekly Boss", "#fb7185", "#f43f5e", "#ffffff")
        self.btn_boss.setMinimumHeight(44)
        self.btn_boss.clicked.connect(self.claim_boss)
        card_layout.addWidget(self.btn_boss)

        layout.addWidget(card)
        layout.addStretch()

    def _update_boss(self):
        wb = self.data.get("weekly_boss") or {}
        minutes = wb.get("minutes", 0)
        claimed = wb.get("claimed", False)
        self.boss_bar.setMaximum(WEEKLY_BOSS_MINUTES)
        self.boss_bar.setValue(min(minutes, WEEKLY_BOSS_MINUTES))
        pct = min(100, int(minutes / WEEKLY_BOSS_MINUTES * 100))
        status = "　✅ 本周Boss已被击败" if claimed else ""
        self.boss_prog.setText(
            f"本周累计学习：{minutes} / {WEEKLY_BOSS_MINUTES} 分钟（{pct}%）{status}")
        self.btn_boss.setEnabled(minutes >= WEEKLY_BOSS_MINUTES and not claimed)

    def claim_boss(self):
        wb = self.data.get("weekly_boss") or {}
        if wb.get("claimed"):
            return
        if wb.get("minutes", 0) < WEEKLY_BOSS_MINUTES:
            QMessageBox.information(self, "充能不足",
                                    f"本周还需累计学习 {WEEKLY_BOSS_MINUTES - wb.get('minutes', 0)} 分钟才能挑战 Boss。")
            return
        xp = roll((100, 300))
        add_xp(self.data, xp, "Weekly Boss", "本周学习目标达成")
        self.data["primogems"] += 80
        self.data["intertwined_fate"] += 2
        loot_n = random.randint(1, 10)
        extra = ""
        if loot_n == 10:
            add_xp(self.data, 500, "💎 Boss JACKPOT", "+500XP")
            self.data["intertwined_fate"] += 3
            extra = "\n💎 Boss Loot 10！+500XP + 纠缠之缘×3"
        self.data["weekly_boss"]["claimed"] = True
        save_data(self.data)
        QMessageBox.information(self, "👹 Boss Defeated!",
                                f"+{xp} XP，+💎80原石，+🎴2纠缠之缘{extra}")
        self.refresh()

    # ==================== 商店 Tab ====================
    def _build_shop_tab(self):
        self.shop_tab = QWidget()
        layout = QVBoxLayout(self.shop_tab)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        xp_card = CardFrame()
        xp_layout = QVBoxLayout(xp_card)
        xp_layout.setContentsMargins(20, 16, 20, 16)
        xp_layout.setSpacing(8)

        shop_title = QLabel("🛒 祈愿资源商店（XP 兑换）")
        shop_title.setStyleSheet("color: #d4a853; font-size: 18px; font-weight: bold; letter-spacing: 2px;")
        xp_layout.addWidget(shop_title)

        shop_desc = QLabel("学习赚 XP，XP 兑抽卡资源——所有奖励都为祈愿服务。消费只扣 Spendable，Lifetime 不变。")
        shop_desc.setStyleSheet("color: #9a9080; font-size: 13px;")
        xp_layout.addWidget(shop_desc)

        self.shop_balance = QLabel()
        self.shop_balance.setStyleSheet("color: #fbbf24; font-size: 15px; font-weight: bold; padding: 6px 0;")
        xp_layout.addWidget(self.shop_balance)

        self.shop_items_layout = QVBoxLayout()
        xp_layout.addLayout(self.shop_items_layout)
        layout.addWidget(xp_card)

        bottom = QHBoxLayout()
        bottom.setSpacing(16)

        sg_card = CardFrame()
        sg_layout = QVBoxLayout(sg_card)
        sg_layout.setContentsMargins(16, 12, 16, 12)
        sg_layout.setSpacing(6)

        sg_title = QLabel("✨ 星辉商店")
        sg_title.setStyleSheet("color: #d4a853; font-size: 15px; font-weight: bold; letter-spacing: 1px;")
        sg_layout.addWidget(sg_title)

        self.sg_balance_label = QLabel()
        self.sg_balance_label.setStyleSheet("color: #7aa8c0; font-size: 12px; font-weight: bold;")
        sg_layout.addWidget(self.sg_balance_label)

        self.sg_items_layout = QVBoxLayout()
        sg_layout.addLayout(self.sg_items_layout)
        bottom.addWidget(sg_card)

        prim_card = CardFrame()
        prim_layout = QVBoxLayout(prim_card)
        prim_layout.setContentsMargins(16, 12, 16, 12)
        prim_layout.setSpacing(6)

        prim_title = QLabel("💠 原石兑换")
        prim_title.setStyleSheet("color: #9a7fc8; font-size: 15px; font-weight: bold; letter-spacing: 1px;")
        prim_layout.addWidget(prim_title)

        self.primogem_balance_label = QLabel()
        self.primogem_balance_label.setStyleSheet("color: #9a7fc8; font-size: 12px; font-weight: bold;")
        prim_layout.addWidget(self.primogem_balance_label)

        self.exchange_btn = StyledButton("💠160原石 → 🎴1纠缠之缘", "#a855f7", "#c084fc", "#ffffff")
        self.exchange_btn.clicked.connect(self.exchange_primogem)
        prim_layout.addWidget(self.exchange_btn)
        prim_layout.addStretch()

        bottom.addWidget(prim_card)
        layout.addLayout(bottom)

        hist_card = CardFrame()
        hist_layout = QVBoxLayout(hist_card)
        hist_layout.setContentsMargins(20, 12, 20, 12)

        hist_title = QLabel("近期兑换（选中可删除退还；⚠ 表示资源已消耗不可退）")
        hist_title.setStyleSheet("color: #9494b8; font-size: 13px; padding-bottom: 6px;")
        hist_layout.addWidget(hist_title)

        self.purchase_list = QListWidget()
        self.purchase_list.setStyleSheet("QListWidget { background-color: #14171d; color: #e8e0d0; "
                                         "border: 1px solid #3d3528; border-radius: 4px; font-size: 12px; padding: 4px; } "
                                         "QListWidget::item { padding: 6px; } "
                                         "QListWidget::item:selected { background-color: #3d3528; color: #d4a853; }")
        self.purchase_list.setMaximumHeight(100)
        hist_layout.addWidget(self.purchase_list)

        del_btn = StyledButton("🗑 删除选中并退还", "#fb7185", "#f43f5e", "#ffffff")
        del_btn.clicked.connect(self.del_purchase)
        hist_layout.addWidget(del_btn)

        layout.addWidget(hist_card)

    def _render_shop(self):
        self.shop_balance.setText(
            f"💰 可用 XP：{self.data['spendable_xp']:,}　｜　⚡双倍经验卡 ×{self.data.get('double_cards', 0)}"
            f"　｜　💫 星尘 ×{self.data.get('stardust', 0)}")
        self.sg_balance_label.setText(
            f"✨ 星辉：{self.data.get('starglitter', 0)}　　🎴 纠缠之缘：{self.data['intertwined_fate']}")
        self.primogem_balance_label.setText(f"💠 原石：{self.data['primogems']:,}")

        while self.shop_items_layout.count():
            item = self.shop_items_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        for item in SHOP_ITEMS:
            row = QFrame()
            row.setObjectName("shopRow")
            row.setStyleSheet("QFrame#shopRow { background-color: #0e0e1c; border-radius: 6px; }")
            row_layout = QHBoxLayout(row)
            row_layout.setContentsMargins(12, 8, 12, 8)

            lbl = QLabel(f"🎁 {item['label']}")
            lbl.setStyleSheet("color: #e8e0d0; font-size: 13px;")
            row_layout.addWidget(lbl, 1)

            price = QLabel(f"{item['xp']} XP")
            price.setStyleSheet("color: #fbbf24; font-size: 13px; font-weight: bold;")
            row_layout.addWidget(price)

            btn = QPushButton("兑换")
            btn.setFixedSize(60, 28)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet("QPushButton { background-color: #2d2d50; color: white; border: none; "
                              "border-radius: 6px; font-size: 11px; } "
                              "QPushButton:hover { background-color: #3d3d6a; }")
            btn.clicked.connect(lambda checked, it=item: self.buy_item(it))
            row_layout.addWidget(btn)

            self.shop_items_layout.addWidget(row)

        while self.sg_items_layout.count():
            item = self.sg_items_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        for item in STARGITTER_SHOP:
            row = QFrame()
            row.setObjectName("sgRow")
            row.setStyleSheet("QFrame#sgRow { background-color: #0e1a2a; border-radius: 6px; }")
            row_layout = QHBoxLayout(row)
            row_layout.setContentsMargins(10, 6, 10, 6)

            lbl = QLabel(item["item"])
            lbl.setStyleSheet("color: #f5f5fa; font-size: 12px;")
            lbl.setWordWrap(True)
            row_layout.addWidget(lbl, 1)

            can_afford = self.data.get("starglitter", 0) >= item["cost"]
            btn = QPushButton(f"✨{item['cost']}")
            btn.setFixedSize(56, 26)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setEnabled(can_afford)
            btn.setStyleSheet(
                "QPushButton { background-color: #0e3a4a; color: #7aa8c0; border: none; "
                "border-radius: 4px; font-size: 11px; font-weight: bold; } "
                "QPushButton:hover { background-color: #1a4a5a; } "
                "QPushButton:disabled { background-color: #16202a; color: #44535c; }")
            btn.clicked.connect(lambda checked, it=item: self.buy_starglitter(it))
            row_layout.addWidget(btn)

            self.sg_items_layout.addWidget(row)

        self.purchase_list.clear()
        for p in self.data.get("purchases", []):
            flag = "" if purchase_refundable(self.data, p) else " ⚠不可退"
            self.purchase_list.addItem(f"{p.get('time', '')} {p['item']} (-{p['xp']}XP){flag}")

    def buy_item(self, item):
        t = item.get("type")
        reply = QMessageBox.question(self, "确认兑换", f"花费 {item['xp']} XP 兑换：\n{item['label']}")
        if reply != QMessageBox.StandardButton.Yes:
            return
        if not spend_xp(self.data, item["xp"], item["label"], t, item.get("amount", 0)):
            QMessageBox.warning(self, "XP不足", f"需要 {item['xp']} XP。")
            return
        amount = item.get("amount", 0)
        if t == "double_card":
            self.data["double_cards"] = self.data.get("double_cards", 0) + amount
            msg = f"⚡ 双倍经验卡 ×{amount}（当前 {self.data['double_cards']} 张）\n结束学习时自动消耗，XP ×2"
        elif t == "primogem":
            self.data["primogems"] += amount
            msg = f"💠 原石 ×{amount}"
        elif t == "starglitter":
            self.data["starglitter"] += amount
            msg = f"✨ 星辉 ×{amount}"
        elif t == "fate":
            self.data["intertwined_fate"] += amount
            msg = f"🎴 纠缠之缘 ×{amount}"
        elif t == "stardust":
            self.data["stardust"] = self.data.get("stardust", 0) + amount
            msg = (f"💫 星尘 ×{amount}（当前 {self.data['stardust']}）\n"
                   f"10 / 30 / 70 可兑换随机三 / 四 / 五星角色")
        else:
            msg = item["label"]
        save_data(self.data)
        QMessageBox.information(self, "🎉 兑换成功", msg)
        self.refresh()

    def buy_starglitter(self, item):
        if self.data.get("starglitter", 0) < item["cost"]:
            QMessageBox.warning(self, "星辉不足",
                                f"需要 ✨{item['cost']} 星辉，当前 ✨{self.data.get('starglitter', 0)}。\n"
                                f"（重复获得角色：五星+10星辉，四星/三星+2星辉）")
            return
        reply = QMessageBox.question(self, "确认兑换",
                                     f"花费 ✨{item['cost']} 星辉兑换：\n{item['item']}")
        if reply != QMessageBox.StandardButton.Yes:
            return
        if exchange_starglitter(self.data, item):
            QMessageBox.information(self, "🎉 兑换成功",
                                    f"已兑换：{item['item']}\n\n"
                                    f"✨ 星辉：{self.data.get('starglitter', 0)}\n"
                                    f"🎴 纠缠之缘：{self.data['intertwined_fate']}")
            self.refresh()
        else:
            QMessageBox.warning(self, "兑换失败", "星辉不足。")

    def exchange_primogem(self):
        if self.data["primogems"] < 160:
            QMessageBox.warning(self, "原石不足",
                                f"需要 💠160 原石，当前 💠{self.data['primogems']}。")
            return
        reply = QMessageBox.question(self, "确认兑换", "花费 💠160 原石兑换 🎴1 纠缠之缘？")
        if reply != QMessageBox.StandardButton.Yes:
            return
        if exchange_primogems_to_fate(self.data):
            QMessageBox.information(self, "🎉 兑换成功",
                                    f"🎴 纠缠之缘：{self.data['intertwined_fate']}\n"
                                    f"💠 原石：{self.data['primogems']:,}")
            self.refresh()
        else:
            QMessageBox.warning(self, "原石不足", "需要 💠160 原石。")

    def del_purchase(self):
        sel = self.purchase_list.currentRow()
        if sel < 0:
            QMessageBox.information(self, "提示", "请先选中一条记录。")
            return
        p = self.data["purchases"][sel]
        if not purchase_refundable(self.data, p):
            QMessageBox.warning(self, "无法退还",
                                "该笔兑换对应的资源已被消耗（或数量不足），无法退还。")
            return
        reply = QMessageBox.question(self, "确认", f"删除并退还 {p['xp']} XP 及对应资源？\n{p['item']}")
        if reply == QMessageBox.StandardButton.Yes:
            delete_purchase(self.data, sel)
            self.refresh()

    # ==================== 历史记录 Tab ====================
    def _build_history_tab(self):
        self.history_tab = QWidget()
        layout = QVBoxLayout(self.history_tab)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        self.stats_label = QLabel()
        self.stats_label.setStyleSheet("color: #e8e0d0; font-size: 14px; padding: 8px 0;")
        layout.addWidget(self.stats_label)

        btn_row = QHBoxLayout()
        hint = QLabel("选中后可删除（自动回滚XP）")
        hint.setStyleSheet("color: #9a9080; font-size: 12px;")
        btn_row.addWidget(hint)
        btn_row.addStretch()
        del_btn = StyledButton("🗑 删除选中", "#fb7185", "#f43f5e", "#ffffff")
        del_btn.clicked.connect(self.del_record)
        btn_row.addWidget(del_btn)
        layout.addLayout(btn_row)

        self.history_tree = QTableWidget(0, 4)
        self.history_tree.setHorizontalHeaderLabels(["时间", "类型", "详情", "XP"])
        self.history_tree.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.history_tree.setStyleSheet("""
            QTableWidget {
                background-color: #14171d;
                color: #e8e0d0;
                gridline-color: #2a2520;
                border: 1px solid #3d3528;
                border-radius: 4px;
                font-size: 12px;
            }
            QTableWidget::item { padding: 6px; }
            QHeaderView::section {
                background-color: #1e232b;
                color: #d4a853;
                border: none;
                border-bottom: 1px solid #d4a853;
                padding: 8px;
                font-weight: bold;
                letter-spacing: 1px;
            }
        """)
        layout.addWidget(self.history_tree, 1)

    def _render_history(self):
        history = self.data.get("history", [])
        total_xp = sum(h.get("xp", 0) for h in history)
        total_sessions = sum(1 for h in history if h.get("type") in ("Session", "完成奖励", "学习"))
        total_minutes = sum(h.get("minutes", 0) for h in history if h.get("type") == "学习")
        self.stats_label.setText(
            f"📊 总记录：{len(history)} 条 | 学习次数：{total_sessions} | "
            f"累计学习：{total_minutes} 分钟 | 累计 XP：{total_xp:+,}")
        self.history_tree.setRowCount(0)
        for h in reversed(history):
            row = self.history_tree.rowCount()
            self.history_tree.insertRow(row)
            xp = h.get("xp", 0)
            if xp > 0:
                xp_color = "#34d399"
            elif xp < 0:
                xp_color = "#fb7185"
            else:
                xp_color = "#9494b8"
            items = [h.get("time", ""), h.get("type", ""), h.get("detail", ""),
                     f"{xp:+d}" if xp != 0 else "-"]
            for col, text in enumerate(items):
                item = QTableWidgetItem(text)
                item.setForeground(QColor(xp_color))
                if col == 3:
                    item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                self.history_tree.setItem(row, col, item)

    def del_record(self):
        sel = self.history_tree.currentRow()
        if sel < 0:
            QMessageBox.information(self, "提示", "请先选中一条记录。")
            return
        history = self.data.get("history", [])
        idx = len(history) - 1 - sel
        if idx < 0 or idx >= len(history):
            return
        h = history[idx]
        reply = QMessageBox.question(self, "确认",
                                     f"删除这条记录并回滚 {h.get('xp', 0)} XP？\n{h.get('detail', '')}")
        if reply == QMessageBox.StandardButton.Yes:
            delete_history_record(self.data, idx)
            self.refresh()


# ============================================================
# 每日角色小课堂对话框
# ============================================================
class DailyClassDialog(QDialog):
    def __init__(self, parent, char, vocab):
        super().__init__(parent)
        self.setWindowTitle("📚 角色小课堂")
        self.setFixedSize(480, 440)
        self.setStyleSheet("background-color: #14171d; color: #e8e0d0;")
        self._char = char
        self._vocab = vocab
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        rarity = self._char["rarity"]
        rarity_color = "#d4a853" if rarity == 5 else ("#9a7fc8" if rarity == 4 else "#5a8a9a")
        card_bg = "#2a2010" if rarity == 5 else ("#1a1525" if rarity == 4 else "#101a20")

        header = QFrame()
        header.setObjectName("classHeader")
        header.setStyleSheet(f"QFrame#classHeader {{ background-color: {card_bg}; border: none; }}")
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(24, 16, 24, 16)
        header_layout.setSpacing(4)

        bar = QFrame()
        bar.setFixedHeight(3)
        bar.setStyleSheet(f"background-color: {rarity_color}; border: none;")
        layout.addWidget(bar)

        stars = QLabel("★" * rarity)
        stars.setStyleSheet(f"color: {rarity_color}; font-size: 14px; border: none;")
        header_layout.addWidget(stars)

        title = QLabel(f"📚 {self._char['name']}的小课堂")
        title.setStyleSheet("color: #f5f5fa; font-size: 20px; font-weight: bold; border: none;")
        header_layout.addWidget(title)

        subtitle = QLabel(f"《{self._char['anime']}》 「{self._char['title']}」")
        subtitle.setStyleSheet("color: #9a9080; font-size: 11px; border: none;")
        header_layout.addWidget(subtitle)
        layout.addWidget(header)

        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(24, 16, 24, 16)
        content_layout.setSpacing(10)

        intro = QLabel(f"「{self._char['name']}：今天我来教你一个词——」")
        intro.setStyleSheet(f"color: {rarity_color}; font-size: 13px; font-weight: bold;")
        intro.setWordWrap(True)
        content_layout.addWidget(intro)

        word_row = QHBoxLayout()
        lbl1 = QLabel("📖 单词：")
        lbl1.setStyleSheet("color: #9a9080; font-size: 13px;")
        word_row.addWidget(lbl1)
        word = QLabel(self._vocab["word"])
        word.setStyleSheet("color: #8b5cf6; font-size: 18px; font-weight: bold;")
        word_row.addWidget(word)
        word_row.addStretch()
        content_layout.addLayout(word_row)

        mean_row = QHBoxLayout()
        lbl2 = QLabel("📝 释义：")
        lbl2.setStyleSheet("color: #9a9080; font-size: 13px;")
        mean_row.addWidget(lbl2)
        mean = QLabel(self._vocab["meaning"])
        mean.setStyleSheet("color: #e8e0d0; font-size: 14px;")
        mean_row.addWidget(mean)
        mean_row.addStretch()
        content_layout.addLayout(mean_row)

        lbl3 = QLabel("💬 例句：")
        lbl3.setStyleSheet("color: #9a9080; font-size: 13px;")
        content_layout.addWidget(lbl3)

        example = QLabel(self._vocab["example"])
        example.setStyleSheet("color: #f5f5fa; font-size: 12px;")
        example.setWordWrap(True)
        content_layout.addWidget(example)

        content_layout.addSpacing(8)

        quote = QLabel(self._char.get("wish_text", "加油学习！"))
        quote.setStyleSheet(f"color: {rarity_color}; font-size: 12px; font-style: italic;")
        quote.setAlignment(Qt.AlignmentFlag.AlignCenter)
        quote.setWordWrap(True)
        content_layout.addWidget(quote)

        content_layout.addStretch()

        btn = QPushButton("✅ 记住了！")
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setMinimumWidth(140)
        btn.setStyleSheet("QPushButton { background-color: #8b5cf6; color: white; border: none; "
                          "border-radius: 6px; padding: 10px 24px; font-size: 14px; font-weight: bold; } "
                          "QPushButton:hover { background-color: #a78bfa; }")
        btn.clicked.connect(self.accept)
        content_layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignCenter)

        hint = QLabel("每天登录随机一个角色教你一个词！")
        hint.setStyleSheet("color: #9a9080; font-size: 10px;")
        hint.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(hint)

        layout.addWidget(content, 1)


# ============================================================
# 抽卡动画对话框
# ============================================================
class WishDialog(QDialog):
    def __init__(self, parent, results):
        super().__init__(parent)
        self.setWindowTitle("🎴 祈愿")
        self.setFixedSize(480, 640)
        self.setStyleSheet("background-color: #14171d; color: #e8e0d0;")
        self._results = results if isinstance(results, list) else [results]
        self._idx = 0
        self._build()
        self._animate_current()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(10)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        self.progress_label = QLabel()
        self.progress_label.setStyleSheet("color: #9a9080; font-size: 12px;")
        self.progress_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.progress_label)

        title = QLabel("祈 愿")
        title.setStyleSheet("color: #8888aa; font-size: 24px; font-weight: bold;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        self.stars_label = QLabel()
        self.stars_label.setStyleSheet("color: #8888aa; font-size: 28px;")
        self.stars_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.stars_label)

        self.avatar_label = QLabel()
        self.avatar_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.avatar_label.setFixedSize(160, 160)
        layout.addWidget(self.avatar_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.name_label = QLabel()
        self.name_label.setStyleSheet("color: #f5f5fa; font-size: 22px; font-weight: bold;")
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.name_label)

        self.anime_label = QLabel()
        self.anime_label.setStyleSheet("color: #9494b8; font-size: 13px;")
        self.anime_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.anime_label)

        self.skill_label = QLabel()
        self.skill_label.setStyleSheet("color: #9a7fc8; font-size: 12px; font-weight: bold;")
        self.skill_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.skill_label.setWordWrap(True)
        layout.addWidget(self.skill_label)

        self.weapon_label = QLabel()
        self.weapon_label.setStyleSheet("color: #d4a853; font-size: 12px; font-weight: bold;")
        self.weapon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.weapon_label.setWordWrap(True)
        layout.addWidget(self.weapon_label)

        self.xp_label = QLabel()
        self.xp_label.setStyleSheet("color: #7ab88a; font-size: 16px; font-weight: bold;")
        self.xp_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.xp_label)

        self.quote_label = QLabel()
        self.quote_label.setStyleSheet("color: #9a9080; font-size: 12px; font-style: italic;")
        self.quote_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.quote_label.setWordWrap(True)
        layout.addWidget(self.quote_label)

        layout.addStretch()

        self.continue_btn = QPushButton("确认")
        self.continue_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.continue_btn.setMinimumWidth(140)
        self.continue_btn.setStyleSheet("QPushButton { background-color: #8b5cf6; color: white; border: none; "
                                        "border-radius: 6px; padding: 10px 24px; font-size: 14px; font-weight: bold; } "
                                        "QPushButton:hover { background-color: #a78bfa; }")
        self.continue_btn.clicked.connect(self._next_or_close)
        layout.addWidget(self.continue_btn, alignment=Qt.AlignmentFlag.AlignCenter)

    def _animate_current(self):
        r = self._results[self._idx]
        for lbl in [self.name_label, self.anime_label, self.skill_label,
                    self.weapon_label, self.xp_label, self.quote_label]:
            lbl.setText("")
        # 重置样式
        self.name_label.setStyleSheet("color: #f5f5fa; font-size: 22px; font-weight: bold;")
        self.weapon_label.setStyleSheet("color: #d4a853; font-size: 12px; font-weight: bold;")
        self.avatar_label.clear()
        self.continue_btn.hide()
        if len(self._results) > 1:
            self.progress_label.setText(f"第 {self._idx + 1} / {len(self._results)} 抽")
        else:
            self.progress_label.setText("")
        self.stars_label.setText("★" * r["rarity"])
        color = "#d4a853" if r["rarity"] == 5 else ("#9a7fc8" if r["rarity"] == 4 else "#5a8a9a")
        self.stars_label.setStyleSheet(f"color: {color}; font-size: 28px; letter-spacing: 4px;")
        if r["rarity"] == 5:
            self._gold_flash(0)
        QTimer.singleShot(800 if r["rarity"] == 5 else 500, self._reveal)

    def _gold_flash(self, count):
        if count >= 3:
            self.setStyleSheet("background-color: #14171d; color: #e8e0d0;")
            return
        self.setStyleSheet("background-color: #3d2e10; color: #e8e0d0;")
        QTimer.singleShot(120, lambda: self.setStyleSheet("background-color: #14171d; color: #e8e0d0;"))
        QTimer.singleShot(240, lambda: self._gold_flash(count + 1))

    def _reveal(self):
        r = self._results[self._idx]
        if r.get("is_character"):
            # 角色展示（祈愿四/五星 或 星尘兑换任意星级）
            if r.get("char_id"):
                avatar = generate_avatar_pixmap(r["char_id"], 140)
                if avatar:
                    self.avatar_label.setPixmap(avatar)
            self.name_label.setText(r["char_name"])
            if r.get("anime") and r["anime"] != "—":
                self.anime_label.setText(f"《{r['anime']}》 【{r['element']}】")
            if r.get("skill_name"):
                new_tag = "（新解锁！）" if r.get("skill_new") else ""
                self.skill_label.setText(f"⚔️ 专属技能：{r['skill_name']} {new_tag}")
            if r.get("weapon_name"):
                if r.get("weapon_new"):
                    self.weapon_label.setText(f"🗡️ 专武解锁：{r['weapon_name']}（R1）")
                elif r.get("weapon_refine", 0) >= 5:
                    self.weapon_label.setText(f"🗡️ 专武已满炼：{r['weapon_name']}（R5）")
                else:
                    self.weapon_label.setText(f"🗡️ 专武精炼：{r['weapon_name']} → R{r['weapon_refine']}")
            if r.get("char_id"):
                char = (FIVE_STAR_CHARS if r["rarity"] == 5
                        else (FOUR_STAR_CHARS if r["rarity"] == 4 else THREE_STAR_CHARS)).get(r["char_id"], {})
                quote = char.get("wish_text", "")
                if quote:
                    QTimer.singleShot(400, lambda: self.quote_label.setText(quote))
        elif r.get("stardust_gain"):
            # [v7] 三星祈愿：星尘
            self.name_label.setText(f"💫 星尘 ×{r['stardust_gain']}")
            self.name_label.setStyleSheet("color: #06b6d4; font-size: 20px; font-weight: bold;")
            total = r.get("stardust_total", 0)
            self.anime_label.setText(f"星尘累计：{total}")
            if total >= STARDUST_NEEDED[5]:
                self.weapon_label.setText("✅ 可兑换随机五星角色！")
            elif total >= STARDUST_NEEDED[4]:
                self.weapon_label.setText("✅ 可兑换随机四星角色！")
            elif total >= STARDUST_NEEDED[3]:
                self.weapon_label.setText("✅ 可兑换随机三星角色！")
            else:
                self.weapon_label.setText("集满 10 / 30 / 70 可兑换随机角色")
        else:
            self.name_label.setText("祈愿小奖励")
            self.name_label.setStyleSheet("color: #06b6d4; font-size: 18px; font-weight: bold;")
        if r["xp"] > 0:
            self.xp_label.setText(f"+{r['xp']} XP")
        if len(self._results) > 1 and self._idx < len(self._results) - 1:
            self.continue_btn.setText("下一个 ▶")
        else:
            self.continue_btn.setText("确认")
        QTimer.singleShot(500, self.continue_btn.show)

    def _next_or_close(self):
        if self._idx < len(self._results) - 1:
            self._idx += 1
            self._animate_current()
        else:
            self.accept()


# ============================================================
# 入口
# ============================================================
def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = IELTSMainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
