
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
RUN git clone https://github.com/NOAA-PMEL/FerretDatasets && \
    mv FerretDatasets fer_dsets

#====================================================================================
# fast installation

USER root
WORKDIR /opt
RUN git clone https://github.com/PBrockmann/fast

#====================================================================================
ENV FER_DIR=/opt/pyferret-7.3-RHEL7-64
ENV FER_PALETTE=${HOME} /opt/pyferret-7.3-RHEL7-64/ppl /opt/fast

#====================================================================================
# Make sure the contents of our repo are in ${HOME}
COPY . ${HOME}
USER root
RUN chown -R ${NB_UID} ${HOME}
USER ${NB_USER}

WORKDIR ${HOME}
