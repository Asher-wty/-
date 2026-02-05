# config.py
# 核心依据：低温工况技术优化规则表.xlsx

# 1. 分温区生产参数配置 (依据：生产端能耗优化量化规则表)
# key: 温度上限(不包含), value: {参数}
PRODUCTION_RULES = {
    -5: {
        "zone_name": "-5~-10℃",
        "ratio": {"原油": 0.92, "降凝剂": 0.04, "稀释剂": 0.04},
        "rpm_range": (50, 55),
        "power_range": (18, 20),
        "energy_coeff": 1.10  # 综合能耗修正系数
    },
    -10: {
        "zone_name": "-10~-20℃",
        "ratio": {"原油": 0.90, "降凝剂": 0.05, "稀释剂": 0.05},
        "rpm_range": (45, 50),
        "power_range": (22, 25),
        "energy_coeff": 1.25
    },
    -20: {
        "zone_name": "-20~-30℃",
        "ratio": {"原油": 0.88, "降凝剂": 0.06, "稀释剂": 0.06},
        "rpm_range": (40, 45), # 专利核心改良点
        "power_range": (28, 32),
        "energy_coeff": 1.48
    },
    -30: {
        "zone_name": "-30℃以下",
        "ratio": {"原油": 0.85, "降凝剂": 0.07, "稀释剂": 0.08},
        "rpm_range": (35, 40),
        "power_range": (35, 40),
        "energy_coeff": 1.75
    }
}

# 2. 施工端阈值配置 (依据：施工端能耗优化逻辑.csv)
CONSTRUCTION_RULES = {
    "transport_distance_limit_km": 5.0,     # 运输半径阈值
    "transport_loss_rate": 0.06,            # 超距能耗增加 6%
    "daily_start_limit": 2,                 # 每日启停次数限制
    "start_loss_rate": 0.25,                # 超频启停增加 25%
    "no_preheat_loss": 0.40,                # 未预热增加 40%
    "gap_time_limit_min": 20,               # 工序间隔阈值
    "gap_loss_per_10min": 0.08              # 每超10分钟增加 8%
}