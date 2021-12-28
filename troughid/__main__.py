import argparse
import configparser
import pathlib

from troughid._tec import prepare_tec_dataset
from troughid._auroral_boundary import prepare_auroral_boundary_dataset


DESCRIPTION = """Trough-ID

This script completes the following:
    - downloads all datasets
    - prepares datasets
    - runs trough id
    - saves config file
    - sets directories in main config file

required info:
- base directory
    this will download data to
        base_dir/madrigal_tec/...
        base_dir/kp...
        base_dir/auroral_boundary/...
    script will prepare all available data and run trough id
    trough id will run with default settings
    prepared data will be saved in
        base_dir/processed/tec/...
        base_dir/processed/auroral_boundary/...
        base_dir/processed/trough/...
- date range
- name, email and affiliation for madrigal
- trough id settings
"""


def write_config_file(base_dir):
    prepared = base_dir / 'prepared'
    paths = dict(
        madrigal_tec=base_dir / 'madrigal_tec',
        kp=base_dir / 'kp.txt',
        raw_auroral_boundary=base_dir / 'raw_auroral_boundary',
        tec=prepared / 'tec',
        auroral_boundary=prepared / 'auroral_boundary',
        trough=prepared / 'trough',
    )

    config_file = pathlib.Path(__file__).parent / "config.ini"
    config = configparser.ConfigParser()
    config.add_section('PATHS')
    for k, v in paths.items():
        config.set('PATHS', k, str(v))

    with open(config_file, 'w') as f:
        config.write(f)


def download_all_datasets(base_dir):
    ...


def prepare_all_datasets():
    prepare_tec_dataset()
    prepare_auroral_boundary_dataset()


def run_trough_id():
    ...


def main():
    """Main script
    """
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument("base_dir", type=pathlib.Path, help="base directory where datasets will be downloaded to")
    args = parser.parse_args()

    write_config_file(args.base_dir)

    args.base_dir.mkdir(parents=True, exist_ok=True)
    download_all_datasets(args.base_dir)
    prepare_all_datasets()
    run_trough_id()


if __name__ == "__main__":
    main()
