# backend/core/game_logic.py

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class GameLinkedList:
    def __init__(self):
        self.head = None
        self.values_set = set()

    def reset(self):
        """Resets the list to the initial seed 'Rock'"""
        self.head = Node("Rock")
        self.values_set = {"rock"}
        
    def add(self, value: str) -> bool:
        print(f"Checking if '{value}' is in {self.values_set}")
        if value.lower() in self.values_set:
            print(f"DUPLICATE DETECTED: '{value}' is already in {self.values_set}")
            return False

        new_node = Node(value)
        self.values_set.add(value.lower())

        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

        return True

    def get_all_guesses(self) -> list:
        result = []
        current = self.head
        while current:
            result.append(current.value)
            current = current.next
        return result
