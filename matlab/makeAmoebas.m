close all
clear all
octave_flag = true% 
if octave_flag
  octave_core_file_limit(-1)
  crash_dumps_octave_core(0)
  setenv("GNUTERM", "X11")
  graphics_toolkit('gnuplot')
  %%setenv("GNUTERM", "qt")
end%if


global amoeba_struct

amoeba_struct                         = struct;
amoeba_struct.name                    = 'amoeba2D';
rand('twister', sum(100*clock));
amoeba_struct.rand_state              = {rand('twister')};
amoeba_struct.num_segments            = 2^3;
amoeba_struct.image_rect_size         = 256;
amoeba_struct.num_targets             = 1;
amoeba_struct.num_distractors         = 4 - amoeba_struct.num_targets;
amoeba_struct.segments_per_distractor = 2^(-1);  % 2^(-2);%as fraction of num_segments
amoeba_struct.target_outer_max        = 0.85;%1; %max/min outer radius of target annulus, units of image rect
amoeba_struct.target_outer_min        = 0.15;%0.5;%1.0;%
amoeba_struct.target_inner_max        = 0.85;%0.75;%1.0;% %max/min inner radius in units of outer radius
amoeba_struct.target_inner_min        = 0.15;%0.25;%1.0;%
amoeba_struct.num_phi                 = 1024;
amoeba_struct.num_fourier             = 4;
amoeba_struct.min_gap                 = 8; %%16;
amoeba_struct.max_gap                 = 16; %%32;
amoeba_struct.base_shape              = 0;
amoeba_struct.root_path               = '/vast/home/gkenyon/amoeba2D';
amoeba_struct.foldername              = "target";

num_trials = 40;
plot_amoeba2D = 1;
plot_skip = 1;
fmt_trial_str = "%05i";
  
[STATUS, MSG, MSGID]                  = mkdir(amoeba_struct.root_path);
num_fourier_pow2 = 2.^[2:5];
for num_fourier = num_fourier_pow2
    
  amoeba_struct.num_fourier = num_fourier;
  amoeba2D_parent_foldername          = [num2str(num_fourier), 'FC'];
  [STATUS, MSG, MSGID]                = mkdir(amoeba_struct.root_path, amoeba2D_parent_foldername);

  for num_targets = 0 : 1
    
    amoeba2D_filename_root = ['amoeba_', num2str(num_targets), '_', num2str(num_fourier)];
    if plot_amoeba2D
    endif
  
    if num_targets > 0
      amoeba_struct.num_targets     = 1;
      amoeba2D_foldername           = 'target';
    else
      amoeba_struct.num_targets     = 0;
      amoeba2D_foldername           = 'distractor';
    endif
    amoeba_struct.num_distractors   = 4 - amoeba_struct.num_targets;
    amoeba_struct.foldername        = amoeba2D_foldername;
    amoeba2D_parent_folderpath      = [amoeba_struct.root_path, filesep, amoeba2D_parent_foldername];
    [STATUS, MSG, MSGID]            = mkdir(amoeba2D_parent_folderpath, amoeba2D_foldername);
    
    for i_trial = 1:num_trials

      amoeba_struct.name            = [amoeba2D_filename_root, '_', num2str(i_trial, fmt_trial_str)];
      amoeba2D_filename             = [amoeba2D_parent_folderpath, filesep, amoeba2D_foldername, filesep, amoeba_struct.name];     

      if mod( i_trial, plot_skip ) == 0
	disp(amoeba_struct.name);
      endif
      [amoeba_image] = amoeba2Dx(amoeba_struct);
      
      if plot_amoeba2D 
	[fh_amoeba2D] = figure('name', amoeba2D_filename);
	plotAmoeba2D(amoeba_struct, amoeba_image, fh_amoeba2D);
	%%saveas(fh_amoeba2D, [amoeba2D_filename, '.png'], 'png');
	print(fh_amoeba2D, [amoeba2D_filename, '.png']);
	close(fh_amoeba2D);
      endif
      
    endfor % i_trial
    
  endfor % num_fourier_pow2
  
endfor % for num_targets

  
