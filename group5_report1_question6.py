import itertools
import rpy2.robjects as robjects
import rpy2.robjects.lib.ggplot2 as ggplot2
from rpy2.robjects.packages import importr
                
def plot_histogram(fastq_file, plot_filename_png):
    r = robjects.r
    r.library("ggplot2")
    grdevices = importr('grDevices')
    
    sizes = []
    
    with open(fastq_file, 'rb') as f:
        # skip first line
        for _ in itertools.islice(f, 0, 1):
            pass
        fourthlines = itertools.islice(f, 0, None, 4)
        for line in fourthlines:
            sizes.append(len(line))
            
    sizes = robjects.IntVector([s for s in sizes])

    sizes_min = min(sizes)
    sizes_max = max(sizes)
    
    binwidth = (sizes_max - sizes_min) / 20
    
    d = {'sizes' : sizes}
    df = robjects.DataFrame(d)
    
    # plot
    gp = ggplot2.ggplot(df)
    
    pp = gp + ggplot2.aes_string(x='sizes') \
            + ggplot2.geom_histogram(binwidth=binwidth) \
            + ggplot2.theme_bw() \
            + ggplot2.ggtitle(plot_filename_png)
            
    grdevices.png(plot_filename_png, width = 8.5, height = 8.5, 
                units = "in", res = 300)
    pp.plot()
    grdevices.dev_off()

# TODO: make a main function that takes filename and filename_png
# TODO: should run like this 
# "python group5_report1_question6 fastq/1D-fail.fastq 1D-fail.png"
# Would need to add check that filename_png has .png extension

#fastq_file = "fastq/1D-fail.fastq"
#plot_filename_png = "1D-fail.png"

#fastq_file = "fastq/2D-fail.fastq"
#plot_filename_png = "2D-fail.png"

#fastq_file = "fastq/1D-pass.fastq"
#plot_filename_png = "1D-pass.png"

fastq_file = "fastq/2D-pass.fastq"
plot_filename_png = "2D-pass.png"

plot_histogram(fastq_file, plot_filename_png)