ProvGen v1.0 by James Rogers
05/06/2018

=========================Set up=========================
The generator needs four things from you:

-LandMap: Defines land/sea/lake provinces. Each colored
 with their respective color:
	-Land:#9644C0
	-Sea :#051412
	-Lake:#00FF00

-ProvDenseMap: Defines the size of each land province,
 with black being the smallest and white the largest.
 Sea provinces are based on coastal distance and not
 this map.

-Settings: -Sets the largest/smallest land/sea province size
	   -Mountain range width defines how mountainous 
            terrain is divided up into smaller ranges

-TerrainMap: Defines terrain using the following colors:
	-Plains  :#FF8142
	-Forest  :#59C755
	-Hills   :#F8FF99
	-Jungle  :#7FBF00
	-Marsh   :#4C6023
	-Mountain:#7C877D
	-Desert  :#FF3F00
 Urban terrain is placed down as a single pixel. The closest
 province to each pixel will be set as urban.
	-Urban   :#9B00FF

All input maps should be the same size. Examples are included.

=======================How to Use=======================
Once you have these four files in the Input folder, and
you have cleared the Output folder, click on ProvGenv1.0.exe 
and wait for the prompt to close.

The generated files should appear in the Output folder.
"colormap_rgb_cityemissivemask_a" has to be converted to a
dds format to be compatible with HOI, so this is saved in the
"Convert" folder.

========================Donations=======================
I'm never going to put this software behind a pay wall, but
if you could spare a dollar to keep me developing this though
the summer (and eventually turn this into a random map
generator) then I'd be extremely grateful :)

paypal:jamesrogers221194@hotmail.co.uk

Thanks for using ProvGen!

==========================Help==========================
I have made a discord server to discuss the program. If
you are having any issues or want to offer a suggestion
then join us: https://discord.gg/GrRaXXU











