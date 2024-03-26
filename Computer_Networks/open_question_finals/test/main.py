import sys

from net_emulator import NetworkEmulator

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Need topology file and router to be marlked down")
        sys.exit(1)
    # if len(sys.argv) > 2 and len(sys.argv) < 3:
    #     print("Need 2 routers from the topology whose route is marked down")
    #     sys.exit(1)

    topology_file = sys.argv[1]
    router1 = sys.argv[2]
    router2 = sys.argv[3]
    net = NetworkEmulator()
    net.rtInit(topology_file)
    net.displayFIBTables("Initial")
    net.initializeRouteUpdation()
    net.displayFIBTables("Final")

    print("Simulating link down...")

    net.linkDown(router1, router2, 999999)
    print("Recomputing routes after link cost update:")
    net.initializeRouteUpdation()
    net.displayFIBTables("Final FIB Tables after link cost update:")