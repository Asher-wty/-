# construction_model.py
# 施工端逻辑模型 - V2.0 (字典返回版)
from config import CONSTRUCTION_RULES
import math

class LogisticsOptimizer:
    """施工端流程优化模型：负责诊断运输、启停及工序衔接的能耗风险"""

    def calculate_transport_impact(self, distance_km):
        """计算运输环节能耗方案"""
        limit = CONSTRUCTION_RULES['transport_distance_limit_km']
        
        if distance_km > limit:
            loss = CONSTRUCTION_RULES['transport_loss_rate']
            return {
                "状态": "风险",
                "诊断": f"运输半径 {distance_km}km 已超过基准线 {limit}km",
                "能耗影响": f"预计增加 {int(loss*100)}%",
                "优化方案": "1. 启动电伴热补温；2. 优化下一批次运输路径"
            }
        return {
            "状态": "达标",
            "诊断": "运输距离合理",
            "能耗影响": "0%",
            "优化方案": "维持当前路径，确保保温层完好"
        }

    def calculate_startup_impact(self, starts_count, is_preheated):
        """计算设备启停优化方案"""
        loss = 0.0
        advices = []
        status = "达标"

        # 规则1：判断启停次数
        if starts_count > CONSTRUCTION_RULES['daily_start_limit']:
            loss += CONSTRUCTION_RULES['start_loss_rate']
            advices.append(f"启停过频(已达{starts_count}次)，建议合并作业")
            status = "警告"
            
        # 规则2：判断预热状态
        if not is_preheated:
            loss += CONSTRUCTION_RULES['no_preheat_loss']
            advices.append("未预热启动，下次必须预热≥30分钟")
            status = "警告"
            
        # 如果没有建议，就是操作规范
        if not advices:
            advices = ["操作规范，继续保持"]

        return {
            "状态": status,
            "总能耗增幅": f"{int(loss*100)}%",
            "优化方案": advices 
        }

    def calculate_process_gap(self, gap_minutes):
        """计算工序衔接优化方案"""
        limit = CONSTRUCTION_RULES['gap_time_limit_min']
        
        if gap_minutes > limit:
            over_time = gap_minutes - limit
            steps = math.ceil(over_time / 10)
            loss = steps * CONSTRUCTION_RULES['gap_loss_per_10min']
            return {
                "状态": "能耗高",
                "诊断": f"衔接间隔 {gap_minutes}min 超过标准 {limit}min",
                "能耗影响": f"预计增加 {int(loss*100)}%",
                "优化方案": "1. 调整储罐出口泵流量；2. 增加临时加热功率"
            }
        return {
            "状态": "高效",
            "诊断": "工序衔接紧凑",
            "能耗影响": "0%",
            "优化方案": "无需干预"
        }