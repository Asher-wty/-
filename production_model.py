# production_model.py
from config import PRODUCTION_RULES

class MixingOptimizer:
    def __init__(self, current_temp):
        self.temp = current_temp
        self.rule = self._get_rule_by_temp()

    def _get_rule_by_temp(self):
        """根据环境温度匹配最佳工况规则"""
        if self.temp > -5:
            return None # 非低温工况
        elif self.temp > -10:
            return PRODUCTION_RULES[-5]
        elif self.temp > -20:
            return PRODUCTION_RULES[-10]
        elif self.temp > -30:
            return PRODUCTION_RULES[-20]
        else:
            return PRODUCTION_RULES[-30]

    def optimize_process(self, current_viscosity):
        """
        核心算法：计算推荐参数
        输入：当前原油黏度
        输出：优化后的转速、配比、能耗预测
        """
        if not self.rule:
            return "当前温度无需启动低温优化模式"

        # 1. 基础转速推荐
        base_rpm = sum(self.rule['rpm_range']) / 2
        
        # 2. 实现文档中的“黏度-转速”联动逻辑
        # 规则：每升高 100mPa·s，转速 + 3r/min (基于基准黏度 2000mPa.s)
        viscosity_diff = max(0, current_viscosity - 2000)
        rpm_adjustment = (viscosity_diff // 100) * 3
        final_rpm = min(base_rpm + rpm_adjustment, 60) # 设置个物理上限

        return {
            "工况温区": self.rule['zone_name'],
            "建议物料配比": self.rule['ratio'],
            "基础转速(r/min)": base_rpm,
            "智能调整后转速(r/min)": final_rpm,
            "预计功率(kW)": sum(self.rule['power_range']) / 2,
            "能耗修正系数": self.rule['energy_coeff']
        }

    def calculate_savings(self, standard_energy_cost):
        """计算优化后的节能量"""
        # 假设：如果不优化，低温会导致能耗指数级上升 (模拟系数 1.8)
        # 优化后，使用修正系数 (如 1.48)
        unoptimized_coeff = 1.8
        optimized_coeff = self.rule['energy_coeff']
        
        savings = standard_energy_cost * (unoptimized_coeff - optimized_coeff)
        return round(savings, 2)