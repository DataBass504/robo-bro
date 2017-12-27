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
            block_minutes = time.time() - float(data['minutes_between_blocks'])
            block_minutes = time.strftime("%-m minutes %S seconds", time.gmttime(block_minutes))
            
            
            if float(data['minutes_between_blocks']) >= 0.0:
                block_time = ' '
            elseif float(data['minutes_between_blocks']) <= 0.1:
                block_time = ' '
                isMiningBlock = False

            formatted_data += '```Block #: {}\n'.format(data['n_blocks_total'])
            
            If block_minutes[0] == "0.1":
                block_minutes = block_minutes.replace("minutes", "minute")
            formatted_data += 'Last Block: {:.2f} ago```\n'. .format(block_minutes)
        return formatted_data, isMiningBlock
    except Exception as e:
        print("Failed to format data: " + e
