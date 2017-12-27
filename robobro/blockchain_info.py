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
        @param fiat - desired currency (i.e. 'EUR', 'USD')
        @return - formatted currency data
        """
        try:
            isMiningBlock = True
            fomatted_data = ''
            block_minutes = ''
            
            if float(data['minutes_between_blocks]) >= 0.0:
                block_time = ' :rocket:'
            else:
                block_time = ' :small_red_triangle_down:'
                isMiningBlock = False

            formatted_data += '``` {}\n'.format(data['n_blocks_total'])
            formatted_data += 'Last Block: {:.2f} minutes ago```\n'.format(float(data['minutes_between_blocks']))
