from blockchain import statistics
from operator import itemgetter
import datetime
import time

stats = statistics.get()



class BlockchainInfo:
    
    def _format_blockchain_info(self, data, block):
        """
        Formats the data fetched

        @param block - the current block number
        @return - formatted currency data
        """
        try:
            isMiningBlock = True
            fomatted_data = ''
            block_minutes = ''
            
            if float(data['minutes_between_blocks]) >= 0.0:
                block_time = ' '
            else:
                block_time = ' '
                isMiningBlock = False

            formatted_data += '```Block #: {}\n'.format(data['n_blocks_total'])
            formatted_data += 'Last Block: {:.2f} minutes ago```\n'.format(float(data['minutes_between_blocks']))
