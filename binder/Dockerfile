#====================================================================================
FROM continuumio/miniconda3

#====================================================================================
RUN conda create -n env python=3.6
RUN echo "source activate env" > ~/.bashrc
ENV PATH /opt/conda/envs/env/bin:$PATH

#====================================================================================
LABEL maintainer="Patrick.Brockmann@lsce.ipsl.fr"

LABEL description="This image aims to provide a clean docker base to run pyferret and ferretmagic jupyter ipython extension."

LABEL ref1="http://ferret.pmel.noaa.gov/Ferret/"
LABEL ref2="https://github.com/NOAA-PMEL/PyFerret"

#====================================================================================
ENV NB_USER agentk
ENV NB_UID 1000
ENV HOME /home/${NB_USER}
RUN adduser --disabled-password \
    --gecos "Default user" \
    --uid ${NB_UID} \
    ${NB_USER}

#====================================================================================
USER root

RUN conda install -c conda-forge pyferret

RUN pip install --no-cache-dir notebook==6.*
RUN pip install numpy pandas bokeh
RUN pip install randomcolor
RUN pip install ferretmagic
RUN pip install rpy2

RUN pip install ipywidgets
RUN jupyter nbextension enable --py widgetsnbextension --sys-prefix

#====================================================================================
# Ferret Datasets installation

USER root
WORKDIR /opt
RUN git clone https://github.com/NOAA-PMEL/FerretDatasets fer_dsets

#====================================================================================
# fast installation

USER root
WORKDIR /opt
RUN git clone https://github.com/PBrockmann/fast

#====================================================================================
ENV FER_DIR="/opt/conda/pkgs/pyferret-7.5.0-py37hb511868_2/"
ENV FER_DSETS="/opt/fer_dsets"

ENV FER_DATA=". ${FER_DSETS}/data ${FER_DIR}/contrib /opt/fast"
ENV FER_DESCR=". ${FER_DSETS}/descr"
ENV FER_GRIDS=". ${FER_DSETS}/grids"
ENV FER_GO=". ${FER_DIR}/go ${FER_DIR}/examples ${FER_DIR}/contrib /opt/fast"
ENV FER_PALETTE=". /${FER_DIR}/ppl /opt/fast"
ENV FER_FONTS="${FER_DIR}/ppl/fonts"
ENV PYFER_EXTERNAL_FUNCTIONS="${FER_DIR}/ext_func/pylibs"

ENV PATH="${FER_DIR}/bin:/opt/fast:${PATH}"

#====================================================================================
# Make sure the contents of our repo are in ${HOME}
COPY . ${HOME}
USER root
RUN chown -R ${NB_UID} ${HOME}
USER ${NB_USER}

WORKDIR ${HOME}
