FROM ubuntu:18.04

RUN apt update && apt install -y curl
RUN apt install -y gnupg wget software-properties-common


RUN wget -O sgjp.key http://sgjp.pl/apt/sgjp.gpg.key && apt-key add sgjp.key && add-apt-repository 'deb http://sgjp.pl/apt/ubuntu-bionic bionic main' && apt update
RUN apt install -y python3-pip morfeusz2 python3-morfeusz2
RUN python3 -m pip install jupyter numpy scipy pandas matplotlib scikit-learn nltk tensorflow keras seaborn

RUN python3 -m site &> /dev/null && PATH="$PATH:'python3 -m site --user-base'/bin'"

ENTRYPOINT ["jupyter", "notebook", "--ip=0.0.0.0", "--allow-root", "--notebook-dir=/home/nlp/"]
