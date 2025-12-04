from numpy import *
from amoebaSegments2x import amoebaSegments2x
def amoeba2Dxx(amoeba_struct):
    #if nargin == 0
    #error('amoeba2Dxx requires amoeba_struct');
    #end#if

    amoebas_image_x =  []; #cell( amoeba_struct.num_targets + amoeba_struct.num_distractors, 2 );
    amoebas_image_y =  []; #cell( amoeba_struct.num_targets + amoeba_struct.num_distractors, 2 );

    amoeba_struct.delta_phi = (2*pi)/amoeba_struct.num_phi;

    # List of possible start/stop angles, from 0-2pi. i.e.: linspace(0,2pi,num_phi))
    farg = arange(0,amoeba_struct.num_phi) * amoeba_struct.delta_phi
    fourier_offsets=tile( arange(0,amoeba_struct.num_fourier), (amoeba_struct.num_phi,1) ).T
    farg2 = fourier_offsets * tile( farg, (amoeba_struct.num_fourier,1) )

    amoeba_struct.fourier_arg = farg
    amoeba_struct.fourier_arg2 = farg2

    ## exponential is too regular...
    amoeba_struct.fourier_ratio = ones( (amoeba_struct.num_fourier, 1) );
    amoeba_struct.fourier_ratio = 1.0 / sqrt(arange(0,amoeba_struct.num_fourier)+1);
    amoeba_struct.fourier_ratio[amoeba_struct.fourier_min_holdout-1:amoeba_struct.fourier_min_holdout] = 0;
    amoeba_struct.delta_segment = amoeba_struct.num_phi / amoeba_struct.num_segments;

    random.seed(int64(amoeba_struct.rand_state))

    ##make targets & distractors
    for i_amoeba in arange(0,amoeba_struct.num_targets):
        [amoeba_struct, amoeba_image_x1, amoeba_image_y1] = amoebaSegments2x(amoeba_struct, 0);
        amoebas_image_x += [amoeba_image_x1];
        amoebas_image_y += [amoeba_image_y1];

    random.seed(int64(amoeba_struct.rand_state+1e6))

    ##make distractors
    for i_amoeba in arange(amoeba_struct.num_targets,amoeba_struct.num_targets + amoeba_struct.num_distractors):
        [amoeba_struct, amoeba_image_x1, amoeba_image_y1] = amoebaSegments2x(amoeba_struct, 1);
        amoebas_image_x += [amoeba_image_x1];
        amoebas_image_y += [amoeba_image_y1];

    return amoeba_struct, amoebas_image_x, amoebas_image_y
