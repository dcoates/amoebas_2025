class AmoebaStruct:
    def __init__(self,ntargets,size="large"):
        self.name                    = 'amoeba2D';
        #rand('twister', sum(100*clock));
        #self.rand_state              = {rand('twister')};
        self.num_segments            = 2**3;
        self.min_num_segments        = 2**2;
        self.max_num_segments        = 2**4;
        self.image_rect_size         = 256;
        self.num_targets             = ntargets;
        self.num_distractors         = 4-self.num_targets;
        self.segments_per_distractor = 2**(-1);  # 2**(-2);#as fraction of num_segments
        #max/min outer radius of target annulus, units of image rect
        ## large    amoebas: 0.60 -> 0.85
        ## medium   amoebas: 0.40 -> 0.60
        ## small    amoebas: 0.25 -> 0.40
        self.outer_min_S        = 0.25;
        self.outer_max_S        = 0.40;
        self.outer_min_M        = 0.40;
        self.outer_max_M        = 0.60;
        self.outer_min_L        = 0.60;
        self.outer_max_L        = 0.85;
        if size=='small':
            self.target_outer_max        = self.outer_max_S
            self.target_outer_min        = self.outer_min_S
        elif size=='medium':
            self.target_outer_max        = self.outer_max_M
            self.target_outer_min        = self.outer_min_M
        else: # Large is also default
            self.target_outer_max        = self.outer_max_L
            self.target_outer_min        = self.outer_min_L

        self.random_distractor_sizes = 1; # Randomize (S/M or L) the size of each distractor segment?
        self.inner_max        = 0.85;##max/min inner radius in units of outer radius
        self.inner_min        = 0.15;##
        self.num_phi                 = 1024;
        self.fourier_sparsity        = 0.5;
        self.fourier_max             = 2**5;
        self.fourier_min_holdout     = 2**3; ## set to zero for test data
        self.fourier_max_holdout     = 2**4; ## set to 2**5 (or infinity) for test data
        self.min_gap                 = 4;
        self.max_gap                 = 16;
        self.base_shape              = 0;
        self.root_path               = './images';
        self.foldername              = "target";

        num_trials                            = 4;
        plot_amoeba2D                         = 1;
        plot_skip                             = 1;
        fmt_trial_str                         = "%05i";

        num_fourier = self.fourier_max
        self.num_fourier           = num_fourier;
