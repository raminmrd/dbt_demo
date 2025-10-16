#!/usr/bin/env python3
"""
Data Lineage Visualization Script

This script reads the dbt manifest.json file and creates a visual representation
of the data lineage showing how models depend on each other.
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
    
    # Get all nodes (models, seeds, sources, etc.)
    nodes = manifest.get('nodes', {})
    sources = manifest.get('sources', {})
    
    # Add all nodes to the graph
    for node_id, node_data in nodes.items():
        node_type = node_data.get('resource_type', 'unknown')
        node_name = node_data.get('name', node_id)
        
        # Add node with attributes
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
    
    # Add edges based on dependencies
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
        'seed': '#90EE90',        # Light green
        'model': '#87CEEB',       # Sky blue
        'source': '#FFD700',      # Gold
        'snapshot': '#FFA07A',    # Light salmon
        'test': '#DDA0DD',        # Plum
    }
    return color_map.get(node_type, '#D3D3D3')  # Light gray default


def get_node_layer(node_name):
    """Determine which layer a node belongs to based on naming convention."""
    if node_name.startswith('raw_'):
        return 0
    elif node_name.startswith('stg_'):
        return 1
    elif node_name.startswith('int_'):
        return 2
    elif node_name.startswith('dim_') or node_name.startswith('fct_'):
        return 3
    else:
        return 2  # default to middle


def visualize_lineage(G, output_path='lineage.png'):
    """Create and save a visualization of the data lineage."""
    
    # Create figure with larger size for better readability
    plt.figure(figsize=(20, 12))
    
    # Use hierarchical layout based on node layers
    pos = {}
    layer_counts = {}
    
    # First pass: count nodes in each layer
    for node in G.nodes():
        node_name = G.nodes[node].get('name', node)
        layer = get_node_layer(node_name)
        layer_counts[layer] = layer_counts.get(layer, 0) + 1
    
    # Second pass: position nodes
    layer_positions = {}
    for node in G.nodes():
        node_name = G.nodes[node].get('name', node)
        layer = get_node_layer(node_name)
        
        if layer not in layer_positions:
            layer_positions[layer] = 0
        
        # Calculate position
        x = layer * 3  # Horizontal spacing between layers
        max_in_layer = layer_counts[layer]
        y = (layer_positions[layer] - max_in_layer / 2) * 1.5  # Vertical spacing
        
        pos[node] = (x, y)
        layer_positions[layer] += 1
    
    # Get node colors based on type
    node_colors = [
        get_node_color(G.nodes[node].get('type', 'unknown'))
        for node in G.nodes()
    ]
    
    # Get node labels (use short names)
    labels = {
        node: G.nodes[node].get('name', node).replace('_', '\n')
        for node in G.nodes()
    }
    
    # Draw the graph
    nx.draw_networkx_nodes(
        G, pos,
        node_color=node_colors,
        node_size=3000,
        alpha=0.9,
        edgecolors='black',
        linewidths=2
    )
    
    nx.draw_networkx_labels(
        G, pos,
        labels=labels,
        font_size=8,
        font_weight='bold'
    )
    
    nx.draw_networkx_edges(
        G, pos,
        edge_color='gray',
        arrows=True,
        arrowsize=20,
        arrowstyle='->',
        width=2,
        alpha=0.6,
        connectionstyle='arc3,rad=0.1'
    )
    
    # Add legend
    legend_elements = [
        plt.Line2D([0], [0], marker='o', color='w', label='Seeds',
                  markerfacecolor='#90EE90', markersize=10, markeredgecolor='black'),
        plt.Line2D([0], [0], marker='o', color='w', label='Models',
                  markerfacecolor='#87CEEB', markersize=10, markeredgecolor='black'),
        plt.Line2D([0], [0], marker='o', color='w', label='Sources',
                  markerfacecolor='#FFD700', markersize=10, markeredgecolor='black'),
    ]
    plt.legend(handles=legend_elements, loc='upper left', fontsize=10)
    
    # Add layer labels
    layer_names = {0: 'Raw Data', 1: 'Staging', 2: 'Intermediate', 3: 'Marts'}
    for layer, x in enumerate(range(0, 12, 3)):
        if layer in layer_names:
            plt.text(x, max(y for _, y in pos.values()) + 2, layer_names[layer],
                    fontsize=14, fontweight='bold', ha='center',
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.title('Data Lineage Visualization', fontsize=20, fontweight='bold', pad=20)
    plt.axis('off')
    plt.tight_layout()
    
    # Save the figure
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✓ Lineage visualization saved to: {output_path}")
    
    # Also show the plot
    plt.show()
    
    return output_path


def print_lineage_summary(G):
    """Print a summary of the lineage graph."""
    print("\n" + "="*60)
    print("DATA LINEAGE SUMMARY")
    print("="*60)
    
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
    
    # Find root nodes (no dependencies)
    root_nodes = [node for node in G.nodes() if G.in_degree(node) == 0]
    print(f"\nRoot nodes (sources): {len(root_nodes)}")
    for node in root_nodes:
        print(f"  - {G.nodes[node].get('name', node)}")
    
    # Find leaf nodes (no dependents)
    leaf_nodes = [node for node in G.nodes() if G.out_degree(node) == 0]
    print(f"\nLeaf nodes (final outputs): {len(leaf_nodes)}")
    for node in leaf_nodes:
        print(f"  - {G.nodes[node].get('name', node)}")
    
    print("\n" + "="*60 + "\n")


def main():
    """Main execution function."""
    # Path to the manifest
    manifest_path = Path('lineage_demo/target/manifest.json')
    
    if not manifest_path.exists():
        print(f"❌ Error: Manifest file not found at {manifest_path}")
        print("Please run 'dbt docs generate' first.")
        return
    
    print(f"📖 Loading manifest from: {manifest_path}")
    manifest = load_manifest(manifest_path)
    
    print("🔍 Extracting lineage relationships...")
    lineage_graph = extract_lineage(manifest)
    
    print_lineage_summary(lineage_graph)
    
    print("🎨 Creating visualization...")
    output_path = 'data_lineage.png'
    visualize_lineage(lineage_graph, output_path)
    
    print("\n✅ Done! Your data lineage visualization is ready.")


if __name__ == '__main__':
    main()

