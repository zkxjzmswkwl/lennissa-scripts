from lennissa.engine import ClientProt
from lennissa.core import sleep, send_key
from lennissa.player import action_node, use_item, get_inventory


def is_inv_full():
    return len(get_inventory()) >= 28


def bank(cp1, cp2):
    # Enter Dungeoneering cache
    action_node(52855, 3032, 9771, cp1)
    sleep(7500)
    # Right click orebox
    use_item(1)
    sleep(250)
    # Deposit orebox in deposit slot
    action_node(25937, 1042, 4578, cp2)
    sleep(2500)
    # Leave Dungeoneering cache
    action_node(52864, 1040, 4575, cp1)
    sleep(7500)


def lennissa_init():
    # Packet opcodes/sizes
    # For left clicking nodes
    cp = ClientProt(117, 9)
    # For using item on node
    cp2 = ClientProt(128, 17)

    # Keep track of inventories since bank
    inventories = 0
    while True:
        if is_inv_full():
            # Try to store ore in orebox
            send_key(0x31)
            sleep(500)
            inventories = inventories + 1
            # Bank after 4 inventories. (120~ ore)
            if inventories >= 4:
                bank()
                inventories = 0

        # Action closest Luminite ore to Dungeoneering cache.
        action_node(113056, 3036, 9764, cp)
        # Mine every 4 ticks
        sleep(2400)
