# Maintainer: Srinivasulu, Pavan Kumar
# Email: psrinivasulu@scu.edu

import json
import sys

from router_netemulator import NetworkEmulator
from log import MyLogger

class Main_FIB_DVR():

    def __init__(self):
        super().__init__()
        self.logger = MyLogger.setup_user1_logger()  # Initialize logger from MyLogger class

    def main(self):

        router_list = []
        with open(sys.argv[1]) as f:
            data = json.load(f)
            router_data = data["Network"]
            for each in router_data:
                router_list.append(each["Router"])

        if sys.argv[2] not in router_list or sys.argv[3] not in router_list:
            self.logger.error('Invalid Router name!! Please provide valid router names')
            sys.exit(1)

        # to check if the json file is fed or not
        if len(sys.argv) <= 1:
            self.logger.error('You have not fed net.json file, So I cannot proceed further!!')
            sys.exit(1)

        # to check if user has given correct number of router names
        if len(sys.argv) <= 3:
            self.logger.error(
                'You might have not given required number of router nodes. Please ensure you give two routers.')
            sys.exit(1)

        topology_file = sys.argv[1]
        router1 = sys.argv[2]
        router2 = sys.argv[3]
        net = NetworkEmulator()
        net.rtInit(topology_file)
        net.displayFIBTables("Initial")
        net.initializeRouteUpdation()
        net.displayFIBTables("Final")

        self.logger.info("Triggering Link Failure")

        net.linkDown(router1, router2, 123456789)
        self.logger.info("Recomputing routes after link cost update:")
        net.initializeRouteUpdation()
        net.displayFIBTables("Final FIB Tables after link cost update:")

if __name__ == '__main__':
    main_fib_dvr = Main_FIB_DVR()
    main_fib_dvr.main()
