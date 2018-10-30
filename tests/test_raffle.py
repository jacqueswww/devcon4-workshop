import pytest
from web3 import (
    Web3,
)

ticket_price = Web3.toWei(0.05, 'ether')


@pytest.fixture
def contract(get_contract, w3):
    a1, a2 = w3.eth.accounts[:2]
    with open('./raffle.vy') as f:
        code = f.read()
    c = get_contract(code, *[a1])
    return c


def test_init(contract, w3):
    assert contract.sale_ends() == 6
    assert contract.charity_address() == w3.eth.accounts[0]


def test_buy_zero_address(contract, assert_tx_failed):
    assert_tx_failed(lambda: contract.buy('0x0000000000000000000000000000000000000000', 0))


def test_buy_zero_address(contract, assert_tx_failed):
    assert_tx_failed(lambda: contract.buy('0x0000000000000000000000000000000000000000', 0))



def test_ticket_price(w3, contract, assert_tx_failed):
    a3, a4 = w3.eth.accounts[2:4]
    contract.buy(a4, 44, transact={'value': ticket_price})
    assert_tx_failed(lambda:  contract.buy(a4, 45, transact={'value': ticket_price - 1}))
    assert_tx_failed(lambda:  contract.buy(a4, 45, transact={'value': ticket_price + 1}))


def test_max_participants(w3, contract, assert_tx_failed):
    a4 = w3.eth.accounts[3]
    contract.buy(a4, 200000, transact={'value': ticket_price})
    assert_tx_failed(lambda: contract.buy(a4, 200001, transact={'value': ticket_price}))


def test_cant_rebuy_tickets(w3, contract, assert_tx_failed):
    a1, a2 = w3.eth.accounts[:2]
    contract.buy(a1, 123, transact={'value': ticket_price})
    assert_tx_failed(
        lambda: contract.buy(a2, 123, transact={'value': ticket_price})
    )
    contract.buy(a1, 124, transact={'value': ticket_price})


@pytest.fixture
def buy_tickets(w3, contract):
    _, a2, a3, a4, a5 = w3.eth.accounts[:5]

    contract.buy(a2, 0, transact={'value': ticket_price})
    contract.buy(a3, 1, transact={'value': ticket_price})
    contract.buy(a4, 2, transact={'value': ticket_price})
    contract.buy(a5, 3, transact={'value': ticket_price})

    assert contract.participants(0) == a2
    assert contract.participants(1) == a3
    assert contract.participants(2) == a4
    assert contract.participants(3) == a5

    return contract


def test_buy_particiapants(w3, buy_tickets):
    c = buy_tickets
    assert w3.eth.getBalance(c.address) == w3.toWei(4 * 0.05, 'ether')


def test_sale_round_end(w3, tester, buy_tickets, assert_tx_failed):
    c = buy_tickets
    a4 = w3.eth.accounts[3]
    tester.mine_blocks(num_blocks=4)

    assert_tx_failed(
        lambda: c.buy(a4, 555, transact={'value': ticket_price})
    )

    c.roll_dice(transact={})
    assert c.rolled() == True


def test_payout(w3, tester, buy_tickets):

    c = buy_tickets

    full_pot = w3.eth.getBalance(c.address)
    charity_address = c.charity_address()
    charity_balance_before = w3.eth.getBalance(charity_address)

    tester.mine_blocks(num_blocks=4)

    c.roll_dice(transact={})
    c.payout(transact={})

    charity_balance_after = w3.eth.getBalance(charity_address)

    assert (charity_balance_after - charity_balance_before) == full_pot * 0.9
