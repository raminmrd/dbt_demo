#!/usr/bin/env python3
"""
Advanced Data Lineage Visualization Script

Generates lineage visualizations for the advanced healthcare example
"""

import json
import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path


def load_manifest(manifest_path):
    """Load the dbt manifest.json file."""
    with open(manifest_path, 'r') as f:
        return json.load(f)


def extract_lineage(manifest):
    """Extract lineage relationships from the manifest."""
    G = nx.DiGraph()
    
    # Get all nodes
    nodes = manifest.get('nodes', {})
    sources = manifest.get('sources', {})
    
    # Add nodes
    for node_id, node_data in nodes.items():
        node_type = node_data.get('resource_type', 'unknown')
        node_name = node_data.get('name', node_id)
        
        G.add_node(
            node_id,
            name=node_name,
            type=node_type,
            label=node_name
        )
    
    # Add source nodes
    for source_id, source_data in sources.items():
        source_name = source_data.get('name', source_id)
        G.add_node(
            source_id,
            name=source_name,
            type='source',
            label=source_name
        )
    
    # Add edges
    for node_id, node_data in nodes.items():
        depends_on = node_data.get('depends_on', {})
        parent_nodes = depends_on.get('nodes', [])
        
        for parent_id in parent_nodes:
            if parent_id in G.nodes:
                G.add_edge(parent_id, node_id)
    
    return G


def get_node_color(node_type):
    """Return color based on node type."""
    color_map = {
        'seed': '#90EE90',
        'model': '#87CEEB',
        'source': '#FFD700',
        'snapshot': '#FF69B4',
    }
    return color_map.get(node_type, '#D3D3D3')


def get_node_layer(node_name):
    """Determine layer based on naming convention."""
    if node_name.startswith('raw_'):
        return 0
    elif node_name.startswith('stg_'):
        return 1
    elif node_name.startswith('int_'):
        return 2
    elif node_name.startswith('dim_') or node_name.startswith('fct_'):
        return 3
    elif node_name.startswith('snap_'):
        return 4
    else:
        return 2


def visualize_lineage(G, output_path='data_lineage_advanced.png'):
    """Create visualization of data lineage."""
    
    plt.figure(figsize=(24, 16))
    
    pos = {}
    layer_counts = {}
    
    # Count nodes per layer
    for node in G.nodes():
        node_name = G.nodes[node].get('name', node)
        layer = get_node_layer(node_name)
        layer_counts[layer] = layer_counts.get(layer, 0) + 1
    
    # Position nodes
    layer_positions = {}
    for node in G.nodes():
        node_name = G.nodes[node].get('name', node)
        layer = get_node_layer(node_name)
        
        if layer not in layer_positions:
            layer_positions[layer] = 0
        
        x = layer * 4
        max_in_layer = layer_counts[layer]
        y = (layer_positions[layer] - max_in_layer / 2) * 1.2
        
        pos[node] = (x, y)
        layer_positions[layer] += 1
    
    # Node colors
    node_colors = [
        get_node_color(G.nodes[node].get('type', 'unknown'))
        for node in G.nodes()
    ]
    
    # Labels
    labels = {
        node: G.nodes[node].get('name', node).replace('_', '\n')
        for node in G.nodes()
    }
    
    # Draw
    nx.draw_networkx_nodes(
        G, pos,
        node_color=node_colors,
        node_size=2500,
        alpha=0.9,
        edgecolors='black',
        linewidths=2
    )
    
    nx.draw_networkx_labels(
        G, pos,
        labels=labels,
        font_size=7,
        font_weight='bold'
    )
    
    nx.draw_networkx_edges(
        G, pos,
        edge_color='gray',
        arrows=True,
        arrowsize=15,
        arrowstyle='->',
        width=1.5,
        alpha=0.6,
        connectionstyle='arc3,rad=0.1'
    )
    
    # Legend
    legend_elements = [
        plt.Line2D([0], [0], marker='o', color='w', label='Sources',
                  markerfacecolor='#FFD700', markersize=10, markeredgecolor='black'),
        plt.Line2D([0], [0], marker='o', color='w', label='Seeds',
                  markerfacecolor='#90EE90', markersize=10, markeredgecolor='black'),
        plt.Line2D([0], [0], marker='o', color='w', label='Models',
                  markerfacecolor='#87CEEB', markersize=10, markeredgecolor='black'),
        plt.Line2D([0], [0], marker='o', color='w', label='Snapshots',
                  markerfacecolor='#FF69B4', markersize=10, markeredgecolor='black'),
    ]
    plt.legend(handles=legend_elements, loc='upper left', fontsize=12)
    
    # Layer labels
    layer_names = {0: 'Sources', 1: 'Staging', 2: 'Intermediate', 3: 'Marts', 4: 'Snapshots'}
    for layer, x in enumerate(range(0, 20, 4)):
        if layer in layer_names:
            plt.text(x, max(y for _, y in pos.values()) + 1.5, layer_names[layer],
                    fontsize=16, fontweight='bold', ha='center',
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.title('Advanced Healthcare Data Lineage', fontsize=22, fontweight='bold', pad=20)
    plt.axis('off')
    plt.tight_layout()
    
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✓ Lineage visualization saved to: {output_path}")
    
    return output_path


def print_lineage_summary(G):
    """Print summary of the lineage graph."""
    print("\n" + "="*70)
    print("ADVANCED HEALTHCARE DATA LINEAGE SUMMARY")
    print("="*70)
    
    print(f"\nTotal nodes: {G.number_of_nodes()}")
    print(f"Total edges: {G.number_of_edges()}")
    
    # Count by type
    type_counts = {}
    for node in G.nodes():
        node_type = G.nodes[node].get('type', 'unknown')
        type_counts[node_type] = type_counts.get(node_type, 0) + 1
    
    print("\nNodes by type:")
    for node_type, count in sorted(type_counts.items()):
        print(f"  {node_type}: {count}")
    
    # Root nodes
    root_nodes = [node for node in G.nodes() if G.in_degree(node) == 0]
    print(f"\nRoot nodes (sources/seeds): {len(root_nodes)}")
    
    # Leaf nodes
    leaf_nodes = [node for node in G.nodes() if G.out_degree(node) == 0]
    print(f"\nLeaf nodes (final outputs): {len(leaf_nodes)}")
    for node in leaf_nodes:
        print(f"  - {G.nodes[node].get('name', node)}")
    
    print("\n" + "="*70 + "\n")


def main():
    """Main execution."""
    manifest_path = Path('lineage_advanced/target/manifest.json')
    
    if not manifest_path.exists():
        print(f"❌ Error: Manifest file not found at {manifest_path}")
        print("Please run 'cd lineage_advanced && dbt docs generate' first.")
        return
    
    print(f"📖 Loading manifest from: {manifest_path}")
    manifest = load_manifest(manifest_path)
    
    print("🔍 Extracting lineage relationships...")
    lineage_graph = extract_lineage(manifest)
    
    print_lineage_summary(lineage_graph)
    
    print("🎨 Creating visualization...")
    visualize_lineage(lineage_graph)
    
    print("\n✅ Done! Your advanced lineage visualization is ready.")


if __name__ == '__main__':
    main()

