from dataclasses import dataclass
from typing import Optional

@dataclass
class Node():
    value: str
    left: Optional["Node"] = None
    right: Optional["Node"] = None
    
    def is_leaf(self) -> bool:
        return self.left is None and self.right is None

class Tree():
    def __init__(self, root: Optional[Node] = None) -> None:
        self.root = root
        self.known = []
    
    def update_node(self, node: Node, data: tuple) -> None:
        parent = self.search_parent_node(node, self.root)
        animal = data[0]
        question = data[1]
        answer = data[2]
        if answer == 'n':
            if parent.left is node:
                parent.left = Node(question, node, Node(animal))
            else:
                parent.right = Node(question, node, Node(animal))
        if answer == 'y':
            if parent.left is node:
                parent.left = Node(question, Node(animal), node)
            else:
                parent.right = Node(question, Node(animal), node)
        
    def search_parent_node(self, target: Node, node: Node):
        if node is None or target is self.root:
            return None
        
        if (node.left is not None and node.left is target) or (node.right is not None and node.right is target):
            return node
        
        l = self.search_parent_node(target, node.left)
        
        if l is not None:
            return l
        
        return self.search_parent_node(target, node.right)
    
    def add_known_animal(self, animal) -> None:
        self.known.append(animal)

class Game():
    def __init__(self) -> None:
        self.animals: Optional[Tree] = None
        self.create_game()
    
    def create_game(self) -> None:
        root = Node("Does it swim? ")
        root.left = Node("Is it a fish? ")
        root.right = Node("Is it a bird? ")
        self.animals = Tree(root)
        self.animals.add_known_animal("fish")
        self.animals.add_known_animal("bird")
    
    def print_win(self) -> None:
        print("\nI got it right!")
    
    def get_new_question(self) -> tuple[str]:
        animal = input("\nWhat animal are you thinking of? ")
        self.animals.add_known_animal(animal)
        animal = f"I am thinking on a {animal}, am I correct? "
        question = input("\nWhat is a question that distinguishes your animal from my guess? ")
        while True:
            answer = input("\nWhat is the answer to your question? (y/n): ")
            if answer.lower() in ['y', 'n']:
                break
        
        return (
            animal,
            question,
            answer
        )
    
    def play(self) -> None:
        current_node = self.animals.root
        while True:
            if current_node.is_leaf():
                answer = input(f"\n{current_node.value}")
                if answer == "y":
                    self.print_win()
                else:
                    self.animals.update_node(current_node, self.get_new_question())
                current_node = self.animals.root
            else:
                answer = input(f"\n{current_node.value} (y/n): ")
                if answer.lower() == 'y':
                    current_node = current_node.left
                else:
                    current_node = current_node.right

def main():
    game = Game()
    game.play()

if __name__ == '__main__':
    main()