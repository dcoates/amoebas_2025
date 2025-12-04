import numpy as np
import matplotlib.pyplot as plt

def draw1(amoeba_struct, xs,ys,debug_colors=False,do_show=True):
    """ Draw amoeba segements using matplotlib.
        If debug_colors, target solid others dashed.
        All segments have unique hue.
    """
    cmap1 = plt.cm.jet 

    fig=plt.figure(figsize=(5,5))

    for n,x1 in enumerate(xs):
        am1_x=xs[n]
        am1_y=ys[n]

        for nseg,seg1 in enumerate(am1_x):
            segs1_x = am1_x[nseg]
            segs1_y = am1_y[nseg]
            if debug_colors:
                col1=cmap1(nseg/len(am1_x))
                ls = '-' if n<amoeba_struct.num_targets else '--'
                lw = 2 if n<amoeba_struct.num_targets else 1
            else:
                col1='k'
                ls = '-'
                lw=1
            fig.gca().plot( segs1_x, segs1_y, color=col1, label='%d:%d'%(n,nseg), ls=ls, lw=lw )

    plt.xlim(0,amoeba_struct.image_rect_size)
    plt.ylim(0,amoeba_struct.image_rect_size)
    if debug_colors:
        plt.legend()
    else:
        plt.axis('equal')
        plt.axis('off')

    # Get the plot data as an RGB string and convert to a NumPy array
    if do_show:
        plt.show()
    fig.canvas.draw()
    data = np.frombuffer(fig.canvas.buffer_rgba(), dtype=np.uint8)
    image_array = data.reshape(fig.canvas.get_width_height()[::-1] + (4,))
    return image_array
