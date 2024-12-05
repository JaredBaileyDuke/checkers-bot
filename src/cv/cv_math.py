"""
Math functions for computer vision, to identify where the object is on the checkerboard.

Positions can be used by the robot arm to pick up the object at specific locations.
"""
import cv2

# AprilTag locations, center points
at23 = (1013, 61) # 23
at17 = (257, 77) # 17
at5 = (279, 683) # 5
at11 = (1017, 665) # 11

# Image 15 square locations, center points
e2 = (537, 343) # e2 on sample_images/15.jpg
g8 = (943, 199) # g8 on sample_images/15.jpg

# Percentage of squares between AprilTags
e2_x_perc = 0.5 * (e2[0] - at17[0]) / (at23[0] - at17[0]) + \
            0.5 * (e2[0] - at5[0]) / (at11[0] - at5[0])
e2_y_perc = 0.5 * (e2[1] - at17[1]) / (at5[1] - at17[1]) + \
            0.5 * (e2[1] - at23[1]) / (at11[1] - at23[1])
g8_x_perc = 0.5 * (g8[0] - at17[0]) / (at23[0] - at17[0]) + \
            0.5 * (g8[0] - at5[0]) / (at11[0] - at5[0])
g8_y_perc = 0.5 * (g8[1] - at17[1]) / (at5[1] - at17[1]) + \
            0.5 * (g8[1] - at23[1]) / (at11[1] - at23[1])

# Compare percentage of e2 and g8, using this to determine the location of all squares
vert_1_square_perc = (1/2) * (e2_y_perc - g8_y_perc) # 2 squares between e2 and g8
horiz_1_square_perc = (1/6) * (g8_x_perc - e2_x_perc) # 6 squares between e2 and g8

# Calculate the center point of each square
a1 = (at17[0] + (at23[0] - at17[0]) * (e2_x_perc + horiz_1_square_perc * -1),
        at17[1] + (at5[1] - at17[1]) * (e2_y_perc + vert_1_square_perc * 4))
a2 = (at17[0] + (at23[0] - at17[0]) * (e2_x_perc + horiz_1_square_perc * 0),
        at17[1] + (at5[1] - at17[1]) * (e2_y_perc + vert_1_square_perc * 4))
a3 = (at17[0] + (at23[0] - at17[0]) * (e2_x_perc + horiz_1_square_perc * 1),
        at17[1] + (at5[1] - at17[1]) * (e2_y_perc + vert_1_square_perc * 4))
a4 = (at17[0] + (at23[0] - at17[0]) * (e2_x_perc + horiz_1_square_perc * 2),
        at17[1] + (at5[1] - at17[1]) * (e2_y_perc + vert_1_square_perc * 4))
a5 = (at17[0] + (at23[0] - at17[0]) * (e2_x_perc + horiz_1_square_perc * 3),
        at17[1] + (at5[1] - at17[1]) * (e2_y_perc + vert_1_square_perc * 4))
a6 = (at17[0] + (at23[0] - at17[0]) * (e2_x_perc + horiz_1_square_perc * 4),
        at17[1] + (at5[1] - at17[1]) * (e2_y_perc + vert_1_square_perc * 4))
a7 = (at17[0] + (at23[0] - at17[0]) * (e2_x_perc + horiz_1_square_perc * 5),
        at17[1] + (at5[1] - at17[1]) * (e2_y_perc + vert_1_square_perc * 4))
a8 = (at17[0] + (at23[0] - at17[0]) * (e2_x_perc + horiz_1_square_perc * 6),
        at17[1] + (at5[1] - at17[1]) * (e2_y_perc + vert_1_square_perc * 4))

b1 = (at17[0] + (at23[0] - at17[0]) * e2_x_perc + horiz_1_square_perc * -1,
        at17[1] + (at5[1] - at17[1]) * e2_y_perc + vert_1_square_perc * 3)
b2 = (at17[0] + (at23[0] - at17[0]) * e2_x_perc + horiz_1_square_perc * 0,
        at17[1] + (at5[1] - at17[1]) * e2_y_perc + vert_1_square_perc * 3)
b3 = (at17[0] + (at23[0] - at17[0]) * e2_x_perc + horiz_1_square_perc * 1,
        at17[1] + (at5[1] - at17[1]) * e2_y_perc + vert_1_square_perc * 3)
b4 = (at17[0] + (at23[0] - at17[0]) * e2_x_perc + horiz_1_square_perc * 2,
        at17[1] + (at5[1] - at17[1]) * e2_y_perc + vert_1_square_perc * 3)
b5 = (at17[0] + (at23[0] - at17[0]) * e2_x_perc + horiz_1_square_perc * 3,
        at17[1] + (at5[1] - at17[1]) * e2_y_perc + vert_1_square_perc * 3)
b6 = (at17[0] + (at23[0] - at17[0]) * e2_x_perc + horiz_1_square_perc * 4,
        at17[1] + (at5[1] - at17[1]) * e2_y_perc + vert_1_square_perc * 3)
b7 = (at17[0] + (at23[0] - at17[0]) * e2_x_perc + horiz_1_square_perc * 5,
        at17[1] + (at5[1] - at17[1]) * e2_y_perc + vert_1_square_perc * 3)
b8 = (at17[0] + (at23[0] - at17[0]) * e2_x_perc + horiz_1_square_perc * 6,
        at17[1] + (at5[1] - at17[1]) * e2_y_perc + vert_1_square_perc * 3)

c1 = (at17[0] + (at23[0] - at17[0]) * e2_x_perc + horiz_1_square_perc * -1,
        at17[1] + (at5[1] - at17[1]) * e2_y_perc + vert_1_square_perc * 2)
c2 = (at17[0] + (at23[0] - at17[0]) * e2_x_perc + horiz_1_square_perc * 0,
        at17[1] + (at5[1] - at17[1]) * e2_y_perc + vert_1_square_perc * 2)
c3 = (at17[0] + (at23[0] - at17[0]) * e2_x_perc + horiz_1_square_perc * 1,
        at17[1] + (at5[1] - at17[1]) * e2_y_perc + vert_1_square_perc * 2)
c4 = (at17[0] + (at23[0] - at17[0]) * e2_x_perc + horiz_1_square_perc * 2,
        at17[1] + (at5[1] - at17[1]) * e2_y_perc + vert_1_square_perc * 2)
c5 = (at17[0] + (at23[0] - at17[0]) * e2_x_perc + horiz_1_square_perc * 3,
        at17[1] + (at5[1] - at17[1]) * e2_y_perc + vert_1_square_perc * 2)
c6 = (at17[0] + (at23[0] - at17[0]) * e2_x_perc + horiz_1_square_perc * 4,
        at17[1] + (at5[1] - at17[1]) * e2_y_perc + vert_1_square_perc * 2)
c7 = (at17[0] + (at23[0] - at17[0]) * e2_x_perc + horiz_1_square_perc * 5,
        at17[1] + (at5[1] - at17[1]) * e2_y_perc + vert_1_square_perc * 2)
c8 = (at17[0] + (at23[0] - at17[0]) * e2_x_perc + horiz_1_square_perc * 6,
        at17[1] + (at5[1] - at17[1]) * e2_y_perc + vert_1_square_perc * 2)

d1 = (at17[0] + (at23[0] - at17[0]) * e2_x_perc + horiz_1_square_perc * -1,
        at17[1] + (at5[1] - at17[1]) * e2_y_perc + vert_1_square_perc * 1)
d2 = (at17[0] + (at23[0] - at17[0]) * e2_x_perc + horiz_1_square_perc * 0,
        at17[1] + (at5[1] - at17[1]) * e2_y_perc + vert_1_square_perc * 1)
d3 = (at17[0] + (at23[0] - at17[0]) * e2_x_perc + horiz_1_square_perc * 1,
        at17[1] + (at5[1] - at17[1]) * e2_y_perc + vert_1_square_perc * 1)
d4 = (at17[0] + (at23[0] - at17[0]) * e2_x_perc + horiz_1_square_perc * 2,
        at17[1] + (at5[1] - at17[1]) * e2_y_perc + vert_1_square_perc * 1)
d5 = (at17[0] + (at23[0] - at17[0]) * e2_x_perc + horiz_1_square_perc * 3,
        at17[1] + (at5[1] - at17[1]) * e2_y_perc + vert_1_square_perc * 1)
d6 = (at17[0] + (at23[0] - at17[0]) * e2_x_perc + horiz_1_square_perc * 4,
        at17[1] + (at5[1] - at17[1]) * e2_y_perc + vert_1_square_perc * 1)
d7 = (at17[0] + (at23[0] - at17[0]) * e2_x_perc + horiz_1_square_perc * 5,
        at17[1] + (at5[1] - at17[1]) * e2_y_perc + vert_1_square_perc * 1)
d8 = (at17[0] + (at23[0] - at17[0]) * e2_x_perc + horiz_1_square_perc * 6,
        at17[1] + (at5[1] - at17[1]) * e2_y_perc + vert_1_square_perc * 1)

e1 = (at17[0] + (at23[0] - at17[0]) * e2_x_perc + horiz_1_square_perc * -1,
        at17[1] + (at5[1] - at17[1]) * e2_y_perc + vert_1_square_perc * 0)
e2 = (at17[0] + (at23[0] - at17[0]) * e2_x_perc + horiz_1_square_perc * 0, 
        at17[1] + (at5[1] - at17[1]) * e2_y_perc + vert_1_square_perc * 0)
e3 = (at17[0] + (at23[0] - at17[0]) * e2_x_perc + horiz_1_square_perc * 1,
        at17[1] + (at5[1] - at17[1]) * e2_y_perc + vert_1_square_perc * 0)
e4 = (at17[0] + (at23[0] - at17[0]) * e2_x_perc + horiz_1_square_perc * 2,
        at17[1] + (at5[1] - at17[1]) * e2_y_perc + vert_1_square_perc * 0)
e5 = (at17[0] + (at23[0] - at17[0]) * e2_x_perc + horiz_1_square_perc * 3,
        at17[1] + (at5[1] - at17[1]) * e2_y_perc + vert_1_square_perc * 0)
e6 = (at17[0] + (at23[0] - at17[0]) * e2_x_perc + horiz_1_square_perc * 4,
        at17[1] + (at5[1] - at17[1]) * e2_y_perc + vert_1_square_perc * 0)
e7 = (at17[0] + (at23[0] - at17[0]) * e2_x_perc + horiz_1_square_perc * 5,
        at17[1] + (at5[1] - at17[1]) * e2_y_perc + vert_1_square_perc * 0)
e8 = (at17[0] + (at23[0] - at17[0]) * e2_x_perc + horiz_1_square_perc * 6,
        at17[1] + (at5[1] - at17[1]) * e2_y_perc + vert_1_square_perc * 0)

f1 = (at17[0] + (at23[0] - at17[0]) * e2_x_perc + horiz_1_square_perc * -1,
        at17[1] + (at5[1] - at17[1]) * e2_y_perc + vert_1_square_perc * -1)
f2 = (at17[0] + (at23[0] - at17[0]) * e2_x_perc + horiz_1_square_perc * 0,
        at17[1] + (at5[1] - at17[1]) * e2_y_perc + vert_1_square_perc * -1)
f3 = (at17[0] + (at23[0] - at17[0]) * e2_x_perc + horiz_1_square_perc * 1,
        at17[1] + (at5[1] - at17[1]) * e2_y_perc + vert_1_square_perc * -1)
f4 = (at17[0] + (at23[0] - at17[0]) * e2_x_perc + horiz_1_square_perc * 2,
        at17[1] + (at5[1] - at17[1]) * e2_y_perc + vert_1_square_perc * -1)
f5 = (at17[0] + (at23[0] - at17[0]) * e2_x_perc + horiz_1_square_perc * 3,
        at17[1] + (at5[1] - at17[1]) * e2_y_perc + vert_1_square_perc * -1)
f6 = (at17[0] + (at23[0] - at17[0]) * e2_x_perc + horiz_1_square_perc * 4,
        at17[1] + (at5[1] - at17[1]) * e2_y_perc + vert_1_square_perc * -1)
f7 = (at17[0] + (at23[0] - at17[0]) * e2_x_perc + horiz_1_square_perc * 5,
        at17[1] + (at5[1] - at17[1]) * e2_y_perc + vert_1_square_perc * -1)
f8 = (at17[0] + (at23[0] - at17[0]) * e2_x_perc + horiz_1_square_perc * 6,
        at17[1] + (at5[1] - at17[1]) * e2_y_perc + vert_1_square_perc * -1)

g1 = (at17[0] + (at23[0] - at17[0]) * e2_x_perc + horiz_1_square_perc * -1,
        at17[1] + (at5[1] - at17[1]) * e2_y_perc + vert_1_square_perc * -2)
g2 = (at17[0] + (at23[0] - at17[0]) * e2_x_perc + horiz_1_square_perc * 0,
        at17[1] + (at5[1] - at17[1]) * e2_y_perc + vert_1_square_perc * -2)
g3 = (at17[0] + (at23[0] - at17[0]) * e2_x_perc + horiz_1_square_perc * 1,
        at17[1] + (at5[1] - at17[1]) * e2_y_perc + vert_1_square_perc * -2)
g4 = (at17[0] + (at23[0] - at17[0]) * e2_x_perc + horiz_1_square_perc * 2,
        at17[1] + (at5[1] - at17[1]) * e2_y_perc + vert_1_square_perc * -2)
g5 = (at17[0] + (at23[0] - at17[0]) * e2_x_perc + horiz_1_square_perc * 3,
        at17[1] + (at5[1] - at17[1]) * e2_y_perc + vert_1_square_perc * -2)
g6 = (at17[0] + (at23[0] - at17[0]) * e2_x_perc + horiz_1_square_perc * 4,
        at17[1] + (at5[1] - at17[1]) * e2_y_perc + vert_1_square_perc * -2)
g7 = (at17[0] + (at23[0] - at17[0]) * e2_x_perc + horiz_1_square_perc * 5,
        at17[1] + (at5[1] - at17[1]) * e2_y_perc + vert_1_square_perc * -2)
g8 = (at17[0] + (at23[0] - at17[0]) * e2_x_perc + horiz_1_square_perc * 6,
        at17[1] + (at5[1] - at17[1]) * e2_y_perc + vert_1_square_perc * -2)

h1 = (at17[0] + (at23[0] - at17[0]) * e2_x_perc + horiz_1_square_perc * -1,
        at17[1] + (at5[1] - at17[1]) * e2_y_perc + vert_1_square_perc * -3)
h2 = (at17[0] + (at23[0] - at17[0]) * e2_x_perc + horiz_1_square_perc * 0,
        at17[1] + (at5[1] - at17[1]) * e2_y_perc + vert_1_square_perc * -3)
h3 = (at17[0] + (at23[0] - at17[0]) * e2_x_perc + horiz_1_square_perc * 1,
        at17[1] + (at5[1] - at17[1]) * e2_y_perc + vert_1_square_perc * -3)
h4 = (at17[0] + (at23[0] - at17[0]) * e2_x_perc + horiz_1_square_perc * 2,
        at17[1] + (at5[1] - at17[1]) * e2_y_perc + vert_1_square_perc * -3)
h5 = (at17[0] + (at23[0] - at17[0]) * e2_x_perc + horiz_1_square_perc * 3,
        at17[1] + (at5[1] - at17[1]) * e2_y_perc + vert_1_square_perc * -3)
h6 = (at17[0] + (at23[0] - at17[0]) * e2_x_perc + horiz_1_square_perc * 4,
        at17[1] + (at5[1] - at17[1]) * e2_y_perc + vert_1_square_perc * -3)
h7 = (at17[0] + (at23[0] - at17[0]) * e2_x_perc + horiz_1_square_perc * 5,
        at17[1] + (at5[1] - at17[1]) * e2_y_perc + vert_1_square_perc * -3)
h8 = (at17[0] + (at23[0] - at17[0]) * e2_x_perc + horiz_1_square_perc * 6,
        at17[1] + (at5[1] - at17[1]) * e2_y_perc + vert_1_square_perc * -3)

list_of_points = [a1, a2, a3, a4, a5, a6, a7, a8,
                    b1, b2, b3, b4, b5, b6, b7, b8,
                    c1, c2, c3, c4, c5, c6, c7, c8,
                    d1, d2, d3, d4, d5, d6, d7, d8,
                    e1, e2, e3, e4, e5, e6, e7, e8,
                    f1, f2, f3, f4, f5, f6, f7, f8,
                    g1, g2, g3, g4, g5, g6, g7, g8,
                    h1, h2, h3, h4, h5, h6, h7, h8
                    ]

# Convert to integer
list_of_points = [(int(point[0]), int(point[1])) for point in list_of_points]

# Import image 15, and draw dots on each square
image = cv2.imread("sample_images/15.jpg")
output_image = image.copy()

for point in list_of_points:
    print("Point: ", point)
    cv2.circle(output_image, point, 5, (7, 120, 242), -1)

cv2.imshow("Image", output_image)
cv2.waitKey(0)
cv2.destroyAllWindows()