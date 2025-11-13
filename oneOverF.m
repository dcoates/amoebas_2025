function oneOverF(amoeba_struct, amoeba_image, fh_amoeba2D)

  if ~exist('amoeba_struct') || isempty(amoeba_struct)
    error('oneOverF requires amoeba_struct');
  endif

  if ~exist('amoeba_image') || isempty(amoeba_image)
    [amoeba_image] = amoeba2Dx(amoeba_struct)
  endif

  if nargin <= 2
    fh_amoeba2D = figure('Name', 'amoeba');
  else
    superimpose_flag = 0;
    if superimpose_flag
      hold on;
    else
      clf(fh_amoeba2D);
    endif
  endif
  figure(fh_amoeba2D);
  set(fh_amoeba2D, 'Units', 'pixels');
  axis tight
  axis square
  axis off
  box off
  set(gca, 'Units', 'pixels');
  axis( [0 amoeba_struct.image_rect_size 0 amoeba_struct.image_rect_size] );
  set(fh_amoeba2D,'Color',[0 0 0]);
  hold on
  figPos = get(fh_amoeba2D, 'Position');
  axisPos = get(gca, 'Position');
  num_pixels = amoeba_struct.image_rect_size;%64;
  line_width = 1;
% set(fh_amoeba2D, 'Position', [ figPos(1)-num_pixels/2 figPos(2)-num_pixels/2 num_pixels num_pixels ]);
% set(gca, 'Position', [0 0 num_pixels num_pixels]);

  for i_amoeba = 1 : amoeba_struct.num_targets + amoeba_struct.num_distractors
    amoeba_image_x = amoeba_image{i_amoeba, 1};
    amoeba_image_y = amoeba_image{i_amoeba, 2};
    for i_seg = 1 : size(amoeba_image_x,1)
      ph = plot( amoeba_image_x{i_seg}, amoeba_image_y{i_seg});
      set(ph, 'LineWidth', line_width);
      if i_amoeba <= amoeba_struct.num_targets
        set(ph, 'Color', 'k');
      else
        set(ph, 'Color', 'k');
      endif
    endfor 
  endfor

endfunction
