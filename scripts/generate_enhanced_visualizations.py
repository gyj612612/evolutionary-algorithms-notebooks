"""
Generate enhanced visualizations for CE310 coursework notebooks.
Addresses feedback: encoding comparison, parameter heatmaps, primitive evolution, deceptive comparison.
"""

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.gridspec import GridSpec

RESULT_ROOT = Path("results")
VIZ_ROOT = Path("figures")
VIZ_ROOT.mkdir(exist_ok=True)


def plot_encoding_comparison():
    """Task 2/3: Encoding comparison bar chart with error bars."""
    task3 = pd.read_csv(RESULT_ROOT / "part1" / "task3_main" / "task3_summary.csv")
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    for idx, obj in enumerate(["15max", "soft15max"]):
        ax = axes[idx]
        data = task3[task3["objective"] == obj]
        
        x_pos = np.arange(len(data))
        colors = ["#3498db" if "4bit" in c else "#e74c3c" for c in data["condition"]]
        
        bars = ax.bar(x_pos, data["best_of_run_mean"], 
                      yerr=data["best_of_run_std"],
                      color=colors, alpha=0.7, capsize=5)
        
        ax.set_xticks(x_pos)
        ax.set_xticklabels(data["condition"], rotation=45, ha="right", fontsize=9)
        ax.set_ylabel("Mean Best-of-Run Fitness", fontsize=11)
        ax.set_title(f"Encoding Comparison: {obj}", fontsize=12, fontweight="bold")
        ax.grid(axis="y", alpha=0.3)
        
        # Add legend
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor="#3498db", alpha=0.7, label="4-bit positional"),
            Patch(facecolor="#e74c3c", alpha=0.7, label="15-bit non-positional")
        ]
        ax.legend(handles=legend_elements, loc="upper left", fontsize=9)
    
    plt.tight_layout()
    plt.savefig(VIZ_ROOT / "part1_encoding_comparison.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("✓ Created: part1_encoding_comparison.png")


def plot_parameter_heatmap():
    """Task 3: Parameter tuning heatmap (pop_size × tournament_size)."""
    tuning = pd.read_csv(RESULT_ROOT / "part1" / "task3_tuning" / "tuning_summary.csv")
    
    # Pivot for heatmap
    pivot = tuning.pivot(index="pop_size", columns="tournament_size", values="best_of_run_mean")
    
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(pivot, annot=True, fmt=".2f", cmap="YlGnBu", 
                cbar_kws={"label": "Mean Best-of-Run Fitness"},
                linewidths=0.5, ax=ax)
    ax.set_title("Parameter Tuning: Population Size × Tournament Size", 
                 fontsize=13, fontweight="bold", pad=15)
    ax.set_xlabel("Tournament Size", fontsize=11)
    ax.set_ylabel("Population Size", fontsize=11)
    
    plt.tight_layout()
    plt.savefig(VIZ_ROOT / "part1_parameter_heatmap.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("✓ Created: part1_parameter_heatmap.png")


def plot_deceptive_comparison():
    """Task 4: Deceptive vs non-deceptive side-by-side curves."""
    task3 = pd.read_csv(RESULT_ROOT / "part1" / "task3_main" / "task3_summary.csv")
    task4 = pd.read_csv(RESULT_ROOT / "part1" / "task4_trap" / "task4_summary.csv")
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    conditions = [
        ("4bit_L10", "4bit", 10),
        ("4bit_L30", "4bit", 30),
        ("15bit_L10", "15bit", 10),
        ("15bit_L30", "15bit", 30),
    ]
    
    for idx, (cond_name, enc, L) in enumerate(conditions):
        ax = axes[idx // 2, idx % 2]
        
        # Load soft15max baseline
        soft_cond = f"{enc}_L{L}_soft15max"
        soft_dir = RESULT_ROOT / "part1" / "task3_main" / soft_cond
        if soft_dir.exists():
            soft_agg = pd.read_csv(soft_dir / "generation_aggregated.csv")
            ax.plot(soft_agg["generation"], soft_agg["best_fitness_mean"],
                   label="soft-15-max (baseline)", linewidth=2, color="#2ecc71")
            ax.fill_between(soft_agg["generation"],
                           soft_agg["best_fitness_mean"] - soft_agg["best_fitness_std"],
                           soft_agg["best_fitness_mean"] + soft_agg["best_fitness_std"],
                           alpha=0.2, color="#2ecc71")
        
        # Load trap
        trap_cond = f"{enc}_L{L}_soft15trap_int"
        trap_dir = RESULT_ROOT / "part1" / "task4_trap" / trap_cond
        if trap_dir.exists():
            trap_agg = pd.read_csv(trap_dir / "generation_aggregated.csv")
            ax.plot(trap_agg["generation"], trap_agg["best_fitness_mean"],
                   label="soft-15-trap (deceptive)", linewidth=2, color="#e74c3c", linestyle="--")
            ax.fill_between(trap_agg["generation"],
                           trap_agg["best_fitness_mean"] - trap_agg["best_fitness_std"],
                           trap_agg["best_fitness_mean"] + trap_agg["best_fitness_std"],
                           alpha=0.2, color="#e74c3c")
        
        # Add deceptive local optimum line
        ax.axhline(y=14.0, color="gray", linestyle=":", linewidth=1.5, 
                  label="Local optimum (I=0 → score=14)")
        ax.axhline(y=15.0, color="black", linestyle=":", linewidth=1.5,
                  label="Global optimum (I=15 → score=15)")
        
        ax.set_xlabel("Generation", fontsize=10)
        ax.set_ylabel("Best Fitness", fontsize=10)
        ax.set_title(f"{cond_name}: Deceptive vs Non-Deceptive", fontsize=11, fontweight="bold")
        ax.legend(fontsize=8, loc="lower right")
        ax.grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(VIZ_ROOT / "part1_deceptive_comparison.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("✓ Created: part1_deceptive_comparison.png")


def plot_primitive_evolution_detailed():
    """Task 8: Primitive frequency evolution with subplots for each primitive."""
    primitives = ["NOP", "X", "+", "-", "*", "1", "-1", "0"]
    
    for problem in ["problem1", "problem2"]:
        # Find best condition
        task7 = pd.read_csv(RESULT_ROOT / "part2" / "task7_experiments" / "task7_summary.csv")
        prob_data = task7[task7["problem"] == problem].sort_values("best_of_run_mean", ascending=(problem=="problem2"))
        best_cond = prob_data.iloc[0]["condition"]
        
        # Load aggregated history
        cond_dir = RESULT_ROOT / "part2" / "task7_experiments" / best_cond
        agg = pd.read_csv(cond_dir / "generation_aggregated.csv")
        
        # Create subplot grid
        fig = plt.figure(figsize=(16, 10))
        gs = GridSpec(3, 3, figure=fig, hspace=0.3, wspace=0.3)
        
        for idx, prim in enumerate(primitives):
            ax = fig.add_subplot(gs[idx // 3, idx % 3])
            
            col_mean = f"freq_{prim}_mean"
            col_std = f"freq_{prim}_std"
            
            if col_mean in agg.columns:
                ax.plot(agg["generation"], agg[col_mean], linewidth=2, color="#3498db")
                ax.fill_between(agg["generation"],
                               agg[col_mean] - agg[col_std],
                               agg[col_mean] + agg[col_std],
                               alpha=0.2, color="#3498db")
                
                # Add initial expectation line
                ax.axhline(y=0.125, color="red", linestyle="--", linewidth=1, 
                          label="Initial (12.5%)")
                
                ax.set_xlabel("Generation", fontsize=9)
                ax.set_ylabel("Frequency", fontsize=9)
                ax.set_title(f"Primitive: {prim}", fontsize=10, fontweight="bold")
                ax.grid(alpha=0.3)
                ax.legend(fontsize=8)
        
        # Add overall title
        fig.suptitle(f"Primitive Frequency Evolution: {problem} (Best Config: {best_cond})",
                    fontsize=14, fontweight="bold", y=0.995)
        
        plt.savefig(VIZ_ROOT / f"part2_primitive_evolution_{problem}_detailed.png", 
                   dpi=150, bbox_inches="tight")
        plt.close()
        print(f"✓ Created: part2_primitive_evolution_{problem}_detailed.png")


def plot_gp_parameter_impact():
    """Task 7: GP parameter impact visualization (pop_size × tournament_size)."""
    task7 = pd.read_csv(RESULT_ROOT / "part2" / "task7_experiments" / "task7_summary.csv")
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    for idx, problem in enumerate(["problem1", "problem2"]):
        ax = axes[idx]
        data = task7[task7["problem"] == problem]
        
        # Pivot for heatmap
        pivot = data.pivot(index="pop_size", columns="tournament_size", values="best_of_run_mean")
        
        sns.heatmap(pivot, annot=True, fmt=".1f", cmap="RdYlGn" if problem=="problem1" else "RdYlGn_r",
                   cbar_kws={"label": "Mean Best-of-Run Fitness"},
                   linewidths=0.5, ax=ax)
        ax.set_title(f"{problem}: Parameter Impact", fontsize=12, fontweight="bold")
        ax.set_xlabel("Tournament Size", fontsize=10)
        ax.set_ylabel("Population Size", fontsize=10)
    
    plt.tight_layout()
    plt.savefig(VIZ_ROOT / "part2_parameter_impact_heatmap.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("✓ Created: part2_parameter_impact_heatmap.png")


def plot_computational_cost():
    """Task 7: Computational cost comparison across configurations."""
    task7 = pd.read_csv(RESULT_ROOT / "part2" / "task7_experiments" / "task7_summary.csv")
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    for idx, problem in enumerate(["problem1", "problem2"]):
        ax = axes[idx]
        data = task7[task7["problem"] == problem].sort_values("mean_execute_calls_per_generation")
        
        x_pos = np.arange(len(data))
        colors = plt.cm.viridis(data["mean_execute_calls_per_generation"] / data["mean_execute_calls_per_generation"].max())
        
        bars = ax.barh(x_pos, data["mean_execute_calls_per_generation"], color=colors, alpha=0.8)
        ax.set_yticks(x_pos)
        ax.set_yticklabels([f"pop{r['pop_size']}_t{r['tournament_size']}" 
                           for _, r in data.iterrows()], fontsize=8)
        ax.set_xlabel("Mean Execute Calls per Generation", fontsize=10)
        ax.set_title(f"{problem}: Computational Cost", fontsize=12, fontweight="bold")
        ax.grid(axis="x", alpha=0.3)
        
        # Add reduction ratio text
        for i, (_, row) in enumerate(data.iterrows()):
            reduction = row.get("execute_call_reduction_ratio", 0) * 100
            ax.text(row["mean_execute_calls_per_generation"] + 5, i, 
                   f"{reduction:.0f}% saved", fontsize=7, va="center")
    
    plt.tight_layout()
    plt.savefig(VIZ_ROOT / "part2_computational_cost.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("✓ Created: part2_computational_cost.png")


def main():
    print("Generating enhanced visualizations for CE310 coursework...")
    print()
    
    print("[Part 1 Visualizations]")
    plot_encoding_comparison()
    plot_parameter_heatmap()
    plot_deceptive_comparison()
    print()
    
    print("[Part 2 Visualizations]")
    plot_primitive_evolution_detailed()
    plot_gp_parameter_impact()
    plot_computational_cost()
    print()
    
    print(f"✓ All visualizations saved to: {VIZ_ROOT.absolute()}")
    print()
    print("These figures can be embedded in notebooks with:")
    print("  from IPython.display import Image, display")
    print("  display(Image(filename='figures/part1_encoding_comparison.png'))")


if __name__ == "__main__":
    main()
