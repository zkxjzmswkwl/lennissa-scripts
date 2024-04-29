# Author: Carter
# Description: Runs Necromancy runes for ~24m/hr depending on familiar used, pouches, outfit etc.
# Revision Date: 4/29/2024
from time import sleep
from cockbot5 import console, scene, paint, interface
from cockbot5.scene import ObjectType, ActionType
from cockbot5.core import log, direct_action


# TODO: move this to cockstd
def distance(pos, enemy_pos):
    return ((enemy_pos.x - pos.x) ** 2 + (enemy_pos.y - pos.y) ** 2) ** 0.5


def surge():
    interface.action(1, -1, 109445165, False)


def sorc_pot():
    interface.action(1, -1, 93716557, False)


def inv_full():
    return len(interface.get_inventory()) >= 28


class Script:
    def __init__(self):
        log("Script __init__")
        self.bank()
        self.passing_bracelet()

    def __dtor__(self):
        log("Script __dtor__")

    def get_closest_node(self, pos, node_name):
        nodes = scene.get_entities(ObjectType.LOCATION)
        nodes = [node for node in nodes if node_name in node.get_name()]
        if not nodes:
            return None
        closest = min(nodes, key=lambda n: distance(pos, n.get_position()))
        return closest

    def passing_bracelet(self):
        """
        Use Passing Bracelet to tp top of Um. Done in 1 tick.
        """
        # Put Passing Bracelet on (6th inventory slot)
        interface.action(2, 6, 96534533, False)
        # Use second teleport on Passing Bracelet
        interface.action(3, 9, 95944719, False)

    def bank(self):
        bank_chest = self.get_closest_node(scene.get_hero_position(), "Bank chest")
        if bank_chest is not None:
            # Right click -> "Use" bank chest
            bank_chest.do_action(ActionType.LOC_ONE)
            # Wait until we're within 1 tile of the bank to make sure the interface is open
            while distance(scene.get_hero_position(), bank_chest.get_position()) > 1:
                sleep(0.1)
            #  Load preset 2 interface action
            interface.action(1, 2, 33882231, True)
        else:
            log("No bank chest found.")

    def on_move(self, position):
        """
        This function is called whenever the player moves.
        """
        log(f"money schmoves: {position.x},{position.y}")
        # The exact tile where the Passing Bracelet tps you to.
        if position.x == 1164 and position.y == 1838:
            # Put on Infinity Ethereal gloves for set bonus
            interface.action(2, 6, 96534533, False)
            sleep(0.6)
            # Find and click on portal
            dark_portal = self.get_closest_node(
                scene.get_hero_position(), "Dark portal"
            )
            if dark_portal is not None:
                # Click on portal
                dark_portal.do_action(ActionType.NODE_ONE)
                sleep(1)
                # Surge towards portal
                surge()
                # Make sure we are still targeting the portal
                sleep(1)
                dark_portal.do_action(ActionType.NODE_ONE)

                # The portal drops you in a new world where the Y is always > 1900.
                # So we can check that to infer when the teleport animation has gone through.
                while scene.get_hero_position().y < 1900:
                    log("Walking to Dark portal.")
                    sleep(0.1)

                # Start walking towards the Bone altar
                direct_action(127381, 1294, 1957, ActionType.NODE_ONE)
                # Pop our sorc pot while walking
                sorc_pot()
                # Retarget the Bone altar in case the sorc pot animation interrupted it
                direct_action(127381, 1294, 1957, ActionType.NODE_ONE)
            else:
                log("No Dark portal found.")
                return

    def on_server_tick(self):
        """
        This function is called every server tick (600ms).
        """
        pass

    def on_inventory_update(self, update_type):
        """
        This function is called whenever the player's inventory is updated.
        """
        pass

    def on_exp_drop(self):
        """
        This function is called whenever the player receives experience.
        """
        sleep(1.4)
        interface.action(1, -1, 93716583, False)
        sleep(4)
        self.bank()
        self.passing_bracelet()
