import xml.etree.ElementTree as ET
import re

def parse_sms_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    transactions = []

    for sms in root.findall('sms'):
        body = sms.attrib.get('body', '')
        date = sms.attrib.get('date', '')
        address = sms.attrib.get('address', '')

        # Initialize fields
        amount = None
        receiver_name = None
        receiver_phone = None
        txn_type = None

        # Extract amount (first number before RWF)
        match_amount = re.search(r'(\d[\d,]*)\s*RWF', body)
        if match_amount:
            amount = float(match_amount.group(1).replace(',', ''))

        # Determine transaction type
        if 'received' in body.lower() or 'bank deposit' in body.lower():
            txn_type = 'received'
        elif 'payment' in body.lower():
            txn_type = 'payment'
        elif 'transferred to' in body.lower():
            txn_type = 'transfer'
        else:
            txn_type = 'other'

        # Extract receiver name & phone for transfer/payment messages
        if txn_type in ['payment', 'transfer']:
            # Example patterns:
            # "to Jane Smith 74631" or "to Robert Brown (250791666666)"
            # Try to get name and phone number
            match = re.search(r'to ([A-Za-z ]+)[\s\(]?(\d{9,12})?\)?', body)
            if match:
                receiver_name = match.group(1).strip()
                if match.group(2):
                    receiver_phone = match.group(2).strip()

        transaction = {
            'id': sms.attrib.get('date_sent', date),
            'sender': address,
            'receiver_name': receiver_name,
            'receiver_phone': receiver_phone,
            'amount': amount,
            'type': txn_type,
            'timestamp': date,
            'body': body
        }

        transactions.append(transaction)

    return transactions


if __name__ == "__main__":
    transactions = parse_sms_xml('./modified_sms_v2.xml')
    for t in transactions:
        print(t)
