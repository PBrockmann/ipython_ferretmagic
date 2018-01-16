
#====================================================================================
FROM yuxiaorui/python-2.7-slim

#====================================================================================
RUN pip install --no-cache-dir notebook==5.*
RUN apt-get update && apt-get -y install wget git

#====================================================================================
ENV NB_USER agentk
ENV NB_UID 1000
ENV HOME /home/${NB_USER}
RUN adduser --disabled-password \
    --gecos "Default user" \
    --uid ${NB_UID} \
    ${NB_USER}

#====================================================================================
# pyferret installation

USER root
WORKDIR /opt
RUN wget https://github.com/NOAA-PMEL/PyFerret/releases/download/v7.3/pyferret-7.3-RHEL7-64.tar.gz && \
    tar xvfz pyferret-7.3-RHEL7-64.tar.gz
#RUN wget ftp://ftp.pmel.noaa.gov/ferret/pub/data/fer_dsets.tar.gz && \
#    tar xvfz fer_dsets.tar.gz

#====================================================================================
# fast installation

USER root
WORKDIR /opt
RUN git clone https://github.com/PBrockmann/fast

#====================================================================================
# Make sure the contents of our repo are in ${HOME}
COPY . ${HOME}
USER root
RUN chown -R ${NB_UID} ${HOME}
USER ${NB_USER}

