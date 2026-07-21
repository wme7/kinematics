import argparse

def command_line_options():
    parser = argparse.ArgumentParser(
        description='Bumpy-road vehicle vibration demo')
    parser.add_argument('--m', '--mass', type=float, default=60)
    parser.add_argument('--k', '--spring', type=float, default=60)
    parser.add_argument('--b', '--damping', type=float, default=80)
    parser.add_argument('--v', '--velocity', type=float, default=5)
    parser.add_argument('--roadfile', type=str, default='bumpy.csv',
                        help='local CSV (or URL) with road data')
    args = parser.parse_args()
    return args.roadfile, args.m, args.b, args.k, args.v
