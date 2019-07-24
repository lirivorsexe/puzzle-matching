# puzzle-matching
The task is to find matching pieces in a mixed dataset of white rectangles randomly cut in halves (so that bottom ad top edge remain intact).
After being cut various transformations (translation, rotation, shearing) have been applied individually on the pieces.
## Algorithm description
1. Find the shape's vertices
2. Find their convex hull
3. Find the shape's base edge
  - Find the longest convex hull's segment
  - For the found segment and two segments adjacent to it on both sides:
    - Calculate coordinates of 50 points equally distributed over those 3 segments
    - Move the points 5 pixels towards the middle of the shape
    - Check if the ratio of black pixels among them is <= 0.1
    - If the condition is satisfied algorithm continues, otherwise the next longest segment is being checked
4. Find the vertex laying the furthest away from the base edge
5. For both the side edges: look for the points in the same distance as the further one, laying on the line determined by the side edges
6. Find the shape determined by two points found in the previous step and two endpoints of the base edge
7. Transform the shape to the original dimensions (regarding width only, the height is unknown yet), so that the base edge lies on the bottom, and two side edges are perpendicular to it
8. Count number of black pixels in every column above the shape
9. Normalize the black pixels' count vector, by dividing it's values by the highest one

After executing above steps, for every vector an element-wise sum with all the other vectors is calculated. 

Ranking of most similar shapes is determined by the ascending order of standard deviations of the calculated sums

## Execution
To run the checking script (provided by the teacher):
```
python3 check.py <path_to_folder_containing_run.sh> <path_to_all_data_sets>
```
To show n most similar pieces to every piece in single dataset:
```
python3 main.py <path_to_single_data_set> <n>
```
