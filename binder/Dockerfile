#====================================================================================
FROM python:2.7.16-buster

#====================================================================================
LABEL maintainer="Patrick.Brockmann@lsce.ipsl.fr"

LABEL description="This image aims to provide a clean docker base to run pyferret and ferretmagic jupyter ipython extension."

LABEL ref1="http://ferret.pmel.noaa.gov/Ferret/"
LABEL ref2="https://github.com/NOAA-PMEL/PyFerret"

#====================================================================================
RUN apt-get update && apt-get -y install wget git
#RUN apt-get update && apt-get -y install libgfortran3
RUN apt-get update && apt-get -y install r-base

RUN pip install --no-cache-dir notebook==6.0.0
RUN pip install numpy pandas bokeh
RUN pip install randomcolor
RUN pip install ferretmagic==20181001
RUN pip install rpy2==3.0.5

RUN pip install ipywidgets
RUN jupyter nbextension enable --py widgetsnbextension --sys-prefix

#====================================================================================
ENV NB_USER agentk
ENV NB_UID 1000
ENV HOME /home/${NB_USER}
RUN adduser --disabled-password \
    --gecos "Default user" \
    --uid ${NB_UID} \
    ${NB_USER}

#====================================================================================
# libpng15 (needed by pyferret)

#USER root
#WORKDIR /opt
#RUN wget --no-check-certificate https://sourceforge.net/projects/libpng/files/libpng15/1.5.30/libpng-1.5.30.tar.gz && \
#    tar xvfz libpng-1.5.30.tar.gz
#RUN cd libpng-1.5.30 && \
#    ./configure --prefix=/usr/local/libpng && \
#    make check && \
#    make install
#
#ENV LD_LIBRARY_PATH="/usr/local/libpng/lib:${LD_LIBRARY_PATH}"

#====================================================================================
# pyferret installation

USER root
WORKDIR /opt
RUN wget https://github.com/NOAA-PMEL/PyFerret/releases/download/v7.5.0/PyFerret-7.5.0-RHEL7-64-Python2.7.tar.gz && \
    tar xvfz PyFerret-7.5.0-RHEL7-64-Python2.7.tar.gz
RUN git clone https://github.com/NOAA-PMEL/FerretDatasets && \
    mv FerretDatasets fer_dsets

#====================================================================================
# fast installation

USER root
WORKDIR /opt
RUN git clone https://github.com/PBrockmann/fast

#====================================================================================
ENV FER_DIR="/opt/PyFerret-7.5.0-RHEL7-64-Python2.7"
ENV FER_DSETS="/opt/fer_dsets"

ENV PYTHONPATH="${FER_DIR}/lib/python2.7/site-packages:${PYTHONPATH}"
ENV LD_LIBRARY_PATH="${FER_DIR}/lib/python2.7/site-packages/pyferret:${LD_LIBRARY_PATH}"

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
