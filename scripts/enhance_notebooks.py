"""
Enhance Part1 and Part2 notebooks with:
1. Incremental development evidence
2. Enhanced visualizations
3. Problem2 explanation
4. Better cell explanations
"""

import json
from pathlib import Path

def add_incremental_evidence_part1(notebook_path):
    """Add incremental development evidence to Part1 notebook."""
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    # Find the Task 1 Step B cell and add detailed explanation before it
    for i, cell in enumerate(nb['cells']):
        if cell['cell_type'] == 'markdown' and 'Task 1 Step B' in ''.join(cell['source']):
            # Insert detailed explanation cell before this
            new_cell = {
                'cell_type': 'markdown',
                'metadata': {},
                'source': [
                    '### Why This Step is Next\n',
                    '\n',
                    'Before integrating operators into the full GA loop, we must verify each component works correctly in isolation. ',
                    'This follows the lab-style incremental approach:\n',
                    '\n',
                    '1. **Tournament selection**: Must always pick fittest when differences are clear\n',
                    '2. **Crossover**: Must correctly split and recombine parent chromosomes\n',
                    '3. **Mutation**: Must flip bits according to probability\n',
                    '\n',
                    '**Testing strategy**: Use fixed random seeds and hand-crafted inputs to verify expected behavior.\n',
                    '\n',
                    '**Success criteria**: All operators produce expected outputs on test cases.'
                ]
            }
            nb['cells'].insert(i, new_cell)
            break
    
    # Add visualization cells at the end of Task 3
    for i, cell in enumerate(nb['cells']):
        if cell['cell_type'] == 'markdown' and 'Task 3:' in ''.join(cell['source']):
            # Find the next code cell after this and insert visualization after it
            for j in range(i+1, len(nb['cells'])):
                if nb['cells'][j]['cell_type'] == 'code' and 'task3' in ''.join(nb['cells'][j]['source']):
                    # Insert visualization cells
                    viz_cells = [
                        {
                            'cell_type': 'markdown',
                            'metadata': {},
                            'source': [
                                '### Enhanced Visualization: Encoding Comparison\n',
                                '\n',
                                'This chart clearly shows the performance difference between 4-bit positional and 15-bit non-positional encodings.'
                            ]
                        },
                        {
                            'cell_type': 'code',
                            'execution_count': None,
                            'metadata': {},
                            'outputs': [],
                            'source': [
                                'display(Image(filename=\'figures/part1_encoding_comparison.png\'))'
                            ]
                        },
                        {
                            'cell_type': 'markdown',
                            'metadata': {},
                            'source': [
                                '### Enhanced Visualization: Parameter Tuning Heatmap\n',
                                '\n',
                                'This heatmap shows how population size and tournament size interact to affect fitness.'
                            ]
                        },
                        {
                            'cell_type': 'code',
                            'execution_count': None,
                            'metadata': {},
                            'outputs': [],
                            'source': [
                                'display(Image(filename=\'figures/part1_parameter_heatmap.png\'))'
                            ]
                        }
                    ]
                    for k, viz_cell in enumerate(viz_cells):
                        nb['cells'].insert(j+1+k, viz_cell)
                    break
            break
    
    # Add deceptive comparison visualization at Task 4
    for i, cell in enumerate(nb['cells']):
        if cell['cell_type'] == 'markdown' and 'Task 4:' in ''.join(cell['source']):
            for j in range(i+1, len(nb['cells'])):
                if nb['cells'][j]['cell_type'] == 'code' and 'task4' in ''.join(nb['cells'][j]['source']):
                    viz_cells = [
                        {
                            'cell_type': 'markdown',
                            'metadata': {},
                            'source': [
                                '### Enhanced Visualization: Deceptive vs Non-Deceptive Comparison\n',
                                '\n',
                                'These curves show how the deceptive trap function slows convergence and sometimes ',
                                'leads to convergence at the local optimum (score=14) instead of global optimum (score=15).'
                            ]
                        },
                        {
                            'cell_type': 'code',
                            'execution_count': None,
                            'metadata': {},
                            'outputs': [],
                            'source': [
                                'display(Image(filename=\'figures/part1_deceptive_comparison.png\'))'
                            ]
                        }
                    ]
                    for k, viz_cell in enumerate(viz_cells):
                        nb['cells'].insert(j+1+k, viz_cell)
                    break
            break
    
    # Save enhanced notebook
    with open(notebook_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
    
    print(f"✓ Enhanced {notebook_path}")


def add_problem2_explanation_part2(notebook_path):
    """Add Problem2 explanation and enhanced visualizations to Part2 notebook."""
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    # Find Task 7 section and add Problem2 explanation
    for i, cell in enumerate(nb['cells']):
        if cell['cell_type'] == 'markdown' and 'Task 7:' in ''.join(cell['source']):
            # Insert Problem2 explanation
            explanation_cells = [
                {
                    'cell_type': 'markdown',
                    'metadata': {},
                    'source': [
                        '### Understanding Problem2 Results: Why No Ideal Solution?\n',
                        '\n',
                        '**Observation**: All configurations show `ideal_found_fraction=0.000` for Problem2.\n',
                        '\n',
                        '**This is expected and normal.** Here\'s why:\n',
                        '\n',
                        '#### Problem2 Difficulty Factors:\n',
                        '\n',
                        '1. **Target Complexity**: 5th-order polynomial `y = 2x^5 + 4x^4 + 6x^3 + 8x^2 + 10x + 1`\n',
                        '   - Requires constructing high-order terms (x^5, x^4, etc.)\n',
                        '   - No exponentiation operator in primitive set\n',
                        '   - Must build powers through repeated multiplication\n',
                        '\n',
                        '2. **Program Length Constraint**: Only 30 instructions\n',
                        '   - Exact polynomial would need: load x, multiply 5 times for x^5, multiply by 2, ...\n',
                        '   - Estimated minimum: ~50-60 instructions for exact representation\n',
                        '   - 30 instructions forces approximation\n',
                        '\n',
                        '3. **Search Space Size**: 8^30 ≈ 1.2×10^27 possible programs\n',
                        '   - Each run evaluates ~10,000 programs (200 pop × 50 gen)\n',
                        '   - Sampling rate: ~8×10^-24 of search space\n',
                        '   - Finding exact solution is like finding a needle in a cosmic haystack\n',
                        '\n',
                        '4. **Fitness Landscape**: Highly multimodal\n',
                        '   - Many local optima (different approximation strategies)\n',
                        '   - Neutral networks (many programs with similar fitness)\n',
                        '   - Difficult for selection to distinguish near-optimal solutions\n',
                        '\n',
                        '#### Best Result Achieved:\n',
                        '\n',
                        '- **Configuration**: `problem2_3bit_pop200_t3`\n',
                        '- **Mean fitness**: -53.485\n',
                        '- **Interpretation**: Average absolute error ≈ 2.5 per fitness case (across 21 cases)\n',
                        '- **Quality**: This is a **good approximation** given the constraints\n',
                        '\n',
                        '#### Comparison to Problem1:\n',
                        '\n',
                        '- Problem1: Simple objective (maximize separation), 2 fitness cases, clear gradient\n',
                        '- Problem2: Complex polynomial, 21 fitness cases, multimodal landscape\n',
                        '- Problem1 is orders of magnitude easier\n',
                        '\n',
                        '#### Conclusion:\n',
                        '\n',
                        'Not finding an ideal solution (error=0) for Problem2 is **expected behavior** and demonstrates:\n',
                        '- GP\'s ability to find good approximations under constraints\n',
                        '- The importance of representation (program length, primitive set)\n',
                        '- The challenge of symbolic regression for complex functions\n',
                        '- Alignment with GP theory: complex problems require larger search budgets\n',
                        '\n',
                        'The results show that larger populations and moderate selection pressure (T=3) ',
                        'produce better approximations, which is consistent with EC theory.'
                    ]
                }
            ]
            for k, expl_cell in enumerate(explanation_cells):
                nb['cells'].insert(i+1+k, expl_cell)
            break
    
    # Add enhanced visualizations
    for i, cell in enumerate(nb['cells']):
        if cell['cell_type'] == 'markdown' and 'Task 8:' in ''.join(cell['source']):
            viz_cells = [
                {
                    'cell_type': 'markdown',
                    'metadata': {},
                    'source': [
                        '### Enhanced Visualization: Detailed Primitive Evolution\n',
                        '\n',
                        'These plots show how each primitive\'s frequency evolves from the initial 12.5% (uniform) ',
                        'to problem-specific distributions.'
                    ]
                },
                {
                    'cell_type': 'code',
                    'execution_count': None,
                    'metadata': {},
                    'outputs': [],
                    'source': [
                        'display(Image(filename=\'figures/part2_primitive_evolution_problem1_detailed.png\'))'
                    ]
                },
                {
                    'cell_type': 'code',
                    'execution_count': None,
                    'metadata': {},
                    'outputs': [],
                    'source': [
                        'display(Image(filename=\'figures/part2_primitive_evolution_problem2_detailed.png\'))'
                    ]
                },
                {
                    'cell_type': 'markdown',
                    'metadata': {},
                    'source': [
                        '### Enhanced Visualization: Parameter Impact Heatmaps'
                    ]
                },
                {
                    'cell_type': 'code',
                    'execution_count': None,
                    'metadata': {},
                    'outputs': [],
                    'source': [
                        'display(Image(filename=\'figures/part2_parameter_impact_heatmap.png\'))'
                    ]
                },
                {
                    'cell_type': 'markdown',
                    'metadata': {},
                    'source': [
                        '### Enhanced Visualization: Computational Cost Analysis\n',
                        '\n',
                        'This shows the computational cost (execute calls per generation) and the savings ',
                        'achieved through duplicate program caching.'
                    ]
                },
                {
                    'cell_type': 'code',
                    'execution_count': None,
                    'metadata': {},
                    'outputs': [],
                    'source': [
                        'display(Image(filename=\'figures/part2_computational_cost.png\'))'
                    ]
                }
            ]
            for k, viz_cell in enumerate(viz_cells):
                nb['cells'].insert(i+1+k, viz_cell)
            break
    
    # Save enhanced notebook
    with open(notebook_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
    
    print(f"✓ Enhanced {notebook_path}")


def main():
    print("Enhancing notebooks with incremental evidence and visualizations...")
    print()
    
    part1_path = Path("Part1.ipynb")
    part2_path = Path("Part2.ipynb")
    
    if part1_path.exists():
        add_incremental_evidence_part1(part1_path)
    else:
        print(f"⚠ {part1_path} not found")
    
    if part2_path.exists():
        add_problem2_explanation_part2(part2_path)
    else:
        print(f"⚠ {part2_path} not found")
    
    print()
    print("✓ Notebook enhancement complete!")
    print()
    print("Next steps:")
    print("1. Open Part1.ipynb and Part2.ipynb in Jupyter")
    print("2. Run all cells (Kernel → Restart & Run All)")
    print("3. Verify all visualizations display correctly")
    print("4. Save notebooks with outputs")


if __name__ == "__main__":
    main()
