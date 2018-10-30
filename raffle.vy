# Simple raffle example, don't use random generation on chain!

# Log statements
TicketBought: event({ticket_number: uint256, participant: address})
WinnerPicked: event({ticket_number: uint256})

# Constants
BLOCKS_PER_ROUND: constant(uint256) = 10
MAX_PARTICIPANTS: constant(uint256) = 200000
SALE_ROUND_LENGTH: constant(uint256) = 5
ROLL_ROUND_LENGTH: constant(uint256) = 10



# lotto_state
# 1: ticket sale
# 2: closed & generate round
# 3: payout
sale_ends: public(uint256)
rolled: public(bool)
winning_number: public(uint256)
participants: public(address[uint256])
participant_count: uint256
charity_address: public(address)


@public
def __init__(_charity_address: address):
    # Assign charity to pay out to.
    # Set sale_ends to SALE_ROUND_LENGTH block away.
    pass

@payable
@public
def buy(participant: address, ticket_number: uint256):
    # Assign prarticipant address to ticket number
    # Increment participant_count
    pass


@private
@constant
def generate_rand() -> uint256:
    # DO NOT EVER DEPLOY THIS TO MAINNET.
    # Hash the the previous block number,
    # Convert to uint256 and modulo by the participant_count
    return 1


# Roll the dice, and store the winning number.
@public
def roll_dice():
    # Make sure sale has ended
    # Generate winning number and store
    # Set rolled
    pass


# if you have the winning ticket cash out.
@public
def payout():
    # send 10% to winner
    # destroy contract and payout 90% (or the balance) to charity address.
    pass
