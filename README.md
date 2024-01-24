# MotorEase
This repo holds the code for the MotorEase accessibility testing tool.

## Purpose
MotorEase is a software testing tool aimed at detecting motor impaired user accessibility guidelines within Android applications using Screenshots and XML data from Android testing tools. Provided is the information on how to use MotorEase.

## Provenance

The MotorEase code and data is available on Github at: (https://github.com/SageSELab/MotorEase)[https://github.com/SageSELab/MotorEase]

The MotorEase code and data has been permanently archived on Zenodo at: (https://doi.org/10.5281/zenodo.10460701)[https://doi.org/10.5281/zenodo.10460701]

## Setup & Usage

- Go to line 106 in the MotorEase.py file and change the file path to the folder that holds the code and data folders
- Go to line 46 and add the file path for your Glove EMbeddings txt file. MotorEase requires glove embeddings to work, and needs the download for the model. The model is large and not able to be hosted on GitHub. Please visit https://nlp.stanford.edu/projects/glove/ and download 1 of the 4 available options. 
- There are 2 ways to build the project, using Docker or a Python Environment
- Using Environment: The Code directory will have a requirements.txt file that lists all required packages for MotorEase to run. In your command line, create a new python environment: ``` python3 -m venv .venv``` Once your environment is created, activate it with this command: ```source .venv/bin/activate```. Use this command to download all of the dependencies into your virtual environment:  ```!pip install -r requirements.txt --use-deprecated=legacy-resolver```. Once the requirements are installed and there are PNG and XML files in the Data folder, run MotorEase using this command: ```python3 MotorEase.py```
- The output of either method will be a file with the Motor impairment accessibility guideline violations, AccessibilityReport.txt
- If you would like to run MotorEase on your own screenshot/xml pair, remove existing data in the data folder and add PNG screenshots and their XML files from a single application.

<ins>Docker instructions: </ins>

- There are 2 docker builds for this project. The ARM build for Apple Silicon and the AMD build for any other devices. You can find the images hosted on DockerHub here: 

- ARM: https://hub.docker.com/layers/itsarunkv/motorease-arm/latest/images/sha256:df01b242b[…]ae1f7718e4080457?uuid=66b18432-3e64-43dc-96aa-180c4e8c2dfd%0A

- AMD: https://hub.docker.com/layers/itsarunkv/motorease-amd/latest/images/sha256:9e501e139[…]0358df67a442a9dc?uuid=66b18432-3e64-43dc-96aa-180c4e8c2dfd%0A

- Pull your necessary image using this command: ```docker pull itsarunkv/motorease-arm``` or ```docker pull itsarunkv/motorease-amd```

<ins>Docker Image Information: </ins>

- The current docker image is built with sample Screenshot and XML data. This data is a representation of the data used in the study and provides a sample run option for the user. 

- This project uses a GloVe embedding for textual similarities. However, GloVe embedding files are large and difficult to host on GitHub. Therefore, we have created a sampleGlove.txt file within the docker container to act as a dummy GloVe  model in place of a real one. This text file is formatted the exact same way as a Glove model is normally formatted.

<ins>Running the Image: </ins>

- In order to run the image on the container, run this command ``` docker run -it --rm -v $(pwd)/container_files:/container_files itsarunkv/motorease-arm /bin/bash ```

- This command will allow you to enter the container and use it as a terminal. This will allow you to make wget commands and modify any existing data within. 

- In order to run the project, navigate to the Code directory and run ``` python3 MotorEase.py ```. The python script will run and will take the data from the Data folder and the GloVe embeddings from the sampleGlove.txt file. The program will run and notify the user at every stage. Finally, the logs will show that an accessibility report has been generated, and can be viewed. They can be viewed in the predictions2.txt file. 


<ins>Adding your own information:</ins>

- With the inclusion of placeholder data throughout the project, we make it easy to run and check for execution. However, this tool is designed for developers to check Motor accessibility issues within their project. This requires both an authentic GloVe embedding file and screenshots (PNG files) and UI-Automator files (XML) to be in the container. This can be done using the wget command. 

- GloVe embeddings used: ```wget https://nlp.stanford.edu/data/glove.42B.300d.zip```

- When you download your GloVe embedding file, rename it to sampleGlove.txt and delete the placeholder sampleGlove.txt file so that the code can use the real embeddings. 

- In order to load your own images, navigate to the Data folder in the container and delete the existing photos. Use the wget command to download your images into the directory so they may be used. 



## Guideline Appendix

| Accessibility Guidelines             |     Guideline Description                                  | Guideline Source | Previous Implementation                                    |    Implmeted by MotorEase                                    |
|--------------------------------------|---------------------------------------|---------------------------------------|---------------------------------------|---------------------------------------|
| Visual Touch Target Size             |    This guideline corresponds to the visual bounds of an icon without its padding. We ensure that the visual icon has a size of at least 48x48px.                                  |[40, 64] | | | x |
| Touch Target Size.                   |  This guideline looks at the bounding box of an element on the screen and requres the bounding box irrespective of the icon size, to be a minimum of 48x48px.                                    |[2, 8, 9, 11, 17, 20, 27, 38, 40, 62] | x |  |
| Persistent Elements                  |  This guideline requires elements that appear across multiple screens to remain in a similar general locations across screens. This makes it easier for users to anticipate where an icon may be.                                    |[2, 9, 11] |  | x |
| Clickable Span                       |    This guideline requires elements that can be interacted with are large enough. this includes text with hyperlinks as well.                                   |[20] | x |  |
| Duplicate Bounds                     |   This guideline looks at bounding boxes for elements on the screen and suggests that developers not have any elements that may share identical bounding boxes, or have an element with two bounding boxes of the same size.                                   |[20]  |  |  |
| Editable Item Descriptions           |  Editable items like text fields and date windows need descriptions to let users know that they can be interacted with and can be edited.                                     |[20, 34] | x |  |
| Expanding Section Closure            | This guideline requires sections such as pop-ups and lists to be closable using a visual icon that implies closure. This eliminates the need to close a section using a gesture.                                      |[2, 8, 9, 11] |  | x |
| Non-Native Elements                  |    This guideline requires developers to use native tools in the construction of their application in order to be compatible with native assistive features.                                 |[8, 27]  |  x |  |
| Visual Icon Distance                 |  This guideline looks at the visual distance between any given icons on the screen. It requires icons to be a minimum of 8px in distance to aboid mistaps.                                    |[11, 17, 62, 80]  |   | x |
| Labeled Elements                     | This guideline requires elements to have metadata descriptions of the icon and its functionality so that assistive measures such as VoiceOver can vocalize these functionalities.                                       |[20, 34, 35, 41] |  x |  |
| Captioning                           |  Captioning refers to image, audio, and video captioning requirements in the metadata. It requires  media to have a label in order for assistive services to explain the content to the user.                                   |[1, 2, 5, 8, 9, 11, 38, 41, 66, 70]  |  x |  |
| Keyboard Navigation                  | This guideline suggest developers to design interfaces that can be traveresd using a keyboard without needing gestures and complex taps.                                      |[1, 5, 30, 35, 41] |  x |  |
| Traversal Order                      |  This guideline sggests that interfaces that use keyboard navigation need to have a proper and logical traversal order of elements on the screen. An example of this is using the "tab" key to traverse elements on the screen.                                    |[1, 20, 35]  |  x |  |
| Motion Activation                    |  This guideline requires an alternate mode of interaction if motion is used to perform some action.                                     |[2, 8, 9] |   |  |
| Wide gaps between related information| This guideline suggest that related info across the screen should not be scattered so that if a user needs to perform an action related to some information, the action may not be in the same general location                                  | [27]  |  x |  |
| Facial Recognition                   | This guideline checks to see if facial recognition can be used for unlock functions within applications, not requiring motor impaired users to type out a password                                    |[22, 27]  |  x |  |
| Single Tap Navigation                | Single tap navigation requires a single tap traversal of an app while achieving the same functionality. For example: swiping to delete a row in a list must be accomplished through a series of taps that can aid in deleting the row.                                     | [2, 8, 9, 11, 35, 53]| | |
| Poor form design/instructions        | This guideline suggests developers to design forms that have proper traversals and editable descriptions. It also suggests proper distances between form fields.                                       |[1, 5]| | |

## Apps Used
| Name | Package | GooglePlayLink | Downloads | Stars |
|------|---------|----------------|----------|-------|
| Zeus  | app.zeusln.zeus | https://play.google.com/store/apps/details?id=app.zeusln.zeus | 1000 | 4 |
| Rocket.Chat  | chat.rocket.android | https://play.google.com/store/apps/details?id=chat.rocket.android | 500000 | 4.2 |
| Rootless Pixel Launcher  | amirz.rootless.nexuslauncher | https://play.google.com/store/apps/details?id=amirz.rootless.nexuslauncher | 1000000 | 4.2 |
| MTG Familiar  | com.gelakinetic.mtgfam | https://play.google.com/store/apps/details?id=com.gelakinetic.mtgfam | 500000 | 4.4 |
| Launcher  | com.finnmglas.launcher | https://play.google.com/store/apps/details?id=com.finnmglas.launcher | 5000 | 4.1 |
| Library  | com.cgogolin.library | https://play.google.com/store/apps/details?id=com.cgogolin.library | 10000 | 3.4 |
| Simple ToDo  | apps.jizzu.simpletodo | https://play.google.com/store/apps/details?
 id=apps.jizzu.simpletodo&pcampaignid=MKT-Other-
 global-all-co-prtnr-py-PartBadge-Mar2515-1 | 10000 | 4.5 |
| SmartCookieWeb  | com.cookiegames.smartcookie | https://play.google.com/store/apps/details?id=com.cookiegames.smartcookie&pcampaignid=pcampaignidMKT-Other-global-all-co-prtnr-py-PartBadge-Mar2515-1 | 50000 | 3.9 |
| PCAPdroid  | com.emanuelef.remote_capture | https://play.google.com/store/apps/details?id=com.emanuelef.remote_capture | 10000 | 4.3 |
| Rview  | com.ruesga.rview | https://play.google.com/store/apps/details?id=com.ruesga.rview | 5000 | 4.7 |
| Converter NOW  | com.ferrarid.converterpro | https://play.google.com/store/apps/details?id=com.ferrarid.converterpro | 1000 | 4.7 |
| APKShare  | be.brunoparmentier.apkshare | https://play.google.com/store/apps/details?id=be.brunoparmentier.apkshare | 1000 | 4.3 |
| DNS Hero  | com.gianlu.dnshero | https://play.google.com/store/apps/details?id=com.gianlu.dnshero&pcampaignid=MKT-Other-global-all-co-prtnr-py-PartBadge-Mar2515-1 | 5000 | 4 |
| Shaarlier  | com.dimtion.shaarlier | https://play.google.com/store/apps/details?id=com.dimtion.shaarlier | 1000 |  |
| Pdf Viewer Plus  | com.gsnathan.pdfviewer | https://play.google.com/store/apps/details?id=com.gsnathan.pdfviewer | 10000 | 4.6 |
| Taskbar  | com.farmerbb.taskbar | https://play.google.com/store/apps/details?id=com.farmerbb.taskbar | 1000000 | 4.4 |
| Seafile  | com.seafile.seadroid2 | https://play.google.com/store/apps/details?id=com.seafile.seadroid2 | 100000 | 3.8 |
| K-9 Mail  | com.fsck.k9 | https://play.google.com/store/apps/details?id=com.fsck.k9 | 5000000 | 3.9 |
| Gotify  | com.github.gotify | https://play.google.com/store/apps/details?id=com.github.gotify | 5000 | 4.7 |
| RGB Tool  | com.fastebro.androidrgbtool | https://play.google.com/store/apps/details?id=com.fastebro.androidrgbtool | 10000 | 4.1 |
| NoSurf for reddit  | com.aaronhalbert.nosurfforreddit | https://play.google.com/store/apps/details?id=com.aaronhalbert.nosurfforreddit | 1000 | 4.5 |
| Simple Scrobbler  | com.adam.aslfms | https://play.google.com/store/apps/details?id=com.adam.aslfms&pcampaignid=MKT-Other-global-all-co-prtnr-py-PartBadge-Mar2515-1 | 500000 | 3.5 |
| Look4Sat  | com.rtbishop.look4sat | https://play.google.com/store/apps/details?id=com.rtbishop.look4sat | 10000 | 4.3 |
| Lightning  | acr.browser.lightning | https://play.google.com/store/apps/details?id=acr.browser.lightning | 10000 | 4 |
| Movian Remote  | com.claha.showtimeremote | https://play.google.com/store/apps/details?id=com.claha.showtimeremote | 10000 | 4 |
| MHWorld Database  | com.gatheringhallstudios.mhworlddatabase | https://play.google.com/store/apps/details?id=com.gatheringhallstudios.mhworlddatabase | 100000 | 4.7 |
| Just (Video) Player  | com.brouken.player | https://play.google.com/store/apps/details?id=com.brouken.player | 10000 | 4.2 |
| Com-Phone Story Maker  | ac.robinson.mediaphone | https://play.google.com/store/apps/details?id=ac.robinson.mediaphone | 50000 | 3.8 |
| OpenDocument Reader  | at.tomtasche.reader | https://play.google.com/store/apps/details?id=at.tomtasche.reader | 5000000 | 4 |
| ImgurViewer  | com.ensoft.imgurviewer | https://play.google.com/store/apps/details?id=com.ensoft.imgurviewer | 10000 | 4.6 |
| Torchlight  | com.secuso.torchlight2 | https://play.google.com/store/apps/details?id=com.secuso.torchlight2 | 1000 | 4.6 |
| Aria2Android  | com.gianlu.aria2android | https://play.google.com/store/apps/details?id=com.gianlu.aria2android&pcampaignid=MKT-Other-global-all-co-prtnr-py-PartBadge-Mar2515-1 | 5000 | 4.6 |
| arXiv eXplorer - Mobile App for arXiv.org  | com.gbeatty.arxiv | https://play.google.com/store/apps/details?id=com.gbeatty.arxiv&pcampaignid=MKT-Other-global-all-co-prtnr-py-PartBadge-Mar2515-1 | 10000 | 4.7 |
| Track & Graph  | com.samco.trackandgraph | https://play.google.com/store/apps/details?id=com.samco.trackandgraph | 10000 | 4.2 |
| Vectorify da home!  | com.iven.iconify | https://play.google.com/store/apps/details?id=com.iven.iconify | 10000 | 4.5 |
| RxDroid  | at.jclehner.rxdroid | https://play.google.com/store/apps/details?id=at.jclehner.rxdroid | 10000 | 4.5 |
| Hangar  | ca.mimic.apphangar | https://play.google.com/store/apps/details?id=ca.mimic.apphangar | 100000 | 4.1 |
| Man Man  | com.adonai.manman | https://play.google.com/store/apps/details?id=com.adonai.manman | 5000 | 4.5 |
| Nock Nock  | com.afollestad.nocknock | https://play.google.com/store/apps/details?id=com.afollestad.nocknock&utm_source=global_co&utm_medium=prtnr&utm_content=Mar2515&utm_campaign=PartBadge&pcampaignid=MKT-Other-global-all-co-prtnr-py-PartBadge-Mar2515-1 | 1000 | 4.7 |
| RethinkDNS  | com.celzero.bravedns | https://play.google.com/store/apps/details?id=com.celzero.bravedns | 10000 |  |


### Versions/Dependencies 

Check Requirements.txt for most up-to-date versions

Name                    Version                   Build  Channel

absl-py                   1.2.0                    pypi_0    pypi

astunparse                1.6.3                    pypi_0    pypi

beautifulsoup4            4.11.1                   pypi_0    pypi

blis                      0.7.8                    pypi_0    pypi

bzip2                     1.0.8                h620ffc9_4  

c-ares                    1.18.1               h1a28f6b_0  

ca-certificates           2022.07.19           hca03da5_0  

cachetools                5.2.0                    pypi_0    pypi

catalogue                 2.0.8                    pypi_0    pypi

certifi                   2022.6.15       py310hca03da5_0  

charset-normalizer        2.1.0                    pypi_0    pypi

click                     8.1.3                    pypi_0    pypi

cx-oracle                 8.3.0                    pypi_0    pypi

cycler                    0.11.0                   pypi_0    pypi

cymem                     2.0.6                    pypi_0    pypi

db-grader                 1.0                       dev_0    <develop>

en-core-web-trf           3.4.0                    pypi_0    pypi
  
filelock                  3.8.0                    pypi_0    pypi
  
flatbuffers               1.12                     pypi_0    pypi
  
fonttools                 4.34.4                   pypi_0    pypi
  
gast                      0.4.0                    pypi_0    pypi
  
google-auth               2.9.1                    pypi_0    pypi
  
google-auth-oauthlib      0.4.6                    pypi_0    pypi
  
google-pasta              0.2.0                    pypi_0    pypi
  
grpcio                    1.42.0          py310h95c9599_0  
  
h5py                      3.6.0           py310h181c318_0  
  
hdf5                      1.12.1               h160e8cb_2  
  
huggingface-hub           0.8.1                    pypi_0    pypi
  
idna                      3.3                      pypi_0    pypi
  
imageio                   2.19.5                   pypi_0    pypi
  
install                   1.3.5                    pypi_0    pypi
  

jinja2                    3.1.2                    pypi_0    pypi
  
keras                     2.9.0                    pypi_0    pypi
  
keras-preprocessing       1.1.2                    pypi_0    pypi
  
kiwisolver                1.4.4                    pypi_0    pypi
  
krb5                      1.19.2               h3b8d789_0  
  
langcodes                 3.3.0                    pypi_0    pypi
  
libblas                   3.9.0           15_osxarm64_openblas    conda-forge
  
libcblas                  3.9.0           15_osxarm64_openblas    conda-forge
  
libclang                  14.0.1                   pypi_0    pypi
  
libcurl                   7.82.0               hc6d1d07_0  
  
libcxx                    14.0.6               h04bba0f_0    conda-forge
  
libedit                   3.1.20210910         h1a28f6b_0  
  
libev                     4.33                 h1a28f6b_1  
  
libffi                    3.4.2                hc377ac9_4  
  
libgfortran               5.0.0           11_2_0_he6877d6_26  
  
libgfortran5              11.2.0              he6877d6_26  
  
liblapack                 3.9.0           15_osxarm64_openblas    conda-forge
  
libnghttp2                1.46.0               h95c9599_0  
  
libopenblas               0.3.20               hea475bc_0  
  
libssh2                   1.10.0               hf27765b_0 
  
libzlib                   1.2.12               ha287fd2_2    conda-forge
  
llvm-openmp               12.0.0               haf9daa7_1  
  
markdown                  3.4.1                    pypi_0    pypi
  
markupsafe                2.1.1                    pypi_0    pypi
  
matplotlib                3.5.2                    pypi_0    pypi
  
mlxtend                   0.20.0                   pypi_0    pypi
  
murmurhash                1.0.8                    pypi_0    pypi
  
mysql-connector-python    8.0.29                   pypi_0    pypi
  
natsort                   8.1.0                    pypi_0    pypi
  
ncurses                   6.3                  h1a28f6b_3  
  
networkx                  2.8.5                    pypi_0    pypi
  
numpy                     1.23.1                   pypi_0    pypi
  
oauthlib                  3.2.0                    pypi_0    pypi
  
opencv-python             4.6.0.66                 pypi_0    pypi
  
openssl                   1.1.1q               h1a28f6b_0  
  
opt-einsum                3.3.0                    pypi_0    pypi
  
packaging                 21.3                     pypi_0    pypi
  
pandas                    1.4.3                    pypi_0    pypi
  
pathy                     0.6.2                    pypi_0    pypi
  
pillow                    9.2.0                    pypi_0    pypi
  
pip                       22.2.2                   pypi_0    pypi
  
preshed                   3.0.7                    pypi_0    pypi
  
protobuf                  3.19.4                   pypi_0    pypi
  
pyasn1                    0.4.8                    pypi_0    pypi
  
pyasn1-modules            0.2.8                    pypi_0    pypi
  
pycocotools               2.0.4                    pypi_0    pypi
  
pydantic                  1.9.2                    pypi_0    pypi
  
pyparsing                 3.0.9                    pypi_0    pypi
  
python                    3.10.5          h71ab1a4_0_cpython    conda-forge
  
python-dateutil           2.8.2                    pypi_0    pypi
  
python_abi                3.10                    2_cp310    conda-forge
  
pytz                      2022.1                   pypi_0    pypi
  
pywavelets                1.3.0                    pypi_0    pypi
  
pyyaml                    6.0                      pypi_0    pypi
  
readline                  8.1.2                h1a28f6b_1  
  
requests                  2.28.1                   pypi_0    pypi
  
requests-oauthlib         1.3.1                    pypi_0    pypi
  
rsa                       4.9                      pypi_0    pypi
  
scikit-image              0.19.3                   pypi_0    pypi
  
scikit-learn              1.1.2                    pypi_0    pypi
  
scipy                     1.8.1                    pypi_0    pypi
  
semantic-version          2.10.0                   pypi_0    pypi
  
setuptools                65.0.1                   pypi_0    pypi
  
setuptools-rust           1.5.1                    pypi_0    pypi
  
six                       1.15.0                   pypi_0    pypi
  
smart-open                5.2.1                    pypi_0    pypi
  
soupsieve                 2.3.2.post1              pypi_0    pypi
  
spacy                     3.4.1                    pypi_0    pypi
  
spacy-alignments          0.8.5                    pypi_0    pypi
  
spacy-legacy              3.0.9                    pypi_0    pypi
  
spacy-loggers             1.0.3                    pypi_0    pypi
  
spacy-transformers        1.1.8                    pypi_0    pypi
  
sqlite                    3.38.5               h1058600_0  
  
srsly                     2.4.4                    pypi_0    pypi
  
tensorboard               2.9.1                    pypi_0    pypi
  
tensorboard-data-server   0.6.1                    pypi_0    pypi
  
tensorboard-plugin-wit    1.8.1                    pypi_0    pypi
  
tensorflow-deps           2.9.0                         0    apple
  
tensorflow-estimator      2.9.0                    pypi_0    pypi
  
tensorflow-macos          2.9.2                    pypi_0    pypi
  
tensorflow-metal          0.5.0                    pypi_0    pypi
  
termcolor                 1.1.0                    pypi_0    pypi
  
thinc                     8.1.0                    pypi_0    pypi
  
threadpoolctl             3.1.0                    pypi_0    pypi
  
tifffile                  2022.5.4                 pypi_0    pypi
  
tk                        8.6.12               hb8d0fd4_0  
tokenizers                0.12.1                   pypi_0    pypi
  
torch                     1.12.0                   pypi_0    pypi
  
torchaudio                0.12.0                   pypi_0    pypi
  
torchvision               0.13.0                   pypi_0    pypi
  
tqdm                      4.64.0                   pypi_0    pypi
  
transformers              4.21.1                   pypi_0    pypi
  
typer                     0.4.2                    pypi_0    pypi
  
typing-extensions         4.3.0                    pypi_0    pypi
  
tzdata                    2022a                hda174b7_0  
  
urllib3                   1.26.11                  pypi_0    pypi
  
wasabi                    0.10.1                   pypi_0    pypi
  
werkzeug                  2.2.0                    pypi_0    pypi
  
wheel                     0.37.1             pyhd3eb1b0_0  
  
wrapt                     1.14.1                   pypi_0    pypi
  
xz                        5.2.5                h1a28f6b_1  
  
zlib                      1.2.12               h5a0b063_2  
  

