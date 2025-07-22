---
permalink: /
title: ""
excerpt: ""
author_profile: true
redirect_from: 
  - /about/
  - /about.html
---

{% if site.google_scholar_stats_use_cdn %}
{% assign gsDataBaseUrl = "https://cdn.jsdelivr.net/gh/" | append: site.repository | append: "@" %}
{% else %}
{% assign gsDataBaseUrl = "https://raw.githubusercontent.com/" | append: site.repository | append: "/" %}
{% endif %}
{% assign url = gsDataBaseUrl | append: "google-scholar-stats/gs_data_shieldsio.json" %}

<span class='anchor' id='about-me'></span>

**He K**ai, Ph.D., earned his doctorate from the School of Computer Science and Technology at Xi'an Jiaotong University under the supervision of Professor Li Chen (recipient of the Young Thousand Talents Plan in China). He also completed an academic visit at the School of Computer Science and Engineering, Nanyang Technological University, under the guidance of Professor Erik Cambria (IEEE Fellow), with whom he maintains an active academic collaboration. Currently, he is a postdoctoral researcher at the School of Public Health, National University of Singapore, focusing on research in Large Language Model, AI for Healthcare, Affective Computing, Information Extraction.

I currently work as a Research Fellow in NUS. For my full (and timely) publication list, please refer to my Google scholar<a href='https://scholar.google.com/citations?user=4nWk-HYAAAAJ'><img src="https://img.shields.io/endpoint?url={{ url | url_encode }}&logo=Google%20Scholar&labelColor=f6f6f6&color=9cf&style=flat&label=citations"></a>.
                   


<span class='anchor' id='news'></span>

# 🔥 News
- *2025.07*: &nbsp;🎉🎉 Our paper on Chinese Medical Entity Normalization is accepted by ESWA (IF 7.5). Congrats to [Dr. Hou]( ).
- *2025.06*: &nbsp;🎉🎉 Our paper on Fuzzy RAG is accepted by IEEE Transactions on Fuzzy Systems (IF 11.9).
- *2025.05*: &nbsp;🎉🎉 Our paper of Multimodal EHR Survey are accepted Information Fusion (IF 14.8). Congrats to [Dr. Wu](https://scholar.google.com.hk/citations?user=bZOcwEYAAAAJ&hl).
- *2025.05*: &nbsp;🎉🎉 Our two paper are accepted by ACL 2025. Congrats to [Dr. Lin](https://scholar.google.com.hk/citations?user=k8BKz0MAAAAJ&h).
- *2025.05*: &nbsp;🎉🎉 Our paper of neurological condition identification are accepted by MICCAI 2025. Congrats to [Dr. Xu](https://scholar.google.com.hk/citations?user=HzVhJf0AAAAJ&hl).
- *2025.05*: &nbsp;🎉🎉 Our paper of exploring cognitive difference via LLM is accepted by Cognitive Computation. Congrats to [Dr. Bao]( )
- *2025.04*: &nbsp;🎉🎉 Our paper of multimodal meidcal LLM is accepted by Cancer Research (IF 12.5). Congrats to [Dr. Gao](https://scholar.google.com.hk/citations?user=CeP6dkcAAAAJ&hl).
- *2025.04*: &nbsp;🎉🎉 Our paper of diffusion-based difference-aware medical VQA is accepted by IEEE TIP. Congrats to [Dr. Lin](https://scholar.google.com.hk/citations?user=k8BKz0MAAAAJ&h).
- *2025.02*: &nbsp;🎉🎉 Our survey paper on Multiple Instance Learning in computational pathology is accepted by Information Fusion (IF 14.8).
- *2024.12*: &nbsp;🎉🎉 Our paper reveives ****Best Paper Award****, IEEE Transactions on Affective Computing, titled "The Biases of Pre-Trained Language Models: An Empirical Study on PromptBased Sentiment Analysis and Emotion Detection" 




# 📝 Publications 

<!-- <div class='paper-box'><div class='paper-box-image'><div><div class="badge">CVPR 2016</div><img src='images/500x300.png' alt="sym" width="100%"></div></div>
<div class='paper-box-text' markdown="1">

[Deep Residual Learning for Image Recognition](https://openaccess.thecvf.com/content_cvpr_2016/papers/He_Deep_Residual_Learning_CVPR_2016_paper.pdf) -->

<!-- **Kaiming He**, Xiangyu Zhang, Shaoqing Ren, Jian Sun

[**Project**](https://scholar.google.com/citations?view_op=view_citation&hl=zh-CN&user=DhtAFkwAAAAJ&citation_for_view=DhtAFkwAAAAJ:ALROH1vI_8AC) <strong><span class='show_paper_citations' data='DhtAFkwAAAAJ:ALROH1vI_8AC'></span></strong>
- Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus ornare aliquet ipsum, ac tempus justo dapibus sit amet. 
</div>
</div>

- [Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus ornare aliquet ipsum, ac tempus justo dapibus sit amet](https://github.com), A, B, C, **CVPR 2020** -->




<span class='anchor' id='-publications'></span>

<!-- *: corresponding author,&nbsp;&nbsp;‡: co-first author -->


## 2025
- ``ESWA`` ***Multi-granularity Semantic Extraction and Multi-task Fusion for Chinese Medical Entity Normalization Expert Systems With Applications*** <br> Wenhui Hou, **Kai He**, Rui Mao, et al.  [[Paper]]()
- ``IEEE Transactions on Fuzzy Systems`` ***External Retrievals or Internal Priors? From RAG to Epitome-Augmented Generation by Fuzzy Selection*** <br>  **Kai He**, Jiaxing Xu, Qiq Lin, et al.  [[Paper]]()
- ``Information Fusion`` ***Harnessing the Potential of Multimodal EHR data: A Comprehensive Survey of Clinical Predictive Modeling for Intelligent Healthcare*** <br> Wu Jialun, **Kai He**, Rui Mao, et al.  [[Paper]]() 
- ``ACL 2025`` ***Crab: A Novel Configurable Role-Playing LLM with Assessing Benchmark***. <br> **Kai He**, Yucheng Huang, Wenqing Wang, Delong Ran, Dongming Sheng, Junxuan Huang, ***Qika Lin***, Jiaxing Xu, et al.  [[Paper]]() 
- ``ACL 2025`` ***Self-supervised Quantized Representation for Seamlessly Integrating Knowledge Graphs with LLMs***. ***Qika Lin***, Tianzhe Zhao, Kai He, Zhen Peng, Fangzhi Xu, Ling Huang, Jingying Ma, Mengling Feng.  [[Paper]](https://arxiv.org/pdf/2501.18119) 
- ``MICCAI 2025`` ***BrainPrompt: Multi-Level Brain Prompt Enhancement for Neurological Condition Identification***. <br> Xu Jiaxing, **He K**, Tang Y, et. al. [[Paper]]()
- ``Cognitive Computation`` ***Exploring Cognitive Difference in Poetry! Collection via: A Case Study of the Book of Songs***. <br> Bao H, **He K**, Wang YG, Gao ZY, et. al., [[Paper]]()
- ``Cancer Research`` ***Bridging whole slide images and large language model for slide-level question answering***. <br> Gao Z, **He K**, Su W, et al.   [[Paper]](https://aacrjournals.org/cancerres/article/85/8_Supplement_1/2438/757197)
- ``IEEE TIP`` ***Cross-modal Knowledge Diffusion-based Generation for Difference-aware Medical VQA***. <br> Qika Lin, **Kai He**, Yifan Zhu, et al.  . [[Paper]](https://ieeexplore.ieee.org/document/10964089)
- ``Information Fusion`` ***From patches to WSIs: A systematic REVIEW of deep Multiple Instance Learning in computational pathology***. <br> Zhang Y, Gao Z, **He K**, et al. . (IF:14.8) [[Paper]](https://www.sciencedirect.com/science/article/pii/S1566253525001009) 
- ``Information Fusion``  ***A survey on pragmatic processing techniques***. Information Fusion, <br> Mao R, Ge M, Han S, et al. [[Paper]]( https://www.sciencedirect.com/science/article/pii/S1566253524004901 ) 
- ``Information Fusion``  ***A survey of large language models for healthcare: from data, technology, and applications to accountability and ethics***. <br> **He K**, Mao R, Lin Q, et al.   [[Paper]]( https://www.sciencedirect.com/science/article/pii/S1566253525000363 ) 

## 2024
- Lin Q, Zhu Y, Mei X, et al. Has multimodal learning delivered universal intelligence in healthcare? A comprehensive survey[J]. Information Fusion, 2024: 102795.  [[Paper]]( https://www.sciencedirect.com/science/article/pii/S1566253524005736 )
- Xu J, **He K**, Lan M, et al. Contrasformer: a brain network contrastive transformer for neurodegenerative condition identification[C]//Proceedings of the 33rd ACM International Conference on Information and Knowledge Management. 2024: 2671-2681.  [[Paper]]( https://dl.acm.org/doi/pdf/10.1145/3627673.3679560 ) 
- Li Y, Ma X, Zhou X, et al. Integrating K+ Entities into Coreference Resolution on Biomedical Texts[J]. IEEE/ACM Transactions on Computational Biology and Bioinformatics, 2024.  [[Paper]]( https://ieeexplore.ieee.org/abstract/document/10643354 ) 
- Mao R, **He K**, Ong C, et al. MetaPro 2.0: Computational metaphor processing on the effectiveness of anomalous language modeling[C]//Findings of the Association for Computational Linguistics ACL 2024. 2024: 9891-9908.  [[Paper]]( https://aclanthology.org/2024.findings-acl.590.pdf )
- Wu J, Yu X, **He K**, et al. Promise: A pre-trained knowledge-infused multimodal representation learning framework for medication recommendation[J]. Information Processing & Management, 2024, 61(4): 103758.  [[Paper]](  )
- Mao R, **He K**, Zhang X, et al. A survey on semantic processing techniques[J]. Information Fusion, 2024, 101: 101988.  [[Paper]]( https://www.sciencedirect.com/science/article/pii/S0306457324001183 ) 

## 2023
- Zhang X, Mao R, **He K**, et al. Neuro-symbolic sentiment analysis with dynamic word sense disambiguation[C]//Findings of the Association for Computational Linguistics: EMNLP 2023. 2023: 8772-8783.  [[Paper]]( https://aclanthology.org/2023.findings-emnlp.587.pdf ) 
- Wu J, **He K**, Mao R, et al. MEGACare: Knowledge-guided multi-view hypergraph predictive framework for healthcare[J]. Information Fusion, 2023, 100: 101939.  [[Paper]]( https://w.sentic.net/megacare.pdf ) 
- **He K**, Mao R, Huang Y, et al. Template-free prompting for few-shot named entity recognition via semantic-enhanced contrastive learning[J]. IEEE transactions on neural networks and learning systems, 2023.  [[Paper]](https://ieeexplore.ieee.org/abstract/document/10264144 ) 
- Mao R, Li X, **He K**, et al. MetaPro Online: A computational metaphor processing online system[C]//Proceedings of the 61st annual meeting of the association for computational linguistics. Association for Computational Linguistics (ACL), 2023.  [[Paper]]( https://aura.abdn.ac.uk/bitstream/handle/2164/22918/Mao_etal_ACL_Metapro_Online_a_VOR.pdf?sequence=1 )
- **He K**, Huang Y, Mao R, et al. Virtual prompt pre-training for prototype-based few-shot relation extraction[J]. Expert systems with applications, 2023, 213: 118927.  [[Paper]]( https://sentic.net/virtual-prompt-for-relation-extraction.pdf ) 
- Mao R, Liu Q, **He K**, et al. The biases of pre-trained language models: An empirical study on prompt-based sentiment analysis and emotion detection[J]. IEEE transactions on affective computing, 2022, 14(3): 1743-1753.  [[Paper]](https://ieeexplore.ieee.org/abstract/document/9881877  )
- 
## 2022
- **He K**, Mao R, Gong T, et al. JCBIE: a joint continual learning neural network for biomedical information extraction[J]. BMC bioinformatics, 2022, 23(1): 549.  [[Paper]]( https://link.springer.com/content/pdf/10.1186/s12859-022-05096-w.pdf ) 
- Mao B, Jia C, Huang Y, et al. Uncertainty-guided mutual consistency training for semi-supervised biomedical relation extraction[C]//2022 IEEE International Conference on Bioinformatics and Biomedicine (BIBM). IEEE, 2022: 2318-2325.  [[Paper]]( https://ieeexplore.ieee.org/abstract/document/9995416 )
- **He K**, Mao B, Zhou X, et al. Knowledge enhanced coreference resolution via gated attention[C]//2022 IEEE International Conference on Bioinformatics and Biomedicine (BIBM). IEEE, 2022: 2287-2293.  [[Paper]]( https://ieeexplore.ieee.org/abstract/document/9995551 ) 
- Huang Y, **He K**, Wang Y, et al. Copner: Contrastive learning with prompt guiding for few-shot named entity recognition[C]//Proceedings of the 29th International conference on computational linguistics. 2022: 2515-2527.  [[Paper]](https://aclanthology.org/2022.coling-1.222.pdf  ) 
- **He K**, Mao R, Gong T, et al. Meta-based self-training and re-weighting for aspect-based sentiment analysis[J]. IEEE Transactions on Affective Computing, 2022, 14(3): 1731-1742.  [[Paper]]( https://ieeexplore.ieee.org/abstract/document/9870538 )

## Before 2022
- Li Y, Ma X, Zhou X, et al. Knowledge enhanced lstm for coreference resolution on biomedical texts[J]. Bioinformatics, 2021, 37(17): 2699-2705.  [[Paper]]( https://academic.oup.com/bioinformatics/article-pdf/37/17/2699/50339149/btab153.pdf ) 
- **He K**, Yao L, Zhang J W, et al. Construction of genealogical knowledge graphs from obituaries: Multitask neural network extraction system[J]. Journal of medical Internet research, 2021, 23(8): e25670.  [[Paper]]( https://www.jmir.org/2021/8/e25670/ ) 
- Bao H, **He K**, Yin X, et al. Bert-based meta-learning approach with looking back for sentiment analysis of literary book REVIEWs[C]//Natural Language Processing and Chinese Computing: 10th CCF International Conference, NLPCC 2021, Qingdao, China, October 13–17, 2021, Proceedings, Part II 10. Springer International Publishing, 2021: 235-247.  [[Paper]](https://link.springer.com/chapter/10.1007/978-3-030-88483-3_18  )
- **He K**, Wu J, Ma X, et al. Extracting kinship from obituary to enhance electronic health records for genetic research[C]//Proceedings of the Fourth social media mining for health applications (# SMM4H) workshop & shared task. 2019: 1-10.  [[Paper]]( https://aclanthology.org/W19-3201.pdf ) 
- **He K**, Hong N, Lapalme-Remis S, et al. Understanding the patient perspective of epilepsy treatment through text mining of online patient support groups[J]. Epilepsy & Behavior, 2019, 94: 65-71.  [[Paper]]( https://www.sciencedirect.com/science/article/pii/S1525505018309417 ) 
- Li C, Xu X, Zhou G, et al. Implementation of National Health Informatization in China: survey about the status quo[J]. JMIR medical informatics, 2019, 7(1): e12238.  [[Paper]]( https://medinform.jmir.org/2019/1/e12238 ) 


## Under REVIEW

- DivScore: Zero-shot Detection of LLM-Generated Text
in Specialized Domains
Chen Zhihui, He K，  ET. AL. EMNLP, UNDER REVIEW.
- Accurate spatial quantification in computational pathology with multiple instance learning
GAO ZY, MAO AY, HE K, ET. AL. NATURE CANCER, UNDER REVIEW.
-  InTriage: Intelligent Telephone Triage in Pre‑Hospital Emergency Care
HE K, LIN QK, FEi H, ET.AL. EMNLP 2025, UNDER REVIEW.
- Towards Smarter Clinical Predictions: Foundation Models for Integrating Multi‑Source Domain Knowledge in EHRs
WU JL, MEI X, HE K, ET. AL. JOURNAL OF BIOMEDICAL AND HEALTH INFORMATICS, UNDER REVIEW.
- AKECare: A Temporal‑Hierarchical Framework with Knowledge Fusion for Personalized Clinical Predictive
Modeling
WU JL, MEi X, HE K, ET. AL. JOURNAL OF BIOMEDICAL AND HEALTH INFORMATICS, UNDER REVIEW.
- Robust Multimodal Sentiment Analysis via Double Information Bottleneck
HUANG, HT, GONG TLHE K, ET.AL. INFORMATION FUSION, UNDER REVIEW.
- A Survey of Quantized Graph Representation Learning: Connecting Graph Structures with Large Language Models
LIN QK, PENG X, HE K, ET. AL. IJCAI, UNDER REVIEW.
- Language Modeling on Tabular Data: A Survey of Foundations, Techniques and Evolution
RUAN,YC, LAN X, HE K, ET. AL. ARTIFICIAL INTELLIGENCE REVIEW, UNDER REVIEW.
- Unraveling the Evolution of Public Cognition of COVID‑19: A Concept Mapping Analysis through Metaphors in US
Tweets
MAO R, TAN Y, HE K, ET. AL. IJCAI 2025, UNDER REVIEW.
- Multi‑Atlas Brain Network Classification through Consistency Distillation and Complementary Information Fusion
XU JX, LAN MC, HE K, ET. AL. TMI, UNDER REVIEW.
- Towards Unified Neurosymbolic Reasoning on Knowledge Graphs
LIN QK, XU FZ, HE K, ET. AL. AI, UNDER REVIEW.
- Global Entity Relationship Enhancement Network for Multimodal Sarcasm Detection
WANG XB, GE M, HE K, ET. AL. IEEE TRANSACTIONS ON AFFECTIVE COMPUTiNG, UNDER REVIEW

 
<span class='anchor' id='-Honors-and-Awards'></span>

# 🎖 Honors and Awards
- *2024.12* Best Paper Award, IEEE Transactions on Affective Computing. 
- *2024.12* Outstanding Meidcal AI Applications. 
- *2023.03* Outstanding Doctoral Graduate. 
- *2022.09* Outstanding Graduate Student. 
- *2022.09* First-Class Scholarship Award. 

<span class='anchor' id='-Educations-and-Experiences'></span>

# 📖 Educations and Experiences
- *2023.05 - present*, Research Fellow at SSHSPH, National University of Singapore, Singapore. (Supervisor: [Prof. Mengling Feng](https://www.mornin-feng.com/))
- *2021.09 - 2022.09*, Joint Ph.D. at CCDS, Nanyang Technological University, Singapore. (Supervisor: [Prof. Erik Cambria](https://scholar.google.com/citations?user=ilSYpW0AAAAJ))
- *2017.09 - 2023.03*, Ph.D. at School of Computer Science and Technology, Xi’an Jiaotong University, Shannxi, China.  (Supervisor: [Prof. Chen Li](https://chenli.group/))

<span class='anchor' id='-Academic-Projects'></span>

# 💬 Academic Projects
-   Project of Intelligent Telephone Triage in Pre-Hospital Emergency Care. AISG,  Grant AISG2-TC-2022-004.
-   Project of National Natural Science Foundation of China, research on the construction of metabolic pathway model based on semantic analysis of biological text, project number 61772409.
-   National Key RD Project, Research on Effective Mining and Key Information Technology of Big Data of Precision Medicine, Project No. 2018YFC0910404HZ.
-   Project of Shaanxi Provincial Department of Science and Technology, full chain intelligent pathology diagnosis equipment, project number 2021GXLH\-Z\-095.
-   Ningxia Provincial Key RD Program, application demonstration of key technologies for medical big data management and services based on breast cancer, stomach cancer, coronary heart disease and other diseases, project number 2022BEG02025HZ.
-   Project of the Statistical Information Center of the National Health Commission, Research on the framework system of knowledge mapping for artificial intelligence diagnosis and treatment assistance, Project No. 20201076.
-   Project of Shanghai Children's Medical Center affiliated with Shanghai Jiao Tong University School of Medicine, Application of pediatric graded diagnosis and treatment based on artificial intelligence, Project No. 20210506.
-   Project of Xi'an Jiaotong University, Construction of large-scale cross-modal medical knowledge graph, Project No. xzd012020008
-   Project of Application Analysis and Benchmarking System of Artificial Intelligence in Health Care, Grant 20190725.
-   Project of Knowledge mining, fusion and application of multimodal fragmentation, Grant 61721002.

<span class='anchor' id='-Services'></span>

# 💻 Services
- Journal 
   - Associate Editor :
     
       IEEE Transactions on Affective Computing （IF:9.6）
     
   - Reviewer (Selected): 

       IEEE Transactions on Neural Networks and Learning Systems, IEEE Transactions on Affective Computing, Information Fusion, Expert System with Applicatiopn, Neurocomputing, Bioinformastics, Information Processing and Management, Knowledge-Based Systems, Cognitive Computation.

- Conference  
   - Co‑chair of NLP‑SIG workshop, 2023‑now

   - Program Committee Member: 

        ACL’23-25, EMNLP’22-23, COLING’22-23, SIGIR’23, CIKM’24, IJCAI’23-24, IJCNN'25 etc.
