text = '''
Natural Language Processing
    with Deep Learning
     CS224N/Ling284



                       Xiang Lisa Li
       Lecture 12: Neural Language Generation
  Adapted from slides by Antoine Bosselut and Chris Manning
Announcements

1.   IMPORTANT!!! Remember to sign up for AWS by midnight today!
2.   Proposals due on Tuesday
3.   Assignment 4 just due
4.   Assignment 5 is out and due on Friday 11:59PM, Feb 17th
5.   We will hold a HuggingFace transformers tutorial on Friday




2
Today: Natural Language Generation

1. What is NLG?

2. A review: neural NLG model and training algorithm

3. Decoding from NLG models

4. Training NLG models

5. Evaluating NLG Systems

6. Ethical Considerations




3
What is natural language generation?
Natural language generation is one side of natural
language processing. NLP =
   Natural Language Understanding (NLU) +
   Natural Language Generation (NLG)

NLG focuses on systems that produce fluent, coherent
and useful language output for human consumption

Deep Learning is powering next-gen NLG systems!




4
Example Uses of Natural Language Generation
Machine Translation systems
    input: utterances in source languages
    output: translated text in target languages.


Digital assistant (dialogue) systems use NLG
    input: dialog history
    output: text that respond / continue the conversation


Summarization systems (for research articles,
  email, meetings, documents) use NLG
    input: long documents
5   output: summarization of the long documents
More interesting NLG uses

    Creative stories                      Data-to-text                          Visual description




                                        Craig finished his eleven NFL seasons
                                        with 8,189 rushing yards and 566
                                        receptions for 4,911 receiving yards.




        (Rashkin et al.., EMNLP 2020)        (Parikh et al.., EMNLP 2020)            (Krause et al. CVPR 2017)
6
SOTA NLG system

    ChatGPT is an NLG system!
    It’s general purpose and can do many NLG tasks!

    e.g., Chatbot:




7
SOTA NLG system

    ChatGPT is an NLG system!
    It’s general purpose and can do many NLG tasks!

    e.g., Poetry Generation:




8
SOTA NLG system




9
Categorization of NLG tasks
                        Spectrum of open-endedness for Generation Tasks




    Machine
                  Summarization
    Translation




  Source Sentence: 当局已经宣布今天是节假日。

  Reference Translation:
  1. Authorities have announced a national holiday today.
  2. Authorities have announced that today is a national holiday.
  3. Today is a national holiday, announced by the authorities.

                           The output space is not very diverse.
Categorization of NLG tasks
                        Spectrum of open-endedness for Generation Tasks




    Machine                             Task-driven       ChitChat
                  Summarization
    Translation                         Dialog            Dialog



   Input: Hey, how are you?

   Outputs:
   1. Good! You?
   2. I just heard an exciting news, do you want to hear it?
   3. Thx for asking! Barely surviving my hws.

                  The output space is getting more diverse…
Categorization of NLG tasks
                        Spectrum of open-endedness for Generation Tasks




    Machine                             Task-driven       ChitChat        Story
                  Summarization
    Translation                         Dialog            Dialog          Generation



    Input: Write a story about three little pigs?
    Outputs:
    … (so many options) …




                     The output space is extremely diverse…
Categorization of NLG tasks

Less Open-ended                                                More Open-ended

        Machine                       Task-driven   ChitChat       Story
                      Summarization
        Translation                   Dialog        Dialog         Generation


     Open-ended generation: the output distribution still has high freedom

     Non-open-ended generation: the input mostly determines the output
     generation.

     Remark: One way of formalizing categorization this is by entropy.
     These two classes of NLG tasks require different decoding and/or training
     approaches!
13
Today: Natural Language Generation

1. What is NLG?

2. A review: neural NLG model and training algorithm

3. Decoding from NLG models

4. Training NLG models

5. Evaluating NLG Systems

6. Ethical Considerations




14
Basics of natural language generation (review of lecture 5)
• In autoregressive text generation models, at each time step t, our model takes in a
  sequence of tokens as input 𝑦 !" and outputs a new token, 𝑦""
• For model 𝑓( . ) and vocab 𝑉, we get scores 𝑆 = 𝑓 𝑦!" , 𝜃 ∈ ℝ#


                        exp(𝑆* )
     𝑃 𝑦" 𝑦!"     =                        𝑦""         𝑦"")(      𝑦"")'
                    ∑*! ∈ # exp(𝑆*! )
                                                                            …




                𝑦"$%     𝑦"$&      𝑦"$'     𝑦"$(        𝑦""        𝑦")(
15
Basics of natural language generation (review of lecture 5)
• For non-open-ended tasks (e.g., MT), we typically use a encoder-decoder system,
  where this autoregressive model serves as the decoder, and we’d have another
  bidirectional encoder for encoding the inputs.
• For open-ended tasks (e.g., story generation), this autoregressive generation model is
  often the only component.




16
Trained one token at a time by maximum likelihood
• Trained to maximize the probability of the next token 𝑦"∗ given preceding words {𝑦 ∗ }!"
                                                   %
                                          ℒ = − % log 𝑃 𝑦!∗ 𝑦 ∗     &! )
                                                  !#$
     • This is a classification task at each time step trying to predict the actual word 𝑦!∗ in the training data
     • Doing this is often called “teacher forcing” (because you reset at each time step to the ground truth)

                                                                                                   <END>
       𝑦(∗         𝑦'∗         𝑦&∗        𝑦%∗                        ∗
                                                                    𝑦.$&         ∗
                                                                                𝑦.$'        ∗
                                                                                           𝑦.$(      𝑦.∗
                                                        …




17
       𝑦-∗         𝑦(∗         𝑦'∗        𝑦&∗           …            ∗
                                                                    𝑦.$%         ∗
                                                                                𝑦.$&        ∗
                                                                                           𝑦.$'         ∗
                                                                                                       𝑦.$(
Basics of natural language generation (review of lecture 5)
• At inference time, our decoding algorithm defines a function to select a token from this
  distribution:

                    𝑦!! = 𝑔(𝑃 𝑦! 𝑦"! ))                 𝑔( . ) is your decoding algorithm


     • The “obvious” decoding algorithm is to greedily choose the highest probability next
       token according to the model at each time step

• While this basic algorithm sort of works, to do better, the two main avenues are to:

     1. Improve decoding
                                                  Of course, there’s also improving your
                                                  training data or model architecture
     2. Improve the training
18
Today: Natural Language Generation

1. What is NLG?

2. A review: neural NLG model and training algorithm

3. Decoding from NLG models

4. Training NLG models

5. Evaluating NLG Systems

6. Ethical Considerations




19
Decoding: what is it all about?
• At each time step t, our model computes a vector of scores for each token in our
  vocabulary, S ∈ ℝ# :
                                    𝑆 = 𝑓 𝑦"!                     𝑓( . ) is your model


• Then, we compute a probability distribution 𝑃 over these scores with a softmax
  function:
                                                   exp(𝑆# )
                    𝑃 𝑦! = 𝑤 𝑦"!            =
                                              ∑# ! ∈ % exp(𝑆# ! )
• Our decoding algorithm defines a function to select a token from this distribution:

                               𝑦!! = 𝑔(𝑃 𝑦! 𝑦"! ))               𝑔( . ) is your decoding algorithm

20
How to find the most likely string?
• Recall: Lecture 7 on Neural Machine Translation…
• Greedy Decoding
   • Selects the highest probability token in 𝑃 𝑦" 𝑦!" )


                           𝑦!! = 𝐚𝐫𝐠𝐦𝐚𝐱 𝑃 𝑦! = 𝑤 𝑦"! )
                                          𝒘∈𝑽

• Beam Search
   • Discussed in Lecture 7 on Machine Translation
   • Also aims to find strings that maximize the log-prob, but with wider exploration of
     candidates
       Overall, maximum probability decoding is good for low-entropy tasks like MT and
21     summarization!
The most likely string is repetitive for Open-ended Generation

        Context:     In a shocking finding, scientist discovered a herd
                     of unicorns living in a remote, previously
                     unexplored valley, in the Andes Mountains. Even
                     more surprising to the researchers was the fact
                     that the unicorns spoke perfect English.
     Continuation:   The study, published in the Proceedings of the
                     National Academy of Sciences of the United States of
                     America (PNAS), was conducted by researchers from the
                     Universidad Nacional Autónoma de México (UNAM)
                     and the Universidad Nacional Autónoma de México
                     (UNAM/Universidad Nacional Autónoma de México/
                     Universidad Nacional Autónoma de México/
                     Universidad Nacional Autónoma de México/
                     Universidad Nacional Autónoma de México…
22                                                              (Holtzman et. al., ICLR 2020)
Why does repetition happen?




     A self-amplification effect!
23                                  (Holtzman et. al., ICLR 2020)
And it keeps going…




     Scale doesn’t solve this problem: even a 175 billion parameter LM still repeats when we
24   decode for the most likely string.                                            (Holtzman et. al., ICLR 2020)
How can we reduce repetition?
Simple option:
• Heuristic: Don’t repeat n-grams

More complex:
• Use a different training objective:
   • Unlikelihood objective (Welleck et al., 2020) penalize generation of already-seen tokens
   • Coverage loss (See et al., 2017) Prevents attention mechanism from attending to the
     same words
• Use a different decoding objective:
   • Contrastive decoding (Li et al, 2022) searches for strings x that maximize
     logprob_largeLM (x) – logprob_smallLM (x).


25
Is finding the most likely string reasonable for open-ended
generation?       a       ar        t i        r ri i

                    1

                   0.8
     Probability



                   0.6

                   0.4

                   0.2

                    0
                         0        20               40              60                 80                  100

                                                        i     t                            a         ar
                                                                                                a

           It fails to match the uncertainty distribution for human generated text.
26                                                                                             (Holtzman et. al., ICLR 2020)
Time to get random : Sampling!
• Sample a token from the distribution of tokens

                               𝑦!+ ∼ 𝑃 𝑦+ = 𝑤 { 𝑦   ,+ )

                                                           restroom
• It’s random so you can sample any token!
                                                           grocery
                                                           store
                                                           airport
          He wanted                                        bathroom
          to go to the            Model
                                                           beach
                                                           doctor
                                                           hospital
                                                           pub
                                                           gym
27
Decoding: Top-k sampling
• Problem: Vanilla sampling makes every token in the vocabulary an option
   • Even if most of the probability mass in the distribution is over a limited set of
     options, the tail of the distribution could be very long and in aggregate have
     considerable mass (statistics speak: we have “heavy tailed” distributions)
   • Many tokens are probably really wrong in the current context
   • For these wrong tokens, we give them individually a tiny chance to be selected.
   • But because there are many of them, we still give them as a group a high chance to
     be selected.

• Solution: Top-k sampling
   • Only sample from the top k tokens in the probability distribution


28                                                       (Fan et al., ACL 2018; Holtzman et al., ACL 2018)
Decoding: Top-k sampling
• Solution: Top-k sampling
   • Only sample from the top k tokens in the probability distribution
   • Common values are k = 50 (but it’s up to you!)
                                                                                  restroom
                                                                                  grocery
                                                                                  store
                                                                                  airport
                    He wanted                                                     bathroom
                    to go to the              Model
                                                                                  beach
                                                                                  doctor
                                                                                  hospital
     • Increase k yields more diverse, but risky outputs                          pub
     • Decrease k yields more safe but generic outputs                            gym
29


                                                           (Fan et al., ACL 2018; Holtzman et al., ACL 2018)
Issues with Top-k sampling



                             Top-k sampling can cut off too quickly!




                             Top-k sampling can also cut off too slowly!



30                                                   (Holtzman et. al., ICLR 2020)
Decoding: Top-p (nucleus) sampling
• Problem: The probability distributions we sample from are dynamic
   • When the distribution Pt is flatter, a limited k removes many viable options
   • When the distribution Pt is peakier, a high k allows for too many options to have a
     chance of being selected

• Solution: Top-p sampling
   • Sample from all tokens in the top p cumulative probability mass (i.e., where mass is
     concentrated)
   • Varies k depending on the uniformity of Pt




31                                                                      (Holtzman et. al., ICLR 2020)
Decoding: Top-p (nucleus) sampling
• Solution: Top-p sampling
   • Sample from all tokens in the top p cumulative probability mass (i.e., where mass is
     concentrated)
   • Varies k depending on the uniformity of Pt



𝑃!( 𝑦! = 𝑤 { 𝑦       "! )       𝑃!) 𝑦! = 𝑤 { 𝑦        "! )      𝑃!* 𝑦! = 𝑤 { 𝑦           "! )




32                                                                      (Holtzman et. al., ICLR 2020)
Decoding: More to go
• Typical Sampling (Meister et al. 2022)
   • Reweights the score based on the entropy of the distribution.
• Epsilon Sampling (Hewitt et al. 2022)
   • Set a threshold for lower bounding valid probabilities.


𝑃!( 𝑦! = 𝑤 { 𝑦       "! )      𝑃!) 𝑦! = 𝑤 { 𝑦        "! )     𝑃!* 𝑦! = 𝑤 { 𝑦          "! )




33                                                                   (Holtzman et. al., ICLR 2020)
Scaling randomness: Temperature
•        Recall: On timestep t, the model computes a prob distribution Pt by applying the softmax function to
         a vector of scores 𝑠 ∈ ℝ|(|
                                                            exp(𝑆) )
                                           𝑃! (𝑦! = 𝑤) =
                                                         ∑)*∈( exp(𝑆)* )

•        You can apply a temperature hyperparameter 𝜏 to the softmax to rebalance 𝑃! :
                                                           exp 𝑆) /𝜏
                                         𝑃! 𝑦! = 𝑤 =
                                                        ∑)! ∈( exp 𝑆)! /𝜏

•        Raise the temperature 𝜏 > 1: 𝑃! becomes more uniform
          • More diverse output (probability is spread around vocab)
•        Lower the temperature 𝜏 < 1: 𝑃! becomes more spiky
          • Less diverse output (probability is concentrated on top words)
                                 Temperature is a hyperparameter for decoding:
                              It can be tuned for both beam search and sampling.
    34
Improving Decoding: Re-ranking
• Problem: What if I decode a bad sequence from my model?

• Decode a bunch of sequences
   • 10 candidates is a common number, but it’s up to you
• Define a score to approximate quality of sequences and re-rank by this score
   • Simplest is to use (low) perplexity!
       • Careful! Remember that repetitive utterances generally get low perplexity.
     • Re-rankers can score a variety of properties:
       • style (Holtzman et al., 2018), discourse (Gabriel et al., 2021), entailment/factuality (Goyal et al.,
         2020), logical consistency (Lu et al., 2020), and many more …
       • Beware poorly-calibrated re-rankers
     • Can compose multiple re-rankers together.

36
Decoding: Takeaways
• Decoding is still a challenging problem in NLG – there’s a lot more work to be done!

• Different decoding algorithms can allow us to inject biases that encourage different
  properties of coherent natural language generation

• Some of the most impactful advances in NLG of the last few years have come from
  simple but effective modifications to decoding algorithms




37
Today: Natural Language Generation

1. What is NLG?

2. A review: neural NLG model and training algorithm

3. Decoding from NLG models

4. Training NLG models

5. Evaluating NLG Systems

6. Ethical Considerations




38
Is repetition due to how LMs are trained?

         Context:    In a shocking finding, scientist discovered a herd
                     of unicorns living in a remote, previously
                     unexplored valley, in the Andes Mountains. Even
                     more surprising to the researchers was the fact
                     that the unicorns spoke perfect English.

     Continuation:   The study, published in the Proceedings of the
                     National Academy of Sciences of the United States of
                     America (PNAS), was conducted by researchers from the
                     Universidad Nacional Autónoma de México (UNAM)
                     and the Universidad Nacional Autónoma de México
                     (UNAM/Universidad Nacional Autónoma de México/
                     Universidad Nacional Autónoma de México/
                     Universidad Nacional Autónoma de México/
                     Universidad Nacional Autónoma de México…
39                                                              (Holtzman et. al., ICLR 2020)
Diversity Issues
• MLE model learns bad mode of the text distribution.




40
                                                             1

Exposure Bias                                               0.8




                                              Probability
                                                            0.6

                                                            0.4
• Training with teacher forcing leads to                    0.2
  exposure bias at generation time                           0
                                                                  0         20              40                      60               80                   100
   • During training, our model’s inputs                                                          i         t                             a       ar
     are gold context tokens from real,                                                                                                       a

     human-generated texts                                                                                                                    <END>
                                                                      !#∗   !$∗     !%∗     !(∗                       ∗
                                                                                                                     !&'%     ∗
                                                                                                                             !&'$      ∗
                                                                                                                                      !&'#      !&∗
                                                                                                        …


          ℒ456 = − log 𝑃 𝑦"∗ 𝑦 ∗    !" )
                                                                      !!∗   !#∗     !$∗     !%∗         …             ∗
                                                                                                                     !&'(     ∗
                                                                                                                             !&'%      ∗
                                                                                                                                      !&'$         ∗
                                                                                                                                                  !&'#


     • At generation time, our model’s                                                                                                        <END>
       inputs are previously–decoded tokens                                         !($     !("
                                                                                                        …
                                                                                                                     !(&!(   !(&!"    !(&!$     !(&




           ℒ789 = − log 𝑃 𝑦"" 𝑦"   !" )
                                                                                                                …
                                                                       ∗     ∗
                                                                      !!"   !!$      !%∗    !($       !("            !(&!'   !(&!(    !(&!"       !(&!$
                                                                                  <START>

42
Exposure Bias Solutions
• Scheduled sampling (Bengio et al., 2015)
   • With some probability p, decode a token and feed that as the next input, rather than
     the gold token.
   • Increase p over the course of training
   • Leads to improvements in practice, but can lead to strange training objectives

• Dataset Aggregation (DAgger; Ross et al., 2011)
   • At various intervals during training, generate sequences from your current model
   • Add these sequences to your training set as additional examples


                         Basically, variants of the same approach; see:
                         https://nlpers.blogspot.com/2016/03/a-dagger-by-any-other-name-scheduled.html

43
Exposure Bias Solutions
• Retrieval Augmentation (Guu*, Hashimoto*, et al., 2018)
   • Learn to retrieve a sequence from an existing corpus of human-written prototypes
     (e.g., dialogue responses)
   • Learn to edit the retrieved sequence by adding, removing, and modifying tokens in
     the prototype – this will still result in a more “human-like” generation

• Reinforcement Learning: cast your text generation model as a Markov decision process
       •   State s is the model’s representation of the preceding context
       •   Actions a are the words that can be generated
       •   Policy 𝜋 is the decoder
       •   Rewards r are provided by an external score
     • Learn behaviors by rewarding the model when it exhibits them – go study CS 234


44
Reward Estimation
• How should we define a reward function? Just use your evaluation metric!
   • BLEU (machine translation; Ranzato et al., ICLR 2016; Wu et al., 2016)
   • ROUGE (summarization; Paulus et al., ICLR 2018; Celikyilmaz et al., NAACL 2018)
   • CIDEr (image captioning; Rennie et al., CVPR 2017)
   • SPIDEr (image captioning; Liu et al., ICCV 2017)

• Be careful about optimizing for the task as opposed to “gaming” the reward!
   • Evaluation metrics are merely proxies for generation quality!
   • “even though RL refinement can achieve better BLEU scores, it barely improves the
     human impression of the translation quality” – Wu et al., 2016



45
Reward Estimation
• What behaviors can we tie to rewards?
  • Cross-modality consistency in image captioning (Ren et al., CVPR 2017)
  • Sentence simplicity (Zhang and Lapata, EMNLP 2017)
  • Temporal Consistency (Bosselut et al., NAACL 2018)
  • Utterance Politeness (Tan et al., TACL 2018)
  • Formality (Gong et al., NAACL 2019)

• Human Preference (RLHF): this is the technique behind ChatGPT!
   • (Zieglar et al. 2019, Stiennon et al., 2020)
   • Human ranking the generated text based on their preference.
   • Learn a reward function of the human preference.          See discussion of RLHF in
                                                                        the next lecture

46
Training: Takeaways
• Teacher forcing is still the main algorithm for training text generation models



• Exposure bias causes text generation models to lose coherence easily
   • Models must learn to recover from their own bad samples
       • E.g., scheduled sampling, DAgger
     • Or not be allowed to generate bad text to begin with (e.g., retrieval + generation)

• Training with RL can allow models to learn behaviors that are preferred by human
  preference / metrics.



48
Today: Natural Language Generation

1. What is NLG?

2. A review: neural NLG model and training algorithm

3. Decoding from NLG models

4. Training NLG models

5. Evaluating NLG Systems

6. Ethical Considerations




49
Types of evaluation methods for text generation




     Ref: They walked to the grocery store .


     Gen: The woman went to the hardware store .




 Content Overlap Metrics                           Model-based Metrics                    Human Evaluations




50                                                             (Some slides repurposed from Asli Celikyilmaz from EMNLP 2020 tutorial)
Content overlap metrics

                          Ref: They walked to the grocery store .


                          Gen: The woman went to the hardware store .

     • Compute a score that indicates the lexical similarity between generated and gold-
       standard (human-written) text
     • Fast and efficient and widely used
     • N-gram overlap metrics (e.g., BLEU, ROUGE, METEOR, CIDEr, etc.)




51
N-gram overlap metrics
Word overlap–based metrics (BLEU, ROUGE, METEOR, CIDEr, etc.)

• They’re not ideal for machine translation

• They get progressively much worse for tasks that are more open-ended than machine
  translation
   • Worse for summarization, as longer output texts are harder to measure
   • Much worse for dialogue, which is more open-ended that summarization
   • Much, much worse story generation, which is also open-ended, but whose
     sequence length can make it seem you’re getting decent scores!



52
A simple failure case
n-gram overlap metrics have no concept of semantic relatedness!

                    Are you enjoying the
                      CS224N lectures?

                                                        Heck yes !
                                Score:
                                 0.61           Yes !

                                  0.25          You know it !

            False negative          0           Yup .

53
            False positive        0.67          Heck no !
Model-based metrics to capture more semantics

     • Use learned representations of words and
       sentences to compute semantic similarity
       between generated and reference texts

     • No more n-gram bottleneck because text
       units are represented as embeddings!

     • The embeddings are pretrained, distance
       metrics used to measure the similarity can
       be fixed



55
 Model-based metrics: Word distance functions

                         Vector Similarity                          Word Mover’s
                         Embedding based similarity for             Distance
                         semantic distance between text.
                                                                    Measures the distance
                         •   Embedding Average (Liu et al., 2016)   between two sequences (e.g.,
                         •   Vector Extrema (Liu et al., 2016)      sentences, paragraphs, etc.),
                         •   MEANT (Lo, 2017)                       using word embedding
                         •   YISI (Lo, 2019)
                                                                    similarity matching.
                                                                    (Kusner et.al., 2015; Zhao et al., 2019)




BERTSCORE
Uses pre-trained contextual embeddings from
BERT and matches words in candidate and
reference sentences by cosine similarity.
(Zhang et.al. 2020)

 56
Model-based metrics: Beyond word matching

                                      Sentence Movers Similarity :
                                      Based on Word Movers Distance to evaluate text in a continuous space
                                      using sentence embeddings from recurrent neural network
                                      representations.

                                      (Clark et.al., 2019)




     BLEURT:
     A regression model based on BERT returns a score that
     indicates to what extent the candidate text is grammatical
     and conveys the meaning of the reference text.

     (Sellam et.al. 2020)

57
Evaluating Open-ended Text Generation

     MAUVE
     MAUVE computes information divergence in a quantized embedding
     space, between the generated text and the gold reference text (Pillutla
     et.al., 2022).




58
MAUVE (details)




59
How to evaluate an evaluation metric?




60                                      (Liu et al, EMNLP 2016)
Human evaluations




• Automatic metrics fall short of matching human decisions

• Human evaluation is most important form of evaluation for text generation
  systems.

• Gold standard in developing new automatic metrics
   • New automated metrics must correlate well with human evaluations!
61
Human evaluations
     • Ask humans to evaluate the quality of generated text

     • Overall or along some specific dimension:
        • fluency
        • coherence / consistency                  Note: Don’t compare human
        • factuality and correctness               evaluation scores across
        • commonsense
                                                   differently conducted studies




                                                                                    For details Celikyilmaz, Clark, Gao, 2020
        • style / formality
        • grammaticality
                                                   Even if they claim to evaluate
                                                   the same dimensions!
        • typicality
        • redundancy

62
Human evaluation: Issues
• Human judgments are regarded as the gold standard
• Of course, we know that human eval is slow and expensive
• Beyond the cost of human eval, it’s still far from perfect:

• Humans Evaluation is hard:
      •   Results are inconsistent / not reproducible
      •   can be illogical
      •   misinterpret your question
      •   Precision not recall.
      •   …



63
Learning from human feedback




ADEM:                                              HUSE:
A learned metric from human judgments for dialog   Human Unified with Statistical Evaluation (HUSE),
system evaluation in a chatbot setting.            determines the similarity of the output distribution
                                                   and a human reference distribution.
(Lowe et.al., 2017)
                                                   (Hashimoto et.al. 2019)
Evaluating LMs by interacting with them


 Evaluating Human Language Model
 Interaction (Lee et al. 2022)

 Prior work:
 Third-party evaluates the quality of
 the output

 This work:
 All the other axes.

65
Evaluation: Takeaways
• Content overlap metrics provide a good starting point for evaluating the quality of
  generated text, but they’re not good enough on their own.

• Model-based metrics can be more correlated with human judgment, but behavior is
  not interpretable

• Human judgments are critical
   • But humans are inconsistent!

• In many cases, the best judge of output quality is YOU!
   • Look at your model generations. Don’t just rely on numbers!
   • Publicly release large samples of the output of systems that you create!

67
Today: Natural Language Generation

1. What is NLG?

2. A review: neural NLG model and training algorithm

3. Decoding from NLG models

4. Training NLG models
                                        Warning:
5. Evaluating NLG Systems               Some of the content on the
6. Ethical Considerations               next few slides may be
                                        disturbing

68
 ChatGPT is heavily filtered to not generated toxic content:




69
But there are still
problems:

jailbreak the detection
tool




        https://twitter.com/semenov_roman_/
        status/1621465137025613825



70
But there are still
problems:

Factual errors.




71
Ethics: Biases in text generation models
(Warning: examples contain sensitive content)



• Text generation models are often
  constructed from pretrained language
  models

• Language models learn harmful patterns
  of bias from large language corpora

• When prompted for this information,
  they repeat negative stereotypes




72                                              (Sheng et al., EMNLP 2019)
Hidden Biases: Universal adversarial triggers
(Warning: examples contain highly sensitive content)




• Adversarial inputs can trigger VERY
  toxic content

• These models can be exploited in
  open-world contexts by ill-
  intentioned users




73                                                     (Wallace et al., EMNLP 2019)
Hidden Biases: Triggered innocuously
(Warning: examples contain sensitive content)


• Pretrained language models can
  degenerate into toxic text even from
  seemingly innocuous prompts

• Models should not be deployed without
  proper safeguards to control for toxic
  content

• Models should not be deployed without
  careful consideration of how users will
  interact with it


74                                              (Gehman et al., EMNLP Findings 2020)
Ethics: Think about what you’re building


• Large-scale pretrained language models allow us to build NLG
  systems for many new applications

• Before deploying / publishing NLG models:
   • Check if the model’s output is not harmful
   • The model is robust to trigger words
   • …More…




75                                (Zellers et al., NeurIPS 2019)
Concluding Thoughts
• Interacting with natural language generation systems quickly shows their limitations

• Even in tasks with more progress, there are still many improvements ahead

• Evaluation remains a huge challenge.
   • We need better ways of automatically evaluating performance of NLG systems

• With the advent of large-scale language models, deep NLG research has been reset
  • It’s never been easier to jump in the space!

• One of the most exciting and fun areas of NLP to work in!

76

'''