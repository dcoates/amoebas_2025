from numpy import *
import numpy as np
from scipy.stats import norm

def pol2cart(theta_radians,rho):
    """
    Converts polar coordinates (rho, theta_radians) to Cartesian coordinates (x, y).
    theta_radians should be in radians.
    """
    x = rho * cos(theta_radians)
    y = rho * sin(theta_radians)
    return x, y

def amoebaSegments2x(amoeba_struct, distractor_flag):

    ## gap_offest                         = amoeba_struct.delta_segment * random.rand(1);
    ## old method made segments of fixed length
    ## list_segments              = [1; round(gap_offest:amoeba_struct.delta_segment:amoeba_struct.num_phi)'];
    ## list_segments(end, 2)      = amoeba_struct.num_phi;
    ## new method makes segments of variable length
    amoeba_struct.num_segments             = amoeba_struct.min_num_segments - 1 + int(ceil((amoeba_struct.max_num_segments -
                                                                                        amoeba_struct.min_num_segments + 1) * random.rand(1))[0]);
    delta_gap                              = list( amoeba_struct.min_gap - 1 + ceil(random.rand(amoeba_struct.num_segments) *
                                                                              (amoeba_struct.max_gap - amoeba_struct.min_gap + 1)) )
    segments_start                         = list( sorted(ceil(random.rand(amoeba_struct.num_segments) * amoeba_struct.num_phi) ) )

    ## make sure each segment is at least as long as the gap following it
    # roll <- circshift
    while True:
        remove_segments_ndx                    = where((segments_start - roll(segments_start,1)) < delta_gap)[0];

        #print( remove_segments_ndx )
        # Always remove first one... (?)
        if len(remove_segments_ndx) > 1:
            remove_segments_ndx                  = remove_segments_ndx[1:];
        else:
            break # Done

        for idx1 in remove_segments_ndx[::-1]: # Remove from the end to the beginning (since indxs change with removal)
            segments_start.pop(idx1)
            delta_gap.pop(idx1)

        #print( segments_start, delta_gap )

    ## define start and end points of each segment including the gaps between segments
    cumsum_gap                             = cumsum(delta_gap);   
    segments_end                           = roll(segments_start,-1);
    segments_end[-1]                      = amoeba_struct.num_phi + segments_start[0];
    segments_start                         = segments_start + cumsum_gap;
    segments_end                           = segments_end   + cumsum_gap;

    #print( segments_start, segments_end )
    ## fix bondaries
    ## first remove any segments greater than 2*pi (but keep the first wrap-around values)
    excess_segments_ndx                    = where(segments_start > amoeba_struct.num_phi)[0]
    first_start                            = segments_start[0];
    if len(excess_segments_ndx)>0:
        wrap_start                           = segments_start[excess_segments_ndx[0]] - amoeba_struct.num_phi;
    else:
        wrap_start                           = first_start;
    if len(excess_segments_ndx)>0:
        segments_start                       = segments_start[0:excess_segments_ndx[0]];
        segments_end                         = segments_end[0:excess_segments_ndx[0]];

    last_end                               = segments_end[-1];
    if wrap_start < first_start:
        segments_start[0]                    = wrap_start; ## use the wrap-around start value as the starting point of the first or second segment
        if last_end > amoeba_struct.num_phi:  ## use the final end point value as the end point of the new fist segment
            segments_end[-1]                = amoeba_struct.num_phi;
            segments_start                     = concatenate( ([1], segments_start) );
            segments_end                       = concatenate( ([last_end - amoeba_struct.num_phi], segments_end) );
        ## do nothing
    else:
        if last_end <= amoeba_struct.num_phi:
            ## do nothing
            pass
        elif first_start - (last_end - amoeba_struct.num_phi) > amoeba_struct.min_gap: ##use the last end point as the end point of the new first segment
            segments_end[-1]                  = amoeba_struct.num_phi;
            segments_start                     = concatenate( ([1], segments_start));
            segments_end                       = concatenate( ([last_end - amoeba_struct.num_phi], segments_end));
        else: ## just delete the first starting point, making one continous segment that spans the origin
            segments_end[-1]                 = amoeba_struct.num_phi;
            segments_start                     = concatenate( ([1], segments_start[1:]) );
    #print( segments_start, segments_end )

    amoeba_struct.num_segments             = len(segments_start);
    list_segments                          = dstack( (segments_start, segments_end) )[0];

    randn_vals = norm.ppf(random.rand(amoeba_struct.num_fourier)) # In order to match with MATLAB exactly (rand equiv, randn not)
    mask = random.rand(amoeba_struct.num_fourier) > amoeba_struct.fourier_sparsity;
    fourier_coef                           = amoeba_struct.fourier_ratio * randn_vals * mask;
    fourier_coef2                          = tile( amoeba_struct.fourier_ratio * fourier_coef, [amoeba_struct.num_phi,1]).T;
    fourier_phase                          = (pi/2) * random.rand(amoeba_struct.num_fourier);
    fourier_phase2                         = tile(fourier_phase, [amoeba_struct.num_phi,1]).T;
    #print( fourier_phase.shape, fourier_phase2.shape, fourier_coef.shape, fourier_coef2.shape )
    fourier_term                           = fourier_coef2 * cos( amoeba_struct.fourier_arg2 + fourier_phase2);
    fourier_sum                            = sum(fourier_term, 0);
    fourier_max                            = np.max(fourier_sum);
    fourier_min                            = np.min(fourier_sum);
    if (distractor_flag == 1) and (amoeba_struct.random_distractor_sizes):
        which_size=np.random.randint(3)
        if which_size==0:
            outer_max=amoeba_struct.outer_max_S
            outer_min=amoeba_struct.outer_min_S
            inner_max=amoeba_struct.inner_max
            inner_min=amoeba_struct.inner_min
        elif which_size==1:
            outer_max=amoeba_struct.outer_max_M
            outer_min=amoeba_struct.outer_min_M
            inner_max=amoeba_struct.inner_max
            inner_min=amoeba_struct.inner_min
        else:
            outer_max=amoeba_struct.outer_max_L
            outer_min=amoeba_struct.outer_min_L
            inner_max=amoeba_struct.inner_max
            inner_min=amoeba_struct.inner_min
    else:
        outer_max=amoeba_struct.target_outer_max
        outer_min=amoeba_struct.target_outer_min
        inner_max=amoeba_struct.inner_max
        inner_min=amoeba_struct.inner_min
    outer_diameter                         = \
        ( random.rand(1) * ( outer_max - outer_min ) + outer_min ) * fix(amoeba_struct.image_rect_size/2);
    inner_diameter                         = \
        ( random.rand(1) * ( inner_max - inner_min ) + inner_min ) * outer_diameter;
    r_phi                                  = inner_diameter + \
        ( fourier_sum - fourier_min ) * \
        ( outer_diameter - inner_diameter ) / (fourier_max - fourier_min +  ( (fourier_max - fourier_min) == 0 ) );
 
    amoeba_image_x = []
    amoeba_image_y = []
    for nseg, seg1 in enumerate(list_segments):
        idx_first = int(seg1[0]-1)
        idx_last  = int(seg1[1]-1)
        angles = amoeba_struct.fourier_arg[ idx_first:idx_last+1 ]
        phis   = r_phi[idx_first:idx_last+1]
        [seg_x1,seg_y1] = pol2cart(angles, phis )
        amoeba_image_x += [seg_x1]
        amoeba_image_y += [seg_y1]


    # if distractor_flag == 1, then rotate segments
    if distractor_flag == 1:
        tot_segs                             = 0;
        while( tot_segs < amoeba_struct.num_segments ):
            poisson_num                      = int(
                fix( -log( random.rand(1) ) * amoeba_struct.segments_per_distractor * amoeba_struct.num_segments ))
            #print( poisson_num)
            if poisson_num >  amoeba_struct.segments_per_distractor * amoeba_struct.num_segments:
                poisson_num                    = fix(amoeba_struct.segments_per_distractor * amoeba_struct.num_segments);

            if poisson_num < 1:
                poisson_num                  = 1;

            tot_segs                         = tot_segs + poisson_num;
            if tot_segs > amoeba_struct.num_segments:
                poisson_num                  = tot_segs - amoeba_struct.num_segments;
                tot_segs                     = amoeba_struct.num_segments;

            ave_x                            = 0;
            ave_y                            = 0;
            for i_seg1 in arange(tot_segs - poisson_num + 1, tot_segs+1):
                i_seg = int(i_seg1-1)
                ave_x                        = ave_x + mean(amoeba_image_x[i_seg]);
                ave_y                        = ave_y + mean(amoeba_image_y[i_seg]);
 
            ave_x                            = ave_x / poisson_num;
            ave_y                            = ave_y / poisson_num;

            rand_theta                       = ( pi / 8 ) + random.rand(1) * ( 7* pi / 4 );

            for i_seg1 in arange(tot_segs - poisson_num + 1,tot_segs+1):
                i_seg = int(i_seg1-1)
                x_old                        = amoeba_image_x[i_seg];
                y_old                        = amoeba_image_y[i_seg];
                x_old                        = x_old - ave_x;
                y_old                        = y_old - ave_y;
                x_new                        = cos(rand_theta) * x_old + sin(rand_theta) * y_old;
                y_new                        = cos(rand_theta) * y_old - sin(rand_theta) * x_old;
                x_new                        = x_new + ave_x;
                y_new                        = y_new + ave_y;
                amoeba_image_x[i_seg]        = x_new;
                amoeba_image_y[i_seg]        = y_new;


    # fix boundary conditions (use mirror BCs)
    #  added conditional
    #  || distractor_flag == 1
    # to eliminate difference in global density of clutter vs amoebas,
    # especiaolly at corners...
    offset_x                                 = 2 * ( random.rand(1) - 0.5 ) * ( fix(amoeba_struct.image_rect_size/2) - \
        ( (distractor_flag == 0) | (distractor_flag == 1) ) * outer_diameter );
    offset_y                                 = 2 * ( random.rand(1) - 0.5 ) * ( fix(amoeba_struct.image_rect_size/2) - \
        ( (distractor_flag == 0) | (distractor_flag == 1) ) * outer_diameter );

    for i_seg_ndx,seg1 in enumerate(amoeba_image_x):
        amoeba_segment_x                     = amoeba_image_x[i_seg_ndx];
        amoeba_segment_y                     = amoeba_image_y[i_seg_ndx];
        amoeba_segment_x                     = \
            amoeba_segment_x + fix(amoeba_struct.image_rect_size/2) + offset_x;
        amoeba_segment_x                     = \
            amoeba_segment_x * ((amoeba_segment_x >= 1) & (amoeba_segment_x <= amoeba_struct.image_rect_size)) + \
            (2 * amoeba_struct.image_rect_size - amoeba_segment_x ) * (amoeba_segment_x > amoeba_struct.image_rect_size) + \
            (1 - amoeba_segment_x) * (amoeba_segment_x < 1);
        amoeba_segment_y                     = \
            amoeba_segment_y + fix(amoeba_struct.image_rect_size/2) + offset_y;
        amoeba_segment_y                     = \
            amoeba_segment_y * ((amoeba_segment_y >= 1) & (amoeba_segment_y <= amoeba_struct.image_rect_size)) + \
            (2 * amoeba_struct.image_rect_size - amoeba_segment_y ) * (amoeba_segment_y > amoeba_struct.image_rect_size) + \
            (1 - amoeba_segment_y) * (amoeba_segment_y < 1);
        amoeba_image_x[i_seg_ndx]            = amoeba_segment_x;
        amoeba_image_y[i_seg_ndx]            = amoeba_segment_y;

    return amoeba_struct,amoeba_image_x,amoeba_image_y

