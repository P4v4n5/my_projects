import json
from router import NetworkNode

class NetworkEmulator:
    def __init__(self):
        self.nodes = {}
        self.node_updated = True

    def init_topology(self, filename):
        try:
            with open(filename, 'r') as f:
                topology = json.load(f)
        except Exception as e:
            print(f'Error: {e}')
            return None

        for node_config in topology['Network']:
            node = NetworkNode(node_config['Node'], self)
            for conn_id, cost in node_config['Connections'].items():
                node.add_connection(conn_id, cost)
            self.nodes[node.identifier] = node

    def display_routing_tables(self, stage):
        print(f"\n{stage} Routing Tables:")
        for node in self.nodes.values():
            print(f"Node {node.identifier}: {node.routing_table}")

    def initialize_routing_update(self):
        while self.node_updated:
            self.node_updated = False
            for node in self.nodes.values():
                if node.start_routing_update():
                    self.node_updated = True

    def link_down(self, node_id, conn_id, new_cost):
        node = self.nodes.get(node_id)
        if node and node.update_connection_cost(conn_id, new_cost):
            self.node_updated = True  # Trigger the routing update process again
            print(f"Link {conn_id} from Node {node_id} cost updated to {new_cost}.")
        else:
            print(f"Failed to update cost for link {conn_id} from Node {node_id}.")
