# Using exiftools to extract location and other data from images

exiftools allows extraction of tens of different types of metadata recorded by mobile phones and digital cameras.

It is particularly effective for investigatiors of crimes against children if the GPS data on the user's phone is turned on---we can easily extract the GPS coordinates of where each photo was taken.

The other metadata that can be supplied seems like a useful input for a neural network---a network could possibly learn patterns in the metadata (image brightness, exposure time, etc) and determine if the images were taken in the same place, even in the absence of location data.