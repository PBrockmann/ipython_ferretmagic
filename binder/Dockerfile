#====================================================================================
FROM continuumio/miniconda3

#====================================================================================
RUN conda create -n env python=3.8
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

RUN conda init bash
RUN conda create -n FERRET -c conda-forge pyferret ferret_datasets --yes
RUN conda activate FERRET

RUN conda install -c r rpy2

RUN pip install --no-cache-dir notebook==6.*
RUN pip install numpy pandas bokeh
RUN pip install randomcolor
RUN pip install ferretmagic

RUN pip install ipywidgets
RUN jupyter nbextension enable --py widgetsnbextension --sys-prefix

#====================================================================================
# fast installation

USER root
WORKDIR /opt
RUN git clone https://github.com/PBrockmann/fast

ENV FER_DATA=". ${FER_DATA} /opt/fast"
ENV FER_GO=". ${FER_GO} /opt/fast"
ENV FER_PALETTE=". /${FER_PALETTE} /opt/fast"
ENV PATH="${FER_DIR}/bin:/opt/fast:${PATH}"

#====================================================================================
# Make sure the contents of our repo are in ${HOME}
COPY . ${HOME}
USER root
RUN chown -R ${NB_UID} ${HOME}
USER ${NB_USER}

WORKDIR ${HOME}
