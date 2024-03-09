Here are some codes about the creation of tp5 file, which is the necessary input file for [MODerate resolution atmospheric TRANsmission](http://modtran.spectral.com/).

Descriptions of files:  
create_cards.py: creation of CARD 1-5  
read_profiles.py: read atmospheric profiles (such as tempearture and moisture), then feed into CARD 2C  
read_outputs.py: read the target variables from MODTRAN output files (.tp7 and .flx)  
main.ipynb: an example  
