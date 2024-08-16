

class Collision:
    def __init__(self,drones,dependent = None):
        if not isinstance(drones,list):
            raise TypeError(f"List type expected, received {type(drones).__name__}")
        self.drones_involved = drones
        self.dependent_collisions = dependent # collisions that can be resolved
        # once this one is resolved

    def get_involved_drones(self):

        return

class Dependency_Tree:
    def __init__(self):