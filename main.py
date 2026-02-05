# main.py
# 新疆低温稠油处理 · 双端能耗优化系统 (工程演示版 V2.1)
import time
import sys
import traceback

def main():
    print("="*70)
    print("   ❄️ 新疆低温稠油集输 · 双端能耗自适应优化系统 V2.0")
    print("   技术核心：分温区自适应控制 (生产端) + 流程动态诊断 (施工端)")
    print("="*70)

    try:
        # 1. 初始化检测
        print("\n正在初始化核心算法模块...")
        try:
            from production_model import MixingOptimizer
            from construction_model import LogisticsOptimizer
            print(">> [OK] 算法库加载成功")
        except ImportError as e:
            print(f"\n[❌ 严重错误] 缺少必要文件！\n错误详情: {e}")
            print("请检查：config.py, production_model.py, construction_model.py 是否在同一目录。")
            input("\n按回车键退出...")
            return

        # =========================================================
        # 场景 1：生产端混合优化 (计算机器参数)
        # =========================================================
        print("\n" + "█"*10 + " [场景 1] 生产端：设备工况自适应计算 " + "█"*10)
        
        print("\n[模拟传感器数据接入]:")
        try:
            temp_input = input("   👉 请输入当前环境温度 (°C) [推荐 -25]: ").strip()
            current_temp = float(temp_input) if temp_input else -25.0
            
            visc_input = input("   👉 请输入原油当前黏度 (mPa.s) [推荐 2500]: ").strip()
            current_viscosity = float(visc_input) if visc_input else 2500.0
        except ValueError:
            print("   [⚠️ 输入有误] 自动切换至默认参数 (-25℃, 2500mPa.s)")
            current_temp = -25.0
            current_viscosity = 2500.0

        # 执行核心算法
        prod_opt = MixingOptimizer(current_temp)
        result = prod_opt.optimize_process(current_viscosity)
        
        print(f"\n>>> 正在调用《低温分温区规则库》... (目标温度: {current_temp}℃)")
        time.sleep(1) 
        
        print("\n" + "-"*30)
        print("💡 生产端智能控制方案")
        print("-" * 30)
        if isinstance(result, dict):
            print(f"• [工况温区]: {result['工况温区']}")
            print(f"• [推荐转速]: {result['智能调整后转速(r/min)']} r/min (已补偿黏度阻力)")
            print(f"• [物料配比]: 原油 {int(result['建议物料配比']['原油']*100)}% : 降凝剂 {int(result['建议物料配比']['降凝剂']*100)}% : 稀释剂 {int(result['建议物料配比']['稀释剂']*100)}%")
            print(f"• [传动模式]: 齿轮传动 (齿比 1:3)")
            
            # 模拟经济效益
            base_cost = 1000 
            saved = prod_opt.calculate_savings(base_cost)
            print(f"\n💰 [效益测算]: 相比传统模式，预计每小时节约电费 ¥{saved}")
        else:
            print(f"  {result}")

        print("\n" + "="*70)
        input("按回车键进入 [施工端] 模拟...\n")

        # =========================================================
        # 场景 2：施工端流程诊断 (诊断 + 量化 + 建议工况)
        # =========================================================
        print("█"*10 + " [场景 2] 施工端：流程能耗诊断与优化 " + "█"*10)
        log_opt = LogisticsOptimizer()
        
        print("\n[录入现场作业数据]:")

        try:
            # 输入部分
            dist_str = input("   1. 运输半径 (km) [默认 8.0]: ").strip()
            dist = float(dist_str) if dist_str else 8.0

            starts_str = input("   2. 今日启停次数 [默认 3]: ").strip()
            starts = int(starts_str) if starts_str else 3

            pre_str = input("   3. 是否已预热? (y/n) [默认 n]: ").strip().lower()
            is_pre = True if pre_str == 'y' else False

            gap_str = input("   4. 工序衔接间隔 (分钟) [默认 45]: ").strip()
            gap = int(gap_str) if gap_str else 45

        except ValueError:
            print("   [⚠️ 输入有误] 使用测试数据运行...")
            dist, starts, is_pre, gap = 8.0, 3, False, 45
        
        print(f"\n>>> 正在根据《施工端能耗优化逻辑表》比对阈值...")
        time.sleep(1)
        
        print("\n" + "-"*30)
        print("📋 施工端智能诊断报告")
        print("-" * 30)
        
        # --- 1. 运输环节诊断 ---
        t_res = log_opt.calculate_transport_impact(dist)
        print(f"🚛 [运输环节]: {t_res['状态']}")
        print(f"   ├─ 诊断结果: {t_res['诊断']}")
        
        if t_res['状态'] != '达标':
            print(f"   ├─ ❌ 量化损耗: {t_res['能耗影响']}")
            print(f"   └─ ✅ 建议工况: 请将运输半径控制在 5.0km 以内，或开启电伴热。")
        else:
            print(f"   └─ ✅ 保持现状: 符合节能运输标准。")

        print("")

        # --- 2. 启停管理诊断 ---
        s_res = log_opt.calculate_startup_impact(starts, is_pre)
        print(f"🔄 [设备启停]: {s_res['状态']}")
        
        # 处理优化方案列表
        advice_str = "; ".join(s_res['优化方案'])
        print(f"   ├─ 诊断结果: {advice_str}")
        
        # 这里的判断逻辑做了增强，防止报错
        loss_val = 0
        if '%' in s_res['总能耗增幅']:
            try:
                loss_val = float(s_res['总能耗增幅'].strip('%'))
            except:
                loss_val = 0

        if loss_val > 0:
            print(f"   ├─ ❌ 量化损耗: 能耗增加 {s_res['总能耗增幅']}")
            print(f"   └─ ✅ 建议工况: 单日启停 ≤2次，且启动前必须预热 >30分钟。")
        else:
            print(f"   └─ ✅ 保持现状: 启停频率与预热操作规范。")

        print("")

        # --- 3. 工序衔接诊断 ---
        g_res = log_opt.calculate_process_gap(gap)
        print(f"⏱️ [工序衔接]: {g_res['状态']}")
        print(f"   ├─ 诊断结果: {g_res['诊断']}")
        
        if g_res['状态'] != '高效':
            print(f"   ├─ ❌ 量化损耗: {g_res['能耗影响']}")
            print(f"   └─ ✅ 建议工况: 混合到储存的间隔时间应 ≤20分钟。")
        else:
            print(f"   └─ ✅ 保持现状: 流程衔接紧凑。")

        print("\n" + "="*70)
        print("系统演示结束。数据已准备好推流至可视化前端。")

    except Exception as e:
        print(f"\n\n[❌ 程序运行出错]\n错误信息: {e}")
        traceback.print_exc()

    input("\n✅ 演示完毕，按回车键退出程序...")

if __name__ == "__main__":
    main()