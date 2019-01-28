## Frequency Analysis

Using kaggle data as preliminary data, we had performed most frequent word analysis on music genres using all the data we had.

To do this, we firstly tokenized lyrics and then removed non-alphanumeric characters. Next, we removed lyrics-specific tokens such as "chorus" and "verse". Finally, we removed common stop-words such as "i" and "he".

With the resulting tokens, we then extracted tokens that were unique to each genre in order to display key differences between the genres.

The corresponding WordClouds can be seen below:

**1. Hip-Hop**

<img src = "/data/img/cloudhip-hopPlain.png" width = "500">

**2. Rock**

<img src = "/data/img/cloudrockPlain.png" width = "500">

**3. Country**

<img src = "/data/img/cloudcountryPlain.png" width = "500">

And finally, we had tried to use the same analysis on an artist. Here, we did it for Beyonce.

**4. Beyonce**

<img src = "/data/img/cloudbeyoncePlain.png" width = "500">
