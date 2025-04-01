
import time
from argparse import ArgumentParser

from gw_certificate.gw_certificate import GWCertificate, GW_CERT_VERSION
from gw_certificate.tests import TESTS, TESTS_DEFAULT
from gw_certificate.tests.throughput import STRESS_DEFAULT_PPS
from gw_certificate.tests.registration import REG_CERT_OWNER_ID, RegistrationTest
from gw_certificate.tests.uplink import UplinkTest
from gw_certificate.tests.throughput import StressTest

def filter_tests(tests_names):
    chosen_tests = []
    if tests_names == []:
        return TESTS_DEFAULT
    for test_class in TESTS:
        for test_name in tests_names:
            if test_name in test_class.__name__.lower() and test_class not in chosen_tests:
                chosen_tests.append(test_class)
    return chosen_tests

def main():
    usage = (
        "usage: wlt-gw-certificate [-h] -owner OWNER -gw GW\n"
        f"                          [-tests {{connection, uplink, downlink, stress}}] [-update] [-pps {STRESS_DEFAULT_PPS}]\n"
        "                           [-agg AGG] [-env {prod, test, dev}]"
        )

    parser = ArgumentParser(prog='wlt-gw-certificate',
                            description=f'Gateway Certificate {GW_CERT_VERSION} - CLI Tool to test Wiliot GWs', usage=usage)

    required = parser.add_argument_group('required arguments')
    required.add_argument('-gw', type=str, help="Gateway ID", required=True)
    optional = parser.add_argument_group('optional arguments')
    optional.add_argument('-owner', type=str, help="Owner ID", required=False, default=REG_CERT_OWNER_ID)
    optional.add_argument('-suffix', type=str, help="Topic suffix", default='', required=False)
    optional.add_argument('-tests', type=str, choices=['registration', 'connection', 'uplink', 'downlink', 'actions', 'stress'],
                          help="Tests to run. Registration omitted by default.", required=False, nargs='+', default=[])
    optional.add_argument('-update', action='store_true', help='Update test board firmware', default=False, required=False)
    optional.add_argument('-pps', type=int, help='Single packets-per-second rate to simulate in the stress test',
                          choices=STRESS_DEFAULT_PPS, default=None, required=False)
    optional.add_argument('-agg', type=int, help='Aggregation time [seconds] the Uplink stages wait before processing results',
                          default=0, required=False)
    optional.add_argument('-env', type=str, help='Environment for the registration test (Internal usage)',
                          choices=['prod', 'test', 'dev'], default='prod', required=False)
    args = parser.parse_args()

    tests = filter_tests(args.tests)
    topic_suffix = '' if args.suffix == '' else '-'+args.suffix

    if args.pps != None and StressTest not in tests:
        parser.error("Packets per second (-pps) flag can only be used when 'stress' is included in test list (e.g. -tests stress)")
    if args.agg != 0 and UplinkTest not in tests:
        parser.error("Aggregation time (-agg) flag can only be used when 'uplink' is included in test list (e.g. -tests uplink)")
    if args.owner == REG_CERT_OWNER_ID and not all(test == RegistrationTest for test in tests):
        print(f"Note: using default owner ID (-owner) - {REG_CERT_OWNER_ID}..")
        time.sleep(2)
        # parser.error("The -owner flag is required when running any test other than the RegistrationTest.")

    gwc = GWCertificate(gw_id=args.gw, owner_id=args.owner, topic_suffix=topic_suffix, tests=tests, update_fw=args.update,
                        stress_pps=args.pps, aggregation_time=args.agg, env=args.env)
    gwc.run_tests()
    gwc.create_results_html()

def main_cli():
    main()

if __name__ == '__main__':
    main()
    