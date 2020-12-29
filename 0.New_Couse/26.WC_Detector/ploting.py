from Ob_Detect import df
from bokeh.plotting import figure, output_file, show
from bokeh.models import HoverTool, ColumnDataSource

# Convert data type to display
df["Start_string"]=df["Start"].dt.strftime("%Y/%m/%d %H:%M:%S")
df["End_string"]=df["End"].dt.strftime("%Y/%m/%d %H:%M:%S")
cds=ColumnDataSource(df)

# Set grap confige
p=figure(x_axis_type='datetime',height=200, width=500, sizing_mode = "scale_width", title="Motion Graph")
# Set color
p.yaxis.minor_tick_line_color=None
#p.ygrid[0].ticker.desired_num_ticks=1

# Set start and end time when click on grap
hover=HoverTool(tooltips=[("Start:","@Start_string"),("End:", "@End_string")])
p.add_tools(hover)

# Get motion data
p.quad(left="Start", right="End", bottom=0, top=1, color="green", source=cds)

output_file("./26.WC_Detector/Grap.html")
show(p)
