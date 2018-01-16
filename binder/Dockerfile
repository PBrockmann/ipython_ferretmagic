
#====================================================================================
FROM python:2.7.14-stretch

#====================================================================================
RUN pip install --no-cache-dir notebook==5.*
RUN apt-get update && apt-get -y install wget git
RUN apt-get update && apt-get -y install libpng

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
ENV FER_DSETS=/opt/fer_dsets

ENV PYTHONPATH=${FER_DIR}/lib/python2.7/site-packages:${PYTHONPATH}
ENV LD_LIBRARY_PATH=${FER_DIR}/lib/python2.7/site-packages/pyferret

ENV FER_DATA=.:${FER_DSETS}/data:${FER_DIR}/contrib:/opt/fast
ENV FER_DESCR=.:${FER_DSETS}/descr
ENV FER_GRIDS=.:${FER_DSETS}/grids
ENV FER_GO=.:${FER_DIR}/go:${FER_DIR}/examples:${FER_DIR}/contrib:/opt/fast
ENV FER_PALETTE=.:/${FER_DIR}/ppl:/opt/fast
ENV FER_FONTS=${FER_DIR}/ppl/fonts
ENV PYFER_EXTERNAL_FUNCTIONS=${FER_DIR}/ext_func/pylibs

#====================================================================================
# Make sure the contents of our repo are in ${HOME}
COPY . ${HOME}
USER root
RUN chown -R ${NB_UID} ${HOME}
USER ${NB_USER}

WORKDIR ${HOME}
