This is the code that I used to generate the DRM-ARM move count stats.

Use `g++ -std=c++14 -Wall gen_full_data.cpp` to compile

and `./a.out` to generate the "full_data.csv" file.

The format for this file is : <index_of_eo_to_dr_case>,<corner_orientations>,<position_of_eslice_edges>,<length_of_optimal>,<optimal_sequence>.
Detailed info:
    - index = coordinate for the case (i.e. a integer that is associated to the position. You can compute the coordinate given the position and vice-versa)
    - corner orientations are 0 (oriented), 1 (cw twisted) or 2 (ccw twisted). Corner order is [ULF, URF, URB, ULB, DLF, DRF, DRB, DLB]
    - eslice edges positions are stored as a bit array (1 means there is an E slice edge at this position, 0 if there isnt). Edge order is : [UF, UR, UB, UL, LF, RF, RB, LB, DF, DR, DB, DL]
    - optimal sequence is only the first one that is found by the search algorithm, others are discarded (there may be easier ones depending on the case). It is optimal in the FB-EO-preserving metric : {U,D,R,L,F2,B2}

