#!/usr/bin/env python3
"""
Interactive HTML Data Lineage Visualization

This script creates an interactive HTML visualization of the dbt lineage
that can be opened in a web browser.
"""

import json
import networkx as nx
from pathlib import Path


def load_manifest(manifest_path):
    """Load the dbt manifest.json file."""
    with open(manifest_path, 'r') as f:
        return json.load(f)


def extract_lineage(manifest):
    """Extract lineage relationships from the manifest."""
    G = nx.DiGraph()
    
    nodes = manifest.get('nodes', {})
    sources = manifest.get('sources', {})
    
    for node_id, node_data in nodes.items():
        node_type = node_data.get('resource_type', 'unknown')
        node_name = node_data.get('name', node_id)
        description = node_data.get('description', '')
        
        G.add_node(
            node_id,
            name=node_name,
            type=node_type,
            label=node_name,
            description=description
        )
    
    for source_id, source_data in sources.items():
        source_name = source_data.get('name', source_id)
        G.add_node(
            source_id,
            name=source_name,
            type='source',
            label=source_name,
            description='Source data'
        )
    
    for node_id, node_data in nodes.items():
        depends_on = node_data.get('depends_on', {})
        parent_nodes = depends_on.get('nodes', [])
        
        for parent_id in parent_nodes:
            if parent_id in G.nodes:
                G.add_edge(parent_id, node_id)
    
    return G


def generate_html_visualization(G, output_path='lineage_interactive.html'):
    """Generate an interactive HTML visualization."""
    
    # Prepare nodes data
    nodes_data = []
    for node in G.nodes():
        node_attrs = G.nodes[node]
        node_type = node_attrs.get('type', 'unknown')
        
        # Determine color based on type
        color_map = {
            'seed': '#90EE90',
            'model': '#87CEEB',
            'source': '#FFD700',
        }
        color = color_map.get(node_type, '#D3D3D3')
        
        nodes_data.append({
            'id': node,
            'label': node_attrs.get('name', node),
            'title': f"{node_attrs.get('name', node)}<br>Type: {node_type}",
            'color': color,
            'type': node_type
        })
    
    # Prepare edges data
    edges_data = []
    for edge in G.edges():
        edges_data.append({
            'from': edge[0],
            'to': edge[1]
        })
    
    # Create HTML with vis.js
    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Data Lineage Visualization</title>
    <script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
    <style>
        body {{
            font-family: Arial, Helvetica, sans-serif;
            margin: 0;
            padding: 0;
        }}
        #header {{
            background-color: #2c3e50;
            color: white;
            padding: 20px;
            text-align: center;
        }}
        #info {{
            background-color: #ecf0f1;
            padding: 15px;
            margin: 0;
        }}
        #mynetwork {{
            width: 100%;
            height: 700px;
            border: 1px solid lightgray;
        }}
        .legend {{
            padding: 15px;
            background-color: #f8f9fa;
        }}
        .legend-item {{
            display: inline-block;
            margin-right: 20px;
        }}
        .legend-color {{
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 1px solid black;
            margin-right: 5px;
            vertical-align: middle;
        }}
        #stats {{
            padding: 15px;
            background-color: #fff;
            margin: 10px;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .stat-item {{
            display: inline-block;
            margin-right: 30px;
            font-size: 14px;
        }}
        .stat-value {{
            font-weight: bold;
            color: #2c3e50;
        }}
    </style>
</head>
<body>
    <div id="header">
        <h1>📊 Data Lineage Visualization</h1>
        <p>Interactive view of your dbt data pipeline</p>
    </div>
    
    <div id="info">
        <div id="stats">
            <div class="stat-item">
                <span class="stat-value">{G.number_of_nodes()}</span> Total Nodes
            </div>
            <div class="stat-item">
                <span class="stat-value">{G.number_of_edges()}</span> Dependencies
            </div>
            <div class="stat-item">
                <span class="stat-value">{len([n for n in G.nodes() if G.nodes[n].get('type') == 'seed'])}</span> Seeds
            </div>
            <div class="stat-item">
                <span class="stat-value">{len([n for n in G.nodes() if G.nodes[n].get('type') == 'model'])}</span> Models
            </div>
        </div>
    </div>
    
    <div class="legend">
        <div class="legend-item">
            <span class="legend-color" style="background-color: #90EE90;"></span>
            <span>Seeds (Raw Data)</span>
        </div>
        <div class="legend-item">
            <span class="legend-color" style="background-color: #87CEEB;"></span>
            <span>Models (Transformations)</span>
        </div>
        <div class="legend-item">
            <span class="legend-color" style="background-color: #FFD700;"></span>
            <span>Sources</span>
        </div>
    </div>
    
    <div id="mynetwork"></div>
    
    <script type="text/javascript">
        // Create nodes and edges
        var nodes = new vis.DataSet({json.dumps(nodes_data, indent=8)});
        
        var edges = new vis.DataSet({json.dumps(edges_data, indent=8)});
        
        // Create network
        var container = document.getElementById('mynetwork');
        var data = {{
            nodes: nodes,
            edges: edges
        }};
        
        var options = {{
            nodes: {{
                shape: 'dot',
                size: 20,
                font: {{
                    size: 14,
                    face: 'Arial'
                }},
                borderWidth: 2,
                borderWidthSelected: 4
            }},
            edges: {{
                arrows: {{
                    to: {{
                        enabled: true,
                        scaleFactor: 1
                    }}
                }},
                color: {{
                    color: '#848484',
                    highlight: '#2c3e50'
                }},
                width: 2,
                smooth: {{
                    type: 'cubicBezier',
                    roundness: 0.2
                }}
            }},
            layout: {{
                hierarchical: {{
                    direction: 'LR',
                    sortMethod: 'directed',
                    levelSeparation: 200,
                    nodeSpacing: 150
                }}
            }},
            physics: {{
                enabled: false
            }},
            interaction: {{
                hover: true,
                tooltipDelay: 200,
                navigationButtons: true,
                keyboard: true
            }}
        }};
        
        var network = new vis.Network(container, data, options);
        
        // Add click event
        network.on("click", function (params) {{
            if (params.nodes.length > 0) {{
                var nodeId = params.nodes[0];
                var node = nodes.get(nodeId);
                alert("Node: " + node.label + "\\nType: " + node.type);
            }}
        }});
    </script>
    
    <div style="padding: 20px; background-color: #f8f9fa; margin-top: 10px;">
        <h3>💡 Tips:</h3>
        <ul>
            <li>Click and drag to pan around the visualization</li>
            <li>Scroll to zoom in and out</li>
            <li>Click on a node to see details</li>
            <li>Hover over nodes to see tooltips</li>
            <li>Use the navigation buttons in the bottom right</li>
        </ul>
    </div>
</body>
</html>
"""
    
    with open(output_path, 'w') as f:
        f.write(html_content)
    
    print(f"✓ Interactive HTML visualization saved to: {output_path}")
    print(f"  Open it in your browser: file://{Path(output_path).absolute()}")
    
    return output_path


def main():
    """Main execution function."""
    manifest_path = Path('lineage_demo/target/manifest.json')
    
    if not manifest_path.exists():
        print(f"❌ Error: Manifest file not found at {manifest_path}")
        print("Please run 'dbt docs generate' first.")
        return
    
    print(f"📖 Loading manifest from: {manifest_path}")
    manifest = load_manifest(manifest_path)
    
    print("🔍 Extracting lineage relationships...")
    lineage_graph = extract_lineage(manifest)
    
    print("🎨 Creating interactive HTML visualization...")
    output_path = 'lineage_interactive.html'
    generate_html_visualization(lineage_graph, output_path)
    
    print("\n✅ Done! Open the HTML file in your browser to explore the lineage interactively.")


if __name__ == '__main__':
    main()

