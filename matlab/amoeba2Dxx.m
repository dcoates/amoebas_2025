
function [amoeba_image] = amoeba2Dxx(amoeba_struct)

% the following parameters should be packaged into an amoeba
  if nargin == 0
    error('amoeba2Dxx requires amoeba_struct');
  end%if

  amoeba_image = cell( amoeba_struct.num_targets + amoeba_struct.num_distractors, 2 );

  amoeba_struct.delta_phi = (2*pi)/amoeba_struct.num_phi;
  amoeba_struct.fourier_arg = (0:(amoeba_struct.num_phi-1)) * amoeba_struct.delta_phi;
  amoeba_struct.fourier_arg2 = ...
    repmat((0:(amoeba_struct.num_fourier-1))',[1, amoeba_struct.num_phi]) .* ...
    repmat( amoeba_struct.fourier_arg, [amoeba_struct.num_fourier, 1] );
  %% exponential is too regular...
  amoeba_struct.fourier_ratio = ones(amoeba_struct.num_fourier, 1);
  %amoeba_struct.fourier_ratio(:) = 1.0 ./ sqrt([1:amoeba_struct.num_fourier]);  
  amoeba_struct.fourier_ratio(:) = 1.0 ./ ([1:amoeba_struct.num_fourier]);  
  amoeba_struct.fourier_ratio(amoeba_struct.fourier_min_holdout:amoeba_struct.fourier_min_holdout) = 0;
  
  rand('twister', amoeba_struct.rand_state);

  %%make targets & distractors
  for i_amoeba = 1 : amoeba_struct.num_targets
    [amoeba_image_x, amoeba_image_y] = amoebaSegments2x(amoeba_struct, 0);
    amoeba_image{i_amoeba, 1} = amoeba_image_x;
    amoeba_image{i_amoeba, 2} = amoeba_image_y;
  end%for

  rand('twister', amoeba_struct.rand_state+1e6);

  %%make distractors
  for i_amoeba = amoeba_struct.num_targets + 1 : amoeba_struct.num_targets + amoeba_struct.num_distractors
    [amoeba_image_x, amoeba_image_y] = amoebaSegments2x(amoeba_struct, 1);
    amoeba_image{i_amoeba, 1} = amoeba_image_x;
    amoeba_image{i_amoeba, 2} = amoeba_image_y;
  end%for

end%function
