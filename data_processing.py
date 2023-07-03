# data_processing.py
import pandas as pd
import re

def process_data():
    # Step 1: Extract and process the data from the text file
    file_path = "data.txt"

    # Read the data from the text file
    with open(file_path, "r") as file:
        text = file.read()

    # Splitting the text into individual entries
    entries = text.split('\n')

    # Initialize an empty list to store data dictionaries for each entry
    data_list = []

    # Loop through each entry to extract and process the data
    for entry in entries:
        # Extract the symbol using regular expression
        symbol_match = re.search(r"symbol='([^']*)'", entry)
        if symbol_match:
            symbol = symbol_match.group(1)
        else:
            symbol = None

        # Extract the different parts of the symbol
        underlying = None
        expiry_date = None
        strike_price = None
        option_type = None

        if symbol:
            # Extract the underlying symbol (for index)
            underlying_match = re.match(r"^([A-Z]+)", symbol)
            if underlying_match:
                underlying = underlying_match.group(1)

            # Extract the expiry date and strike price (for options)
            option_match = re.match(r"^[A-Z]+(\d{2}[A-Z]{3}\d{2})(\d+)([A-Z]{2})$", symbol)
            if option_match:
                expiry_date = option_match.group(1)
                strike_price = option_match.group(2)
                option_type = option_match.group(3)

        # Extracting values using string manipulation
        symbol = entry[entry.index("symbol='") + 8:entry.index("',")]
        ltp = int(entry[entry.index("LTP=") + 4:entry.index(", LTQ")])
        ltq = int(entry[entry.index("LTQ=") + 4:entry.index(", totalTradedVolume")])
        total_traded_volume = int(entry[entry.index("totalTradedVolume=") + 18:entry.index(", bestBid")])
        best_bid = int(entry[entry.index("bestBid=") + 8:entry.index(", bestAsk")])
        best_ask = int(entry[entry.index("bestAsk=") + 8:entry.index(", bestBidQty")])
        best_bid_qty = int(entry[entry.index("bestBidQty=") + 11:entry.index(", bestAskQty")])
        best_ask_qty = int(entry[entry.index("bestAskQty=") + 11:entry.index(", openInterest")])
        open_interest = int(entry[entry.index("openInterest=") + 13:entry.index(", timestamp")])
        timestamp = entry[entry.index("timestamp=") + 11:entry.index(", sequence")]
        sequence = int(entry[entry.index("sequence=") + 9:entry.index(", prevClosePrice")])
        prev_close_price = int(entry[entry.index("prevClosePrice=") + 15:entry.index(", prevOpenInterest")])
        prev_open_interest = int(entry[entry.index("prevOpenInterest=") + 17:-1])

        # Create a dictionary with the extracted values
        data = {
            "Symbol": symbol,
            "Underlying": underlying,
            "Expiry Date": expiry_date,
            "Strike Price": strike_price,
            "Option Type": option_type,
            "LTP": ltp,
            "LTQ": ltq,
            "Total Traded Volume": total_traded_volume,
            "Best Bid": best_bid,
            "Best Ask": best_ask,
            "Best Bid Qty": best_bid_qty,
            "Best Ask Qty": best_ask_qty,
            "Open Interest": open_interest,
            "Timestamp": timestamp,
            "Sequence": sequence,
            "Prev Close Price": prev_close_price,
            "Prev Open Interest": prev_open_interest
        }

        # Append the data dictionary to the list
        data_list.append(data)

    # Step 2: Convert the list of data dictionaries into a DataFrame
    df = pd.DataFrame(data_list)

    # Return the processed data
    return df
