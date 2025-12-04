function [amoeba_image_x, amoeba_image_y] = amoebaSegments2x(amoeba_struct, distractor_flag)

if nargin == 1
    distractor_flag                = 0;
end
%%gap_offest                         = amoeba_struct.delta_segment * rand(1);
%% old method made segments of fixed length
%% list_segments              = [1; round(gap_offest:amoeba_struct.delta_segment:amoeba_struct.num_phi)'];
%% list_segments(end, 2)      = amoeba_struct.num_phi;
%% new method makes segments of variable length
amoeba_struct.num_segments             = amoeba_struct.min_num_segments - 1 + ceil((amoeba_struct.max_num_segments - amoeba_struct.min_num_segments + 1) * rand(1,1));
delta_gap                              = amoeba_struct.min_gap - 1 + ceil(rand(amoeba_struct.num_segments, 1) * (amoeba_struct.max_gap - amoeba_struct.min_gap + 1));
segments_start                         = sort(ceil(rand(amoeba_struct.num_segments, 1) * amoeba_struct.num_phi), 1, "ascend");

%% make sure each segment is at least as long as the gap following it
remove_segments_ndx                    = find((segments_start - circshift(segments_start,1)) < delta_gap);
if numel(remove_segments_ndx) > 1
  remove_segments_ndx                  = remove_segments_ndx(2:end);
else
  remove_segments_ndx                  = [];
end
while ~isempty(remove_segments_ndx)
  segments_start(remove_segments_ndx)  = [];
  delta_gap(remove_segments_ndx)       = [];
  remove_segments_ndx                  = find((segments_start - circshift(segments_start,1)) < delta_gap);
  if numel(remove_segments_ndx) > 1
    remove_segments_ndx                = remove_segments_ndx(2:end);
  else
    remove_segments_ndx                = [];
  end
end

%% define start and end points of each segment including the gaps between segments
cumsum_gap                             = cumsum(delta_gap);   
segments_end                           = circshift(segments_start,-1);
segments_end(end)                      = amoeba_struct.num_phi + segments_start(1);
segments_start                         = segments_start + cumsum_gap;
segments_end                           = segments_end   + cumsum_gap;

%% fix bondaries
%% first remove any segments greater than 2*pi (but keep the first wrap-around values)
excess_segments_ndx                    = find(segments_start > amoeba_struct.num_phi, 1, "first");
first_start                            = segments_start(1);
if ~isempty(excess_segments_ndx)
  wrap_start                           = segments_start(excess_segments_ndx) - amoeba_struct.num_phi;
else
  wrap_start                           = first_start;
end
if ~isempty(excess_segments_ndx)
  segments_start                       = segments_start(1:excess_segments_ndx-1);
  segments_end                         = segments_end(1:excess_segments_ndx-1);
end

last_end                               = segments_end(end);
if wrap_start < first_start 
  segments_start(1)                    = wrap_start; %% use the wrap-around start value as the starting point of the first or second segment
  if last_end > amoeba_struct.num_phi  %% use the final end point value as the end point of the new fist segment
    segments_end(end)                  = amoeba_struct.num_phi;
    segments_start                     = [1; segments_start];
    segments_end                       = [(last_end - amoeba_struct.num_phi); segments_end];
  else
    %% do nothing
  end
else 
  if last_end <= amoeba_struct.num_phi 
    %% do nothing
  elseif first_start - (last_end - amoeba_struct.num_phi) > amoeba_struct.min_gap %%use the last end point as the end point of the new first segment
    segments_end(end)                  = amoeba_struct.num_phi;
    segments_start                     = [1; segments_start];
    segments_end                       = [(last_end - amoeba_struct.num_phi); segments_end];
  else %% just delete the first starting point, making one continous segment that spans the origin
    segments_end(end)                  = amoeba_struct.num_phi;
    segments_start                     = [1; segments_start(2:end)];
  end
end
amoeba_struct.num_segments             = length(segments_start);
list_segments                          = [segments_start, segments_end];

randn_vals = norminv(rand(amoeba_struct.num_fourier,1),0,1); % DRC: so we can perfectly match MATLAB&Python
fourier_coef                           = amoeba_struct.fourier_ratio .* randn_vals .* (rand(amoeba_struct.num_fourier, 1) > amoeba_struct.fourier_sparsity);
fourier_coef2                          = repmat( amoeba_struct.fourier_ratio .* fourier_coef, [1, amoeba_struct.num_phi]);
fourier_phase                          = (pi/2) * rand(amoeba_struct.num_fourier, 1);
fourier_phase2                         = repmat(fourier_phase, [1, amoeba_struct.num_phi]);
fourier_term                           = fourier_coef2 .* cos( amoeba_struct.fourier_arg2 + fourier_phase2);
fourier_sum                            = sum(fourier_term, 1);
fourier_max                            = max(fourier_sum(:));
fourier_min                            = min(fourier_sum(:));
outer_diameter                         = ...
    ( rand(1) * ( amoeba_struct.target_outer_max - amoeba_struct.target_outer_min ) + amoeba_struct.target_outer_min ) ...
    * fix(amoeba_struct.image_rect_size/2);
inner_diameter                         = ...
    ( rand(1) * ( amoeba_struct.target_inner_max - amoeba_struct.target_inner_min ) + amoeba_struct.target_inner_min ) ...
    * outer_diameter;
r_phi                                  = inner_diameter + ...
    ( fourier_sum - fourier_min ) .* ...
    ( outer_diameter - inner_diameter ) ./ (fourier_max - fourier_min +  ( (fourier_max - fourier_min) == 0 ) );

seg_list                               = 1 : amoeba_struct.num_segments;
amoeba_image_x                         = cell(amoeba_struct.num_segments,1);
amoeba_image_y                         = cell(amoeba_struct.num_segments,1);

% extract x,y pairs for each segment
i_seg_ndx                                = 0;
for i_seg = seg_list
    i_seg_ndx                            = i_seg_ndx + 1;
    [amoeba_segment_x, amoeba_segment_y] = pol2cart( ...
        amoeba_struct.fourier_arg( list_segments(i_seg,1):list_segments(i_seg,2) ), ...
        r_phi( list_segments(i_seg,1):list_segments(i_seg,2) ) );
    amoeba_image_x{i_seg_ndx}            = amoeba_segment_x;
    amoeba_image_y{i_seg_ndx}            = amoeba_segment_y;
end    


% if distractor_flag == 1, then rotate segments
if distractor_flag == 1
    tot_segs                             = 0;
    while( tot_segs < amoeba_struct.num_segments )
        poisson_num                      = fix( -log( rand(1) ) * amoeba_struct.segments_per_distractor * amoeba_struct.num_segments )
	if poisson_num >  amoeba_struct.segments_per_distractor * amoeba_struct.num_segments
	  poisson_num                    = fix(amoeba_struct.segments_per_distractor * amoeba_struct.num_segments);
	end
        if poisson_num < 1
            poisson_num                  = 1;
        end
        tot_segs                         = tot_segs + poisson_num;
        if tot_segs > amoeba_struct.num_segments 
            poisson_num                  = tot_segs - amoeba_struct.num_segments;
            tot_segs                     = amoeba_struct.num_segments;
        end
        ave_x                            = 0;
        ave_y                            = 0;
        for i_seg = tot_segs - poisson_num + 1: tot_segs
            ave_x                        = ave_x + mean(amoeba_image_x{i_seg}(:));
            ave_y                        = ave_y + mean(amoeba_image_y{i_seg}(:));
        end
        ave_x                            = ave_x / poisson_num;
        ave_y                            = ave_y / poisson_num;
        rand_theta                       = ( pi / 8 ) + rand(1) * ( 7* pi / 4 );
        for i_seg = tot_segs - poisson_num + 1: tot_segs
            x_old                        = amoeba_image_x{i_seg};
            y_old                        = amoeba_image_y{i_seg};
            x_old                        = x_old - ave_x;
            y_old                        = y_old - ave_y;
            x_new                        = cos(rand_theta) * x_old + sin(rand_theta) * y_old;
            y_new                        = cos(rand_theta) * y_old - sin(rand_theta) * x_old;
            x_new                        = x_new + ave_x;
            y_new                        = y_new + ave_y;
            amoeba_image_x{i_seg}        = x_new;
            amoeba_image_y{i_seg}        = y_new;
        end 
    end
end

    
% fix boundary conditions (use mirror BCs)
%  added conditional
%  || distractor_flag == 1
% to eliminate difference in global density of clutter vs amoebas,
% especiaolly at corners...
offset_x                                 = 2 * ( rand(1) - 0.5 ) * ( fix(amoeba_struct.image_rect_size/2) - ...
    ( distractor_flag == 0 || distractor_flag == 1 ) * outer_diameter );
offset_y                                 = 2 * ( rand(1) - 0.5 ) * ( fix(amoeba_struct.image_rect_size/2) - ...
    ( distractor_flag == 0 || distractor_flag == 1 ) * outer_diameter );
i_seg_ndx                                = 0;
for i_seg = seg_list
    i_seg_ndx                            = i_seg_ndx + 1;
    amoeba_segment_x                     = amoeba_image_x{i_seg_ndx};
    amoeba_segment_y                     = amoeba_image_y{i_seg_ndx};
    amoeba_segment_x                     = ...
        amoeba_segment_x + fix(amoeba_struct.image_rect_size/2) + offset_x;
    amoeba_segment_x                     = ...
        amoeba_segment_x .* ((amoeba_segment_x >= 1) & (amoeba_segment_x <= amoeba_struct.image_rect_size)) + ...
        (2 * amoeba_struct.image_rect_size - amoeba_segment_x ) .* (amoeba_segment_x > amoeba_struct.image_rect_size) + ...
        (1 - amoeba_segment_x) .* (amoeba_segment_x < 1);
    amoeba_segment_y                     = ...
        amoeba_segment_y + fix(amoeba_struct.image_rect_size/2) + offset_y;
    amoeba_segment_y                     = ...
        amoeba_segment_y .* ((amoeba_segment_y >= 1) & (amoeba_segment_y <= amoeba_struct.image_rect_size)) + ...
        (2 * amoeba_struct.image_rect_size - amoeba_segment_y ) .* (amoeba_segment_y > amoeba_struct.image_rect_size) + ...
        (1 - amoeba_segment_y) .* (amoeba_segment_y < 1);
    amoeba_image_x{i_seg_ndx}            = amoeba_segment_x;
    amoeba_image_y{i_seg_ndx}            = amoeba_segment_y;
end
