import json

class NetworkNode:
    def __init__(self, identifier, net):
        self.identifier = identifier
        self.connections = {}
        self.routing_table = {}
        self.network = net
        self.routing_iteration = 0

    def add_connection(self, conn_id, cost):
        self.connections[conn_id] = cost
        self.routing_table[conn_id] = (cost, conn_id)

    def receive_data(self, packet):
        header = packet.get('header', {})
        if header.get('packet_type') == 'ROUTING' and header.get('destination') == 'FLOOD':
            print(f"Node {self.identifier} received data from {header.get('sender')}: {packet['data']}")
            return self.update_routing_table(packet['data'], header.get('sender'))
        return False

    def update_routing_table(self, new_routes, sender):
        routing_updated = False
        for dest, (cost, next_hop) in new_routes.items():
            if dest == self.identifier:
                continue
            if dest not in self.routing_table or cost + self.connections[sender] < self.routing_table[dest][0]:
                print(f"Node {self.identifier} updating routing table for destination {dest} via {sender} with cost {cost + self.connections[sender]}")
                self.routing_table[dest] = (cost + self.connections[sender], sender)
                routing_updated = True
        if routing_updated:
            self.routing_iteration += 1
            self.send_routing_table_to_neighbors()
        return routing_updated

    def send_routing_table_to_neighbors(self):
        packet = {
            'header': {
                'packet_type': 'ROUTING',
                'destination': 'FLOOD',
                'sender': self.identifier,
                'iteration': self.routing_iteration
            },
            'data': self.routing_table
        }
        for neighbor in self.connections:
            if neighbor in self.network.nodes:
                self.network.nodes[neighbor].receive_data(packet)
        print(f"Node {self.identifier} sent routing table to neighbors: {self.routing_table}")

    def start_routing_update(self):
        return self.send_routing_table_to_neighbors()

    def update_connection_cost(self, conn_id, new_cost):
        print(f"Node {self.identifier} connections: {self.connections}")
        if conn_id in self.connections:
            self.connections[conn_id] = new_cost
            if conn_id in self.routing_table:
                self.routing_table[conn_id] = (new_cost, conn_id)
            return True
        return False


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

    def start_routing_updates(self):
        return self.initialize_routing_update()
