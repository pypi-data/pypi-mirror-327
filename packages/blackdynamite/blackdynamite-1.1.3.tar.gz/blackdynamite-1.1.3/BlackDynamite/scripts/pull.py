#!/usr/bin/env python

import os
import subprocess

import BlackDynamite as BD


def main(argv=None):
    parser = BD.bdparser.BDParser()
    group = parser.register_group('pull')
    group.add_argument("--fetch_runs_data", action='store_true')

    params = parser.parseBDParameters(argv)
    raise RuntimeError("needs to be thought carefully")

    command = ["rsync", "-au", "--info=progress2",
               os.path.join(params['remote_URI'], '.bd'), "."]

    params = parser.parseBDParameters(argv)
    mybase = BD.Base(**params)

    print('BD study: ', mybase.schema)
    raise
    # run_dir = os.path.join('.', "BD-" + mybase.schema + "-runs")

    p = subprocess.run(command)
    if p.returncode != 0:
        raise RuntimeError("An error occurred while retrieving the database")

    if params['fetch_runs_data']:
        command = ["rsync", "-au", "--info=progress2",
                   "BD-", "."]
        p = subprocess.run(command, cwd=params['dest_dir'])
        if p.returncode != 0:
            raise RuntimeError("An error occurred while retrieving the database")


if __name__ == "__main__":
    main()
