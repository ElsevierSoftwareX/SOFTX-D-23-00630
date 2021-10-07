__author__ = "Julián Arenas-Guerrero"
__credits__ = ["Julián Arenas-Guerrero"]

__license__ = "Apache-2.0"
__maintainer__ = "Julián Arenas-Guerrero"
__email__ = "arenas.guerrero.julian@outlook.com"


import logging
import time
import sys
import pandas as pd

import utils

from mapping.mapping_parser import MappingParser
from materializer import Materializer


def retrieve_mappings(config):
    if config.is_read_parsed_mappings_file_provided():
        # retrieve parsed mapping from file and finish mapping processing
        mappings = pd.read_csv(config.get_parsed_mappings_read_path(), keep_default_na=False)
        logging.info(str(len(mappings)) + ' mappings rules loaded from file.')
    else:
        mappings_parser = MappingParser(config)

        start_time = time.time()
        mappings = mappings_parser.parse_mappings()
        logging.info('Mappings processed in ' + utils.get_delta_time(start_time) + ' seconds.')

    if config.is_write_parsed_mappings_file_provided():
        mappings.sort_values(by=['id'], axis=0).to_csv(config.get_parsed_mappings_write_path(), index=False)
        logging.info('Parsed mapping rules saved to file.')
        sys.exit()

    return mappings


def process_materialization(mappings, config):
    materializer = Materializer(mappings, config)

    start_time = time.time()
    if config.is_multiprocessing_enabled():
        materializer.materialize_concurrently()
    else:
        materializer.materialize()

    logging.info('Materialization finished in ' + utils.get_delta_time(start_time) + ' seconds.')