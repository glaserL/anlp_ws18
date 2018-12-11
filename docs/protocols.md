# Meeting Protocols

## Nov. 20 2018

1. We brainstormed the following ideas: classifying music genres from billboard songs, generating new possibly cheesy song lyrics, making tools to convert simple text into fancy text, making tools to help prevent people from plagiarizing

2. We all really liked the idea of generating cheesy or nice songs based on the personality of a person. We could make some inferences on the personality using the Twitter API given the user's twitter username. We also wanted to implement a Telegram bot to communicate this song with the user. This is where we stopped.

## Nov. 29 2018

1. We discussed further ideas for the exact implementation techniques for our project. We brainstormed using a Recursive Neural Network (RNN) with word-embedding to generate words of music related to one another. We could then use these vector spaces to generate lyrics of songs. We found an already developed implementation of this here: https://github.com/minimaxir/textgenrnn.

2. Since this is already developed, we suggested using this on our project and perhaps optimizing it for our purposes.

3. However, as a counter-argument, we realized that using RNNs might be counter-productive since they do not represent the crux of what we learned in our ANLP module. We mostly learned statistical/probabilistic techniques and will not be delving into neural networks significantly. Therefore, it might not make sense to take a neural-network-centric approach.

4. This brings us back to using "simpler" models such as n-gram text generation, Naive Bayes, HMMs, etc., for our project. However, we are uncertain of how we should go about this and how realistic it is for us to develop a complex project with these models.

5. We proposed developing a very simple implementation of our idea for now and perhaps deepening this further by implementing it as one of our group project modules or PMs. This would be a natural continuation of our current work and would therefore be efficient for the future.

6. To get a realistic idea of what we should do for our current ANLP project, we decided that we should consult Tatjana and ask her about her views on what is reasonable for us to implement given the skills we learned from this module. We propose to do this tomorrow, on Friday Nov 30. 2018. We hope that this will give us clarity on a reasonable task for the ANLP project which could be expanded later on as a PM.


## Dec. 4 2018

1. We talked about tasks we'd have to do for the original song generation idea:
   * preprocessing of the data for RNN (bigram/trigram?)
  * write simple neural network that can perform task
  * create vocabulary for each genre
  * Problems involved: length and structure of songs, grammaticality, rhymes


2. To make the project for feasible (~workload of 1 homework), we discussed narrowing task down and also different but related ideas:
  * Classification? For example: Can we improve the maximum entropy classifier?
  * Generating smaller/easier texts (Haikus?)

3. The classification idea seemed interesting, possible ideas for classification were:
  * determining genre of a song
  * determining artist of a song

4. We decided to look into creating a neat data base so that we don't have to struggle with noisy csv files

5. An idea that seemed cool to all of us was to look at the development of genres over time:
  * Example: Check 70s Rock songs and 00s Rock songs and see if the classifier works - if it doesn't determine why. Relevant factors that could lead to significant differences could be: type/token ratio, word length, sophisticated words
  * it would also be interesting to look at artist features like gender or the general sentiment of a decade

6. Idea seems also nice because the results can be visualized and presented in a good way. We can extract simple things like the top words of genres over time and more sophisticated things like presenting the change of the word vector over time

7. We will meet Tatjana on the 11.12. and discuss our ideas with her. Until the meeting with her, we will look at the following tasks:
  * Luis: Data base
  * Jules: Research of papers, techniques
  * Atreya: Data set research


## Dec. 11 2018 (Meeting with Tatjana)
* She was reminded of research in socio linguistics, how do new words emerge and how do they spread, which topics are discussed more
  * suggested author: Cristian Danescu-Niculescu-Mizil 
* Told paper about spread of new words in an online forum about beer
* "Social science" approach suggesting hypotheses and scrutinizing their validity would be fine 
* but she also suggested we should come up with a defined task that we can go for to keep a tighter feedback loop
* "if the dataset is large, it will always be significant" we should be aware of that
* taking ideas from Fell/Sporleder paper is fine
* ask Fell to get his data
* Can we come up with something like a minimal baseline on which we can improve on?
* Compare to the sporleder paper! Maybe also come up with new ones, see what happens for us.
* We don't need to finish everything we mention in the planning paper. Must haves: motivation, why, how, and how one will contribute.
* General Informaion: These project modules are more on one special topic, while only the individual project is actually thought up by an individual where we could extend that
