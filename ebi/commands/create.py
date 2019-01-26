import logging
import subprocess
import sys
import time

from .. import appversion
from utils import TemporaryMergedYaml

logger = logging.getLogger(__name__)
CONFIG_DELIMITER = ','


def main(parsed):
    if parsed.version:
        version = parsed.version
    else:
        version = str(int(time.time()))

    appversion.make_application_version(parsed.app_name, version, parsed.dockerrun, parsed.ebext)

    logger.info('Ok, now creating version %s for environment %s', version, parsed.env_name)
    payload = ['eb', 'create', parsed.env_name,
               '--timeout=45',
               '--version=' + version,
               '--cname=' + parsed.cname]
    if parsed.profile:
        payload.append('--profile=' + parsed.profile)
    if parsed.region:
        payload.append('--region=' + parsed.region)

    if not parsed.cfg:
        sys.exit(subprocess.call(payload))

    cfgs = parsed.cfg.split(CONFIG_DELIMITER)
    with TemporaryMergedYaml(cfgs) as merged_config:
        payload.append('--cfg=' + merged_config.name)
        sys.exit(subprocess.call(payload))


def apply_args(parser):
    parser.add_argument('app_name', help='Application name to create')
    parser.add_argument('env_name', help='Environ name to deploy')
    parser.add_argument('cname', help='cname for created server')
    parser.add_argument('--version', help='Version label you want to specify')
    parser.add_argument('--profile', help='AWS account')
    parser.add_argument('--region', help='AWS region')
    parser.add_argument('--dockerrun', help='Path to file used as Dockerrun.aws.json')
    parser.add_argument('--ebext', help='Path to directory used as .ebextensions/')
    parser.add_argument('--cfg', help='Configuration template name to eb create')
    parser.set_defaults(func=main)
