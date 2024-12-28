from collections import deque

class BinaryTree:
    def __init__(self, value = None):
        self.value = value
        self.left = None
        self.right = None

    def get_lt(self):
        return self.left
    def get_rt(self):
        return self.right
    def get_node(self):
        return self.value

    def add_right(self, value):
        if self.value is None:
            self.value = value
        elif self.right is None:
            self.right = BinaryTree(value)
        else:
            self.right.add_right(value)
    def add_left(self, value):
        if self.value is None:
            self.value = value
        elif self.left is None:
            self.left = BinaryTree(value)
        else:
            self.left.add_left(value)
    def add(self, value):
        if self.value is None:
            self.value = value
        elif self.left is None:
            self.left = BinaryTree(value)
        elif self.right is None:
            self.right = BinaryTree(value)
        else:
            self.left.add(value)

    def is_leaf(self):
        return self.left is None and self.right is None and self.value is not None

    def flatten_leaves(self):
        if self.is_leaf():
            return [self.value]
        else:
            if self.left is not None and self.right is not None:
                return self.left.flatten_leaves() + self.right.flatten_leaves()
            elif self.left is None and self.right is not None:
                return self.right.flatten_leaves()
            elif self.left is not None and self.right is None:
                return self.left.flatten_leaves()
            else:
                return []

    def flatten_nodes(self):
        if self.is_leaf():
            return [self.value]
        else:
            if self.left is not None and self.right is not None:
                return [self.value] + self.left.flatten_nodes() + self.right.flatten_nodes()
            elif self.left is None and self.right is not None:
                return [self.value] + self.right.flatten_nodes()
            elif self.left is not None and self.right is None:
                return[self.value] + self.left.flatten_nodes()
            else:
                return []

    def __str__(self):
        if not self.value:
            return "Empty tree"
        levels = []
        queue = deque([(self, 0)])

        while queue:
            node, level = queue.popleft()
            if level == len(levels):
                levels.append([])
            levels[level].append(str(node.value))
            if node.left:
                queue.append((node.left, level + 1))
            if node.right:
                queue.append((node.right, level + 1))

        return "\n".join("Level " + str(i) + ": " + " ".join(level) for i, level in enumerate(levels))

    def to_dict(self):
        """
        Transforms the tree into a dictionary where keys are levels and values
        are lists of node values at those levels.
        """
        if not self.value:
            return {}

        level_dict = {}
        queue = deque([(self, 0)])  # (node, level)

        while queue:
            node, level = queue.popleft()

            if level not in level_dict:
                level_dict[level] = []  # Initialize list for the current level

            level_dict[level].append(node.value)  # Add node's value to the level

            # Add children to the queue
            if node.left:
                queue.append((node.left, level + 1))
            if node.right:
                queue.append((node.right, level + 1))

        return level_dict