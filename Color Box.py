class CubeSolver:
    def __init__(self, n):
        self.n = n
        self.faces = {}  # Will store the 6 faces

    def rotate_matrix_right(self, matrix):
        # Rotate a face clockwise
        return list(zip(*matrix[::-1]))

    def rotate_matrix_left(self, matrix):
        # Rotate a face counter-clockwise
        return list(zip(*matrix))[::-1]

    def matrix_to_list(self, matrix):
        return [list(row) for row in matrix]

    def turn_left(self):
        # Save current state
        old_front = [row[:] for row in self.faces[4]]
        old_left = [row[:] for row in self.faces[5]]
        old_back = [row[:] for row in self.faces[2]]
        old_right = [row[:] for row in self.faces[6]]

        # Update faces
        self.faces[4] = old_right
        self.faces[5] = old_front
        self.faces[2] = old_left
        self.faces[6] = old_back

        # Rotate top and base
        self.faces[3] = self.matrix_to_list(self.rotate_matrix_right(self.faces[3]))
        self.faces[1] = self.matrix_to_list(self.rotate_matrix_left(self.faces[1]))

    def turn_right(self):
        # Save current state
        old_front = [row[:] for row in self.faces[4]]
        old_right = [row[:] for row in self.faces[6]]
        old_back = [row[:] for row in self.faces[2]]
        old_left = [row[:] for row in self.faces[5]]

        # Update faces
        self.faces[4] = old_left
        self.faces[6] = old_front
        self.faces[2] = old_right
        self.faces[5] = old_back

        # Rotate top and base
        self.faces[3] = self.matrix_to_list(self.rotate_matrix_left(self.faces[3]))
        self.faces[1] = self.matrix_to_list(self.rotate_matrix_right(self.faces[1]))

    def rotate_front(self):
        # Save current state
        old_front = [row[:] for row in self.faces[4]]
        old_base = [row[:] for row in self.faces[1]]
        old_back = [row[:] for row in self.faces[2]]
        old_top = [row[:] for row in self.faces[3]]

        # Update faces
        self.faces[4] = old_top
        self.faces[1] = old_front
        self.faces[2] = old_base
        self.faces[3] = old_back

        # Rotate left and right
        self.faces[5] = self.matrix_to_list(self.rotate_matrix_right(self.faces[5]))
        self.faces[6] = self.matrix_to_list(self.rotate_matrix_left(self.faces[6]))

    def rotate_back(self):
        # Save current state
        old_front = [row[:] for row in self.faces[4]]
        old_top = [row[:] for row in self.faces[3]]
        old_back = [row[:] for row in self.faces[2]]
        old_base = [row[:] for row in self.faces[1]]

        # Update faces
        self.faces[4] = old_base
        self.faces[3] = old_front
        self.faces[2] = old_top
        self.faces[1] = old_back

        # Rotate left and right
        self.faces[5] = self.matrix_to_list(self.rotate_matrix_left(self.faces[5]))
        self.faces[6] = self.matrix_to_list(self.rotate_matrix_right(self.faces[6]))

    def rotate_left(self):
        # Save current state
        old_top = [row[:] for row in self.faces[3]]
        old_left = [row[:] for row in self.faces[5]]
        old_base = [row[:] for row in self.faces[1]]
        old_right = [row[:] for row in self.faces[6]]

        # Update faces
        self.faces[3] = old_right
        self.faces[5] = old_top
        self.faces[1] = old_left
        self.faces[6] = old_base

        # Rotate front and back
        self.faces[4] = self.matrix_to_list(self.rotate_matrix_left(self.faces[4]))
        self.faces[2] = self.matrix_to_list(self.rotate_matrix_right(self.faces[2]))

    def rotate_right(self):
        # Save current state
        old_top = [row[:] for row in self.faces[3]]
        old_right = [row[:] for row in self.faces[6]]
        old_base = [row[:] for row in self.faces[1]]
        old_left = [row[:] for row in self.faces[5]]

        # Update faces
        self.faces[3] = old_left
        self.faces[6] = old_top
        self.faces[1] = old_right
        self.faces[5] = old_base

        # Rotate front and back
        self.faces[4] = self.matrix_to_list(self.rotate_matrix_right(self.faces[4]))
        self.faces[2] = self.matrix_to_list(self.rotate_matrix_left(self.faces[2]))


def solve(n, k, faces, rotations, query):
    # Initialize cube solver
    cube = CubeSolver(n)

    # Load faces into solver
    face_num = 1
    current_face = []
    for face in faces:
        current_face.append(face)
        if len(current_face) == n:
            cube.faces[face_num] = current_face
            current_face = []
            face_num += 1

    # Perform rotations
    for rotation in rotations:
        if rotation == "turn left":
            cube.turn_left()
        elif rotation == "turn right":
            cube.turn_right()
        elif rotation == "rotate front":
            cube.rotate_front()
        elif rotation == "rotate back":
            cube.rotate_back()
        elif rotation == "rotate left":
            cube.rotate_left()
        elif rotation == "rotate right":
            cube.rotate_right()

    # Get color at queried position
    face, row, col = query.split()
    face = (
        face
        if face.isdigit()
        else {"top": 3, "base": 1, "front": 4, "back": 2, "left": 5, "right": 6}[face]
    )
    return cube.faces[int(face)][int(row) - 1][int(col) - 1]


# Process input
n, k = map(int, input().split())
faces = []
for _ in range(6 * n):
    faces.append(input().split())
rotations = []
for _ in range(k):
    rotations.append(input())
query = input()

# Get and print result
result = solve(n, k, faces, rotations, query)
print(result)
